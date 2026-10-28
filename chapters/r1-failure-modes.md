# R1. Failure modes {#r1}

> [!RULE]
> Name the failure before you fix it.

This page lists what goes wrong by the symptom you see, with the smallest fix for each. Use it in two places. In Phase 3, walk a miss down the card [Why did this miss?](#c6), then find its symptom here and record the fix in the [iteration ledger](#r2-8). At the kickoff, seed the [risk log](#r2-18) from the engagement rows and review it at every readout.

Every row names its branch on that card:

- **never written**: the decision exists nowhere in the context, or sits in the wrong place.
- **written, not served**: it is in the context and did not arrive for this question, or arrived crowded out or cut short.
- **served, ignored**: it arrived and the agent took another path.
- **key wrong**: the fault is on the measuring side: the golden set, the grader, or reading run-to-run variation as a real change.
- **budget**: the fault is in the harness. It ran out of steps, errored, or cannot export what the loop needs.

For an engagement row, the branch is the kind of miss the failure first shows in the traces.

The Evidence column says **measured** when a benchmark comparison backs the row, and **diagnosis** when the row comes from reading traces or from engagements, with no measured comparison.

## Agent failures {#r1-agent}

| Symptom | Cause | Fix | Branch | Evidence | Phase |
|---|---|---|---|---|---|
| A plausible number from clean SQL, and finance says it is wrong | A business decision, such as which stages count or which accounts are out, is written nowhere | Write it into a metric; let provenance or the owner settle it | never written | measured | Phase 2 |
| Different numbers for the same question on different runs | A missing decision, made afresh on each run | Ask the question several times and compare the SQL; send each split to the conflict list | never written | measured | Phase 3 |
| The agent silently picks one of several definitions in use | A conflict nobody resolved | Flag the conflict instead of answering; resolve it by provenance, then the owner | never written | measured | Phase 2 |
| A metric returns a total above the key, and its SQL looks clean | The metric encoded one team's definition where the question has two owners (top 100 by deal count, not ARR) | Raise the conflict from the raw trace; both owners resolve it; version the metric | never written | diagnosis | Phase 3 |
| A house rule is served as an instruction, and a governed answer still breaks it | An instruction never reaches SQL the harness runs as served | Write the rule into the metric's population and filters | never written | diagnosis | Phase 3 |
| Totals are several times too large | Wrong grain: a deal counted once per contract term | State the grain; check that each key appears once when you test the metric against the warehouse | never written | diagnosis | Phase 2 |
| Multi-table questions fail with a join graph or semantic views in place | Declared joins say what connects, never how the answer is assembled | Serve a composed statement: a metric or a complete trusted past query | never written | measured | Phase 2 |
| Every piece is served and a multi-step answer still fails | The state it needs does not exist in the warehouse, such as "created and still open" | Pre-assemble it as a metric, or build the state in the warehouse; hold that kind of question back until then | never written | measured | Phase 3 |
| Filters, joins and metric names are all in context, and the answer is still wrong | The parts were served as separate hints | Serve whole decisions: population, grain, time rule and filters in one statement | never written | diagnosis | Phase 2 |
| A large documentation effort barely moves the score | Documentation describes tables and carries no decisions | Keep it as the floor; spend the next hour on metrics | never written | measured | Phase 2 |
| Generation yields hundreds of trivial "metrics" | Profiling and scratch queries promoted to candidates | Filter candidates by provenance: distinct analysts, runs, recency | never written | diagnosis | Phase 2 |
| Right on launch day, drifting within weeks | Definitions change and nothing feeds back | Feed traces and user corrections to the conflict list; rerun the golden set on every change | never written | diagnosis | In production |
| Loading the whole context into the prompt lowers accuracy and raises cost | Dumping instead of retrieving | Retrieve per question from the context layer | written, not served | measured | Phase 2 |
| A written term or trusted query is never retrieved | The question's word ("slipped") appears in neither the query's text nor its title | Give the business term its alternate labels and link it to the query | written, not served | measured | Phase 3 |
| Glossary definitions on columns add context and no accuracy | Business terms served as column prose | Use business terms to route question words to the right metric or query | written, not served | measured | Phase 2 |
| The agent copies the start of a served query and improvises the rest | SQL cut short to save tokens | Serve complete statements, literals kept | written, not served | measured | Phase 2 |
| A second retriever on top of metrics adds nothing | Near-variants compete with the metric | Rank metrics above retrieved queries; never blend the two | written, not served | measured | Phase 2 |
| Wide dashboard objects cost questions | They crowd the decisive metric out | Keep metrics narrow and atomic; cap what is served per question | written, not served | measured | Phase 2 |
| Search recall improves and accuracy does not | Recall counts candidates found; accuracy needs the decisive one served | Measure answers against the golden set, never retrieval alone | written, not served | measured | Phase 3 |
| Column profiles bloat the prompt with no gain | Profiling describes data shape and carries no decisions | Look up values only when a question names one | written, not served | measured | Phase 2 |
| Generic methodology or instruction packs add cost and no accuracy | Generic prose competes with domain rules | Serve small, domain-specific rules only | written, not served | measured | Phase 2 |
| Embedding search misses the query that shares the question's field names | Embeddings blur identifiers and literals | Rank on field names and literals first, provenance as the tie-break | written, not served | measured | Phase 2 |
| The agent answers from the wrong table | Table choice fails before any SQL is written | Serve one authoritative source per concept; put metrics on it | written, not served | measured | Phase 2 |
| A schema change silently breaks trusted queries | Nothing re-checks them when a table changes | Rerun the regression set and re-test against the warehouse on every schema change; pull what fails | written, not served | diagnosis | In production |
| An ontology makes number questions slower and worse | It mirrored the schema, and it was used to write SQL when its job is to explain causes | Metrics for what, ontology for why; bind entities to metrics | written, not served | measured | Why-questions |
| The metric was served and the agent ignored it | Context that is only placed in front of the agent gets skipped | Make it a rule the agent must follow, or run the metric's SQL as served | served, ignored | measured | Phase 3 |
| The metric is in context and still assembled wrong | The metric was served as prose | Serve name and SQL | served, ignored | measured | Phase 2 |
| The agent retyped a served statement and broke it | Long served SQL copied by hand | Fill the declared parameters and run the served statement as stored | served, ignored | diagnosis | Phase 3 |
| The agent found the right value, kept exploring, and answered something else | No rule to stop | A rule the agent follows: a value from a query that matches the definition is the answer | served, ignored | diagnosis | Phase 3 |
| A governed question returns the wrong number from the right metric | A parameter took a default, such as a calendar quarter for win rate | Make the time parameter required, with no default; check at the launch gate | served, ignored | diagnosis | Phase 3 |
| The governed lane says "no metric" on a question it should answer | No metric covers it, or retrieval missed it | Count wrong refusals next to correct ones at the launch gate; add the metric or fix the term link | written, not served | diagnosis | Phase 4 |
| A house rule served as an instruction breaks a question that passed | The rule caught more than it meant (a partner org the key counts) | Rerun the whole set after every change; scope the rule to the field that defines it | never written | diagnosis | Phase 3 |
| A high score nobody reproduces on a fresh set | Golden-set SQL leaked into the context | Purge by hash; exclude the agent's own queries from history; audit runs for leaks | key wrong | measured | Phase 1 |
| A business term hands the agent the answer | A term matches the expected answer's label | Serve a value term only when the question names that value | key wrong | diagnosis | Phase 1 |
| Answers within tolerance are graded right while the logic is wrong | Grading on data alone | Grade returned data first, then the SQL against the item's decisions | key wrong | diagnosis | Phase 1 |
| A question no change ever fixes, or one the agent gets right on every run and is graded wrong | The key itself is wrong (the grader used the calendar quarter) | Audit the key before tuning; correct and reseal it | key wrong | measured | Phase 3 |
| An item passes on every run and the answer is still wrong | The key is wrong and the agent matched it | At every gate, re-grade five random passes by hand against their source; correct in either direction | key wrong | diagnosis | Phase 4 |
| A governed answer is wrong the same way on every run | A wrong metric is wrong every time, for everyone; repeat runs can't see it | Test and approve every metric before it serves; keep a golden-set item per metric; run the random pass audit | never written | diagnosis | Phase 2 |
| A one-run gain is announced as progress | Single runs vary by several questions | Treat gaps smaller than your run-to-run variation as unresolved; score items right on every run | key wrong | measured | Phase 3 |
| A high overall score hides confident wrong answers on board numbers | Exploratory SQL is right most of the time and wrong the rest | Put exact recurring numbers in the governed lane: metric or no answer | key wrong | measured | Phase 0 |
| Errored runs drag the average down | Harness errors counted as wrong answers | Report errors separately; never average them in | budget | diagnosis | Phase 3 |
| A higher step budget turns refusals into wrong answers | Freed refusals become guesses | Fix the missing context before you touch the budget | budget | measured | Phase 3 |
| An exploration toolkit adds nothing | More discovery keeps the agent sampling instead of committing | Fewer, stronger tools; one context call before any SQL | budget | measured | Phase 0 |
| The harness spends its step budget finding its tools | A deferred-tool pattern in the harness | Load the context tool up front; size the budget to the harness | budget | diagnosis | Phase 0 |

## Engagement failures {#r1-engagement}

These rows come from our field engagements. Each maps to a Phase 0 decision or to a practice in running the engagement.

| Symptom | Cause | Fix | Branch | Evidence | Phase |
|---|---|---|---|---|---|
| The weeks slip; decisions wait for one person | The one person who can settle definitions has minutes a week | Agree their time before Phase 1 starts; let provenance settle what it can | never written | diagnosis | Phase 0 |
| The conflict list grows faster than the owner can resolve it | Every conflict treated as urgent and sent to a person | Let provenance settle the clear cases; bring the owner only the split ones, ranked by use; the rest wait in the backlog | never written | measured | Phase 2 |
| A dispute settled while sealing surfaces weeks later in a trace | The wall between the key and the context hid the conflict along with the value | Send the dispute to the conflict list as well, with no sealed value attached | never written | diagnosis | Phase 1 |
| A pasted list of IDs is set aside and nobody traces it | A set-aside item is not a conflict, so it never reaches the owner | Trace every pasted list to its source before approving the concept it touches | never written | diagnosis | Phase 2 |
| The sponsor asks "why did it drop?" before the agent gets the number right twice | Why-questions pulled forward | Defer why until the numbers are released; put the question in the backlog with a date | never written | diagnosis | Phase 2 |
| Three domains in scope, and none reaches the bar | Going broad | One domain, its problem and its users; domain two starts from what domain one built | never written | diagnosis | Phase 0 |
| A governance steward attends every review and nothing gets decided | Governance stands in for the domain owner | Decisions come from the definition's owner | never written | diagnosis | Phase 0 |
| Every answer must be exact, judged against a dashboard | The use case is a dashboard | Exact recurring numbers go through the governed lane, or stay on the dashboard | never written | diagnosis | Phase 0 |
| The company cannot run a round of fixes without the delivery team | The loop was run for them; the handover was a document | One pass together, one alone, before the delivery team leaves | never written | diagnosis | Phase 4 |
| Two domains own the same word and disagree, and nobody can decide | No one decides across domains | The sponsor names an arbiter before domain two's Phase 0 ends | never written | diagnosis | Phase 4 |
| High pilot accuracy fails the first real user | The test set came from the tuning examples | Build the golden set from real questions, seal it, and add questions the builder never saw before launch | key wrong | diagnosis | Phase 1 |
| The golden set is still being written in Phase 3 | Drafted from scratch | Start from verified dashboards, reports and analyst work; seal at least 20 in Phase 1 | key wrong | diagnosis | Phase 1 |
| Every miss becomes a question for the delivery team | The company's side never took on correctness | The company's graders keep the golden set, and the company settles its own definitions | key wrong | diagnosis | Phase 0 |
| The sponsor rejects a result the team celebrated | The bar was never written down | Set the bar in Phase 0, before any result exists | key wrong | diagnosis | Phase 0 |
| Phase 3 starts with no traces to read | Trace export arrived last | Test one trace end to end, per call, before Phase 1 | budget | diagnosis | Phase 0 |
| The clock starts, then stops for a data-handling review | Security was approached late | Walk security through what leaves the building in Phase 0 | budget | diagnosis | Phase 0 |
| Score changes cannot be traced to any context change | The harness or model changed and the baseline was not rerun | Rerun the golden set on any harness or model change before comparing | budget | diagnosis | Phase 3 |
| The agent is rebuilt after launch for a different surface | The surface was decided late | Choose the agent architecture in Phase 0 | budget | diagnosis | Phase 0 |
| The engagement ships custom code nobody can maintain | Delivery built one-off tooling | Leave metrics, the golden set, the decisions log and the iteration ledger | budget | diagnosis | Phase 4 |
| The company asks the delivery team to run the agent | Harness ownership was never made explicit | Settle it in Phase 0: the harness is the company's | budget | diagnosis | Phase 0 |

## When a miss will not sort cleanly {#r1-instruments}

Sometimes a miss will not sort into one branch of [Why did this miss?](#c6). These checks find where the remaining gap lives. Run the first one before the others, because it needs no golden set.

| Check | How | What it tells you |
|---|---|---|
| Ask it several times | Run the same question with everything fixed and compare the SQL | Where the runs split, two definitions compete; resolve it as a conflict |
| Serve one source at a time | Serve a single kind of context per run | What each kind of context is worth |
| Serve the answer as prose | Give the agent its own procedure in words | If accuracy does not move, the gap was never knowledge; serve SQL or a rule |
| Count the steps | Compare the steps the expected SQL needs with the steps the agent built | Whether the miss is assembly; pre-build it as a metric or a table |

The last three need the golden set to score. The context engineer sees only the verdicts.
