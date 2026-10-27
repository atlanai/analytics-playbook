# Authoring guide: V3 syntax, component contracts, diagrams

Chapters are pandoc Markdown in `chapters/`. `python3 build.py` assembles them into `playbook.html` (the artifact fragment) and `PLAYBOOK.md`; `--check` lints; `--site DIR` writes the GitHub Pages files plus `DIR/gallery.html` (every diagram once, for review; not linked from the book). Needs pandoc. V3_SPEC.md wins over anything here that disagrees.

## Files and order

| Slot | File | Id | Falls back to (V2) |
|---|---|---|---|
| Why it is hard | `01-why-hard` | `#ch01` | `01-tenth-question`; `02-what-it-must-know` and `02b-evals-first` are built until it exists |
| How to build one · the method | `00-method` | `#start`, `#lifecycle`, `#rules`, `#start-map` | |
| How to build one · principles | `02a-evals-first`, `02b-metric-unit`, `02c-serve-per-question` | `#ch-evals`, `#ch02` (with `#ch-sv`), `#ch-retrieval` | |
| How to build one · phases | `03-phase-0`, `04-week-1`, `05-week-2`, `06-week-3`, `07-week-4` | `#ch03` … `#ch07` | `04-phase-0`, `05-weeks-1-2`, `06-weeks-3-4`, `07-weeks-5-6`, `08-release-and-run` |
| How to build one · after launch | `08-after-launch` | `#ch-run`, `#ch08`, `#ch09` | `07b-keep-it-running`, `08-answer-why`, `09-delivery-lead` are built until it exists |
| Toolkit | `00-start` (doors, assessment), `cards`, `r2-templates`, `10-straight-answers`, `videos`, `podcasts` | `#doors`, `#assess`, `#cards`, `#r2`, `#ch10`, `#videos`, `#listen` | |
| Research and reference | `r0-results`, `r3-evidence`, `r6-field-research`, `r1-failure-modes` … `r5-tooling` | `#results`, `#r3`, `#r6`, `#r1` … `#r5` | |

The sidebar groups pages by what the reader is doing (`NAV_GROUPS` in `build.py`: Why it is hard, How to build one, Toolkit, Research and reference; `NAV_SECTION` puts the Learn and Resources headings above them), each group collapsible and opened on the current page; a page not named there falls into a trailing group named after its part. The table above still sets the reading order and prev/next.

The exact V3 file always wins. Until it exists the build uses the V2 file and warns. A V2 fallback whose id now belongs to a V3 file is dropped. `03-what-we-measured` and `09-handover` are legacy: built only until `03-phase-0.md` / `09-delivery-lead.md` exist, then ignored (the build tells you to delete them).

Every `#` heading is its own page (an `<article>`) and needs an explicit id. **Readers never see a chapter number** (V3 decision 3): not in headings, the contents, the doors, prev/next, the phase strip or figure numbers. A leading number in the source (`# 5. Phase 2: …`, `# 0.1 The whole method…`) is stripped at render time, so you may keep or drop it. Anchors never change.

- Start, Part I and Part III display the title only: `# What the agent has to know {#ch02}`.
- Part II displays its phase once, as the small label above the title: `# Phase 2: generate metrics {#ch05}` renders the label "Phase 2" and the title "Generate metrics". Without the prefix the label comes from the slot. In the contents, prev/next and doors the page is "Phase 2 · Generate metrics".
- Reference keeps R1-R3 (`# R2. Glossary {#r4}`); Toolkit and Research pages carry no number (`# How we measured {#r3}`).
- Figures are numbered per page ("Figure 2"); Reference keeps "Figure R1.2".
- Every page also has a `#<id>-intro` anchor on its header, for a door step that means "the opening only".

**Front matter** (optional, first thing in the file):

```
---
phase: Phase 2    for: context engineer, domain owner
produces: metrics, resolved conflicts    minutes: 13
---
```

Keys: `phase`, `weeks`, `for`, `produces`, `minutes`. Only `for`, `produces` and the minutes are displayed; `phase` and `weeks` are never printed (that caused "Phase 2 · Generate metrics · Weeks 2"). Minutes are computed from the words a reader reads (code blocks and drawn diagrams excluded; tables and captions counted) when `minutes` is missing. The phase strip (Phase 0 · Phase 1 · Phase 2 · Phase 3 · Phase 4 · After launch) appears on every Part II page and lights the page's own slot; `phase: Phase 0` / `phase: Phase 3` (or a leading digit) overrides which slot lights.

