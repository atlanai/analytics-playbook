# Changelog

Version history of The FDE Playbook for Analytics Agents, newest first. Older entries describe the book as it stood then.

**Unreleased.** GitHub star count; no version label.

- The GitHub link at the bottom of the sidebar shows the repository's star count.
- Removed the version label from the header, the cover, the Markdown copies and the README.

**Unreleased.** One job per opening page.

- The Overview now says what you walk away with and what is inside the book, before the reading paths.
- Why analytics agents are hard is the problem and just enough proof: five steps and the hard one (moved from the method page), the tenth question, the five hidden decisions and the model chart. It ends with a table of the four problems and where the book fixes each.
- The method at a glance is the plan only: the lifecycle, eight rules that link to their evidence, the gates, the step map and the running example.
- The context ladder opens The method at a glance, as what closes the gap. Moved the rest of the evidence out of the opening chapter: what teams try first to What we found, the SQL-and-sentence comparison to The metric is the unit, the fixed-test case and run-to-run guidance to Evals first, and other teams' results to What others found.
- Removed the builder's story comic.
- The sponsor's reading path now starts with Why analytics agents are hard.

**Unreleased.** Refresh the three podcasts.

- Renamed certified metrics to metrics; the benchmark's metrics had no owner review.
- Replaced the sponsoring, building and delivery recordings with NotebookLM conversations based on the updated guide, retaining the compact Listen controls.
- Added recording-derived transcripts and episode clarifications. Updated titles, durations and source provenance.

**Unreleased.** Remove the evidence register.

- Removed the evidence register tables and their search entries from the published guide. How we measured keeps the benchmark methodology.
- Removed the register file from the repository. Evidence IDs remain in build metadata for identifier checks; maintainers review sources in pull requests. Updated chart source labels and the cover's methodology link.

**Unreleased.** No product page.

- How Atlan helps is removed, with its Registry diagram and its place in the contents. The book describes the method only, and the README FAQ, the method page, the glossary and the tooling page no longer point to a product page.

**Unreleased.** Read it with your agent.

- **Copy page.** A menu at the top right of every page copies the page as Markdown for an agent, opens it as plain text, or opens it in Claude, ChatGPT or Perplexity.
- **Markdown beside every page.** The site publishes each page as `<page>.md`, with `llms.txt` as the index and `llms-full.txt` as the whole book.

**V4.0, 2026-10-23.** Problem, method, reference.

- **Three parts, in the order a reader meets them.** *Why it is hard* names the four problems in one chapter: the tenth question, what the question means, deciding the same way every time, and knowing you are right. Each section ends with where its fix lives. *How to build one* opens with the method on one page, then one page per principle (evals first, the metric is the unit, serve per question), the five phases, and one chapter on keeping it running. *How Atlan helps*, the Toolkit and Research and reference follow.
- **One opening page.** The lifecycle page and "The method at a glance" are merged; "How to read this book" sits beside the reading paths.
- **Fewer, fuller chapters.** Four explainers fold into the three principle pages; three post-launch chapters fold into *Keep it running*. The tool comparison and "one model in six syntaxes" become a reference page, *Semantic layers compared*. The skeptic FAQ, *Straight answers*, moves to the Toolkit. Every anchor the old chapters carried still resolves, and every evidence chip is still cited.
- **Navigation.** The contents are five groups under two headings, Learn and Resources, each with an icon and a page count; groups open on the page you are on, and the first chapter is now *Why analytics agents are hard*. The chosen reading path is a stepper at the top of the contents, with a way to stop following it. The reading paths are rewritten over the new spine, and a card for partner delivery joins the set.
- **Readability.** A heading that promises a count names the items in the text; one idea per paragraph, the measurement last. The authoring guide carries the checks.

**Unreleased.** Listen to the guide.

- Three NotebookLM podcasts, one per reading track, with a small Listen action beside the reading choices.
- One dismissible player appears after a click and keeps playing while readers navigate the guide. It includes seeking, rewind, speed and optional download controls.
- The episode list uses compact rows. Audio is served with the site and fetched only on request; starting another episode replaces the first.

**Unreleased.** The method on one map.

