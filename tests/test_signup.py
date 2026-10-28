"""Regression coverage for signup output, without a browser or external services."""

import importlib.util
import json
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("playbook_build", ROOT / "build.py")
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class Document(HTMLParser):
    """Collect actual elements rather than matching IDs inside scripts or styles."""

    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.head_elements = []
        self.element_contexts = []
        self.open_elements = []
        self.in_head = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        element = (tag, dict(attrs))
        self.elements.append(element)
        self.element_contexts.append((tag, element[1], tuple(self.open_elements)))
        if tag == "head":
            self.in_head = True
        if self.in_head:
            self.head_elements.append(element)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.open_elements.append(element)

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        for index in range(len(self.open_elements) - 1, -1, -1):
            if self.open_elements[index][0] == tag:
                del self.open_elements[index:]
                break

    def with_id(self, element_id):
        return [attrs for _, attrs in self.elements if attrs.get("id") == element_id]

    def links_with_class(self, class_name):
        return [attrs.get("href") for tag, attrs in self.elements
                if tag == "a" and class_name in attrs.get("class", "").split()]


class SignupBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = build.TPL.read_text()
        cls.articles = [{
            "id": "test-chapter",
            "title": "Example chapter",
            "title_html": "Example chapter",
            "num": "1",
            "part_key": "part1",
            "html": '<header class="ch-head"><h1>Example chapter</h1></header>',
        }]
        cls.home, _ = build.landing(cls.articles, {"bars": [
            {"label": "Baseline", "value": 10},
            {"label": "With context", "value": 20},
        ]})
        cls.nav = build.build_nav(cls.articles, [("Example", "part1")])
        cls.body = ''.join(f'<article class="ch" id="{article["id"]}">{article["html"]}</article>'
                           for article in cls.articles)

    def render(self, site_url, mode, preview=False):
        with patch.multiple(build, SITE_URL=site_url, SIGNUP_PREVIEW=preview):
            return build.render(self.template, self.body, self.nav, self.home, [], mode, self.articles)

    def assert_dialog_structure(self, document):
        dialogs = [(tag, attrs, parents) for tag, attrs, parents in document.element_contexts
                   if attrs.get("id") == "updates"]
        self.assertEqual(len(dialogs), 1)
        tag, attrs, parents = dialogs[0]
        self.assertEqual(tag, "dialog")
        self.assertNotIn("open", attrs)
        self.assertEqual(attrs.get("closedby"), "none")
        self.assertFalse(any(parent_tag == "article" for parent_tag, _ in parents))
        descendants = [(tag, attrs) for tag, attrs, parents in document.element_contexts
                       if any(parent_attrs.get("id") == "updates" for _, parent_attrs in parents)]
        descendant_ids = {attrs.get("id") for _, attrs in descendants}
        for label in ("aria-labelledby", "aria-describedby"):
            self.assertIn(label, attrs)
            self.assertTrue(set(attrs[label].split()) <= descendant_ids)
        for control_id in ("signup-close", "signup-dismiss"):
            controls = [(tag, attrs) for tag, attrs in descendants if attrs.get("id") == control_id]
            self.assertEqual(controls, [])
        self.assertFalse(any(tag == "form" and attrs.get("method") == "dialog"
                             for tag, attrs in descendants))
        self.assertTrue(any(tag == "a" and attrs.get("href") == build.SIGNUP_ORIGIN + "/#updates"
                            and any(parent_tag == "noscript" for parent_tag, _ in parents)
                            for tag, attrs, parents in document.element_contexts))

    def test_signup_is_one_accessible_dialog_outside_the_regular_articles(self):
        for site_url, mode, preview in (
            (build.SIGNUP_ORIGIN, "site-index", False),
            (build.SIGNUP_ORIGIN, "site-index", True),
            (build.SIGNUP_ORIGIN, "site", False),
            (build.SIGNUP_ORIGIN, "site", True),
        ):
            with self.subTest(site_url=site_url, mode=mode, preview=preview):
                document = Document(self.render(site_url, mode, preview))
                self.assert_dialog_structure(document)
                self.assertEqual(len(document.with_id("home")), 1)
                self.assertEqual(len(document.with_id("test-chapter")), 1)

    def assert_link_only(self, html):
        document = Document(html)
        self.assertEqual(len(document.with_id("updates")), 1)
        self.assertEqual(document.with_id("signup-embed"), [])
        self.assertEqual(document.with_id("signup-mount"), [])
        self.assertFalse(any(tag == "dialog" for tag, _ in document.elements))
        self.assertTrue(any(tag == "a" and attrs.get("href") == build.SIGNUP_ORIGIN + "/#updates"
                            for tag, attrs in document.elements))
        # Source can contain the loader, but fallback editions must not eagerly load it.
        self.assertFalse(any(tag == "script" and "hsforms" in attrs.get("src", "")
                             for tag, attrs in document.elements))

    def test_standalone_artifact_is_link_only_even_with_production_configuration(self):
        for site_url in ("", build.SIGNUP_ORIGIN, build.SIGNUP_ORIGIN + "/"):
            for preview in (False, True):
                with self.subTest(site_url=site_url, preview=preview):
                    self.assert_link_only(self.render(site_url, "artifact", preview))

    def test_default_and_fork_homepages_cannot_mount_production_form(self):
        for site_url in (
            "",
            "http://localhost:8000",
            "https://example.org/playbook/",
            "http://analytics-playbook.atlan.com/",
            "https://analytics-playbook.atlan.com.example.org/",
            "https://analytics-playbook.atlan.com/fork/",
            "https://analytics-playbook.atlan.com/?preview=1",
        ):
            with self.subTest(site_url=site_url):
                for mode in ("site-index", "site"):
                    self.assert_link_only(self.render(site_url, mode))

    def test_canonical_hosted_pages_have_one_mount_and_a_no_script_fallback(self):
        for site_url in (build.SIGNUP_ORIGIN, build.SIGNUP_ORIGIN + "/"):
            with self.subTest(site_url=site_url):
                document = Document(self.render(site_url, "site-index"))
                self.assertEqual(len(document.with_id("updates")), 1)
                self.assertEqual(len(document.with_id("signup-mount")), 1)
                embeds = document.with_id("signup-embed")
                self.assertEqual(len(embeds), 1)
                self.assertIn("hidden", embeds[0])
                self.assertNotIn("data-local-preview", embeds[0])
                fallbacks = document.with_id("signup-fallback")
                self.assertEqual(len(fallbacks), 1)
                self.assertNotIn("hidden", fallbacks[0])

    def test_local_preview_is_explicit_and_requires_a_canonical_homepage_build(self):
        document = Document(self.render(build.SIGNUP_ORIGIN, "site-index", preview=True))
        self.assertEqual(document.with_id("signup-embed")[0].get("data-local-preview"), "true")
        for site_url in ("", "http://localhost:8765", "https://example.org/playbook/"):
            with self.subTest(site_url=site_url):
                self.assert_link_only(self.render(site_url, "site-index", preview=True))

    def test_preview_opt_in_accepts_only_the_explicit_environment_value(self):
        for value, expected in (("", False), ("0", False), ("true", False), ("1", True)):
            with self.subTest(value=value), patch.dict("os.environ", {"PB_SIGNUP_PREVIEW": value}):
                module = importlib.util.module_from_spec(SPEC)
                SPEC.loader.exec_module(module)
                self.assertIs(module.SIGNUP_PREVIEW, expected)

    def test_non_hosted_render_modes_cannot_mount_production_form(self):
        for mode in ("artifact", "preview", ""):
            with self.subTest(mode=mode):
                self.assert_link_only(self.render(build.SIGNUP_ORIGIN, mode))

    def test_upgrade_policy_is_only_in_opted_in_canonical_hosted_page_heads(self):
        def policies(elements):
            return [attrs.get("content") for tag, attrs in elements
                    if tag == "meta" and attrs.get("http-equiv", "").lower() == "content-security-policy"]

        for site_url in ("", "https://example.org/playbook/", build.SIGNUP_ORIGIN + "/"):
            for preview in (False, True):
                with self.subTest(site_url=site_url, preview=preview), tempfile.TemporaryDirectory() as directory:
                    with patch.multiple(build, SITE_URL=site_url, SIGNUP_PREVIEW=preview):
                        build.write_site(directory, self.template, self.articles, self.nav, self.home, [])
                        with patch.multiple(build, DIAGRAM_IDS=[], EXTRA_DIAGRAMS=[]):
                            build.write_gallery(directory, self.template, self.nav, {})
                    homepage = Document((Path(directory) / "index.html").read_text())
                    chapter = Document((Path(directory) / "test-chapter.html").read_text())
                    gallery = Document((Path(directory) / "gallery.html").read_text())
                    expected = ["upgrade-insecure-requests"] if preview and site_url == build.SIGNUP_ORIGIN + "/" else []
                    for page in (homepage, chapter, gallery):
                        self.assertEqual(policies(page.head_elements), expected)
                        self.assertEqual(policies(page.elements), expected)
                    artifact = Document(self.render(site_url, "artifact", preview))
                    self.assertEqual(policies(artifact.elements), [])

    def test_generated_chapter_navigation_reaches_homepage_signup(self):
        for site_url in ("", "https://example.org/playbook/", build.SIGNUP_ORIGIN + "/"):
            with self.subTest(site_url=site_url), tempfile.TemporaryDirectory() as directory:
                with patch.object(build, "SITE_URL", site_url):
                    build.write_site(directory, self.template, self.articles, self.nav, self.home, [])
                homepage = Document((Path(directory) / "index.html").read_text())
                chapter = Document((Path(directory) / "test-chapter.html").read_text())
                self.assertEqual(homepage.links_with_class("toc-signup"), ["#updates"])
                self.assertEqual(chapter.links_with_class("toc-signup"), ["index.html#updates"])
                self.assertEqual(len(homepage.with_id("updates")), 1)
                if site_url == build.SIGNUP_ORIGIN + "/":
                    self.assertEqual(len(chapter.with_id("signup-mount")), 1)
                    self.assert_dialog_structure(chapter)
                else:
                    self.assertEqual(chapter.with_id("signup-mount"), [])


