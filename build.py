#!/usr/bin/env python3
"""Build The FDE Playbook for Analytics Agents (V3): chapters/*.md -> playbook.html (+ PLAYBOOK.md, --site).

    python3 build.py                 # build PLAYBOOK.md and playbook.html (artifact fragment)
    python3 build.py --check         # build, then lint; exit 1 on any content or build failure
    python3 build.py --site out/     # also write out/index.html (single-page app) + one file per chapter
    python3 build.py --version v2.0  # version string for the cover and top bar

Chapters are pandoc Markdown with the V2 syntax (see AUTHORING.md): four callouts, fenced divs
for .scene / .diagram / .card / .template / .component, hidden evidence IDs, and an optional
front-matter block per chapter. Needs pandoc on PATH.
"""
import glob
import base64
import hashlib
import html as htmlmod
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import os

ROOT = Path(__file__).parent
CH = Path(os.environ.get("PB_CHAPTERS", ROOT / "chapters"))      # override for test builds
OUT = Path(os.environ.get("PB_OUT", ROOT))                        # where playbook.html / PLAYBOOK.md go
DIAG = ROOT / "diagrams"
TPL = ROOT / "template.html"
TITLE = "The FDE Playbook for Analytics Agents"
SITE_URL = os.environ.get("PB_SITE_URL", "")  # optional canonical base for the .md links; unset, they stay relative
REPO_URL = os.environ.get("PB_REPO_URL", "https://github.com/atlanai/analytics-playbook")  # the public source repo; PB_REPO_URL overrides it

# (part label, part key, [slot]). A slot is (V3 stem, [V2 fallback stems], legacy). The exact V3 file wins; until a
# writer creates it the build uses the first V2 fallback that exists and says so. A legacy slot is a V2 chapter
# that V3 folds away (ch3, the separate handover chapter): it is included only while its file still exists, so
# old links keep resolving during the rewrite, and the build warns.
ORDER = [
    ("Why it is hard", "part1", [("01-why-hard", ["01-tenth-question"], False)]),
    ("How to build one", "part2",
     [("00-method", [], False), ("02a-evals-first", [], False), ("02b-metric-unit", [], False), ("02c-serve-per-question", [], False),
      ("03-phase-0", ["04-phase-0"], False), ("04-week-1", ["05-weeks-1-2"], False),
      ("05-week-2", ["06-weeks-3-4"], False), ("06-week-3", ["07-weeks-5-6"], False),
      ("07-week-4", ["08-release-and-run"], False),
      ("08-after-launch", [], False)]),
    ("Toolkit", "cards",
     [("00-start", [], False), ("cards", [], False), ("r2-templates", [], False),
      ("videos", [], False), ("podcasts", [], False)]),
    ("Research", "research",
     [("r0-results", [], False), ("r3-evidence", [], False), ("r6-field-research", [], False)]),
    ("Reference", "ref",
     [("r1-failure-modes", [], False), ("r4-glossary", [], False), ("r5-tooling", [], False), ("r7-semantic-layers", [], False)]),
]
# The phase strip at the top of Part II chapters: (slot stem, short label, what happens). Links resolve to whichever
# file fills the slot, so the strip works on V2 fallbacks too.
PHASES = [("03-phase-0", "Phase 0", "Before the clock"), ("04-week-1", "Phase 1", "Build the golden set"),
          ("05-week-2", "Phase 2", "Generate metrics"), ("06-week-3", "Phase 3", "Hill-climb from traces"),
          ("07-week-4", "Phase 4", "Release and hand over"), ("08-after-launch", "After launch", "Keep it running")]
SLOT_ARTICLE = {}   # slot stem -> first article id of the file that filled it (set in main)
MD = {}             # article id -> its Markdown page (set in main); the single-file edition carries it inline

# V2 callouts. Legacy V1 kinds still render (so old chapters build) but --check reports them.
LABELS = {"rule": "Rule", "note": "Note", "stop": "Stop", "done": "Definition of done"}
LEGACY = {"leader": ("brief", "For leaders"), "delivery": ("brief", "For the delivery team"),
          "evidence": ("note", "Evidence"), "field": ("note", "Field case"),
          "brief": ("brief", "For leaders")}
BANNED = ["illustrative", "demo data", "robust", "seamless", "unlock"]
DIAGRAM_IDS = ["workload", "lifecycle", "tasks", "phases", "lanes", "loop", "miss-tree", "ladder", "contract", "swimlane",
               "ontology", "five-decisions", "a1-before-after", "closure", "lane-tree", "ontology-tree",
               "two-paths", "answer-key", "grading", "wave", "production-loop",
               "handover", "domain-two", "ceremonies", "data-flows",
               # V3
               "metrics-pipeline", "model-chart", "didnt-work", "agent-architectures", "access-checklist",
               "sql-vs-prose", "why-moves", "evals-why", "retrieval", "scoreboard", "table-split", "areas", "examples", "misses", "ablations", "noise",
               # V3.1
               "sv-gap", "sv-layouts", "sv-feedback", "sv-start", "sv-reach", "sv-alongside", "bench-flow", "metrics-agent",
               "method-map"]
EXTRA_DIAGRAMS = ["negatives"]  # generated from evidence.json when it carries a negatives list
# The one ladder: one model, same questions. evidence.json may override it with a top-level
# "ladder" list of {label, value, id, display?}; the ids are for the audit check only and are never drawn.
LADDER_V3 = [{"id": "E03", "label": "Bare schema", "value": 31.8},
             {"id": "E16", "label": "Descriptions and documentation", "value": 39.3, "display": "39.3%"},
             {"id": "E04", "label": "Usage patterns", "value": 43.9},
             {"id": "E52", "label": "AI-generated metrics and queries", "value": 83.2, "display": "83.2%"}]

WARN, FAIL_CONTENT, FAIL_BUILD = [], [], []
FIG_SEEN = {}   # diagram id -> instances so far (a diagram may appear in several chapters)


def esc(s):
    return htmlmod.escape(s, quote=True)


def strip_tags(s):
    return htmlmod.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def split_fences(text):
    """Yield (is_code, chunk) so nothing is rewritten inside fenced code."""
    parts = re.split(r"(^(?:```|~~~).*?^(?:```|~~~)[ \t]*$)", text, flags=re.M | re.S)
    for i, p in enumerate(parts):
        yield (i % 2 == 1, p)


def outside_code(text, fn):
    return "".join(chunk if code else fn(chunk) for code, chunk in split_fences(text))


# ----------------------------------------------------------------------------- Markdown pre-pass

def front_matter(txt):
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", txt, re.S)
    if not m:
        return {}, txt
    meta = {}
    for line in m.group(1).splitlines():
        for tok in re.split(r"\s{3,}|\t+", line.strip()):
            k, sep, v = tok.partition(":")
            if sep and k.strip():
                meta[k.strip().lower()] = v.strip()
    return meta, txt[m.end():]


CALLOUT_RE = re.compile(r"^> \[!(\w+)(?:[ \t]+([^\]\n]+?))?\][ \t]*(.*)\n((?:>.*(?:\n|$))*)", re.M)


def callouts(text, stem):
    def conv(m):
        kind = m.group(1).lower()
        label = (m.group(2) or "").strip()
        first = m.group(3).strip()
        body = re.sub(r"^> ?", "", m.group(4), flags=re.M).strip("\n")
        if first:
            body = first + "\n" + body
        if kind not in LABELS:
            if kind in LEGACY:
                FAIL_CONTENT.append(f"{stem}: callout [!{kind.upper()}] is not a V2 kind (RULE, NOTE, STOP, DONE)")
            else:
                FAIL_CONTENT.append(f"{stem}: unknown callout kind [!{kind.upper()}]")
        heading = ""
        if kind in ("note", "stop", "evidence", "field", "delivery"):
            bm = re.match(r"^\*\*(.+?)\*\*[ \t]*(?:\n|$)", body)
            if bm:
                heading, body = bm.group(1), body[bm.end():]
            else:
                bm = re.match(r"^\*\*(.+?)\*\*[ \t]+(?=\S)", body)
                if bm and len(bm.group(1)) <= 60:
                    heading, body = bm.group(1), body[bm.end():]
        attrs = ""
        if label:
            attrs += f' label="{label.replace(chr(34), "")}"'
        if heading:
            attrs += f' heading="{heading.replace(chr(34), "")}"'
        return f"\n::: {{.callout .{kind}{attrs}}}\n{body.strip()}\n:::\n\n"
    return outside_code(text, lambda c: CALLOUT_RE.sub(conv, c))


LIST_RE = re.compile(r"^(\s*(?:>\s*)?)(?:[-*+]|\d+[.)])\s")


def fix_glued_lists(text, stem):
    """A list line straight after a paragraph line is a paragraph in pandoc; insert the blank line."""
    def fix(chunk):
        out, prev, n = [], "", 0
        for line in chunk.split("\n"):
            core = re.sub(r"^\s*>\s?", "", prev)
            if (LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev)
                    and not core.startswith(("|", "#", "```", ":::", "---")) and not re.match(r"^\s{2,}", prev)):
                q = re.match(r"^(\s*>)", line)
                out.append(q.group(1) if q else "")
                n += 1
            out.append(line)
            prev = line
        if n:
            WARN.append(f"{stem}: inserted {n} blank line(s) before glued lists")
        return "\n".join(out)
    return outside_code(text, fix)


def load_chapters():
    """Return [(part_label, part_key, stem, meta, markdown, slot)] in V3 order, skipping missing files."""
    chapters, missing = [], []
    for part, key, slots in ORDER:
        for stem, fallbacks, legacy in slots:
            f = CH / f"{stem}.md"
            if legacy and (CH / f"{legacy}.md").exists():
                if f.exists():
                    WARN.append(f"{stem}.md is retired by {legacy}.md (same chapter id); not built. Delete it.")
                continue
            if not f.exists():
                f = next((CH / f"{fb}.md" for fb in fallbacks if (CH / f"{fb}.md").exists()), None)
                if f is None:
                    if not legacy:
                        missing.append(stem)
                    continue
                WARN.append(f"{stem}: V3 file not found; using V2 {f.name}")
            elif legacy:
                WARN.append(f"{stem}: V2 chapter still built until {legacy}.md exists; V3 folds it into other chapters")
            meta, txt = front_matter(f.read_text())
            txt = callouts(txt, f.stem)
            txt = fix_glued_lists(txt, f.stem)
            chapters.append((part, key, f.stem, meta, txt, stem))
    return chapters, missing


def evidence_ids():
    """Read the audit-ID allowlist; detailed evidence is not stored in the guide."""
    try:
        data = json.loads((ROOT / "evidence.json").read_text())
    except (OSError, ValueError) as error:
        FAIL_BUILD.append(f"cannot read audit IDs from evidence.json: {error}")
        return set()
    ids = data.get("audit_ids") if isinstance(data, dict) else None
    if not isinstance(ids, list) or not ids or any(
        not isinstance(i, str) or not re.fullmatch(r"[EMFX]\d{2}", i) for i in ids
    ):
        FAIL_BUILD.append("evidence.json audit_ids must be a nonempty list of evidence IDs")
        return set()
    if len(ids) != len(set(ids)):
        FAIL_BUILD.append("evidence.json contains duplicate audit IDs")
    return set(ids)


# ----------------------------------------------------------------------------- pandoc

