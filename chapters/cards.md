# Cards {#cards}

Cards are one-page checklists you can print. Most close a chapter, and each stands on its own, so you can pin the one you need by your desk and leave the book closed.

:::: {.card #c1 title="The whole method"}
Scope one domain, build the golden set, generate and approve metrics, hill-climb from traces, release and hand over. Real traces feed the next version, and domain two starts from what domain one built.

Five phases: Phase 0 to set up, then Phases 1 to 4 to build, test and launch. Each phase ends at a gate, and you move on only when it is met.

1. Phase 0, before the clock. Pick one domain, set the bar, and decide which questions need an exact answer. Settle access and the agent architecture. Gate: the brief agreed, every access item proved.
2. Phase 1, the golden set. Harvest real questions, seal at least 20 with verified answers, and run the baseline once. Gate: 20 or more sealed, baseline scored.
3. Phase 2, generate metrics. Draft them from past SQL and BI, check them against the warehouse, resolve conflicts, approve. Gate: the metrics scored on the same set.
4. Phase 3, the hill climb. Read the raw trace of every miss and make the smallest fix that closes it. Gate: new questions added for the launch test, and nothing that passed has broken.
5. Phase 4, release and hand over. Pass the launch gate, launch, and hand the loop to your team. Gate: launch approved, first solo run booked.

The rules:

1. Fix the context before you change the model. A better model can't guess a rule nobody wrote down.
2. Write each business rule into a metric's SQL. The agent follows a query and skims a paragraph.
3. Build the golden set before any context. Without it, you can't tell progress from luck.
4. Settle conflicts before the agent sees them: provenance first, then the owner. Never let the agent pick.
5. Board numbers need a metric, or no answer.
6. Start with one domain. It is small enough to finish, and its open questions have someone who can settle them.
7. Read the raw trace of every miss, and feed real usage back.
8. Make the agent reliable on what happened before you ask it why.

The five phases leave you metrics your business owns, a golden set that tests each change, and a team that runs the loop without help.
::::

:::: {.card #c2 title="The sponsor's ask"}
Phase 1 can't start until you make five decisions:

1. The domain: one business area, its problem, its users, which kinds of question are governed, and what is out of scope.
2. The bar: one pass rate for the whole golden set, met on every run, written down now.
3. The agent architecture: where people ask, which harness runs the loop, and which model.
4. The people and their time, as set out in [Phase 0](#hours); the hours are indicative. The domain owner's two to three hours a week matter most: engagements stall where that shrinks to minutes.
5. The start date. Phase 0 ends when the brief is agreed and every access item is proved.

At the end of Phase 4 you decide go, no-go or go with conditions.

At each gate you see evidence and make one decision. [What the sponsor sees at each gate](#c10) lays it out.

Go when the golden set scores at or above your bar on every run, nothing that passed before has broken, the random pass audit is done, and out-of-scope questions are refused. Give each condition a date.

| Exec sponsor | Signature | Date |
|---|---|---|
| | | |
::::

:::: {.card #c3 title="The eval owner's week"}
You own the golden set. The context engineer never drafts, sees or edits an expected answer.

The tasks, in order:

1. Choose two graders and fix the as-of date every answer is computed at.
2. Harvest two or three candidates for every question you will seal. Pull them from the board pack, dashboards, tickets, saved analyst queries and the sponsor's own questions.
3. Rewrite each candidate the way a user would ask it, with no table or column names.
4. Graders draft the expected SQL and answer for each one.
5. Write the grading rules before any result exists: returned data first, then the SQL, with a tolerance per answer type.
6. Graders verify every draft against its source. A question with two defensible answers goes to whoever owns that number before it is sealed.
7. Pick at least 20 and seal them.
8. Purge every past query that computes a sealed answer, by hash. Exclude the agent's service account from the query history. Scan every prompt for sealed values; a hit invalidates the run. Commit the set.
9. The baseline runs once per question. Grade it by code against the sealed answers and record the decision the agent guessed on every miss.

Every item carries five required fields: id, the question as asked, source, expected result and expected SQL. Optional: valid alternatives, tolerance, the decisions the question hides, the wrong answer a guess would produce, and a history of every correction.

An item is sealed when its expected SQL has run read-only on the as-of snapshot, the result matches the trusted source, and no dispute is open. Store the set where neither the agent nor the context side can read it. Never edit a question to make the agent pass.

During Phase 3, the graders draft new questions the context engineer never sees. They are held out of the climb and first scored at the launch gate, so the launch score is not one anyone tuned against.

A definition dispute raised while sealing also goes to the conflict list, with no sealed value attached. Otherwise the context side never sees it.
::::

:::: {.card #c4 title="The builder's minimum harness"}
The harness runs in your environment, and your team builds and runs it. Two shapes work: platform-native, such as Databricks Genie or Snowflake CoWork, or custom, on Google ADK, LangGraph or your own loop.

Build this and stop:

1. One context call per question, before any SQL. At baseline it returns the schema only.
2. One read-only SQL tool. Exploratory queries run as the user. Governed answers run under a fixed service identity, so a board number is the same for every asker.
3. A step budget: a fixed cap on tool calls per question. Don't raise it to cut refusals. A bigger budget turns refusals into wrong answers.
4. On a governed question, run the metric's SQL with only its declared parameters filled in. No metric, no answer.
5. A per-call trace: every served item by name and version, each tool call with its arguments and result, every SQL statement including failed ones, the answer or refusal, tokens, steps and time.

The context call goes in with three things:

- the question text, unedited
- the domain whose context to search
- the user's identity, passed through

It comes back with five:

- metrics: name, version, SQL, owner, provenance
- trusted past queries: the top matches, each as complete SQL
- the rules that apply, as instructions
- the business terms the question matched
- the lane: governed when a metric covers the question, otherwise exploratory

Fix the shape of the call on day one. In Phase 2 the metrics arrive behind the same call and nothing else changes, so later scores compare with the baseline.

You can change the model later. When you do, rerun the golden set on the new model before comparing scores.
::::

:::: {.card #c5 title="How to resolve a conflict"}
A conflict is two definitions of the same thing, both in use. Most settle on evidence; whoever owns that number decides the rest in a short session.

First, let provenance decide. For each variant, show:

- who runs it, and how many different people
- how often, and how recently
- whether it runs clean and matches the warehouse
- which dashboards and reports it feeds

When one variant is run by most analysts, recently, runs clean and matches the trusted report, keep it and record why. No meeting needed.

When the evidence splits, it goes to the owner. The day before, prepare each variant's definition as SQL, where it is used, and both results on the snapshot.

The owner resolves it one of five ways:

1. Choose a variant.
2. Name an authoritative source table.
3. Add a population rule, such as "internal and test accounts are out of every number".
4. Retire an object.
5. Dismiss it, with a note.

If another team owns part of the definition, its owner co-approves. If co-owners can't agree, it goes to the sponsor; the agent serves neither version until then.

Example: the top-100 conflict. One variant ranked customers by number of deals. It fed the sales ops dashboard and had plenty of query history, so Phase 2 approved it. The other ranked by current ARR and fed the finance board pack, but its list lived in a spreadsheet and never appeared in query history. Provenance could see only one side. In Phase 3 the raw trace of the pipeline question surfaced the gap. The RevOps lead and the FP&A partner chose ARR in 20 minutes and also wrote "some early stages never count" into the metric. Sales ops kept its tile, renamed "most active accounts".

What happens next:

1. Record the decision and what would reopen it. The losing variant is retired and kept on record.
2. Re-render the metric and check it against the warehouse again.
3. Rerun the whole golden set.

A definition kept in a spreadsheet leaves no trace in query history, so provenance can't rank it. Before approval, trace any pasted list of IDs back to its source.
::::

:::: {.card #c6 title="Why did this miss?"}
::: {.diagram #miss-tree}
Classify every miss before you fix it. Each kind has one fix.
:::

Read the raw trace first and find the first step where the agent decided without context. Then walk the tree.

1. Is the key wrong? The agent's answer is defensible and the key is not.
   1. Yes. The eval owner re-runs the expected SQL, re-checks the source and reseals. Never edit the question.
   2. No. Go to 2.
2. Did the step budget run out partway through?
   1. Yes. Read what the steps were spent on and supply the missing decision. Raising the budget is not the fix.
   2. No. Go to 3.
3. Is the right decision written down anywhere, as a metric, rule, business term or trusted query?
   1. No. Never written. Draft it; provenance or the owner settles it.
   2. Yes. Go to 4.
4. Was it served for this question? Look for it by name in the context call.
   1. No. Written, not served. Fix retrieval: a term link, alternate labels, ranking.
   2. Yes. Go to 5.
5. Was it used?
   1. No. Served, ignored. Make it a rule the agent must follow, or make the SQL a metric.
   2. Yes, and still wrong on every run. The gap is in the data: the state the answer needs does not exist, or the grain is wrong. Take it to the platform team.

A miss on some runs and not others means the agent is guessing. Ask the question several times and compare the SQL. Where the runs split, a decision is missing.

Make one change per miss, record it, and rerun the whole set to see what else moved.

Before the first round, run the unchanged context two or three times to measure the spread. Work in rounds: a small batch of changes, then a full rerun. When two rounds in a row move the score no more than that spread, and no predicted fix lands, stop and take the gap to the sponsor. Cap Phase 3 at five rounds.
::::

:::: {.card #c7 title="Which lane?"}
::: {.diagram #lane-tree}
Ask it of each kind of question in the brief, not of every question one by one.
:::

Walk this at the kickoff, in about 30 minutes. It sets how the agent answers users. Every golden-set question is graded the same way, against one bar. Why-questions wait until the numbers under them are right.

1. If this answer is wrong and nobody notices, where does it land?
   1. In a board pack, a finance close or a published KPI. The question is governed.
      1. The answer comes from a metric, whose SQL runs as served.
      2. If no metric covers it, the agent says so. No metric, no answer.
   2. In a decision about where to look next. The question is exploratory.
      1. The agent writes the SQL, grounded in trusted past queries.
      2. Every answer shows its SQL and its sources.
2. Later, in production: do two people publish different numbers for an exploratory question?
   1. Yes. It has become governed. Resolve the conflict, write the metric, move it.
   2. No. Leave it where it is.

In the running example, open pipeline with the top 100 customers is governed: it lands in the board pack. Slipped deals are exploratory: they tell a sales leader where to look.
::::

:::: {.card #c8 title="Is an ontology worth it?"}
::: {.diagram #ontology-tree}
Three stop conditions, then one precondition.
:::

No benchmark covers why-questions yet. Treat this tree as judgment.

1. Has the agent passed the launch gate, at or above the bar on every run?
   1. No. Not yet. Go back to the hill climb. A number that changes between runs has nothing to explain.
   2. Yes. Go to 2.
2. Does the domain live in one system, with one schema and one set of keys?
   1. Yes. Rules carry the why. Write the business processes as rules, such as "a deal re-signed on new terms goes back to the first stage", and stop.
   2. No. Go to 3.
3. Is there an entity to link across systems, or a history of changes to reason over?
   1. No. Not worth it yet. Metrics carry most of a why-answer; the ontology helps where it links systems or reasons over history.
   2. Yes. Go to 4.
4. Will a team record what changes in the business, with dates?
   1. No. Start that record first. Without dated changes the agent has no cause to test.
   2. Yes. Build it.

To build it:

1. Seal five to ten why-questions first, each with a written list of the findings you expect.
2. Import what exists: the glossary for entities and vocabulary, the BI semantic model for bindings.
3. Cut it to what those questions touch. The running example needed five entities. Its answer turned on two of their relationships.
4. Bind each entity to its tables and metrics, and check each tie runs.
5. Get the relationships the answers turn on approved.
6. Agree which team records each kind of dated change, such as territories or pricing.
7. Serve it for why-questions only. Rerun the what-question regression set on every release.

The record of what changed is the part that decays. In the running example, the one why-answer that fell short traced to a comp-plan change nobody had written down.
::::

:::: {.card #c9 title="What to do when things stall"}
Six stalls and what you do. Unless a stall says otherwise, the sponsor decides it at the next readout.

1. The domain owner disappears. Conflicts wait unresolved past a weekly session. Let provenance settle what it can, then raise the rest with the sponsor. Ask for the hours back, or a deputy who can decide. The context engineer never decides a definition.
2. Access is blocked. A test fails or a request stalls. Log it that day with a date. In Phase 0 the clock does not start. Mid-phase, work what needs no access and take the blocker to the next readout.
3. The sponsor changes the bar. Record the new bar and its date. Score the last run against both bars. Leave the golden set alone. Agree in writing what the launch gate now tests.
4. You are asked to host the agent for the company. Decline. The harness stays with the company that runs it. Help the company's agent builder stand up the minimum harness in its own environment.
5. Scope creeps into a second domain. Log the new questions in the domain-two plan. They go to domain two's golden set, never this one.
6. Security review stretches Phase 0. Where vendor review applies, Phase 0 can take months. Hand out the access list on day one, walk security through what leaves the building, and keep the gates. Phase 1 starts when the checklist is met. The security lead decides with the sponsor.

Whatever the stall, the clock does not start early and the bar does not move quietly.
::::

:::: {.card #c10 title="What the sponsor sees at each gate"}
One decision per gate. Hold means the next phase waits.

| Gate | You see | You decide | Go when | Hold when |
|---|---|---|---|---|
| End of Phase 0 | the brief, with the bar; the access tests | start the clock | the brief agreed; every access item proved | the brief open, or any item untested |
| End of Phase 1 | 20 or more sealed questions; the baseline score; the decision guessed on each miss | start the metrics work | every item verified against its source | a dispute open or an item unverified |
| End of Phase 2 | the metrics scored on the same set; the change over baseline; conflicts resolved and open | start the hill climb | every served metric checked, owned and versioned | a disputed or unowned metric is served |
| End of Phase 3 | the score after each round of fixes; what broke and what was fixed; the new questions added for the launch test | move to the launch gate | the new questions sealed; nothing that passed has broken | new questions unsealed, or a break unfixed |
| Launch gate, Phase 4 | the whole set, each question run several times, against the bar; the random pass audit; refusals | go, no-go, or go with conditions | at or above the bar on every run; nothing that passed has broken; audit done; out-of-scope questions refused; the first pass your team runs alone booked, within two weeks | below the bar: hold back the failing kind of question by name, move it to the exploratory lane with the sponsor's agreement, or run one more round |

At every gate from Phase 1 on, the eval owner re-grades five passing items by hand, and the score is reported after any correction.

At the launch gate, also check how the governed lane fails. It should refuse questions it has no metric for, and it should never bind a question to the wrong metric.

Expect a low baseline. It prices the decisions your schema leaves out.

A no-go names each gap and its fix. Go with conditions names each condition and its date.
::::

:::: {.card #c11 title="What you need before you start"}
Two lists: the access, and the people. Request everything on day one. An access item is done when its test passes.

Access:

- Read-only warehouse access for the domain's tables (required). Test: a query runs under it.
- Query history for the domain (required). Test: the export has rows and a date range.
- BI reports and semantic models: required if you have them. Test: the export opens.
- Trace export from your harness (required): the context served, every SQL statement, the answer. Test: one trace read end to end. Start this first; it is the item that arrives last.
- Where users will ask, named: the chat surface or tool your users will ask in.

People, on your side:

- An exec sponsor who sets the bar and decides at each gate.
- A domain owner with 2-3 hours a week, and a co-owner if another team owns part of a definition.
- An eval owner and two graders who know the domain.
- An agent builder.
- A platform owner and a security lead, mostly in Phase 0.

People who run the engagement, from a partner or your own team:

- A context engineer (in-house: an analytics engineer), dedicated from Phase 1 to Phase 4.
- A delivery lead (in-house: your program lead), who runs every session and gate.
::::

:::: {.card #c12 title="Is it ready to launch?"}
The launch gate, as a checklist. The sponsor signs when every line holds.

The golden set:

- New questions drafted during Phase 3, held out of the climb and sealed without the context engineer seeing them. They are first scored here, so the launch score is not one anyone tuned against.
- Every question run several times. An answer counts only if it is right on every run.
- The random pass audit done: five passing items re-graded by hand against their source.

The results:

- The golden set at or above the bar in the brief, on every run.
- Everything that passed at the last gate still passes.
- Out-of-scope questions refused, with no number. No question bound to the wrong metric.
- Any kind of question that can't pass is named and held back, or moved to the exploratory lane with the sponsor's agreement, with a date.

The context:

- Every served metric has an owner and a version. Every served item has a record of why it was approved.
- No open conflict is served. Each waits in the backlog with a date.

Launch day:

- The agent asks for context before any SQL. Confirmed in the traces.
- Governed questions run the metric's SQL as served.
- Governed answers run under a fixed service identity.

Running it:

- Production traces reach your log store, per call.
- The full golden set reruns on every context, harness or model change, and the regression set on every schema change, on staging first.
- The previous version can be restored in one step.
- The first run your team does alone is on the calendar, within two weeks.

Decision: go, no-go, or go with conditions. Each condition has a date. Never lower the bar to fit the score.

| Exec sponsor | Decision | Date |
|---|---|---|
| | | |
::::

:::: {.card #c13 title="Replies for the skeptic"}
What a data-platform skeptic asks in the room, and a reply that holds up.

| Question | Straight answer |
|---|---|
| "We already have a semantic layer." | Good. Bring it in as a source. Its measures and filters become candidate metrics alongside past SQL. Serve the SQL each measure produces, because worked SQL beat declarative definitions in our tests. |
| "A better model will fix this." | Pick a model that finishes its tasks, then put the effort into context. On our questions, context moved both models we ran both ways by 26 points or more <!-- E01 E02 -->, and switching models moved the bare-schema score about 10. |
| "Is this just your benchmark?" | It is one warehouse, so your numbers will differ. The direction matches published work: worked SQL examples beat schema alone. Your Phase 1 baseline tells you where you start. |
| "Isn't this few-shot retrieval?" | Largely, yes. Past SQL is the biggest single step, and that is the field's standard result. We add two things on top: a record of what didn't help, such as a join graph, and metrics, which did. |
| "Can't we just write better descriptions?" | Write them, but don't expect much. The same metric served as SQL beat the same metric served as prose. If a fact can be written as something that runs, write it that way. |
| "Curation won't scale to 10,000 tables." | You never curate 10,000 tables; you work one domain at a time. The metrics agent drafts candidates, provenance settles most conflicts, and whoever owns that number decides the rest. |
| "What if our analysts' SQL is wrong?" | Then a generated metric inherits the error. That is why every candidate is checked against the warehouse and approved by an owner before it serves. Where analysts disagree, you have found a decision your business never wrote down. |
| "How long does this take?" | Phase 0 first, which runs longer where vendor and privacy reviews apply. Then four build phases, often a week each. The gates hold even when the calendar stretches. |
| "Who keeps it current?" | Your team. The full golden set reruns on every context, harness or model change, and the regression set on every schema change, on staging first. |
| "Who pays for your people's time?" | You do, and it is the largest cost. When the domain owner can spare only minutes a week, the engagement stalls. |
| "Our warehouse has row-level security." | Governed answers run under a fixed service identity, so a board number is the same for every asker. Exploratory queries run as the asker. |
| "We'd be locked in." | What stays behind is plain files: metric specs, the golden set, the decisions log. Any store that can hold and serve them will do. |
| "Will you run the agent for us?" | No. The harness is yours: your builder, your model, your surface, your logs. Context is served to it. |
::::

:::: {.card #c14 title="Deliver as a partner"}
A partner firm runs the same method and the same gates. These boundaries hold whatever platform the company runs.

1. Request access through the company's platform owner. Work under a read-only identity the company issues. Hold no credentials of your own.
2. The company builds and runs the harness. Help their builder stand it up. Never host it.
3. If a platform vendor is involved, the company names your contact there at the kickoff.
4. The success document carries scope and success criteria. Commercials stay in your contract.
5. Anything you pass to a vendor goes through the company's platform owner, anonymised.
6. Build on the company's shared context store. Nobody can take over a script or notebook that only you can run.
7. Within a week of launch, send the platform owner a short, anonymised pattern write-up: what moved the score, and which fixes the next engagement will need, sorted into keep or throw away.

You never decide a definition and never grade an answer. Those belong to the domain owner and the eval owner.
::::
