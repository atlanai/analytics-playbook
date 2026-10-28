# R2. Glossary {#r4}

> [!RULE]
> One word, one meaning. Where a chapter disagrees with the glossary, the glossary wins and the chapter gets fixed.

Every term names part of the method.

**Agent architecture.** The four parts of an analytics agent: the surface where people ask, the harness that runs the loop, the model, and the context it reads before writing SQL. It is either platform-native, such as Databricks Genie or Snowflake CoWork (formerly Snowflake Intelligence), or custom, built on a framework such as Google ADK or LangGraph.

**Agent builder.** The company's engineer who builds and runs the harness, exports traces and runs every eval, baseline, round and gate.

**Answer key (key).** The sealed expected answer of one golden-set item. The golden set holds one per question.

**As-of date.** The fixed snapshot every expected answer is computed at, such as a fiscal year-end. The harness passes it on every eval run, so sealed answers stay reproducible.

**Bare schema.** The agent with the warehouse schema and nothing else: no descriptions, past queries, metrics or rules. It is the benchmark's floor, and the Phase 1 baseline for a domain with no context yet.

**Baseline.** The first scored run, at the end of Phase 1: the agent on bare schema, or on its existing context, once per sealed question. It prices the decisions your schema leaves out.

**Business changes.** A dated record of what changed in the business, such as a territory realignment or a pricing change, tied to ontology entities so the agent can test them as causes. It is the part of the why-question context that decays first.

**Business term.** A word the business uses, defined once, with its alternate labels, and linked to the metric, query or entity it names. Its main job is retrieval: "slipped" finds a query about deals "pushed" past quarter end. Internal names such as project and product names belong here.