JS_GATE_HARNESS = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const events = () => ({
  listeners: new Map(),
  addEventListener(type, callback) {
    const list = this.listeners.get(type) || []; list.push(callback); this.listeners.set(type, list);
  },
  emit(type, values = {}) {
    const event = Object.assign({type, target: this, defaultPrevented: false,
      preventDefault() {this.defaultPrevented = true;}, stopPropagation() {}}, values);
    for (const callback of this.listeners.get(type) || []) callback(event);
    return event;
  }
});
let focused = null;
function element(id) {
  const classes = new Set();
  return Object.assign(events(), {
    id, children: [], attrs: {}, hidden: false, open: false, isConnected: true, textContent: '',
    classList: {add(...names) {names.forEach(name => classes.add(name));},
      remove(...names) {names.forEach(name => classes.delete(name));},
      contains(name) {return classes.has(name);}, values() {return [...classes];}},
    setAttribute(name, value) {this.attrs[name] = String(value);},
    getAttribute(name) {return this.attrs[name] ?? null;},
    appendChild(child) {this.children.push(child); return child;},
    replaceWith(other) {this.replaced = other;},
    showModal() {this.open = true;},
    close() {this.open = false; this.emit('close');},
    focus() {focused = this.id;},
    getClientRects() {return [{}];},
    getBoundingClientRect() {return {left: 10, top: 10, right: 100, bottom: 100};}
  });
}
const ids = ['updates', 'signup-embed', 'signup-mount', 'signup-status', 'signup-retry',
  'signup-fallback', 'signup-title', 'main'];