def pandoc(md):
    r = subprocess.run(["pandoc", "-f", "markdown+pipe_tables+task_lists+fenced_divs+raw_html-implicit_figures",
                        "-t", "html5", "--section-divs", "--wrap=none", "--columns=100000",
                        "--syntax-highlighting=none"], input=md, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    return r.stdout


def split_level1(h):
    """[(id, classes, inner_html)] for each top-level <section class="level1">."""
    out, pos = [], 0
    tag = re.compile(r"<section\b[^>]*>|</section>")
    open_re = re.compile(r'<section id="([^"]*)" class="(level1[^"]*)">')
    while True:
        m = open_re.search(h, pos)
        if not m:
            break
        depth, i = 1, m.end()
        while depth:
            t = tag.search(h, i)
            if not t:
                sys.exit("unbalanced <section> in pandoc output")
            depth += 1 if t.group(0).startswith("<section") else -1
            i = t.end()
        out.append((m.group(1), m.group(2), h[m.end():t.start()]))
        pos = i
    return out


# ----------------------------------------------------------------------------- HTML transforms

def strip_evidence(h):
    """Chapters carry no chips (V3): drop `[E07]` from text nodes and every HTML comment (`<!-- E14 -->` audit marks)."""
    h = re.sub(r"[ \t]*<!--(?:(?!-->).)*-->(?=[,.;:!?)])", "", h, flags=re.S)   # "25 points <!-- E09 -->," -> "25 points,"
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    out, skip = [], 0
    for tok in re.split(r"(<[^>]+>)", h):
        if tok.startswith("<"):
            if re.match(r"<(pre|code)\b", tok):
                skip += 1
            elif re.match(r"</(pre|code)>", tok):
                skip = max(0, skip - 1)
            out.append(tok)
        else:
            out.append(tok if skip else re.sub(r"(?:[ \t]*\[[EMFX]\d{2}\])+", "", tok))
    return "".join(out)


NUM_HEAD = re.compile(r"^(#|n|%|score|\$)$|%|\$|\bscore\b|\bn\b$", re.I)


def tables(h, article_id):
    def one(m):
        t = m.group(0)
        t = re.sub(r"<colgroup>.*?</colgroup>\s*", "", t, flags=re.S)
        heads = [strip_tags(x) for x in re.findall(r"<th(?=[\s>])[^>]*>(.*?)</th>", t, flags=re.S)]
        body = re.search(r"<tbody>(.*?)</tbody>", t, flags=re.S)
        rows = re.findall(r"<tr>.*?</tr>", body.group(1), flags=re.S) if body else []
        ncol = len(heads) or (len(re.findall(r"<td", rows[0])) if rows else 0)
        cls = []
        is_reg = len(heads) >= 3 and [x.lower() for x in heads[:3]] == ["id", "claim", "value"]
        if is_reg:
            cls += ["reg", "wide"]
        if ncol == 2 and (not heads or not heads[0]):
            cls.append("kv")
        if ncol >= 5 and len(rows) > 8 and not is_reg:
            cls.append("rec")
        # text-heavy tables (long prose cells) stack on phones even with 3-4 columns
        avg = sum(len(strip_tags(r)) for r in rows) / len(rows) if rows else 0
        if 3 <= ncol < 5 and not is_reg and "rec" not in cls and avg > 110:
            cls.append("stack")
        elif ncol >= 5 and not is_reg and "rec" not in cls and avg > 110:
            cls.append("rec")
        if len(rows) > 12 and not is_reg:
            cls.append("sticky")
        if ncol > 7 and not is_reg:
            cls.append("wide")
            WARN.append(f"{article_id}: table with {ncol} columns ({heads[0] if heads else '?'}...) rendered .wide")
        numcols = {i for i, hd in enumerate(heads) if NUM_HEAD.search(hd) and len(hd) <= 12}
        firsts = [strip_tags(re.search(r"<td[^>]*>(.*?)</td>", r, flags=re.S).group(1)) for r in rows if "<td" in r]
        if firsts and heads and heads[0] not in ("#",) and max(len(x) for x in firsts) <= 48 and 0 not in numcols:
            cls.append("rowlabel")

        def cells(row):
            i = [0]

            def td(mm):
                k = i[0]
                i[0] += 1
                lab = heads[k] if k < len(heads) else ""
                c = ' class="num"' if k in numcols else ""
                return f'<td data-label="{esc(lab)}"{c}>'
            return re.sub(r"<td[^>]*>", td, row)
        if body:
            t = t.replace(body.group(0), "<tbody>" + "".join(cells(r) for r in rows) + "</tbody>")
        if heads:
            k = [-1]

            def th(mm):
                k[0] += 1
                return '<th class="num">' if k[0] in numcols else "<th>"
            t = re.sub(r"<th(?=[\s>])[^>]*>", th, t)
        t = t.replace("<table>", f'<table class="{" ".join(cls)}">', 1)
        return f'<div class="tw{" wide" if "wide" in cls else ""}">{t}</div>'
    return re.sub(r"<table>.*?</table>", one, h, flags=re.S)


SQL_KW = r"\b(SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|ON|AND|OR|NOT|IN|AS|WITH|GROUP|BY|ORDER|LIMIT|HAVING|UNION|ALL|DISTINCT|CASE|WHEN|THEN|ELSE|END|IS|NULL|OVER|PARTITION|DESC|ASC|COUNT|SUM|AVG|MIN|MAX|DATE|CAST|EXISTS|BETWEEN|LIKE|INTERVAL|TRUE|FALSE|ROW_NUMBER|COALESCE|EXCEPT|CREATE|TABLE|VIEW|INSERT|INTO|VALUES|UPDATE|SET|DELETE)\b"
HL = {
    "sql": re.compile(r"(?P<cm>--[^\n]*)|(?P<st>'(?:[^'\n]|'')*')|(?P<kw>" + SQL_KW + ")", re.I),
    "yaml": re.compile(r"(?P<cm>(?<![:\w&])#[^\n]*)|(?P<key>^[ \t]*-?[ \t]*[\w .\-/&()]+?(?=:(?:[ \t]|$)))", re.M),
    "markdown": re.compile(r"(?P<hd>^#{1,6}[ \t][^\n]*)|(?P<cm>^\|?[-:| ]+\|?$)|(?P<kw>\*\*[^*\n]+\*\*)", re.M),
    "md": None, "python": re.compile(r"(?P<cm>(?<!&)#[^\n]*)|(?P<st>\"[^\"\n]*\"|'[^'\n]*')|(?P<kw>\b(def|return|import|from|for|in|if|else|while|class|with|as|not|and|or|None|True|False)\b)"),
    "json": re.compile(r"(?P<key>\"[^\"\n]*\"(?=\s*:))|(?P<st>\"[^\"\n]*\")"),
    "bash": re.compile(r"(?P<cm>(?<!&)#[^\n]*)|(?P<st>\"[^\"\n]*\"|'[^'\n]*')"),
}
HL["md"] = HL["markdown"]
PH_RE = re.compile(r"(&lt;[a-z][^&\n]{0,80}?&gt;)")


def highlight(code, lang):
    rx = HL.get(lang)

    def hl(seg):
        if not rx:
            return seg
        return rx.sub(lambda m: f'<span class="{m.lastgroup}">{m.group(0)}</span>', seg)
    parts = PH_RE.split(code)
    return "".join(f'<span class="ph">{p}</span>' if i % 2 else hl(p) for i, p in enumerate(parts))


def code_blocks(h):
    """<pre class="lang"><code>..</code></pre> -> file cards with copy buttons, highlighting, placeholders."""
    def one(m):
        lang = (m.group(1) or "").strip().split()[0] if m.group(1) else ""
        code = m.group(2)
        lines = code.count("\n") + 1
        body = highlight(code, lang)
        tall = ' data-lines="%d"' % lines if lines > 40 else ""
        head = (f'<div class="file-head"><span class="fn"></span><span class="lang">{esc(lang)}</span>'
                f'<button type="button" class="copy" aria-label="Copy code">Copy</button></div>')
        fig = (f'<figure class="file{" tall" if tall else ""}"{tall}>{head}'
               f'<pre class="{esc(lang)}"><code>{body}</code></pre>'
               + ('<button type="button" class="showall">Show all %d lines</button>' % lines if tall and lang != "markdown" else "")
               + "</figure>")
        return with_md_render(fig) if lang == "markdown" else fig
    return re.sub(r'<pre(?: class="([^"]*)")?><code>(.*?)</code></pre>', one, h, flags=re.S)


def md_render(code_html):
    """Markdown shown in a file card: render it (tables become real tables) so nobody scrolls sideways through pipes."""
    raw = htmlmod.unescape(re.sub(r"<[^>]+>", "", code_html))
    r = subprocess.run(["pandoc", "-f", "markdown-raw_html-auto_identifiers+pipe_tables+task_lists", "-t", "html5", "--wrap=none"],
                       input=raw, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def with_md_render(fig_html):
    """Add a rendered panel after each markdown <pre> in a file card; the pre stays for Copy."""
    def one(m):
        pre = m.group(0)
        code = re.search(r"<code>(.*?)</code>", pre, flags=re.S)
        html = md_render(code.group(1)) if code else ""
        if not html:
            return pre
        tab = re.search(r'data-tab="(\d+)"', pre)
        hid = " hidden" if re.search(r"<pre[^>]*\shidden", pre) else ""
        return pre + f'<div class="md-render"{(' data-tab="' + tab.group(1) + '"') if tab else ""}{hid}>{html}</div>'
    out = re.sub(r"<pre[^>]*>.*?</pre>", one, fig_html, flags=re.S)
    return out.replace('<figure class="file', '<figure class="file has-md', 1) if out != fig_html else out


def templates(h, article_id):
    """::: {.template #id file= title=} with two fences (example, blank) -> tabbed file card."""
    def one(attrs, inner):
        tid, fn, title = attr(attrs, "id"), attr(attrs, "data-file"), attr(attrs, "title")
        figs = re.findall(r"<figure class=\"file[^\"]*\"[^>]*>.*?</figure>", inner, flags=re.S)
        prose = re.sub(r"<figure class=\"file[^\"]*\"[^>]*>.*?</figure>", "", inner, flags=re.S).strip()
        if not figs:
            FAIL_BUILD.append(f"{article_id}: template #{tid} has no code block")
            return m.group(0)
        pres = [re.search(r"<pre[^>]*><code>.*?</code></pre>", f, flags=re.S).group(0) for f in figs]
        lang = re.search(r'<pre class="([^"]*)"', pres[0])
        lang = lang.group(1) if lang else ""
        names = ["Example", "Blank template"] if len(pres) > 1 else [""]
        tabs = ""
        if len(pres) > 1:
            tabs = '<div class="tabs" role="tablist">' + "".join(
                f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-tab="{i}">{n}</button>'
                for i, n in enumerate(names)) + "</div>"
        panels = "".join(
            p.replace("<pre", f'<pre role="tabpanel" data-tab="{i}" data-tabname="{names[i]}"{"" if i == 0 else " hidden"}', 1)
            for i, p in enumerate(pres))
        head = (f'<div class="file-head"><span class="fn">{esc(fn)}</span><span class="lang">{esc(lang)}</span>{tabs}'
                f'<button type="button" class="copy" aria-label="Copy code">Copy</button></div>')
        ttl = f'<h3 class="tpl-title" id="{esc(tid)}"><span class="tpl-no">{esc(tid.upper().replace("-", "."))}</span> {esc(title)}</h3>' if title else ""
        fig = f'<figure class="file template-file" data-file="{esc(fn)}">{head}{panels}</figure>'
        if fn.endswith(".md") or lang == "markdown":
            fig = with_md_render(fig)
        return f'<section class="template" data-template="{esc(tid)}">{ttl}{prose}{fig}</section>'

    return replace_divs(h, "template", one)


def find_div(h, cls):
    """Yield (start, end, attrs, inner) for top-level <div ... class="cls"...> blocks (depth-tracked)."""
    open_re = re.compile(r'<div\b([^>]*\bclass="(?:[^"]*\s)?%s(?:\s[^"]*)?"[^>]*)>' % re.escape(cls))
    tag = re.compile(r"<div\b[^>]*>|</div>")
    pos = 0
    while True:
        m = open_re.search(h, pos)
        if not m:
            return
        depth, i = 1, m.end()
        while depth:
            t = tag.search(h, i)
            if not t:
                return
            depth += 1 if t.group(0).startswith("<div") else -1
            i = t.end()
        yield m.start(), i, m.group(1), h[m.end():t.start()]
        pos = i


def replace_divs(h, cls, fn):
    out, last = [], 0
    for s, e, attrs, inner in list(find_div(h, cls)):
        out.append(h[last:s])
        out.append(fn(attrs, inner))
        last = e
    out.append(h[last:])
    return "".join(out)


def attr(attrs, name):
    m = re.search(r'\b%s="([^"]*)"' % re.escape(name), attrs)
    return htmlmod.unescape(m.group(1)) if m else ""


def callout_html(h, article, state):
    def one(attrs, inner):
        kinds = attr(attrs, "class").split()
        kind = next((k for k in kinds if k != "callout"), "note")
        label = attr(attrs, "data-label")
        heading = attr(attrs, "data-heading")
        css, default = (LEGACY[kind] if kind in LEGACY else (kind, LABELS.get(kind, kind.title())))
        inner = inner.strip()
        if css == "rule":
            if not state.get("epigraph"):
                state["epigraph"] = strip_tags(inner)
                return ""
            return f'<div class="callout rule"><div class="callout-label">Rule</div>{inner}</div>'
        if css == "done":
            n = [0]

            def box(m):
                n[0] += 1
                text = strip_tags(m.group(2))[:80]
                key = f'{article}:{hashlib.sha1(text.encode()).hexdigest()[:8]}'
                return f'<li class="task"><input type="checkbox" data-key="{key}" id="k-{key.replace(":", "-")}"{m.group(1)}><label for="k-{key.replace(":", "-")}">{m.group(2)}</label></li>'
            inner = re.sub(r'<li>(?:<label>)?<input type="checkbox"( checked="")?(?: disabled="")? ?/?>\s*(.*?)(?:</label>)?</li>', box, inner, flags=re.S)
            inner = re.sub(r'<ul class="task-list">', '<ul class="task-list">', inner)
            return (f'<section class="callout done" data-items="{n[0]}"><div class="callout-head">'
                    f'<span class="callout-label">Definition of done</span><span class="done-count"></span>'
                    f'<button type="button" class="done-reset">Reset</button></div>{inner}</section>')
        lab = label or heading or default
        title = f'<span class="callout-title">{esc(heading)}</span>' if heading and label else ""
        tag = "aside" if css in ("note", "stop") else "div"
        return f'<{tag} class="callout {css}"><div class="callout-label">{esc(lab)}</div>{title}{inner}</{tag}>'
    return replace_divs(h, "callout", one)


def tldr(h):
    """`::: {.tldr}` -> the "In one minute" box under a chapter's rule. Skim mode keeps it and hides the long form."""
    return replace_divs(h, "tldr", lambda a, inner:
        '<aside class="tldr" aria-label="In one minute"><div class="tldr-head"><span class="tldr-label">In one minute</span>'
        '<button type="button" class="tldr-skim" aria-pressed="false" title="Show every chapter as its one-minute version (S)">Skim the book</button></div>'
        f'{inner}<button type="button" class="tldr-full" hidden>Read the full chapter</button></aside>')


def scenes(h):
    return replace_divs(h, "scene", lambda a, inner:
                        f'<aside class="scene"><div class="scene-label">In practice{(" · " + esc(attr(a, "data-week"))) if attr(a, "data-week") else ""}</div>{inner}</aside>')


def components(h):
    def one(attrs, inner):
        cid = attr(attrs, "id")
        extra = " ".join(f'{k}="{esc(v)}"' for k, v in re.findall(r'\b(data-[\w-]+)="([^"]*)"', attrs))
        return f'<div class="component" data-component="{esc(cid)}" id="{esc(cid)}" {extra}>{inner}</div>'
    return replace_divs(h, "component", one)


def cards(h, collected):
    def one(attrs, inner):
        cid = attr(attrs, "id")
        title = attr(attrs, "title")
        no = cid.upper() if re.fullmatch(r"c\d+", cid) else cid.upper()
        out = (f'<section class="card" id="{esc(cid)}" data-card="{esc(no)}"><header class="card-head">'
               f'<span class="card-no">Card</span><div class="card-title">{esc(title)}</div></header>'
               f'<div class="card-body">{inner}</div></section>')
        collected.append((cid, no, title, inner))
        return out
    return replace_divs(h, "card", one)


def svg_instance(svg, n):
    """Suffix internal ids so a diagram can appear more than once in the document."""
    ids = set(re.findall(r'(?<![\w-])id="([^"]+)"', svg))
    for i in ids:
        svg = re.sub(r'(?<![\w-])id="%s"' % re.escape(i), f'id="{i}-{n}"', svg)
        svg = svg.replace(f"url(#{i})", f"url(#{i}-{n})").replace(f'href="#{i}"', f'href="#{i}-{n}"')
    return svg


def ladder_data():
    """{"bars": [...], "negatives": [...]}: the V3 ladder from evidence.json's "ladder" list when present, else LADDER_V3."""
    ev = ROOT / "evidence.json"
    data = {"bars": LADDER_V3, "negatives": []}
    if ev.exists():
        try:
            j = json.loads(ev.read_text())
        except Exception as e:
            FAIL_BUILD.append(f"evidence.json is not valid JSON: {e}")
            j = {}
        j = j if isinstance(j, dict) else {}
        if isinstance(j.get("ladder"), list) and j["ladder"]:
            data["bars"] = j["ladder"]
        data["negatives"] = j.get("negatives") or []
    return data, "evidence.json" if data["bars"] is not LADDER_V3 else "LADDER_V3"


def _wrap(label, width=15, maxlines=4):
    lines, cur = [], ""
    for w in label.split():
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines - 1] + [lines[maxlines - 1] + "…"]
    return lines


def _val(b):
    return b.get("display") or f'{float(b["value"]):g}%'


def ladder_svg(data):
    """One ladder, four bars, plain labels, no IDs. The last bar is the metrics layer."""
    bars = data["bars"]
    W, H, L, R, T, B = 720, 360, 44, 16, 40, 78
    ph = H - T - B
    n = len(bars)
    gap = 28
    bw = (W - L - R - gap * (n - 1)) / n

    def y(v):
        return T + ph - v / 100 * ph
    o = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Accuracy ladder: '
         + esc(", ".join(f'{b["label"]} {_val(b)}' for b in bars)) + '">', "<title>What moved accuracy</title>",
         f'<text x="{L}" y="18" class="t" style="font-size:12.5px;font-weight:600;fill:var(--ink)">The same questions, bare schema plus one kind of context</text>']
    for tick in (0, 25, 50, 75, 100):
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{y(tick):.1f}" y2="{y(tick):.1f}" style="stroke:var(--line)" />')
        o.append(f'<text x="{L - 8}" y="{y(tick) + 4:.1f}" text-anchor="end" class="m" style="font-size:11px;fill:var(--muted)">{tick}%</text>')
    for i, b in enumerate(bars):
        x = L + i * (bw + gap)
        v = float(b["value"])
        last = i == n - 1
        style = "fill:var(--accent)" if last else "fill:var(--accent-soft);stroke:var(--accent);stroke-width:1"
        o.append(f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{(y(0) - y(v)):.1f}" rx="2" style="{style}" />')
        o.append(f'<text x="{x + bw / 2:.1f}" y="{y(v) - (24 if b.get("note") else 8):.1f}" text-anchor="middle" class="d" style="font-size:{20 if last else 17}px;font-weight:600;fill:var(--ink)">{esc(_val(b))}</text>')
        if b.get("note"):
            o.append(f'<text x="{x + bw / 2:.1f}" y="{y(v) - 8:.1f}" text-anchor="middle" class="t" style="font-size:11px;fill:var(--muted)">{esc(b["note"])}</text>')
        for k, ln in enumerate(_wrap(b["label"], 22)):
            o.append(f'<text x="{x + bw / 2:.1f}" y="{y(0) + 20 + k * 15:.1f}" text-anchor="middle" class="t" style="font-size:12.5px;fill:var(--{"ink" if last else "text"});font-weight:{600 if last else 400}">{esc(ln)}</text>')
    o.append(f'<text x="{W - R}" y="{H - 6}" text-anchor="end" class="m" style="font-size:10px;fill:var(--muted)">Source: internal benchmark</text>')
    o.append("</svg>")
    phone = ['<div class="d"><div class="d-lab">The same questions, bare schema plus one kind of context</div><div class="d-bars">']
    for i, b in enumerate(bars):
        v = float(b["value"])
        phone.append(f'<div class="d-bar{" last" if i == n - 1 else ""}"><div class="d-bar-l"><span>{esc(b["label"])}</span></div>'
                     f'<div class="d-bar-t"><i style="width:{v:.1f}%"></i></div><div class="d-bar-v m">{esc(_val(b))}</div></div>')
    phone.append('</div><p class="d-mono" style="margin:8px 0 0">Source: internal benchmark</p></div>')
    return "".join(o), "".join(phone)


def negatives_html(data):
    """What did not help: a before -> after dumbbell per row (HTML, responsive), text-only where no pair exists."""
    rows = data.get("negatives") or []
    if not rows:
        return ""
    o = ['<div class="d d-dumb">']
    for r in rows:
        b, a = r.get("before"), r.get("after")
        lab = esc(r.get("label", ""))
        idc = f'<span class="m">{esc(r.get("id", ""))}{(" · tier " + esc(r["tier"])) if r.get("tier") else ""}</span>'
        val = esc(r.get("delta_or_value", ""))
        if b is not None and a is not None:
            lo, hi = min(b, a), max(b, a)
            worse = a < b
            o.append(f'<div class="d-row"><div class="d-l">{lab}<br>{idc}</div><div class="d-t"><i class="d-seg" style="left:{lo}%;width:{max(0.3, hi - lo)}%"></i>'
                     f'<b class="d-b" style="left:{b}%" title="before"></b><b class="d-a{" worse" if worse else ""}" style="left:{a}%" title="after"></b></div><div class="d-v m">{val}</div></div>')
        else:
            pos = f'<b class="d-a worse" style="left:{a}%"></b>' if a is not None else ""
            o.append(f'<div class="d-row"><div class="d-l">{lab}<br>{idc}</div><div class="d-t">{pos}</div><div class="d-v m">{val}</div></div>')
    o.append('<div class="d-legend"><span><b class="d-b" style="position:static;display:inline-block"></b> before</span><span><b class="d-a worse" style="position:static;display:inline-block"></b> after</span><span>axis 0-100% of 107 questions</span></div></div>')
    return "".join(o)


def diagram_files(did):
    svg = DIAG / f"{did}.svg"
    htm = DIAG / f"{did}.html"
    phone = DIAG / f"{did}.phone.html"
    main = svg if svg.exists() else (htm if htm.exists() else None)
    return main, (phone if phone.exists() else None)


def diagrams(h, article, state, ladder):
    def one(attrs, inner):
        did = attr(attrs, "id")
        state["fig"] = state.get("fig", 0) + 1
        state["fig_ids"].append(did)
        # cards and unnumbered pages carry no chapter number; 0.1 keeps a single level (Figure 0.1, then 0.1b)
        # chapter numbers are hidden from readers: figures count per page ("Figure 2"); Reference keeps "Figure R1.2"
        num = state["num"] or ""
        figno = f'{num}.{state["fig"]}' if re.fullmatch(r"R\d+", num) else (str(state["fig"]) if state.get("numbered") else "")
        caption = inner.strip()
        n = sum(FIG_SEEN.values()) + 1
        if did == "ladder":
            body, phone = ladder["ladder"]
            body = svg_instance(body, n)
        elif did == "negatives" and ladder.get("negatives"):
            body, phone = ladder["negatives"], ""
        else:
            main, ph = diagram_files(did)
            if not main:
                FAIL_BUILD.append(f"{article}: diagram '{did}' has no diagrams/{did}.svg or .html")
                body, phone = f'<div class="fig-missing">Diagram <code>{esc(did)}</code> is missing</div>', ""
            else:
                body = svg_instance(main.read_text(), n)
                phone = svg_instance(ph.read_text(), n) if ph else ""
        if did not in DIAGRAM_IDS and did not in EXTRA_DIAGRAMS:
            WARN.append(f"{article}: diagram id '{did}' is not in the V2 diagram list")
        fid = f"fig-{did}" if did not in FIG_SEEN else f"fig-{did}-{FIG_SEEN[did] + 1}"
        FIG_SEEN[did] = FIG_SEEN.get(did, 0) + 1
        cls = "fig" + (" has-phone" if phone else "") + (" key-pick" if attr(attrs, "key") else "")
        return (f'<figure class="{cls}" id="{fid}" data-diagram="{esc(did)}"><div class="fig-body">{body}</div>'
                + (f'<div class="fig-phone">{phone}</div>' if phone else "")
                + f'<figcaption><span class="figno">{("Figure " + figno) if figno else "Figure"}</span> {caption}</figcaption></figure>')
    return replace_divs(h, "diagram", one)


def failure_cards(h, article):
    """R1 tables (header has Symptom) -> filterable cards."""
    if article != "r1" and 'data-component="failure-modes"' not in h:
        return h

    def one(m):
        t = m.group(0)
        heads = [strip_tags(x) for x in re.findall(r"<th(?=[\s>])[^>]*>(.*?)</th>", t, flags=re.S)]
        if not any(hd.lower().startswith("symptom") for hd in heads):
            return t
        col = {hd.lower().split()[0]: i for i, hd in enumerate(heads)}
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", re.search(r"<tbody>(.*?)</tbody>", t, flags=re.S).group(1), flags=re.S)
        chs, branches, cards_ = set(), set(), []
        for r in rows:
            tds = re.findall(r"<td[^>]*>(.*?)</td>", r, flags=re.S)

            def g(k):
                return tds[col[k]] if k in col and col[k] < len(tds) else ""
            chlist = re.findall(r"#(ch\d+)", g("chapter"))
            chs.update(chlist)
            branch = strip_tags(g("branch"))
            if branch:
                branches.add(branch)
            ev = g("evidence")
            measured = "1" if re.search(r'\[[EMFX]\d{2}\]|class="ev|^\s*measured', ev, re.I) else "0"
            phase = strip_tags(g("phase"))
            text = strip_tags(" ".join(tds)).lower()
            meta = "".join(f'<span class="chip">{esc(x)}</span>' for x in [branch, phase] if x)
            cards_.append(
                f'<article class="fm" data-ch="{" ".join(chlist)}" data-branch="{esc(branch)}" data-measured="{measured}" data-text="{esc(text)}">'
                f'<div class="fm-head"><span class="fm-no">{g("#")}</span><h4 class="fm-symptom">{g("symptom")}</h4></div>'
                f'<div class="fm-line"><span class="fm-k">Cause</span><span>{g("cause")}</span></div>'
                f'<div class="fm-line"><span class="fm-k">Fix</span><span>{g("fix")}</span></div>'
                f'<div class="fm-foot">{meta}<span class="fm-ev"><span class="chip-dim">{"measured" if measured == "1" else "diagnosis, not measured"}</span></span><span class="fm-ch">{g("chapter")}</span></div></article>')
        chips = "".join(f'<button type="button" class="fchip" data-f="ch" data-v="{c}">Ch {c[2:].lstrip("0") or "0"}</button>' for c in sorted(chs, key=lambda x: int(x[2:])))
        bchips = "".join(f'<button type="button" class="fchip" data-f="branch" data-v="{esc(b)}">{esc(b)}</button>' for b in sorted(branches))
        bar = (f'<div class="fm-filter"><input type="search" class="fm-q" placeholder="Filter by symptom, cause or fix" aria-label="Filter failure modes">'
               f'<div class="fchips">{bchips}{chips}<button type="button" class="fchip" data-f="measured" data-v="1">Measured</button></div>'
               f'<span class="fm-count"></span></div>')
        return f'<div class="fm-block">{bar}<div class="fm-grid">{"".join(cards_)}</div></div>'
    return re.sub(r'<div class="tw[^"]*"><table[^>]*>.*?</table></div>', one, h, flags=re.S)


def parse_title(h1):
    """'7. Phase 3 · Hill-climb' -> ('7', 'Phase 3 · Hill-climb'); 'R3. Evidence' -> ('R3', ...)."""
    text = h1.strip()
    m = re.match(r"^((?:\d+(?:\.\d+)?)|R\d+|C\d+|Appendix [A-Z])[.·:]?\s+(.*)$", text, re.S)
    if m:
        return m.group(1), m.group(2)
    return "", text


def words_of(h):
    return len(re.findall(r"[A-Za-z0-9]+", strip_tags(h)))


def reading_words(h):
    """Words a reader reads: code blocks, drawn diagrams (SVG and their phone twins), scripts and buttons excluded.
    Captions and tables count. Used for every minutes estimate (chapter header and door steps)."""
    h = re.sub(r"<(pre|svg|script|button|style)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r'<div class="fig-phone">.*?</div>(?=<figcaption)', " ", h, flags=re.S)
    return words_of(h)


def minutes_for(words):
    return max(1, round(words / 230))


# Part II headings may carry their phase or week ("# 5. Phase 2: generate metrics"): the label is shown once,
# small, above the title, and the title is the rest ("Generate metrics").
PHASE_TITLE_RE = re.compile(r"^\s*(Phase\s+[0-4]|Week\s+[1-4])\b\s*[:·.,\-–]?\s*(.*)$", re.I | re.S)


def split_phase_title(title_html, slot):
    """('Phase 2', 'Generate metrics') for a Part II title; the label falls back to the slot's phase."""
    m = PHASE_TITLE_RE.match(title_html)
    if m and m.group(2).strip():
        label = re.sub(r"\s+", " ", m.group(1)).title()
        rest = m.group(2).strip()
    else:
        slots = [p[0] for p in PHASES]
        label = PHASES[slots.index(slot)][1] if slot in slots else ""
        rest = title_html.strip()
    rest = re.sub(r"^(<[^>]+>)*([a-z])", lambda mm: (mm.group(1) or "") + mm.group(2).upper(), rest, count=1)
    return label, rest


READ_MORE_RE = re.compile(r"<p>Read more:\s*(.*?)</p>", re.S)


def read_more(h):
    """A paragraph starting `Read more:` becomes the quiet end-of-section link: `Read more: [Phase 2](#ch05)`."""
    def one(m):
        inner = m.group(1).strip()
        if "<a " not in inner:
            FAIL_CONTENT.append(f"'Read more:' paragraph without a link: {strip_tags(inner)[:60]}")
            return m.group(0)
        inner = re.sub(r"(<a\b[^>]*>)(.*?)</a>", lambda a: f'{a.group(1)}<span class="rm-t">{a.group(2)}</span><span class="rm-arrow" aria-hidden="true"> →</span></a>', inner, flags=re.S)
        inner = re.sub(r"\.\s*$", "", inner)
        return f'<p class="read-more"><span class="rm-k">Read more</span> {inner}</p>'
    return READ_MORE_RE.sub(one, h)


def resolve_links(articles, collected):
    """After assembly: card links render as small title chips (never "C6"); an empty link text in a Read more
    line is filled with its target's title."""
    cards_ = {cid: title for cid, _, title, _ in collected}
    titles = {}
    for a in articles:
        titles[a["id"]] = a["title"]
        for m in re.finditer(r'<section id="([^"]+)" class="level[23]">\s*<h[23][^>]*>(.*?)</h[23]>', a["html"], flags=re.S):
            titles.setdefault(m.group(1), strip_tags(m.group(2)))
        for m in re.finditer(r'<h3 class="tpl-title" id="([^"]+)">.*?</span>\s*(.*?)</h3>', a["html"], flags=re.S):
            titles.setdefault(m.group(1), strip_tags(m.group(2)))
    titles.update(cards_)
    for a in articles:
        h = a["html"]
        h = re.sub(r'(<a href="#([^"]+)"[^>]*><span class="rm-t">)(</span>)',
                   lambda m: m.group(1) + esc(titles.get(m.group(2), m.group(2))) + m.group(3), h)

        def card(m):
            cid = m.group(1)
            if cid not in cards_:
                return m.group(0)
            return f'<a class="card-ref" href="#{cid}" title="Card: one-page checklist you can print">{esc(cards_[cid])}</a>'
        h = re.sub(r'<a href="#(c\d+)">(?:(?!</a>).)*</a>', card, h, flags=re.S)
        a["html"] = h


def phase_strip(current):
    cells = []
    for i, (slot, short, name) in enumerate(PHASES):
        on = " on" if i == current else (" past" if current is not None and i < current else "")
        href = SLOT_ARTICLE.get(slot, "")
        tag, attr_ = ("a", f' href="#{href}"') if href else ("span", "")
        cells.append(f'<{tag} class="ps{on}"{attr_}><span class="ps-no">{esc(short)}</span><span class="ps-name">{esc(name)}</span></{tag}>')
    cells.append('<a class="ps ps-loop" href="#lifecycle" title="The whole lifecycle on one page"><span class="ps-no">↻</span><span class="ps-name">The lifecycle</span></a>')
    return f'<nav class="phase-strip" aria-label="The lifecycle">{"".join(cells)}</nav>'


def phase_index(meta_phase, slot):
    """'Phase 0' / '0' -> 0, 'Phase 3' / '3 · Hill climb' -> 3; else the slot's place in PHASES; else None."""
    m = re.match(r"^\s*(?:phase|week|wk)?\s*(\d)\b", meta_phase or "", re.I)
    if m and int(m.group(1)) < len(PHASES):
        return int(m.group(1))
    slots = [p[0] for p in PHASES]
    return slots.index(slot) if slot in slots else None


def transform_article(aid, inner, part_label, part_key, meta, ladder, collected_cards, slot="", stem=""):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", inner, flags=re.S)
    h1 = m.group(1) if m else aid
    inner = inner.replace(m.group(0), "", 1) if m else inner
    num, title = parse_title(h1)
    if meta.get("number"):
        num = meta["number"]
    # readers never see a chapter number (V3 decision 3): only Reference keeps R1-R5
    if not re.fullmatch(r"R\d+", num or ""):
        num = ""
    plabel = ""
    if part_key == "part2":
        plabel, title = split_phase_title(title, slot or stem)
    state = {"num": num, "fig_seen": {}, "fig_ids": [], "numbered": part_key in ("start", "part1", "part2", "part3", "part4")}
    inner = callout_html(inner, aid, state)
    inner = scenes(inner)
    inner = tldr(inner)
    inner = tables(inner, aid)
    inner = code_blocks(inner)
    inner = templates(inner, aid)
    inner = cards(inner, collected_cards)
    inner = components(inner)
    inner = diagrams(inner, aid, state, ladder)
    inner = failure_cards(inner, aid)
    inner = strip_evidence(inner)
    inner = read_more(inner)
    words = words_of(inner)
    minutes = meta.get("minutes") or str(minutes_for(reading_words(inner)))
    # header. No chapter numbers anywhere; Part II shows its phase or week once, as the small label above the title.
    # the small label above the title names the sidebar group the page sits in, so the header and the contents agree
    label = next((g for g, items in NAV_GROUPS if aid in nav_ids(items)), None) or {"start": "Start here", "cards": "Toolkit", "research": "Research", "ref": "Reference"}.get(part_key, part_label)
    if label and strip_tags(label).strip().lower() == strip_tags(title).strip().lower():
        label = ""
    if part_key == "part2" and plabel:
        label = plabel
    chno = num if part_key == "ref" else ""
    metas = []
    for k in ("for", "produces"):
        if meta.get(k):
            metas.append(f'<span><b>{esc(k.title() if k != "for" else "For")}</b> {esc(meta[k])}</span>')
    if aid == "listen":
        metas.append('<span><b>Listen</b> 3 episodes · 9–20 min each</span>')
    else:
        metas.append(f'<span><b>Read</b> {esc(minutes)} min</span>')
    cur = phase_index(meta.get("phase", ""), slot) if slot and (part_key == "part2" or slot in [p[0] for p in PHASES]) else None
    strip = phase_strip(cur) if cur is not None else ""
    epi = f'<p class="epigraph">{esc(state["epigraph"])}</p>' if state.get("epigraph") else ""
    head = (f'<header class="ch-head"><div class="ch-part">{esc(label)}</div>'
            + (f'<div class="ch-no">{esc(chno)}</div>' if chno else "")
            + f'<h1>{title}</h1>{epi}<div class="ch-meta">{"".join(metas)}</div>{strip}</header>')
    head = head.replace('<header class="ch-head">', f'<header class="ch-head" id="{esc(aid)}-intro">', 1)
    nav_title = f"{plabel} · {strip_tags(title)}" if plabel else strip_tags(title)
    return {"id": aid, "num": num, "title": nav_title, "title_html": title, "label": plabel, "part": part_label,
            "part_key": part_key, "html": head + inner, "words": words, "minutes": minutes, "epigraph": state.get("epigraph", ""),
            "fig_ids": state["fig_ids"], "stem": stem}


# ----------------------------------------------------------------------------- assembly

def dedupe_ids(articles):
    seen = {}
    for a in articles:
        def fix(m):
            i = m.group(1)
            if i in seen:
                seen[i] += 1
                WARN.append(f"duplicate id '{i}' in {a['id']} renamed {i}-{seen[i]}")
                return f'id="{i}-{seen[i]}"'
            seen[i] = 1
            return m.group(0)
        a["html"] = re.sub(r'(?<![\w-])id="([^"]+)"', fix, a["html"])
    return seen


# Pages that stay in the book (other pages are built from them, or link into them) but not in the sidebar.
# "doors" feeds the home page's "Pick your path" cards, which already sit at the top of the book.
NAV_HIDE = {"doors"}

# Sidebar groups. Navigation only: ORDER still sets the reading order, prev/next and the book sequence.
# The groups follow what the reader is doing, which is also how the three reading paths split the book:
# sponsors mostly read Understand, builders Build, delivery leads Run. Each group is collapsible and opens
# on the page the reader is on. An article not listed here lands in a trailing group named after its part.
NAV_GROUPS = [
    ("Why it is hard", ["ch01"]),
    ("How to build one", ["start",
                          ("Principles", ["ch-evals", "ch02", "ch-retrieval"]),
                          ("Phases", ["ch03", "ch04", "ch05", "ch06", "ch07"]),
                          ("After launch", ["ch-run"])]),
    ("Toolkit", ["assess", "cards", "r2", "videos", "listen"]),
    ("Research and reference", ["results", "r3", "r6", "r1", "r4", "r5", "r7"]),
]
NAV_BADGE = {"ch-evals": "1", "ch02": "2", "ch-retrieval": "3"}
# A heading above the group it names: what the reader learns, then what they keep to hand.
NAV_SECTION = {"Why it is hard": "Learn", "Toolkit": "Resources"}
# Row icons, Lucide line icons (ISC licence), drawn on a 24-unit grid.
ICONS = {
    "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "hammer": '<path d="m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>',
    "puzzle": '<path d="M15.39 4.39a1 1 0 0 0 1.68-.474 2.5 2.5 0 1 1 3.014 3.015 1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474 2.5 2.5 0 1 0-3.014 3.015 1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474 2.5 2.5 0 1 1-3.014-3.015 1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474 2.5 2.5 0 1 0 3.014-3.015 1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "library": '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
    "chevron": '<path d="m9 18 6-6-6-6"/>',
    "star": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
}
NAV_ICON = {"Why it is hard": "alert", "How to build one": "hammer",
            "Toolkit": "wrench", "Research and reference": "library"}


def icon(name, cls="toc-i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def nav_ids(items):
    """Flat page ids of a NAV_GROUPS entry, sub-labels removed."""
    out = []
    for it in items:
        out.extend(it[1] if isinstance(it, tuple) else [it])
    return out


def build_nav(articles, parts_order):
    by = {a["id"]: a for a in articles}
    placed = set()
    groups = []
    for label, items in NAV_GROUPS:
        rows = []   # (sublabel or None, [articles])
        for it in items:
            sub, ids = it if isinstance(it, tuple) else (None, [it])
            arts = [by[i] for i in ids if i in by and i not in NAV_HIDE]
            placed.update(a["id"] for a in arts)
            if arts:
                rows.append((sub, arts))
        if rows:
            groups.append((label, rows))
    # anything the groups do not name keeps its part label, so a new chapter is never lost from the sidebar
    rest = {}
    for a in articles:
        if a["id"] in placed or a["id"] in NAV_HIDE:
            continue
        rest.setdefault(a["part_key"], []).append(a)
    for label, key in parts_order:
        if key in rest:
            groups.append((label.split("·")[-1].strip(), [(None, rest[key])]))

    def row(a, ico=""):
        no = a["num"] if (a["num"] and str(a["num"]).startswith("R")) else ""
        lab = a.get("label") or ""
        m = re.match(r"(Phase|Week)\s*(\d+)", lab)
        if m:
            no = ("P" if m.group(1) == "Phase" else "W") + m.group(2)
        no = NAV_BADGE.get(a["id"], no)
        title = strip_tags(a["title_html"]) if lab else a["title"]
        return f'<a href="#{a["id"]}" data-ch="{a["id"]}">{ico}<span class="toc-no">{esc(no)}</span><span class="toc-t">{esc(title)}</span><span class="toc-marks"></span></a>'

    out = ['<div class="toc-tools"><input type="search" id="toc-q" placeholder="Filter contents  /" aria-label="Filter contents"><div id="toc-hits" hidden></div></div>',
           f'<a class="toc-home" href="#home">{icon("home")} Overview</a>',
           '<div class="toc-path" id="toc-path"></div>', '<div class="toc-list">']
    for label, rows in groups:
        if label in NAV_SECTION:
            out.append(f'<div class="toc-sec">{esc(NAV_SECTION[label])}</div>')
        ico = icon(NAV_ICON[label]) if label in NAV_ICON else ""
        n = sum(len(arts) for _, arts in rows)
        if n == 1:
            # a group of one page is a plain row: no disclosure to open for a single item
            out.append(f'<div class="toc-solo">{row(rows[0][1][0], ico)}</div>')
            continue
        out.append(f'<details class="toc-part"><summary class="toc-part-label">{ico}<span class="toc-g">{esc(label)}</span>'
                   f'<span class="toc-n">{n}</span>{icon("chevron", "toc-chev")}</summary><ul>')
        for sub, arts in rows:
            if sub:
                out.append(f'<li class="toc-sub" aria-hidden="true">{esc(sub)}</li>')
            for a in arts:
                out.append(f'<li>{row(a)}</li>')
        out.append("</ul></details>")
    out.append("</div>")
    # the star count is filled in by the page script from GitHub's public API; without it the link shows no count
    slug = REPO_URL.removeprefix("https://github.com/").strip("/") if REPO_URL.startswith("https://github.com/") else ""
    out.append(f'<a class="toc-repo" href="{esc(REPO_URL)}" target="_blank" rel="noopener" data-repo="{esc(slug)}">{icon("github")} GitHub'
               f'<span class="toc-stars" hidden>{icon("star", "toc-star")}<span></span></span></a>')
    return "".join(out)


def search_index(articles):
    idx = []
    for a in articles:
        h = a["html"]
        idx.append({"t": a["title"], "id": a["id"], "k": "chapter", "ch": a["id"], "s": a["epigraph"][:140]})
        for m in re.finditer(r'<section id="([^"]+)" class="level[23]">\s*<h([23])[^>]*>(.*?)</h\2>(.*?)(?=<section|</section|$)', h, flags=re.S):
            body = strip_tags(re.sub(r"<(pre|table|figure).*?</\1>", "", m.group(4), flags=re.S))
            idx.append({"t": strip_tags(m.group(3)), "id": m.group(1), "k": "section", "ch": a["id"], "s": body[:140]})
        for m in re.finditer(r'<h3 class="tpl-title" id="([^"]+)">(.*?)</h3>', h, flags=re.S):
            idx.append({"t": strip_tags(m.group(2)), "id": m.group(1), "k": "template", "ch": a["id"], "s": ""})
        for m in re.finditer(r'<article class="fm"[^>]*>.*?<h4 class="fm-symptom">(.*?)</h4>.*?<span class="fm-k">Fix</span><span>(.*?)</span>', h, flags=re.S):
            idx.append({"t": strip_tags(m.group(1)), "id": a["id"], "k": "failure mode", "ch": a["id"], "s": strip_tags(m.group(2))[:140]})
        if a["id"] == "r4":
            for m in re.finditer(r"<p><strong>([^<]{2,60})</strong>(.*?)</p>", h, flags=re.S):
                idx.append({"t": strip_tags(m.group(1)).rstrip("."), "id": a["id"], "k": "glossary", "ch": a["id"], "s": strip_tags(m.group(2))[:140]})
        for m in re.finditer(r'<section class="card" id="([^"]+)" data-card="([^"]+)">.*?<div class="card-title">(.*?)</div>', h, flags=re.S):
            idx.append({"t": strip_tags(m.group(3)), "id": m.group(1), "k": "card", "ch": a["id"], "s": ""})
    return idx


HERO_CAPTION = ("The model and questions stay fixed. Only the context changes: first the bare tables, then AI-generated "
                "metric SQL and trusted past queries, retrieved for each question. The playbook shows you how to build that layer.")
# Plain-language bar names for the cover card, keyed by ladder id. The ladder chart keeps its own labels.
HERO_LABELS = {"E03": "Tables and columns only", "E52": "Plus AI-generated metrics and trusted past queries"}


def element_by_id(h, eid):
    """(tag, outer_html) of the element carrying id="eid" in h, depth-tracked on its own tag; else (None, "")."""
    m = re.search(r'<(\w+)\b[^>]*?(?<![\w-])id="%s"[^>]*>' % re.escape(eid), h)
    if not m:
        return None, ""
    tag = m.group(1)
    rx = re.compile(r"<%s\b[^>]*>|</%s>" % (tag, tag))
    depth, i = 1, m.end()
    while depth:
        t = rx.search(h, i)
        if not t:
            return tag, h[m.start():]
        depth += -1 if t.group(0).startswith("</") else 1
        i = t.end()
    return tag, h[m.start():i]


def level2_sections(h):
    """[(id, h2_html, inner_html)] for each <section class="level2"> in h, nested sections included in inner."""
    out = []
    for m in re.finditer(r'<section id="([^"]+)" class="level2">', h):
        _, outer = element_by_id(h[m.start():], m.group(1))
        hm = re.search(r"<h2[^>]*>(.*?)</h2>", outer, flags=re.S)
        out.append((m.group(1), hm.group(1) if hm else "", outer[hm.end():] if hm else outer))
    return out


def card_minutes(articles, cid):
    """A card reads in about 1-2 minutes: its own words, clamped."""
    art = next((a for a in articles if a["part_key"] == "cards"), None)
    _, outer = element_by_id(art["html"], cid) if art else (None, "")
    return min(2, max(1, round(reading_words(outer) / 230)))


def intro_minutes(a):
    """Minutes for a chapter's opening: after its header, before its first ## section."""
    first = re.search(r'<section id="[^"]+" class="level2">', a["html"])
    intro = a["html"][:first.start()] if first else a["html"]
    intro = re.sub(r'<header class="ch-head"[^>]*>.*?</header>', " ", intro, flags=re.S)
    return minutes_for(reading_words(intro))


def door_steps(articles, body, card_titles):
    """The reading path a door links, in order: the links of its first ordered list, else every non-card link.
    A step is a chapter (#ch03), a section (#ch02-lanes, any id inside a chapter), a chapter's opening before its
    first section (#start-intro) or a card (#c2). Each step is {id, a, t, ch, kind, min}: minutes come from the
    words of that step only (a section runs from its heading to the next heading of the same level); a card
    counts 1-2 minutes."""
    ol = re.search(r"<ol\b.*?</ol>", body, flags=re.S)
    hrefs = re.findall(r'href="#([^"]+)"', ol.group(0) if ol else body)
    if not ol:
        hrefs = [x for x in hrefs if not re.fullmatch(r"c\d+", x)]
    steps, seen = [], set()
    for href in hrefs:
        if href in seen:
            continue
        step = None
        if href in card_titles:
            step = {"id": href, "a": "cards", "t": card_titles[href], "ch": "Card", "kind": "card",
                    "min": card_minutes(articles, href)}
        else:
            for a in articles:
                if href == a["id"]:
                    step = {"id": href, "a": a["id"], "t": a["title"], "ch": "", "kind": "chapter", "min": int(a["minutes"]) if str(a["minutes"]).isdigit() else minutes_for(reading_words(a["html"]))}
                    break
                if href == f'{a["id"]}-intro':
                    step = {"id": href, "a": a["id"], "t": "Opening", "ch": a["title"], "kind": "intro", "min": intro_minutes(a)}
                    break
                tag, outer = element_by_id(a["html"], href)
                if tag:
                    if tag != "section":
                        # an id on a heading, figure or template: count the enclosing section
                        k = a["html"].find(outer)
                        encl = [m for m in re.finditer(r'<section id="([^"]+)" class="level[23]">', a["html"][:k])]
                        for m in reversed(encl):
                            _, o2 = element_by_id(a["html"], m.group(1))
                            if outer in o2:
                                outer = o2
                                break
                    hm = re.search(r"<h[2-4][^>]*>(.*?)</h[2-4]>", outer, flags=re.S)
                    title = strip_tags(hm.group(1)) if hm else href
                    step = {"id": href, "a": a["id"], "t": title, "ch": a["title"], "kind": "section", "min": minutes_for(reading_words(outer))}
                    break
        if step and step["a"] != "cards" or (step and step["kind"] == "card"):
            steps.append(step)
            seen.add(href)
        elif not step:
            WARN.append(f"door link #{href} resolves to nothing; left out of the path")
    # a chapter link followed by links to its own sections means "its opening, then those sections": count the
    # opening only, so the chapter's minutes are not counted twice
    by = {a["id"]: a for a in articles}
    for st in steps:
        if st["kind"] == "chapter" and any(o["a"] == st["a"] and o["kind"] == "section" for o in steps):
            st["min"] = intro_minutes(by[st["a"]])
            st["kind"] = "intro"
            st["id"] = f'{st["a"]}-intro'      # the path then stops at the first section, not the chapter's end
    return steps


def door_step_html(st):
    lead = ""
    if st["kind"] == "card":
        lead = '<span class="ds-ch ds-card">Card</span>'
    elif st["ch"]:
        lead = f'<span class="ds-ch">{esc(st["ch"])}</span>'
    return (f'<li><a href="#{st["id"]}"><span class="ds-no" aria-hidden="true"></span><span class="ds-t">{lead}{esc(st["t"])}</span>'
            f'<span class="ds-min">{st["min"]} min</span></a></li>')


def hero_value(b):
    """The cover number: '80.8' is shown as '~81%' when the ladder bar says 'about 81%', so cover and prose agree."""
    d = (b.get("display") or "").strip()
    m = re.match(r"^about\s+(\d+(?:\.\d+)?%?)$", d)
    if m:
        v = m.group(1)
        return "~" + (v if v.endswith("%") else v + "%")
    return f'{float(b["value"]):g}%'


def landing(articles, ladder, collected=(), vids=()):
    by = {a["id"]: a for a in articles}
    card_titles = {cid: title for cid, _, title, _ in collected}
    bars = ladder["bars"]
    lo, hi = bars[0], bars[-1]
    # the cover readout: the two ends of the ladder as bars on one 0-100% scale (the numbers stay the headline)
    def hero_row(b, on):
        return (f'<div class="hero-row{" on" if on else ""}"><span class="hero-l">{esc(HERO_LABELS.get(b.get("id"), b["label"]))}</span>'
                f'<span class="hero-n">{esc(hero_value(b))}</span>'
                f'<span class="hero-bar" aria-hidden="true"><i style="width:{min(100.0, max(0.0, float(b["value"]))):.1f}%"></i></span></div>')
    hero = (f'<figure class="hero"><div class="hero-k"><span>Questions answered correctly</span><span>107 business questions, one model</span></div>'
            f'{hero_row(lo, False)}{hero_row(hi, True)}<p class="hero-cap">{esc(HERO_CAPTION)} <a href="#r3">How we measured →</a></p></figure>')
    doors_html, paths = "", {}
    src = by.get("doors")
    if src:
        rows = []
        for sid, h2, body in level2_sections(src["html"])[:3]:
            key = re.sub(r"[^a-z]+", "-", strip_tags(h2).lower()).strip("-")
            steps = door_steps(articles, body, card_titles)
            paths[key] = [st["id"] for st in steps]
            body = re.sub(r"<h\d[^>]*>.*?</h\d>", "", body, flags=re.S)
            paras = re.findall(r"<p>(.*?)</p>", body, flags=re.S)
            who = strip_tags(paras[0]) if paras else ""
            in_path = {st["id"] for st in steps}
            cards_ = [c for c in dict.fromkeys(re.findall(r'href="#(c\d+)"', body)) if c not in in_path and c in card_titles]
            # the total counts the path and the extra cards (about 1-2 minutes each)
            total = sum(st["min"] for st in steps) + sum(card_minutes(articles, c) for c in cards_)
            ncards = sum(1 for st in steps if st["kind"] == "card") + len(cards_)
            cards_html = ""
            if cards_:
                cards_html = ('<h3 class="door-rec">Cards for you</h3><p class="door-note">Cards are one-page checklists you can print.</p>'
                              '<ul class="door-cards">' + "".join(
                                  f'<li><a class="card-ref" href="#{c}">{esc(card_titles.get(c, c))}</a></li>' for c in cards_) + "</ul>")
            note = '<p class="door-note">Cards are one-page checklists you can print.</p>' if ncards and not cards_ else ""
            nsteps = sum(1 for st in steps if st["kind"] != "card")
            bid = f"door-{key}"
            info = json.dumps([{"id": st["id"], "a": st["a"], "t": (st["ch"] + " · " if st["ch"] and st["kind"] != "card" else ("Card · " if st["kind"] == "card" else "")) + st["t"]} for st in steps], ensure_ascii=False)
            listen = re.search(r'<p class="door-listen">.*?</p>', body, flags=re.S)
            rows.append(
                f'<details class="door" name="doors" data-role="{key}" data-path="{" ".join(paths[key])}" data-steps="{esc(info)}">'
                f'<summary class="door-sum" id="{bid}-sum"><span class="door-h">{strip_tags(h2)}</span>'
                f'<span class="door-meta">{nsteps} {"reading" if nsteps == 1 else "readings"}{f" · {ncards} {chr(99)}ard{chr(115) if ncards != 1 else chr(32)}".rstrip() if ncards else ""} · about {total} min</span>'
                f'<span class="door-chev" aria-hidden="true"></span></summary>'
                f'<div class="door-body" role="region" aria-labelledby="{bid}-sum">'
                f'<p class="door-who">{esc(who)}</p>'
                f'<div class="door-act"><button type="button" class="door-pick">Follow this path</button>'
                + (re.sub(r'^<p[^>]*>|</p>$', '', listen.group(0)) if listen else "") +
                '<span class="door-start"></span></div>'
                f'<h3 class="door-rec">Recommended reading</h3><ol class="door-steps">{"".join(door_step_html(st) for st in steps)}</ol>{note}{cards_html}</div></details>')
        doors_html = f'<div class="doors">{"".join(rows)}</div>'
    home_vid = "".join(video_block(v) for v in vids if v["aid"] == "home")
    # what the reader walks away with, and the map of the book, written in the reading-paths chapter
    home_secs = ""
    if src:
        secs = {sid: (h2, body) for sid, h2, body in level2_sections(src["html"])}
        for sid in ("paths-outcome", "paths-inside"):
            if sid in secs:
                h2, body = secs[sid]
                home_secs += (f'<section class="home-sec" id="{sid.replace("paths-", "home-")}">'
                              f'<h2 class="home-h">{strip_tags(h2)}</h2>{body}</section>')
    start = "start" if "start" in by else next((a["id"] for a in articles), "")
    first_ch = next((a["id"] for a in articles if a["part_key"] == "part1"), "")
    links = ('<p class="home-links">'
             + (f'<a href="#{first_ch}">Why analytics agents are hard →</a> ' if first_ch else "")
             + ('<a href="#lifecycle">The lifecycle in one picture →</a> ' if "lifecycle" in by else "")
             + f'<a href="#{start}">The method at a glance →</a>'
             + (' <a href="#assess">Where are you starting? →</a>' if "assess" in by else "") + "</p>")
    nch = sum(1 for a in articles if a["part_key"] in ("part1", "part2", "part3", "part4"))
    ncards = len(collected)
    return (f'<article class="ch home" id="home"><header class="cover"><div class="kicker"><span>Atlan</span>'
            f'<span class="meta"><span>Five phases</span><span>{nch} chapters</span>{f"<span>{ncards} cards</span>" if ncards else ""}</span></div>'
            f'<div class="cover-t"><h1>{TITLE}<span>From demo to production.</span></h1>'
            f'<p class="thesis">Your analytics agent gets questions wrong when it lacks your business context. It needs to know what each metric means, which tables join, and how your analysts already write the SQL. A better model leaves that gap open. We measured this on our own benchmark, with one model and one question set throughout. This playbook turns what worked into a method: build that context as a governed, measured asset, one domain at a time.</p></div>'
            '<p class="cover-listen"><a class="listen-cta" href="#listen-sponsor" data-podcast="listen-sponsor">'
            '<span aria-hidden="true">▶</span> Listen to the overview <small>14 min</small></a></p>'
            f'{hero}</header>{home_vid}{home_secs}'
            f'<h2 class="home-h">Pick your path</h2>{doors_html}{links}</article>'), paths


def inline_cards(articles, collected):
    """A chapter that ends with `Card: [C6 …](#c6)` gets a copy of that card right after the link."""
    by = {cid: (cid, no, title, inner) for cid, no, title, inner in collected}
    for a in articles:
        if a["part_key"] == "cards":
            continue

        def clone(m):
            ids = [i for i in re.findall(r'href="#(c\d+)"', m.group(0)) if i in by]
            out = m.group(0)
            for cid in ids:
                _, no, title, inner = by[cid]
                inner = strip_evidence(inner)
                out += (f'<section class="card card-inline" id="{cid}-{a["id"]}" data-card="{no}"><header class="card-head">'
                        f'<span class="card-no">Card</span><div class="card-title">{esc(title)}</div>'
                        f'<a class="card-src" href="#cards">all cards →</a></header><div class="card-body">{inner}</div></section>')
            return out
        a["html"] = re.sub(r'<p>(?:<strong>)?Cards?:?(?:</strong>)?\s*<a href="#c\d+">.*?</p>', clone, a["html"], flags=re.S)


def cards_article(articles, collected):
    idx = next((i for i, a in enumerate(articles) if a["id"] == "cards"), None)
    if not collected:
        return
    clones = "".join(
        f'<section class="card" id="cards-{cid}" data-card="{esc(no)}"><header class="card-head"><span class="card-no">Card</span>'
        f'<div class="card-title">{esc(title)}</div></header><div class="card-body">{strip_evidence(inner)}</div></section>'
        for cid, no, title, inner in collected)
    if idx is None:
        articles.append({"id": "cards", "num": "", "title": "Cards", "title_html": "Cards", "part": "Cards", "part_key": "cards",
                         "html": '<header class="ch-head"><div class="ch-part">Cards</div><h1>Cards</h1><p class="epigraph">One page each. Print them.</p></header>'
                                 f'<div class="cards-collection">{clones}</div>', "words": 0, "minutes": "5", "epigraph": "", "fig_ids": []})
        order = {k: i for i, (_, k, _) in enumerate(ORDER)}
        articles.sort(key=lambda a: order.get(a["part_key"], 99))
    elif 'class="card"' not in articles[idx]["html"]:
        articles[idx]["html"] += f'<div class="cards-collection">{clones}</div>'


def diagram_css():
    """Every diagrams/*.css file, concatenated into the template's style block (per-diagram styles live beside the diagram)."""
    return "\n".join(f"/* diagrams/{f.name} */\n" + f.read_text() for f in sorted(DIAG.glob("*.css")))


def atlan_mark():
    """The Atlan mark (assets/atlan-mark.svg) as a data URI, for the favicon and the top-left brand."""
    return "data:image/svg+xml;base64," + base64.b64encode((ROOT / "assets/atlan-mark.svg").read_bytes()).decode("ascii")


def theme_css():
    """Keep the web reader and standalone HTML on the same self-contained theme."""
    css = (ROOT / "theme.css").read_text()
    for name in ("geist-latin", "geist-mono-latin", "geist-pixel-latin"):
        font = base64.b64encode((ROOT / "assets/fonts" / f"{name}.woff2").read_bytes()).decode("ascii")
        css = css.replace(f'url("assets/fonts/{name}.woff2")', f'url("data:font/woff2;base64,{font}")')
    css = css.replace('url("assets/atlan-mark.svg")', f'url("{atlan_mark()}")')
    license_text = (ROOT / "assets/fonts/OFL.txt").read_text()
    return f"/* Bundled Geist fonts: {license_text} */\n{css}"


def render(template, body, nav, home, idx, mode, articles):
    template = template.replace("/* {{DIAGRAM_CSS}} */", diagram_css())
    template = template.replace("/* {{THEME_CSS}} */", theme_css())
    chapter_list = json.dumps([{"id": a["id"], "t": a["title"], "n": a["num"], "p": a["part_key"], "m": int(a["id"] in MD)}
                               for a in articles])
    md = MD if mode == "artifact" else {}
    out = (template.replace("{{TITLE}}", TITLE).replace("{{NAV}}", nav)
           .replace("{{HOME}}", home).replace("{{BODY}}", body).replace("{{MODE}}", mode)
           .replace("{{IDX}}", json.dumps(idx, ensure_ascii=False).replace("</", "<\\/"))
           .replace("{{CHAPTERS}}", chapter_list.replace("</", "<\\/"))
           .replace("{{SITE_URL}}", esc(SITE_URL)).replace("{{FAVICON}}", atlan_mark()).replace("{{MD}}", json.dumps(md, ensure_ascii=False).replace("</", "<\\/"))
           .replace("{{PODCASTS}}", json.dumps(podcast_catalog(), ensure_ascii=False).replace("</", "<\\/")))
    return out


def site_wrap(fragment):
    m = re.search(r"<title>.*?</title>", fragment, flags=re.S)
    title = m.group(0) if m else f"<title>{TITLE}</title>"
    frag = fragment.replace(title, "", 1)
    return ('<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'{title}<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style></head><body>'
            f"{frag}</body></html>")


def write_site(outdir, template, articles, nav, home, idx):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    body = "".join(f'<article class="ch" id="{a["id"]}" data-part="{a["part_key"]}">{a["html"]}<footer class="ch-foot"></footer></article>' for a in articles)
    frag = render(template, body, nav, home, idx, "site-index", articles)
    (outdir / "index.html").write_text(site_wrap(frag))
    # anchor -> file map
    where = {"home": "index.html"}
    for a in articles:
        where[a["id"]] = f'{a["id"]}.html'
        for i in re.findall(r'(?<![\w-])id="([^"]+)"', a["html"]):
            where.setdefault(i, f'{a["id"]}.html')

    def rewrite(h, self_file):
        def fix(m):
            anchor = m.group(1)
            f = where.get(anchor)
            if not f or f == self_file:
                return m.group(0)
            return f'href="{f}#{anchor}"' if anchor not in ("home",) and anchor != f[:-5] else f'href="{f}"'
        return re.sub(r'href="#([^"]+)"', fix, h)
    for i, a in enumerate(articles):
        fname = f'{a["id"]}.html'
        prev_ = articles[i - 1] if i else None
        next_ = articles[i + 1] if i + 1 < len(articles) else None
        foot = '<footer class="ch-foot"><nav class="pn">' + (f'<a class="prev" href="#{prev_["id"]}"><small>Previous</small>{esc(prev_["title"])}</a>' if prev_ else "<span></span>") + (f'<a class="next" href="#{next_["id"]}"><small>Next</small>{esc(next_["title"])}</a>' if next_ else "<span></span>") + "</nav></footer>"
        body = f'<article class="ch" id="{a["id"]}" data-part="{a["part_key"]}">{a["html"]}{foot}</article>'
        page = render(template, body, nav, "", idx, "site", articles)
        page = page.replace("<title>", f"<title>{esc(a['title'])} · ", 1)
        (outdir / fname).write_text(site_wrap(rewrite(page, fname)))
    return len(articles) + 1


def write_gallery(outdir, template, nav, ladder_html):
    """gallery.html: every diagram id once, for review before any chapter uses it (not linked from the book)."""
    state = {"num": "", "fig_ids": []}
    saved = (list(FAIL_BUILD), list(WARN))      # the gallery reports nothing; --check covers missing files
    figs = []
    for did in DIAGRAM_IDS + [d for d in EXTRA_DIAGRAMS if d not in DIAGRAM_IDS]:
        figs.append(f'<section class="level2" id="g-{did}"><h2>{esc(did)}</h2>'
                    + diagrams(f'<div class="diagram" id="{did}"><p>Gallery preview of <code>{esc(did)}</code>.</p></div>', "gallery", state, ladder_html)
                    + "</section>")
    body = ('<article class="ch" id="gallery" data-part="ref"><header class="ch-head"><div class="ch-part">Review</div>'
            '<h1>Diagram gallery</h1></header>' + "".join(figs) + '<footer class="ch-foot"></footer></article>')
    FAIL_BUILD[:], WARN[:] = saved
    page = render(template, body, nav, "", [], "site", [])
    (Path(outdir) / "gallery.html").write_text(site_wrap(page.replace("<title>", "<title>Gallery · ", 1)))


# ----------------------------------------------------------------------------- check

# Internal codes readers cannot track. Checked on the rendered text of every reading page (Start,
# Parts I-III, Cards; not Reference), with code, inline code and diagrams removed. Each rule is written to catch
# the code as a label, not an ordinary word: "an A1 grade" passes, "In A2, no metric exists" fails.
_A = r"(?<![\w-])A[123](?!\w)(?!-(?!A\d))"
CODE_RULES = [
    ("example label A1-A3",
     r"(?:(?:(?<=\bin\s)|(?<=\bIn\s)|(?<=\bfor\s)|(?<=\bFor\s)|(?<=\bsee\s)|(?<=\bSee\s)|(?<=\blike\s)|(?<=\bfrom\s)|(?<=\bto\s)|(?<=\band\s)|(?<=\bor\s)|(?<=\bon\s)|(?<=\bOn\s)|(?<=\bquestion\s)|(?<=\bQuestion\s)|(?<=\bexample\s)|(?<=\bExample\s)|(?<=\bof\s)|(?<=\())" + _A + r"(?!\s+(?:grade|rating|sauce|paper|size|format|level|steak|note|visa)\b))"
     + r"|(?:" + _A + r"(?=\s*[,:;)]|['’]s\b|\s*[-–/]\s*A[123]\b|\s+(?:and|or|to)\s+A[123]\b"
     + r"|\s+(?:is|was|has|asks|asked|needs|needed|returns|returned|shows|showed|scored|became|comes)\b))"),
    ("record ID like R-001", r"\bR-0\d\d\b"),
    ("ruling ID like PE-004", r"\bPE-\d{3}\b"),
    ("question ID like Q-11", r"\bQ-\d{1,3}\b"),
    ("'item N' reference", r"(?i)\bitems?\s+\d+\b"),
    ("'wave N' label", r"(?i)\bwave\s+\d+\b"),
    ("'row N' reference", r"(?i)\brow\s+\d+\b"),
    ("field-case ID like F04", r"\bF0\d\b"),
    ("evidence ID like E03 or M34", r"(?<![\w-])[EMX]\d{2}(?![\w-])"),
    ("card number like C6", r"(?<![\w-])C(?:[1-9]|1\d)(?![\w-])(?!\s+[a-z])"),
    ("house stage code like S1", r"(?<![\w-])S[1-6](?![\w-])(?!\s+buckets?\b)"),
]
# Calendar dates in the story (V3 tells the engagement in relative weeks). A warning: "the fiscal year ends 30 June"
# is a fact, not a date stamp.
DATE_RE = re.compile(r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b"
                     r"|\b(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}\b(?!,?\s*\d{4})")
CODE_RES = [(name, re.compile(rx)) for name, rx in CODE_RULES]
READING_PARTS = ("start", "part1", "part2", "part3", "part4", "cards")
LINK_DENSITY = 150     # words per cross-reference link; more links than words/150 warns


def reading_text(h):
    """The words a reader sees on a page: no code, no diagrams, no header chrome; tags become spaces."""
    h = re.sub(r"<(pre|code|figure|svg|script|nav)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r'<header class="ch-head"[^>]*>.*?</header>', " ", h, flags=re.S)
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", h)))


def check_codes_and_links(articles):
    for a in articles:
        if a["part_key"] not in READING_PARTS or a["id"] == "r2":
            continue
        text = reading_text(a["html"])
        for name, rx in CODE_RES:
            hits = [m for m in rx.finditer(text)]
            if hits:
                ctx = "; ".join("…" + text[max(0, m.start() - 28):m.end() + 20].strip() + "…" for m in hits[:3])
                FAIL_CONTENT.append(f"{a['id']}: internal code ({name}) x{len(hits)}: {ctx}")
        body = re.sub(r"<(figure|nav)\b.*?</\1>", " ", a["html"], flags=re.S)
        body = re.sub(r'<p class="read-more">.*?</p>', " ", body, flags=re.S)
        body = re.sub(r'<header class="(?:ch-head|card-head)"[^>]*>.*?</header>', " ", body, flags=re.S)
        links = [x for x in re.findall(r'<a ([^>]*)href="#[^"]+"', body) if "class=\"ev" not in x and "card-src" not in x]
        words = a["words"]
        if words >= 150 and len(links) > words / LINK_DENSITY:
            WARN.append(f"{a['id']}: {len(links)} cross-reference links in {words} words (over 1 per {LINK_DENSITY}); "
                        f"keep one 'Read more:' per section")
        dates = DATE_RE.findall(text)
        if dates:
            WARN.append(f"{a['id']}: calendar date(s) {', '.join(sorted(set(dates))[:4])}; V3 uses relative weeks")
        for box in re.findall(r'<section class="callout done".*?</section>', a["html"], flags=re.S):
            if "<a " in box:
                WARN.append(f"{a['id']}: a link inside a checklist (V3: no links in checklists)")

def check(chapters, articles, html_out, ladder):
    src_by = {stem: md for _, _, stem, _, md, _ in chapters}
    html_out = html_out.split("<script>", 1)[0]          # never lint the template's JS
    ids = set(re.findall(r'(?<![\w-])id="([^"]+)"', html_out))
    for a in sorted(set(re.findall(r'href="#([^"]+)"', html_out))):
        if a not in ids:
            FAIL_CONTENT.append(f"broken link: #{a}")
    reg = evidence_ids()
    for i in sorted(set(re.findall(r'data-ev="([EMFX]\d{2})"', html_out))):
        if i not in reg:
            FAIL_CONTENT.append(f"unrecognized evidence ID: {i}")
    for b in ladder["bars"]:
        if b.get("id") and b["id"] not in reg:
            FAIL_BUILD.append(f"ladder bar {b['id']} ({b['label']}) has an unrecognized audit ID")
    for r in ladder.get("negatives") or []:
        if r.get("id") and r["id"] not in reg:
            FAIL_BUILD.append(f"negatives row {r['id']} has an unrecognized audit ID")
    for stem, md in src_by.items():
        prose = "".join(chunk for code, chunk in split_fences(md) if not code)
        for q in sorted(set(re.findall(r"\[E\?\?[^\]]*\]", md))):
            FAIL_CONTENT.append(f"{stem}: unresolved {q}")
        chips = re.findall(r"\[[EMFX]\d{2}\]", re.sub(r"`[^`\n]*`", "", prose))
        if chips:
            FAIL_CONTENT.append(f"{stem}: evidence chip in prose x{len(chips)} ({', '.join(sorted(set(chips))[:4])}); "
                                f"keep the ID as an HTML comment: <!-- E14 -->")
        for c in re.findall(r"<!--(.*?)-->", prose, flags=re.S):
            for i in re.findall(r"\b[EMFX]\d{2}\b", c):
                if i not in reg:
                    FAIL_CONTENT.append(f"{stem}: <!-- {i} --> is not listed in evidence.json audit_ids")
        low = prose.lower()
        for w in BANNED:
            n = len(re.findall(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low))
            if n:
                FAIL_CONTENT.append(f"{stem}: banned word '{w}' x{n}")
        n = len(re.findall(r"\*\*Why\.\*\*", prose))
        if n:
            FAIL_CONTENT.append(f"{stem}: '**Why.**' label x{n}")
        lines = [ln for ln in prose.split("\n") if "—" in ln]
        in_prose = [ln for ln in lines if not ln.lstrip().startswith("|")]
        in_tables = len(lines) - len(in_prose)
        if in_prose:
            FAIL_CONTENT.append(f"{stem}: em dash in prose x{sum(ln.count('—') for ln in in_prose)}")
        if in_tables:
            WARN.append(f"{stem}: em dash inside table cells on {in_tables} line(s) (empty-value markers are allowed)")
    check_codes_and_links(articles)
    # diagrams are reading text too: no chips, codes or dates in any of them
    for d in DIAGRAM_IDS:
        for f in [x for x in diagram_files(d) if x]:
            text = re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<title>.*?</title>|<!--.*?-->", " ", f.read_text(), flags=re.S))))
            for name, rx in CODE_RES:
                hits = [m.group(0) for m in rx.finditer(text)]
                if hits:
                    FAIL_CONTENT.append(f"diagrams/{f.name}: internal code ({name}): {', '.join(sorted(set(hits))[:4])}")
            if re.search(r"\[[EMFX]\d{2}\]", text):
                FAIL_CONTENT.append(f"diagrams/{f.name}: evidence chip")
            dates = DATE_RE.findall(text)
            if dates:
                FAIL_CONTENT.append(f"diagrams/{f.name}: calendar date(s) {', '.join(sorted(set(dates))[:4])}")
    used = {d for a in articles for d in a["fig_ids"]}
    for d in DIAGRAM_IDS:
        if d != "ladder" and not diagram_files(d)[0]:
            FAIL_BUILD.append(f"diagram file missing: diagrams/{d}.svg or .html")
    for d in sorted(set(DIAGRAM_IDS) - used):
        WARN.append(f"diagram '{d}' exists but no chapter uses it yet")


# ----------------------------------------------------------------------------- main

# ----------------------------------------------------------------------------- videos
# One explainer per chapter: (file stem in media/videos/, title, chapter id it sits in). A video is embedded only when
# its .mp4 is present, so the list can lead the files. Durations come from ffprobe and are cached in videos.json,
# because the Pages build has no ffprobe.
VIDEO_DIR = ROOT / "media" / "videos"
VIDEO_URL = "media/videos"
VIDEOS = [("00-overview", "The whole playbook, in brief", "home"),
          ("01a-why-hard", "Why analytics agents are hard", "ch01"),
          ("01b-method", "The method at a glance", "start"),
          ("02-evals", "Why evals come first", "ch-evals"),
          ("03-semantic-views", "Semantic views or metrics?", "r7"),
          ("04-phase0", "Phase 0: before the clock", "ch03"),
          ("05-phase1", "Phase 1: build the golden set", "ch04"),
          ("06-phase2", "Phase 2: generate metrics", "ch05"),
          ("07-phase3", "Phase 3: hill-climb from traces", "ch06"),
          ("08-phase4", "Phase 4: release and hand over", "ch07")]


def video_durations():
    cache = VIDEO_DIR / "videos.json"
    known = json.loads(cache.read_text()) if cache.exists() else {}
    changed = False
    for stem, _, _ in VIDEOS:
        mp4 = VIDEO_DIR / f"{stem}.mp4"
        if not mp4.exists():
            continue
        key = f"{stem}:{mp4.stat().st_size}"
        if known.get(stem, {}).get("key") == key and known[stem].get("floor"):
            continue
        try:
            sec = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                                       capture_output=True, text=True, check=True).stdout.strip())
        except (OSError, subprocess.CalledProcessError, ValueError):
            continue
        known[stem] = {"key": key, "seconds": int(sec), "floor": True}
        changed = True
    if changed:
        cache.write_text(json.dumps(known, indent=1, sort_keys=True))
    return {k: v["seconds"] for k, v in known.items()}


def available_videos():
    secs = video_durations()
    out = []
    for stem, title, aid in VIDEOS:
        if (VIDEO_DIR / f"{stem}.mp4").exists():
            s_ = secs.get(stem)
            dur = f"{s_ // 60}:{s_ % 60:02d}" if s_ else ""
            tx = VIDEO_DIR / f"{stem}.transcript.txt"
            paras = [p_.strip() for p_ in tx.read_text().split("\n\n") if p_.strip()] if tx.exists() else []
            img = next((f"{VIDEO_URL}/{stem}{suf}" for suf in ("-poster.jpg", "-thumb.jpg") if (VIDEO_DIR / f"{stem}{suf}").exists()), "")
            thumb = next((f"{VIDEO_URL}/{stem}{suf}" for suf in ("-thumb.jpg", "-poster.jpg") if (VIDEO_DIR / f"{stem}{suf}").exists()), "")
            out.append({"stem": stem, "title": title, "aid": aid, "dur": dur, "paras": paras, "poster": img, "thumb": thumb})
    return out


def inline_video_images(html):
    """The single-file edition travels without media/: carry each poster and thumbnail inside the page as a data
    URI, so a copy shared on its own shows the video's cover instead of a black frame. The .mp4 files stay out."""
    def data_uri(m):
        f = ROOT / m.group(2)
        if not f.exists():
            return m.group(0)
        return f'{m.group(1)}"data:image/jpeg;base64,{base64.b64encode(f.read_bytes()).decode()}"'
    return re.sub(r'((?:poster|data-poster|src)=)"(media/videos/[^"]+\.jpg)"', data_uri, html)


def video_block(v):
    tx = "".join(f"<p>{esc(p_)}</p>" for p_ in v["paras"])
    if "certif" in tx.lower():   # older narration; drops out once the video is regenerated
        tx = '<p><i>The narration says "certified metrics", and the guide says "metrics": in the benchmark, no person approved the metrics. In the method, each metric\'s owner signs it off.</i></p>' + tx
    dur = f'<span class="vid-d">{esc(v["dur"])}</span>' if v["dur"] else ""
    poster = f' poster="{v["poster"]}"' if v["poster"] else ""
    return (f'<figure class="vid" id="video-{v["stem"]}"><video controls preload="none" playsinline{poster} src="{VIDEO_URL}/{v["stem"]}.mp4"></video>'
            f'<figcaption><span class="vid-k">Watch</span><b>{esc(v["title"])}</b>{dur}</figcaption>'
            + (f'<details class="vid-tx"><summary>Read the transcript</summary>{tx}</details>' if tx else "")
            + '</figure>')


def embed_videos(articles, vids):
    by = {a["id"]: a for a in articles}
    for v in vids:
        if v["aid"] == "home":   # the overview sits on the cover page, which landing() builds
            continue
        a = by.get(v["aid"])
        if not a:
            WARN.append(f"video {v['stem']}: no chapter #{v['aid']}")
            continue
        h, blk = a["html"], video_block(v)
        m = re.search(r'<aside class="tldr".*?</aside>', h, flags=re.S)
        if m:
            a["html"] = h[:m.end()] + blk + h[m.end():]
        else:
            m = re.search(r'<section id="[^"]+" class="level2">', h)
            a["html"] = (h[:m.start()] + blk + h[m.start():]) if m else h + blk
    page = by.get("videos")
    if page:
        page["html"] = re.sub(r'<div class="video-grid">\s*</div>', video_theater(vids, by), page["html"])


def video_theater(vids, by):
    """The Resources page: one large player, the full playlist under it, a transcript for whatever is playing."""
    if not vids:
        return '<p class="vg-empty">The videos are on their way.</p>'
    total = sum(int(v["dur"].split(":")[0]) * 60 + int(v["dur"].split(":")[1]) for v in vids if v["dur"])
    first = vids[0]
    items = []
    for i, v in enumerate(vids):
        ch = strip_tags(by[v["aid"]]["title_html"]) if v["aid"] in by else ("Overview" if v["aid"] == "home" else "")
        tx = "".join(f"<p>{esc(p_)}</p>" for p_ in v["paras"])
        thumb = f'<img src="{v["thumb"]}" alt="" loading="lazy">' if v["thumb"] else '<span class="vt-noimg"></span>'
        items.append(
            f'<li><button type="button" class="vt-item{" is-on" if i == 0 else ""}" data-i="{i}" data-src="{VIDEO_URL}/{v["stem"]}.mp4"'
            f' data-poster="{v["poster"]}" data-title="{esc(v["title"])}" data-dur="{esc(v["dur"])}" data-ch="{v["aid"]}" data-chtitle="{esc(ch)}"'
            f'{" aria-current=" + chr(34) + "true" + chr(34) if i == 0 else ""}>'
            f'<span class="vt-thumb">{thumb}<span class="vt-n">{i + 1}</span>'
            + (f'<span class="vt-d">{esc(v["dur"])}</span>' if v["dur"] else "")
            + f'</span><span class="vt-t">{esc(v["title"])}</span>'
            + (f'<span class="vt-c">{esc(ch)}</span>' if ch.lower() not in v["title"].lower() else "") + '</button>'
            f'<template class="vt-tx-src">{tx}</template></li>')
    tx0 = "".join(f"<p>{esc(p_)}</p>" for p_ in first["paras"])
    ch0 = strip_tags(by[first["aid"]]["title_html"]) if first["aid"] in by else ("Overview" if first["aid"] == "home" else "")
    mins = round(total / 60)
    return (f'<div class="vt" id="video-theater">'
            f'<p class="vt-sum">{len(vids)} videos · about {mins} minutes in all</p>'
            f'<div class="vt-stage"><video class="vt-player" controls playsinline preload="metadata" poster="{first["poster"]}" src="{VIDEO_URL}/{first["stem"]}.mp4"></video>'
            f'<div class="vt-now"><span class="vt-k">Now playing · <span class="vt-pos">1</span> of {len(vids)}</span>'
            f'<b class="vt-title">{esc(first["title"])}</b>'
            f'<span class="vt-meta"><span class="vt-dur">{esc(first["dur"])}</span> · <a class="vt-chlink" href="#{first["aid"]}">Read the chapter: <span class="vt-chname">{esc(ch0)}</span></a></span>'
            f'<label class="vt-auto"><input type="checkbox" id="vt-autoplay" checked> Play the next video automatically</label>'
            f'<details class="vid-tx vt-tx"><summary>Read the transcript</summary><div class="vt-txb">{tx0}</div></details></div></div>'
            f'<ol class="vt-list">{"".join(items)}</ol></div>')


def copy_videos(dest):
    """Copy media/videos/ (mp4, posters, thumbs) next to a built site, skipping files already up to date."""
    if not VIDEO_DIR.exists():
        return
    d = Path(dest) / VIDEO_URL
    d.mkdir(parents=True, exist_ok=True)
    for f in VIDEO_DIR.iterdir():
        t = d / f.name
        if f.suffix in (".mp4", ".jpg") and (not t.exists() or t.stat().st_mtime < f.stat().st_mtime):
            shutil.copy2(f, t)


def podcast_catalog():
    """Only player metadata goes into the site; production notes stay in the repo."""
    data = json.loads((ROOT / "media/podcasts/podcasts.json").read_text())
    return [{"id": p["id"], "track": p["track"], "title": p["title"], "duration": p["duration"],
             "src": "media/podcasts/" + p["file"]} for p in data["episodes"]]


def podcast_files(articles):
    """Validate audio and its accompanying transcripts before publishing them."""
    page = next((a for a in articles if a["id"] == "listen"), None)
    if not page:
        return []
    sources = re.findall(r'<audio\b[^>]*\bsrc="([^"]+)"', page["html"])
    files = []
    if len(sources) != 3:
        FAIL_BUILD.append("podcasts: expected one audio episode for each of the three tracks")
    for src in sources:
        if not re.fullmatch(r"media/podcasts/[a-z0-9-]+\.mp3", src):
            FAIL_BUILD.append(f"podcasts: invalid local audio path {src}")
            continue
        path = ROOT / src
        if not path.is_file() or not path.stat().st_size:
            FAIL_BUILD.append(f"podcasts: missing or empty audio file {src}")
        else:
            files.append(path)
    metadata = json.loads((ROOT / "media/podcasts/podcasts.json").read_text())
    companions = [metadata["editorial_notes"]]
    for episode in metadata["episodes"]:
        companions.append(episode["transcript"])
    for name in companions:
        if not re.fullmatch(r"(?:[a-z0-9-]+\.transcript|editorial-notes)\.txt", name):
            FAIL_BUILD.append(f"podcasts: invalid companion file name {name}")
            continue
        path = ROOT / "media/podcasts" / name
        if not path.is_file() or not path.stat().st_size:
            FAIL_BUILD.append(f"podcasts: missing or empty companion file {name}")
        else:
            files.append(path)
    return files


def copy_podcasts(dest, files):
    target = Path(dest) / "media" / "podcasts"
    target.mkdir(parents=True, exist_ok=True)
    for source in files:
        shutil.copy2(source, target / source.name)


# ----------------------------------------------------------------------------- Markdown for agents
# Each page is also published as <id>.md, with llms.txt (index) and llms-full.txt (whole book), so a reader can hand
# the playbook to their own agent: the page menu copies, views or opens a page's Markdown. The source Markdown is
# cleaned of build syntax: fenced-div markers become plain labels, ids and evidence comments go, anchors become page links.
# Links are relative, so the files work on whichever domain serves them; the menu makes them absolute when it copies.

MD_HEAD = re.compile(r"^# .*?\{#([\w-]+)[^}]*\}[ \t]*$", re.M)
MD_LABELS = {"diagram": "Figure", "tldr": "In short", "scene": "Scene", "card": "Card", "template": "Template"}


def md_sections(text):
    """{article id: markdown} for each top-level heading with an id; headings inside code fences don't count."""
    cuts, pos = [], 0
    for code, chunk in split_fences(text):
        if not code:
            cuts += [(pos + m.start(), m.group(1)) for m in MD_HEAD.finditer(chunk)]
        pos += len(chunk)
    return {aid: text[at:(cuts[i + 1][0] if i + 1 < len(cuts) else len(text))].strip()
            for i, (at, aid) in enumerate(cuts)}


def md_clean(text, where):
    """Pandoc build syntax -> plain Markdown an agent reads without guessing. where: anchor id -> article id."""
    def fence(m):
        attrs = m.group(1)
        cls = next((c for c in re.findall(r"\.([\w-]+)", attrs) if c in MD_LABELS), None)
        if not cls:
            return ""
        title, extra = attr(attrs, "title"), attr(attrs, "week") or attr(attrs, "file")
        label = MD_LABELS[cls] + (f": {title}" if title else "") + (f" ({extra})" if extra else "")
        return f"**{label}**\n"

    def link(m):
        page = where.get(m.group(2))
        return f"]({SITE_URL}{page}.md)" if page else m.group(0)

    def prose(t):
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        t = re.sub(r"^:{3,}[ \t]*\{(.*)\}[ \t]*$\n?", fence, t, flags=re.M)
        t = re.sub(r"^:{3,}[ \t]*$", "", t, flags=re.M)
        t = re.sub(r"^(#+ .*?)[ \t]*\{[^}]*\}[ \t]*$", r"\1", t, flags=re.M)
        t = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", t)
        t = re.sub(r"\]\(#(([\w-]+))\)", link, t)
        return t
    return re.sub(r"[ \t]+$", "", re.sub(r"\n{3,}", "\n\n", outside_code(text, prose)), flags=re.M).strip() + "\n"


def md_preamble(aid):
    page = "index.html" if aid == "home" else f"{aid}.html"
    return (f"> From {TITLE}, an open guide to building analytics agents that answer business questions correctly.\n"
            f"> This page: [{page}]({SITE_URL}{page})\n"
            f"> Index of every page, as Markdown: [llms.txt]({SITE_URL}llms.txt) · The whole playbook in one file: [llms-full.txt]({SITE_URL}llms-full.txt)\n"
            f"> Source: {REPO_URL} · Licence: CC BY 4.0 (text)\n"
            "> Agents: start with llms.txt to find the right page, read it as Markdown, and name the page you answer from.\n\n")


def md_pages(chapters, articles):
    """{article id: markdown with preamble}, plus "home" (the index). Pages with no source of their own get none."""
    where = {}
    for a in articles:
        where[a["id"]] = a["id"]
        for i in re.findall(r'(?<![\w-])id="([^"]+)"', a["html"]):
            where.setdefault(i, a["id"])
    live = {a["id"] for a in articles}
    src = {}
    for _, _, stem, _, _, _ in chapters:
        src.update(md_sections(front_matter((CH / f"{stem}.md").read_text())[1]))
    pages = {aid: md_preamble(aid) + md_clean(md, where) for aid, md in src.items() if aid in live}
    pages["home"] = md_preamble("home") + llms_txt(articles, pages)
    return pages


def llms_txt(articles, pages):
    """The index, in the llms.txt layout: title, one-line summary, then each page by part with its one-line lede."""
    out = [f"# {TITLE}\n", "> How to build an analytics agent that answers business questions correctly: "
           "write the evals first, seal each business rule into a metric, and improve the agent from its traces."]
    part = None
    for a in articles:
        if a["id"] not in pages or a["id"] in NAV_HIDE:
            continue
        if a["part"] != part:
            part = a["part"]
            out.append(f"\n## {part}\n")
        lede = f": {a['epigraph']}" if a.get("epigraph") else ""
        out.append(f"- [{a['title']}]({SITE_URL}{a['id']}.md){lede}")
    return "\n".join(out) + "\n"


def write_md(outdir, articles, pages):
    """<id>.md per page (index.md for home), llms.txt and llms-full.txt beside the site's HTML."""
    outdir = Path(outdir)
    for aid, md in pages.items():
        (outdir / ("index.md" if aid == "home" else f"{aid}.md")).write_text(md)
    (outdir / "llms.txt").write_text(llms_txt(articles, pages))
    body = [pages[a["id"]].split("\n\n", 1)[1] for a in articles if a["id"] in pages]
    (outdir / "llms-full.txt").write_text(md_preamble("home") + "\n\n".join(body))
    return len(pages) + 2


def main():
    args = sys.argv[1:]
    site = args[args.index("--site") + 1] if "--site" in args else None
    if not TPL.exists():
        sys.exit("template.html missing")
    chapters, missing = load_chapters()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "PLAYBOOK.md").write_text("\n\n".join(md for _, _, _, _, md, _ in chapters))
    ladder = ladder_data()[0]
    ladder_html = {"ladder": ladder_svg(ladder), "negatives": negatives_html(ladder), "data": ladder}
    articles, collected = [], []
    parsed = []
    for part, key, stem, meta, md, slot in chapters:
        secs = split_level1(pandoc(md))
        if not secs:
            WARN.append(f"{stem}: no top-level heading; skipped")
        parsed.append((part, key, stem, meta, slot, secs))
    # mid-rewrite, a V2 fallback can reuse an id a V3 file now owns (V2 07-weeks-5-6 and V3 07-week-4 are both #ch07):
    # the V3 file wins and the fallback is dropped
    v3_ids = {aid for _, _, stem, _, slot, secs in parsed if stem == slot for aid, _, _ in secs}
    kept = []
    for row in parsed:
        part, key, stem, meta, slot, secs = row
        clash = [aid for aid, _, _ in secs if aid in v3_ids] if stem != slot else []
        if clash:
            WARN.append(f"{slot}: V2 fallback {stem}.md dropped; its #{clash[0]} now belongs to a V3 file")
            continue
        if secs:
            SLOT_ARTICLE[slot] = secs[0][0]
        kept.append(row)
    parsed = kept
    for part, key, stem, meta, slot, secs in parsed:
        for i, (aid, cls, inner) in enumerate(secs):
            art = transform_article(aid, inner, part, key, meta if i == 0 else {}, ladder_html, collected, slot if i == 0 else "", stem)
            articles.append(art)
    cards_article(articles, collected)
    inline_cards(articles, collected)
    vids = available_videos()
    embed_videos(articles, vids)
    resolve_links(articles, collected)
    dedupe_ids(articles)
    audio_files = podcast_files(articles)
    MD.update(md_pages(chapters, articles))
    home, paths = landing(articles, ladder, collected, vids)
    parts_order = [(p, k) for p, k, _ in ORDER]
    nav = build_nav(articles, parts_order)
    idx = search_index(articles)
    template = TPL.read_text()
    body = "".join(f'<article class="ch" id="{a["id"]}" data-part="{a["part_key"]}">{a["html"]}<footer class="ch-foot"></footer></article>' for a in articles)
    out = render(template, body, nav, home, idx, "artifact", articles)
    out = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           + inline_video_images(out))   # the fragment is also shared as a file on its own
    (OUT / "playbook.html").write_text(out)
    words = sum(a["words"] for a in articles)
    print(f"built playbook.html ({len(out) // 1024} KB, {len(articles)} sections, {words:,} words) and PLAYBOOK.md")
    if missing:
        print("no chapter file for:", ", ".join(missing))
    if site:
        n = write_site(site, template, articles, nav, home, idx)
        copy_videos(site)
        copy_podcasts(site, audio_files)
        write_gallery(site, template, nav, ladder_html)
        n += write_md(site, articles, MD)
        print(f"site: {n} files in {site}/")
    if "--check" in args:
        check(chapters, articles, out, ladder)
    for w in WARN:
        print(" ~", w)
    if "--check" in args:
        for p in FAIL_BUILD:
            print(" ! build:", p)
        for p in FAIL_CONTENT:
            print(" ! content:", p)
        print(f"check: {len(FAIL_BUILD)} build failure(s), {len(FAIL_CONTENT)} content failure(s), {len(WARN)} warning(s)")
        if FAIL_BUILD or FAIL_CONTENT:
            sys.exit(1)


if __name__ == "__main__":
    main()