## Chapter shape

```
# Phase 3: hill-climb from traces {#ch06}

> [!RULE]
> Read the raw trace. The summary hides the step where it guessed.

::: {.scene week="Phase 3"}
80-120 words, relative time, no codes, no calendar dates.
:::

## Classify every miss {#ch06-classify}

Prose, then a task list, then a diagram, card or template.

Read more: [Why did this miss?](#c6)
```

The first `> [!RULE]` becomes the epigraph under the title.

## Readability

A section is read in one pass by someone with a meeting in ten minutes. Four checks before a section ships:

- **A heading that promises a count names the items.** "Five steps" lists the five in the text, in order. The diagram caption does not count; a reader on a phone or a screen reader may never see it.
- **One idea per paragraph, the measurement last.** State the claim, then the example, then the number with its evidence chip. A statistic in the middle of an argument stops the reader.
- **Name what you point at.** "Step two" and "the first of these" send the reader back up the page. Say "step two, context".
- **List or table by shape.** Three or more parallel items make a list. A table only when every row carries the same two or more attributes; otherwise it is a list wearing borders.

## Links (V3: few and quiet)

- **In-prose cross-references** render quietly: ink colour, dotted underline, accent on hover. Keep them rare; `--check` warns above one link per 150 words in a chapter.
- **Read more.** At most one per section, at its end, as its own paragraph starting `Read more:`:

  ```
  Read more: [the full metric spec template](#r2-5)
  Read more: [](#ch05)
  ```

  It renders as a small `READ MORE  the full metric spec template →` line. An empty link text is filled with the target's title (a chapter, a `##` section, a template or a card). `Read more:` without a link fails `--check`.
- **Cards** are always named by title. Any link to `#cN` renders as a small title chip with a card glyph, whatever its link text, so `[the sponsor's ask](#c2)` and `[C2](#c2)` both show "The sponsor's ask". Never write "C2" in prose. The first mention on a page should say what a card is: "one-page checklists you can print".
- A paragraph that starts `Card:` and links to a card still gets a copy of that card rendered right after it.
- No links inside the rules, the phase list or checklists (`--check` warns on links inside `[!DONE]`).

## Evidence IDs

Chapters show no chips. Put the ID as an HTML comment beside the number, for audit:

```
Bare schema scored 31.8% <!-- E03 -->.
```

The build strips every HTML comment from the output. `--check` fails on a visible `[E03]` chip in any chapter, and on a comment ID absent from `evidence.json`'s `audit_ids` list. That list contains identifiers only, not evidence records. Sources and scope belong in the pull request for maintainer review.

## Callouts (four)

```
> [!NOTE]
> **Practice, not measured.** No score backs this section yet.

> [!STOP]
> **The dashboard rule.** If every answer must be exact, build the dashboard.

> [!DONE]
> - [ ] 20 questions sealed
```

- `NOTE`: a bold first line is its title.
- `STOP`: red rule; a bold first line is its title.
- `DONE`: real checkboxes, saved per viewer.
- Any other kind fails `--check`.

## Blocks

| Block | Syntax | What the build does |
|---|---|---|
| Scene | `::: {.scene week="Phase 2"}` … `:::` | a story panel labelled `Scene · Phase 2` |
| Diagram | `::: {.diagram #miss-tree}` one caption paragraph `:::` | injects `diagrams/miss-tree.svg` or `.html` (and `.phone.html` below 640px), numbers it, the paragraph is the caption. A missing file fails `--check`. |
| Card | `::: {.card #c6 title="Why did this miss?"}` body `:::` | only in `cards.md`; one printed page each; the header shows "Card" and the title, never the number |
| Template | `::: {.template #r2-5 file="metric.yaml" title="Metric spec"}` prose, then two fences (filled example, then blank) `:::` | a file card with Example / Blank template tabs and a copy button |
| Component | `::: {.component #self-assessment flag="5,11"}` … `:::` | JS enhances the Markdown inside; the Markdown stays as the no-JS and print fallback |

## Diagram ids