**Card.** A one-page checklist you can print. Most cards close a chapter, and all are collected in [Cards](#cards). Cards are called by their titles.

**Clock.** The build, Phases 1 to 4. It starts once Phase 0's gate is met, so Phase 0 runs before the clock.

**Conflict.** Two definitions of the same thing, both in use, such as two rankings of "top 100 customers". The agent flags a conflict instead of picking a side. It is resolved by provenance first, then by whoever owns that number.

**Conflict record.** The record of a resolved conflict: the variants, their provenance, the decision, who made it, what changed and what would reopen it. Kept on [its template](#r2-6).

**Context.** Everything the agent is given besides the question: the schema, metrics, trusted past queries, rules, business terms and, for why-questions, the ontology.

**Context call.** The one call the harness makes per question, before any SQL, to fetch the context that applies. Its shape is fixed before the baseline so later scores compare.

**Context engineer.** The person running the engagement, from a partner or your own team (in-house: an analytics engineer), who generates candidates, reads traces and runs the hill climb. Never sees an expected answer.

**Context layer.** The governed store of context that sits under any agent and serves it per question.

**Decisions log.** The conflict records ([template](#r2-6)): every place two defensible definitions were in use, who decided, and when. It outlasts the rest of the handover.

**Decoy.** The wrong answer you get when the choices a question hides are guessed the obvious way, recorded on the golden-set item. For the pipeline question it is $1.31B.

**Definition of done.** The checklist that closes a chapter's phase, checked item by item.

**Delivery lead.** The person who runs the engagement phase by phase, from the kickoff to the handover: sessions, gates and readouts.

**Domain.** One business area with its own questions, users and tables, such as sales pipeline. The method runs one domain at a time.

**Domain owner.** The company's person who owns the business definitions in a domain and settles the conflicts provenance cannot. A definition that crosses teams has a co-owner, as the FP&A partner co-owns "top 100 customers".

**Drift.** The slow loss of accuracy as the business changes and the context does not. Traces, user corrections and repeated runs feed it back.

**Eval owner.** The person who drafts and seals the golden set with the graders, and audits the grading.

**Exec sponsor.** The executive who sets the bar, chooses the domain and the agent architecture, and decides at each gate and at launch.

**Exploratory lane.** Long-tail and diagnostic questions, answered by SQL the agent writes, grounded in trusted past queries. Every answer shows its SQL and sources, so a reader can check it before acting.

**Gate.** The checkable condition that ends each step: Phase 0 (brief agreed, access proved), Phase 1 (20 or more sealed, baseline scored), Phase 2 (metrics scored), Phase 3 (new questions added for the launch test, nothing that passed has broken) and the launch gate in Phase 4.

**Generate metrics.** Phase 2's core task: a metrics agent reads past SQL, BI reports and semantic models, and proposes candidate metrics with the real queries behind them. Candidates are then witnessed, conflicts resolved, and the survivors approved.

**Golden set.** The sealed questions with expected answers, expected SQL and a grading method, built from questions the business already asks: at least 20 in Phase 1. During Phase 3 the graders draft new questions the context engineer never sees. They are held out of the climb and first scored at the launch gate, so the launch score is not one anyone tuned against.

**Governed lane.** The numbers the business runs on. They come only from a metric, run as served, and the lane fails loudly: no metric, no answer.

**Grain.** What one row represents before aggregation, such as one row per customer. Most inflated totals are grain errors.

**Harness.** The agent runtime around the model: its loop, tools, prompts and step budget. It belongs to the company, which builds and runs it.

**Hill climb.** Phase 3's loop: run the golden set, read the raw trace of each miss, classify it, make the smallest fix, and rerun. "Hill climb" is the noun; "hill-climb" is the verb.

**House rule.** A rule that holds for every question in the domain, such as "quarter means fiscal quarter". Serve it as a rule, and write it into every metric it touches, because an instruction never reaches SQL the harness runs as served.

**Iteration ledger.** The record of every round: what changed, the fixes predicted before the run, the score, and whether the change was kept.

**Launch gate.** The Phase 4 test: the golden set scores at or above the bar in the brief on every run, nothing that passed has broken, the random pass audit is done, out-of-scope questions are refused, and the first pass your team runs alone is booked, within two weeks. The sponsor decides go, no-go or go with conditions.

**LLM judge.** A model that grades what code cannot, such as whether an answer states its period, filter and unit. It never grades the number itself when code can, and it counts only once calibrated against human graders.

**Metric.** A business number as one executable SQL statement: population, grain, time rule, formula, exclusions and filters, with its provenance. It has an owner and is versioned like code. In the benchmark, no person approved the metrics.

**Metrics agent.** Any model-driven script that reads past SQL, BI reports and semantic models and drafts candidate metrics, each cut from a real statement.

**Metrics layer.** The benchmark setup the book ships: metrics served as SQL, plus trusted past queries, retrieved per question. [What we found](#results) scores it against bare schema.

**Ontology.** The business as a graph: entities, relationships and vocabulary, each bound to its tables and metrics. It serves why-questions; metrics serve the numbers.

**Provenance.** The evidence behind a query or metric: who ran it, how many different people, how often, how recently, and whether it runs clean and matches the warehouse. Provenance settles most conflicts without a meeting, and it is served with every metric.

**Random pass audit.** At every gate from Phase 1 on, five passing items, chosen at random, are re-graded by hand against their source. A key found wrong is corrected in either direction, and the score is reported after the correction.

**Refusal.** The governed lane's answer when no metric covers the question: it says so, with no number. Correct on an out-of-scope question, and a miss on an in-scope one. On the benchmark every refusal counts as a miss.

**Regression set.** The golden-set questions the agent already answers right on every run, rerun on every schema change; the full golden set reruns on every context, harness or model change.

**Resolve a conflict.** Settle which of two definitions is right. Provenance decides first; whoever owns that number decides the rest. The decision is written into the metric as SQL.

**Round.** One small batch of context changes, followed by a rerun of the whole golden set, recorded as one row of the iteration ledger.

**Rule.** A small, versioned instruction the agent must follow, such as `quarter-means-fiscal` or "regions roll up to NA, EMEA and APAC". Also called a skill. A rule that touches one metric goes inside that metric; a rule that touches many stays a rule.

**Run-to-run variation.** How far the score moves between identical runs of an unchanged configuration. A change whose effect sits inside it is unresolved. Measure your own before the first round.

**Seal.** A golden-set item is sealed when its expected SQL has run read-only on the snapshot, the result matches the trusted source and no dispute is open. Sealed items are versioned and never edited to make the agent pass.

**Semantic layer.** Metric and join definitions kept in a tool, so every query reuses them. Snowflake semantic views, Databricks metric views, LookML and dbt MetricFlow are all semantic layers. In Phase 2 you treat yours as a source, like past SQL. See [Why a metric, and not a view](#ch-sv).


**Step budget.** A fixed cap on tool calls per question. Ten is a sound default. Raising it tends to turn refusals into wrong answers.

**Stop rule.** Stop the hill climb when two rounds in a row move the total by no more than the run-to-run variation and none of the predicted fixes lands. Cap Phase 3 at five rounds. If the bar is not cleared by then, take the gap to the sponsor.

**Trace.** The full record of one agent run: every context call, what was served, every SQL statement, the answer, tokens and time.

**Trusted past query.** A complete, real analyst SQL statement, literals kept, served as a worked example with its provenance. It grounds the exploratory lane.

**Version.** An approved, numbered release of a context object or of a domain's context, with a diff and a one-step rollback.

**Witness.** Running a candidate metric or query read-only against the warehouse to prove it runs, returns sane values and has the grain it claims.