- **Find your task, as an explorer.** On the lifecycle page, a rail of the five phases and After launch, around the golden set. Pick a stage to see its numbered steps, and a step to see how it is done, who does it, the template or checklist and the mistake to avoid. Next step walks the whole method in order. It replaces the task board, and reads as an outline in print and without JavaScript.
- **Keep it in step.** CONTRIBUTING.md and the steps for proposing a change now ask for the map to be updated whenever the sections it restates change.

**V3.4, 2026-10-05.** Videos.

- **Nine narrated videos.** The overview sits on the lifecycle page. The tenth question, why evals come first, semantic views or metrics, and each of the five phases now open with their own video, with a transcript under it. Every number on screen matches the text.
- **A Videos page in the Toolkit.** One player and the full playlist, about 26 minutes in all, with autoplay to the next video and the transcript of whatever is playing.
- **Why evals come first** now carries the points from its video: run each question three to five times, what one row of the golden set holds, four properties of an eval worth trusting, and grading in layers.
- **One scoreboard.** The results page ranks every setup in one table.
- **No hand-written context.** How we measured now states the benchmark's rule: our systems built all the context; people wrote only the questions and the sealed answers.

**V3.3, 2026-10-02.** Retrieval, jargon and the research in full.

- **What we found.** A new results page: a scoreboard of every setup with cost and time, joins against single tables, results by business area, four worked examples, why the last answers fail, what each part of the layer is worth, and how much runs vary.
- **How the agent finds its context.** A new chapter on retrieval: one context call per question, served live over MCP, with the architecture and the ranking rules.
- **Jargon.** A callout in [What the agent has to know](chapters/02-what-it-must-know.md) on acronyms and house shorthand.
- **Toolkit and Research.** Templates moved next to the cards. The results, the method and what others found now sit together under Research.
- **One correction.** The shipping configuration missed 17 wrong and 1 refusal, not 16 and 1.

**V3.2, 2026-10-01.** A new design and a full content review.

- **Renamed.** The book is now The FDE Playbook for Analytics Agents.
- **A calmer page.** One type family, one accent colour and one text column: text, code, figures, tables and callouts share the same edges. The contents sit at the left; "On this page" sits on the right on wide screens and under the current chapter on narrower ones. Figures open larger on click. The phase strip is a thin bar, and Skim and Whole book are quiet switches.
- **Find your task.** The task board lists each stage's tasks as how-to links, with the template and checklist beside each one.
- **One name per stage.** The lifecycle, the task board and the chapters use the same phase names.
- **The headline is 83.2%.** It is the certified-layer configuration we ship, on all 107 questions. It replaces about 81%, the median of 12 variant runs.
- **Numbers say what was run.** The model claim now says two models were run both ways and each gained 26 points or more from context; the ladder notes which rungs were measured on another model or older keys.
- **Tighter chapters.** Phase 1 has its own rule, Phase 4 wires the surface chosen in Phase 0 instead of choosing it again, Semantic views or metrics? closes Part I, phase chapters end on their card, and headings say what each section concludes.

**V3.1, 2026-09-29.** A storyline pass after three reader reviews: a sponsor's, a delivery lead's and a skeptical Head of Data's.