V2 ids still available: `phases`, `lanes`, `loop`, `architecture`, `miss-tree`, `contract`, `swimlane`, `ontology`, `five-decisions`, `a1-before-after`, `closure`, `lane-tree`, `ontology-tree`, `two-paths`, `answer-key`, `grading`, `wave`, `production-loop`, `handover`, `domain-two`, `ceremonies`, `data-flows`. `mining-pipeline` is gone; use `metrics-pipeline`.

Updated for V3: `phases` (Phase 0, then Phases 1-4, each with its gate as on the sponsor's gates card, plus the golden-set track; full width on desktop, a compact label-title-gate timeline on phones; for the start page), `swimlane` (hours and a readout in each phase as in the Phase 0 table, co-owner row added) and `ceremonies` (the plan, phase by phase), `answer-key` (golden set, six required fields, no day labels), `loop` (scope → test → generate metrics → resolve conflicts → hill climb → release), `wave` (one round; run-to-run variation), `handover` (one round together, one alone). Diagram text says "golden set", "round", "run-to-run variation" and "test accounts"; never "answer key", "wave", "noise band", "decoy", "trust tag" or metric identifiers like `open_pipeline_top_accounts`.

New in V3:

| Id | What it shows | Where it belongs |
|---|---|---|
| `model-chart` | bare schema vs with context, per model; the 31.8-42.1% bare-schema band; the takeaway written in the chart | ch1 |
| `ladder` | one ladder: bare schema 31.8%, documentation and usage 43.9%, + past SQL 70.1%, + metrics about 81%. Generated at build time from `evidence.json` (a top-level `ladder` list of `{label, value, id, display?}`), else from `LADDER_V3` in build.py. No IDs drawn. | ch2 |
| `didnt-work` | seven "tried it, didn't help" tiles, one-line result each | ch2 |
| `sql-vs-prose` | the same metric as SQL vs as prose: 16 points on multi-table questions | ch2 or Start |
| `metrics-pipeline` | past SQL + BI and semantic models → generate metrics → witness → resolve conflicts → metrics, plus the trusted-query library | Phase 2 |
| `agent-architectures` | UI / harness (yours) / model / context layer, platform-native and custom stacks, wired over MCP | Phase 0 |
| `access-checklist` | the system access and named people you need before Phase 1, as a card | Phase 0 |
| `evals-why` | four tiles: is it right, is it better, what to fix next, is it safe to change | Phase 1, "Why evals come first" |
| `why-moves` | the EMEA question in three moves: number to paths, rule paths out, test each change in SQL | Answer why, EMEA worked through |
| `method-map` | the whole method as an explorer: a rail of stages around the golden set, the stage's numbered steps, and the selected step's how, who, template and the mistake to avoid, with Next step through all of them. The source is a nested `<details>` outline (`.mm-n`, `data-kind`), shown in print and without JS | Lifecycle, "Find your task" (replaces `tasks`) |

`negatives` (dumbbells from `evidence.json`) still generates but is superseded by `didnt-work`.

## Doors (the landing accordion)

`#doors` in `00-start.md` holds three `##` sections, one per reader. The landing turns each into an accordion row (one open at a time, keyboard accessible, the picked path opens on return). Per section, in this order:

```
## I'm sponsoring it {#door-sponsor}

You are the exec sponsor, or the data leader who will answer for the agent.

1. [The tenth question](#ch01)
2. [Phase 0: before the clock](#ch03)
3. [Phase 4: release and hand over](#ch07)

Cards: [the sponsor's ask](#c2), [what the sponsor sees at each gate](#c10)
```

- The first paragraph is the one-line "who you are" shown on the closed row.
- The links of the first ordered list are the path, in order. Without a list, every non-card link in the section is used. **A step can be:**
  - a chapter, `#ch03`: the whole chapter's minutes;
  - a section, `#ch02-lanes` (any `##` or `###` id, or an id inside one): minutes from that section only, its heading to the next heading of the same level; the step shows the chapter title above the section title;
  - a chapter's opening, `#start-intro`: the text before its first `##`;
  - a card, `#c2`: about 1-2 minutes, shown with a "Card" label.
- A chapter link followed by links to its own sections counts as its opening only (`#start` then `#start-learned` = the start page's intro, then "What we learned"), and the path goes to `#start-intro`.
- Card links outside the list become the row's "Cards for you" chips. They count toward the total (1-2 minutes each) but are not stops on the path. To make a card a stop, put it in the list.
- The closed row shows "N readings · M cards · about X min", summed from the steps and cards only.
- "Follow this path" saves the steps. The contents marks each chapter that holds a step. A section, opening or card step ends with its own "Previous / Next on your path" bar, and the chapter footer shows "Next on your path" after its last step, so the reader moves through the anchors in order. The rail lists the path. Extra prose in the section stays on the `#doors` page itself.

## Hero

The cover shows `31.8% → ~81%` (the first and last ladder bars; a bar whose `display` is "about 81%" shows as "~81%") with plain-language bar names from `HERO_LABELS` in build.py (keyed by ladder id; the ladder chart keeps its own labels), a caption, `HERO_CAPTION`, and a "How we measured" link to the methodology chapter (`#r3`). Nothing else.

## Component contracts

**Self-assessment** (`#self-assessment`, in `00-start.md`): gate questions (`**Question 1 · …**`, the question, a two-item `Answer → outcome` list), then the readiness table (`# | Question | 0 | 1 | 2 | If you scored 0, read`), then the bands table (`Score | Where you are | Next step`). `flag="5,11"` names rows that warn when scored 0.

**Failure modes** (R1): any table whose header has a `Symptom` column renders as filterable cards (`#`, `Symptom`, `Cause`, `Fix`, `Evidence`, `Chapter`, `Branch`, `Phase`). The Evidence cell shows "measured" or "diagnosis, not measured"; IDs belong in comments.

**Evidence identifiers** (`evidence.json`): `audit_ids` lists the maintainer-assigned IDs allowed in chapter comments and chart metadata. The build checks identifiers; maintainers verify the underlying evidence.

## Inline syntax

- Code fences carry a language (`sql`, `yaml`, `markdown`, `json`, `python`, `bash`); `<placeholders>` are highlighted; blocks over 40 lines collapse.
- Tables: columns headed `#`, `%`, `n`, `$`, `Score` right-align; wide or text-heavy tables stack on phones; more than seven columns warns.
- Write a blank line before a list (the build inserts it and warns otherwise).

## `--check` (exit 1 on any failure)

Content failures:
- banned words (`illustrative`, `demo data`, `robust`, `seamless`, `unlock`), `**Why.**` labels, em dashes in prose, `[E??]`, broken links, callout kinds outside the four;
- a visible evidence chip `[E03]` in any chapter; an `<!-- E03 -->` comment whose ID is absent from `audit_ids`;
- a `Read more:` paragraph without a link;
- **internal codes** in the rendered text of every reading page (Start, Parts I-III, Cards; Reference is exempt), with code, inline code and diagrams removed, and in the text of every diagram file (see the table below);
- **calendar dates** (`24 July`, `Aug 5`) in any diagram.

Build failures: missing diagram files, evidence.json errors, missing or invalid `audit_ids`, duplicate audit IDs, or a ladder `id` absent from that list.

Warnings: V2 fallbacks and legacy chapters, inserted blank lines, wide tables, duplicate ids, calendar dates in chapter text (a fact like "the fiscal year ends 30 June" is allowed, a date stamp in a scene is not), links inside checklists, and **link density**: more cross-reference links than one per 150 words in a chapter (Read more lines and diagram internals do not count; card chips do).

### Internal-code rules

Each rule catches the code used as a label, not an ordinary word. Matching is case-sensitive unless noted.

| Rule | Fails | Passes |
|---|---|---|
| Example label A1-A3: `A1`/`A2`/`A3` after `in`, `for`, `see`, `like`, `from`, `to`, `and`, `or`, `on`, `of`, `question`, `example` or `(`; or before `,` `:` `;` `)`, `'s`, a range `A1-A3` / `A2/A3`, `and A3`, or a verb (`is`, `was`, `has`, `asks`, `needs`, `returns`, `shows`, `scored`, `became`, `comes`). Never when followed by `grade`, `rating`, `sauce`, `paper`, `size`, `format`, `level`, `steak`, `note`, `visa`. | "In A2, no metric exists", "A2 asks how many", "(A3)", "A1-A3" | "an A1 grade", "A1 paper" |
| Record ID `\bR-0\d\d\b` | R-001 | R-squared |
| Ruling ID `\bPE-\d{3}\b` | PE-004 | |
| Question ID `\bQ-\d{1,3}\b` | Q-11 | Q3 (a fiscal quarter) |
| `item N`, `items N` (any case) | item 6 | 3 items |
| `wave N` (any case) | wave 3 | the second wave |
| `row N` (any case) | row 7 | a row per key |
| Field-case ID `\bF0\d\b` | F04 | |
| Evidence ID `[EMX]` + two digits, standalone | E03, M34 | E2E |
| Card number `C1`-`C19`, standalone, not followed by a lowercase word | C6, "see C10." | "C4 model" |
| House stage code `S1`-`S6`, standalone, not before `bucket` | S1 | S3 bucket |

The rules live in `CODE_RULES` in build.py; reading pages are `READING_PARTS`; the density threshold is `LINK_DENSITY`.

## Adding a diagram

1. Put `diagrams/<id>.svg` (or `.html`) in place, reference it with `::: {.diagram #<id>}`, and add the id to `DIAGRAM_IDS` in build.py and to the table above.
2. SVG rules: a `viewBox` (640 or 720 wide) and no `width`/`height`; every shape carries an explicit `style="fill:…;stroke:…"` using the tokens `var(--bg)`, `var(--panel)`, `var(--tint)`, `var(--line)`, `var(--line-2)`, `var(--ink)`, `var(--text)`, `var(--muted)`, `var(--accent)`, `var(--accent-soft)`, `var(--stop)`, `var(--ok)`; text uses `class="t"`, `"m"` or `"d"` with an inline `font-size`; a `<title>`; one `<marker id="arr">` if needed. Body text 11-13px.
3. HTML diagrams use the shared classes in template.html (`.d`, `.d-box`, `.d-lab`, `.d-mono`, `.d-tree`, `.d-ent`, `.d-phases`, …). Styles a diagram needs beyond those go in `diagrams/<id>.css`, scoped under a class unique to that diagram; build.py injects every `diagrams/*.css` into the page. No inline `<style>` blocks.
4. If the SVG is unreadable at 400px, add `diagrams/<id>.phone.html` (it replaces the SVG below 640px and never prints).
5. Charts carry one small "Source: internal benchmark" line and no IDs. No codes, no calendar dates (`--check` lints diagram text).
6. Check it in `DIR/gallery.html#g-<id>` at 1440px and 400px, with `?theme=light` and `?theme=dark` (headless Chrome defaults to dark, so pass the theme explicitly).

## Markdown for agents

`--site` also writes each page as Markdown (`<id>.md`, the home page as `index.md`) plus `llms.txt` (the index) and `llms-full.txt` (the whole book), so readers can hand the playbook to their own agent. The **Copy page** menu in the top bar copies the current page's Markdown, opens it as plain text, or opens it in Claude, ChatGPT or Perplexity. The single-file `playbook.html` carries the same Markdown inline, so Copy works offline.

The Markdown comes from the chapter source, cleaned: fenced-div markers become a bold label (Figure, In short, Scene, Card, Template), `{#id}` attributes and `<!-- E.. -->` comments are dropped, and `#anchor` links become links to the page that holds them. Those links are relative, so the files work on any domain; when the menu copies a page it makes them absolute from the address the reader is on, and "Open in" uses the same address. Set `PB_SITE_URL` (ending in `/`) to bake one canonical address into the files instead. A single-file edition opened from disk has no address, so its menu offers Copy and View only.

Test a chapter without touching the shared tree: `PB_CHAPTERS=/path/to/scratch/chapters PB_OUT=/path/to/scratch python3 build.py --check --site /path/to/scratch/site`.

## evidence.json (owned by the evidence agent; the build reads it)

- `audit_ids`: nonempty list of unique maintainer-assigned evidence IDs. Contains identifiers only; it does not store claims or results.
- `ladder`: optional list of `{label, value, id, display?}` for the one V3 ladder; each `id` must appear in `audit_ids`. Without it the build uses `LADDER_V3`.
- `negatives`: `{label, delta_or_value, before?, after?, id, tier}` for the legacy `negatives` chart.
- `ladders.open` / `ladders.bounded` (V2) are no longer read.