const nodes = Object.fromEntries(ids.map(id => ['#' + id, element(id)]));
nodes['.tb-nav'] = element('nav-button');
if (!input.mount) nodes['#signup-embed'] = null;
else if (input.preview) nodes['#signup-embed'].setAttribute('data-local-preview', 'true');
const dialog = nodes['#updates'], body = element('body'), head = element('head');
const navLink = element('nav-signup');
const document = Object.assign(events(), {body, head, activeElement: body,
  createElement(tag) {return element(tag);}});
const window = events();
const url = new URL(input.url);
let reloads = 0;
const location = {origin: url.origin, protocol: url.protocol, hostname: url.hostname,
  hash: url.hash, reload() {reloads++;}};
const storage = {...(input.session || {})}, sessionWrites = [], localWrites = [];
const sessionStorage = {
  getItem(key) {if (input.storageBlocked) throw new Error('storage blocked'); return storage[key] ?? null;},
  setItem(key, value) {if (input.storageBlocked) throw new Error('storage blocked');
    sessionWrites.push([key, value]); storage[key] = String(value);}
};
const localStorage = {getItem() {return null;}, setItem(...args) {localWrites.push(args);}};
const timers = new Map(); let timerId = 0;
const context = {document, window, location, sessionStorage, localStorage,
  MODE: input.mode, current: {id: 'test-chapter'},
  $: selector => nodes[selector] || null,
  $$: selector => selector === '.toc-signup' ? [navLink] : [],
  setDrawer() {body.classList.remove('nav-open');},
  history: {replaceState(_state, _title, hash) {location.hash = hash;}},
  setTimeout(callback) {timers.set(++timerId, callback); return timerId;},
  clearTimeout(id) {timers.delete(id);},
  fetch() {throw new Error('Network access is forbidden in gate tests');}
};
vm.runInNewContext(input.source, context, {timeout: 1000});
if (context.signupUi?.auto) context.signupUi.open();
function snapshot() {
  return {open: dialog.open, locked: context.signupUi?.locked() || false,
    auto: context.signupUi?.auto || false, classes: body.classList.values(),
    scripts: head.children.length, frames: nodes['#signup-mount'].children.length,
    retryVisible: !nodes['#signup-retry'].hidden, session: {...storage},
    sessionWrites: [...sessionWrites], localWrites: [...localWrites], focused, reloads};
}
function detail(formId) {
  const result = {formId};
  for (const key of ['email', 'fields', 'submissionValues']) Object.defineProperty(result, key, {
    get() {throw new Error('The gate must not read submitted personal fields');}
  });
  return result;
}
const snapshots = [snapshot()], prevented = [];
for (const action of input.actions || []) {
  if (action === 'success' || action === 'wrong-success' || action === 'failure' || action === 'ready') {
    const type = action === 'ready' ? 'hs-form-event:on-ready' : action === 'failure'
      ? 'hs-form-event:on-submission:failed' : 'hs-form-event:on-submission:success';
    window.emit(type, {detail: detail(action === 'wrong-success' ? 'other-form' : input.form_id)});
  } else if (action === 'malformed-success') {
    window.emit('hs-form-event:on-submission:success', {});
  } else if (action === 'cancel') prevented.push(dialog.emit('cancel').defaultPrevented);
  else if (action === 'escape') prevented.push(document.emit('keydown', {key: 'Escape'}).defaultPrevented);
  else if (action === 'backdrop') dialog.emit('click', {clientX: 0, clientY: 0});
  else if (action === 'close') dialog.close();
  else if (action === 'timeout') {for (const callback of [...timers.values()]) callback();}
  else if (action === 'script-error') head.children[0]?.onerror();
  else if (action === 'open') context.signupUi?.open();
  else if (action === 'retry') nodes['#signup-retry'].emit('click');
  snapshots.push(snapshot());
}
process.stdout.write(JSON.stringify({snapshots, prevented}));
"""


class SignupLifecycleTests(unittest.TestCase):
    """Execute the real gate closure with network-free DOM, storage, and HubSpot events."""

    @classmethod
    def setUpClass(cls):
        cls.node = os.environ.get("NODE_BINARY") or shutil.which("node")
        if not cls.node:
            raise unittest.SkipTest("Node.js is required for isolated signup lifecycle tests")
        template = build.TPL.read_text()
        start = template.index("var signupUi=(function(){")
        end = template.index("\nvar articles=", start)
        cls.source = template[start:end]
        cls.form_id = re.search(r"var formId='([^']+)'", cls.source).group(1)
        cls.session_key = "pb.signup.submitted." + cls.form_id

    def run_gate(self, actions=(), **options):
        payload = {"source": self.source, "form_id": self.form_id, "mount": True,
                   "url": build.SIGNUP_ORIGIN + "/#test-chapter", "mode": "site-index",
                   "preview": False, "actions": actions, **options}
        result = subprocess.run([self.node, "-e", JS_GATE_HARNESS], input=json.dumps(payload),
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_matching_success_unlocks_once_without_reading_or_persisting_fields(self):
        for mode in ("site-index", "site"):
            with self.subTest(mode=mode):
                states = self.run_gate(["open", "success", "success", "open"], mode=mode)["snapshots"]
                self.assertTrue(states[0]["open"])
                self.assertTrue(states[0]["locked"])
                self.assertIn("signup-locked", states[0]["classes"])
                self.assertEqual(states[1]["scripts"], 1)
                for state in states[2:]:
                    self.assertFalse(state["open"])
                    self.assertFalse(state["locked"])
                    self.assertNotIn("signup-locked", state["classes"])
                    self.assertEqual(state["sessionWrites"], [[self.session_key, "1"]])
                    self.assertEqual(state["localWrites"], [])
                    self.assertEqual(state["frames"], 1)
                    self.assertEqual(state["scripts"], 1)

    def test_wrong_form_readiness_and_submission_failure_never_unlock(self):
        states = self.run_gate(["wrong-success", "malformed-success", "ready", "failure"])["snapshots"]
        for state in states:
            self.assertTrue(state["locked"])
            self.assertTrue(state["open"])
            self.assertEqual(state["sessionWrites"], [])

    def test_cancel_escape_backdrop_and_close_cannot_dismiss_the_pending_gate(self):
        result = self.run_gate(["cancel", "escape", "backdrop", "close"])
        self.assertEqual(result["prevented"], [True, True])
        for state in result["snapshots"]:
            self.assertTrue(state["open"])
            self.assertTrue(state["locked"])

    def test_load_failure_keeps_the_gate_locked_and_offers_reload(self):
        for failure in ("script-error", "timeout"):
            with self.subTest(failure=failure):
                states = self.run_gate([failure, "retry"])["snapshots"]
                self.assertTrue(states[1]["open"])
                self.assertTrue(states[1]["locked"])
                self.assertTrue(states[1]["retryVisible"])
                self.assertEqual(states[1]["sessionWrites"], [])
                self.assertEqual(states[2]["reloads"], 1)

    def test_session_success_skips_gate_and_embed_on_following_page_load(self):
        saved = self.run_gate(["success"])["snapshots"][-1]["session"]
        for mode in ("site-index", "site"):
            with self.subTest(mode=mode):
                state = self.run_gate(["open"], mode=mode, session=saved)["snapshots"][-1]
                self.assertFalse(state["open"])
                self.assertFalse(state["locked"])
                self.assertEqual(state["scripts"], 0)
                self.assertEqual(state["frames"], 0)
                self.assertEqual(state["sessionWrites"], [])

    def test_unavailable_storage_does_not_block_success_in_the_current_document(self):
        state = self.run_gate(["success"], storageBlocked=True)["snapshots"][-1]
        self.assertFalse(state["open"])
        self.assertFalse(state["locked"])

    def test_runtime_origin_and_preview_guards_allow_only_intended_hosts(self):
        cases = [
            ("http://127.0.0.1:8765/", False, False),
            ("http://127.0.0.1:8765/", True, True),
            ("http://localhost:8765/", True, True),
            ("http://[::1]:8765/", True, True),
            ("http://localhost.example.org/", True, False),
            ("https://example.org/playbook/", True, False),
            ("https://analytics-playbook.atlan.com.example.org/", True, False),
            ("http://analytics-playbook.atlan.com/", False, False),
            ("file:///example/playbook.html", True, False),
        ]
        for url, preview, eligible in cases:
            with self.subTest(url=url, preview=preview):
                state = self.run_gate(url=url, preview=preview)["snapshots"][0]
                self.assertEqual(state["locked"], eligible)
                self.assertEqual(state["scripts"], int(eligible))
        for mode in ("artifact", "preview"):
            with self.subTest(mode=mode):
                state = self.run_gate(mode=mode, preview=True)["snapshots"][0]
                self.assertFalse(state["locked"])
                self.assertEqual(state["scripts"], 0)


if __name__ == "__main__":
    unittest.main()