- **The start page leads with the problem.** The thesis, "not a model problem, a context problem", now opens the book. "What we learned" and "Rules" merged into one list of eight rules, each tied to what we measured. The page says who "we" is, how long Phase 0 takes, and what your team holds at the end of Phase 4.
- **Numbers carry their scope.** Chapter 1 states the benchmark's limits in one place. Chapter 2 reconciles its headline (about 81%, the median of 12 runs) with its best run (84%), and says which setup each row of "What didn't work" was measured on. Every scene is labelled as the composite engagement.
- **The opening query is right.** The fiscal year ends 30 June, so the hero query now filters fiscal Q3.
- **Atlan on one page.** The product callouts left the chapters. Everything a platform adds, including metric and eval generation, now sits on [How Atlan helps](chapters/11-how-atlan-helps.md); the chapters describe a context layer you can build yourself.
- **Semantic views or metrics?** A new chapter compares storing context per table, per logical table and per metric, scores each against what an agent needs, maps today's tools by how far a metric can reach, and shows how to start without replatforming.
- **A guide for any team.** Phase 0 marks what only matters when a vendor or outside team is involved. The book follows one build path, whether or not an agent already exists, and what you already have is brought in as a source in Phase 2. The ladder now splits table descriptions from usage patterns, and the start of the book carries fewer numbers.
- **How we measured.** The evidence register became How we measured: the benchmark behind every number, with example questions and the decision each one hides, followed by the register.
- **Why evals come first.** The case for the golden set now has its own chapter in Part I; Phase 1 keeps the how-to.
- **Four parts.** Phase 4 now ends at the handover. Part III, After launch, holds Keep it running (the production loop, drift and domain two) and Answer why. Part IV, Leading the program, holds the delivery lead's guide and Straight answers.
- **The lifecycle.** A new first page shows the five steps every question takes, where the hard one is, and the lifecycle the book follows, with each stage one click from its chapter, and a task board that links every task to its section, template and checklist.
- **Read at the depth you have.** Every chapter opens with an "In one minute" box: the short version, one thing to do, and when to skip it. Skim mode (the Skim button, or S) shrinks each chapter to its rule, that box, its key figure and its headings. Press ? for keyboard shortcuts.
- **Answer why, simplified.** One storyline: get the numbers right, add a map of how the business works and a dated record of what changed, then decide whether it is worth building. The ontology diagram is the chapter's key figure.
- **How Atlan helps, reframed.** The page now starts from what breaks when you run the loop a second time, and what a shared store does about each.
- **What others found.** A new reference page summarises the most useful outside work, from engineering teams and research papers, and how each approach scored on our benchmark.
- **The running example closes its loops.** The CRO answers the ARR question, and Phase 3 explains why Phase 2 could not have caught the ranking rule.
- **The book ends on Monday.** Straight answers now carry the four hardest replies inline and close with four things to do on Monday. Phase 2 shows how to generate candidates without a product, and the delivery chapter links the kickoff agenda and pre-read.

**V3.0, 2026-09-29.** A rewrite for first-time readers, after the owner's review of V2. The benchmark and the evidence did not change; how much of it the reader has to carry did.

- **Four weeks, not six.** Phase 0, then Phase 1 (the golden set), Phase 2 (generate certified metrics), Phase 3 (hill-climb from traces) and Phase 4 (release and hand over). The six-week plan asked for more calendar than the work needs.
- **Generate metrics, then resolve conflicts.** "Mine query history" becomes generating metrics from past SQL and BI together, with a metrics generator, bought or built. "Rule on the forks" becomes "resolve conflicts", and provenance (who ran a query, how often, how recently, whether it matches the warehouse) settles most of them before the owner is asked. The method no longer leans on a person for every decision.
- **Simpler method.** The golden set is at least 20 real questions, with one bar per lane on the whole set instead of a bar per question class. No model freeze or fallback model: change the model when you need to and rerun the golden set. Tasks are lists, not day plans. Security stays at what leaves the building and the access list.
- **Outcomes over numbers.** Chapters keep a few plain numbers, each traced to the evidence register by a hidden comment. Evidence chips, run counts and the two-scope comparison left the chapters. The old chapter 3 folded into the first two, which now open on a model chart and a single ladder. The register holds only the results the chapters and cards cite; the failure modes say "measured" or "diagnosis" instead of linking IDs.
- **No internal codes, plainer words.** Question codes, ruling and edit numbers, chapter and card numbers are gone. Cards display by title, and new ones were added: What you need before you start, Is it ready to launch?, and Replies for the skeptic. "Golden set" is the one name for the sealed questions. "Path A / Path B" became "no agent yet" and "you already have one", "waves" became rounds, and "noise" became run-to-run variation.
- **Product callouts.** Short callouts described what a platform adds at each step. (In 3.1 they moved to one page.)
- **Reading.** Fewer inline links, one quiet "Read more" per section, the doors as an accordion, and a fix for the right rail showing the previous page's sections.

**V2.0, 2026-09-29.** A rebuild for reading and for trust. One composite sales engagement ran through a week-by-week Part II, with every artifact shown with its values and the templates filled from it. The register gained tiers, scope and run detail. The governed lane's execution was labelled Design. Ten printable cards, a self-assessment, filterable failure modes and light and dark themes arrived.

**V1.0, 2026-09-27.** First release: front matter, Part I (why agents stall), Part II (the method), Part III (the field guide) and the reference section, followed the same day by a number audit and an editorial red team.
