# Templates {#r2}

> [!RULE]
> Copy the template, fill it from your domain, and keep it in version control next to the context it governs.

Every artifact the method produces is here as a file card. Each card opens on a filled example from the running engagement: the sales domain at a large B2B company whose fiscal year ends 30 June, with every eval answer computed at the fiscal year-end snapshot. The second tab is the blank template. Copy either one.

The order follows the engagement, from Phase 0 to the handover. Chapters show short previews and link here.

Conventions:

- All SQL is DuckDB-compatible, so every example runs on a laptop first.
- Placeholders are written `<like this>`.
- A cell that reads "your run" is one only your own run can fill.
- Every count in an example comes from the engagement's golden set. None is a benchmark result. The engagement is a composite, built to show the method.

| Template | When |
|---|---|
| [Engagement success document](#r2-10) | Phase 0 |
| [Kickoff agenda](#r2-11) | Phase 0 |
| [Before-you-start checklist](#r2-1) | Phase 0 |
| [Domain brief](#r2-2) | Phase 0 |
| [Question-harvest sheet](#r2-15) | Phase 1 |
| [Coverage estimate](#r2-16) | Phase 1, optional |
| [Grading rubric](#r2-4) | Phase 1 |
| [Golden-set item](#r2-3) | Phase 1 |
| [Context call and trace record](#r2-22) | Phase 0 and Phase 1, fixed from the baseline |
| [Trusted past query](#r2-14) | Phase 2 |
| [Metric spec](#r2-5) | Phase 2 |
| [Conflict record](#r2-6) | Phases 2-3 |
| [Trace review sheet](#r2-7) | Phase 3 |
| [Iteration ledger](#r2-8) | Phase 3, then every round |
| [Sponsor readout](#r2-12) | each phase |
| [Risk log](#r2-18) | from the kickoff |
| [Release note](#r2-9) | Phase 4 |
| [Handover checklist](#r2-19) | Phase 4 |
| [Pattern write-up](#r2-20) | Phase 4 |
| [Field postmortem](#r2-21) | Phase 4, or on a trigger |
| [Ontology fragment and business changes](#r2-13) | after release |

## Phase 0 {#r2-phase-0}

::: {.template #r2-10 file="success-document.md" title="Engagement success document"}
What will be delivered and how both sides judge it together. It ends in the sponsor's Phase 4 go or no-go.

```markdown
# Engagement success document: Sales (pipeline and win rate)

## 1. Purpose
One pipeline number for the top 100 customers, the same every time it is asked, that matches finance.
Diagnostic answers on slippage, stage aging and win rate, in the chat tool sales leadership already uses.

## 2. Shared understanding
No agent exists yet. Sales ops, RevOps and finance each publish pipeline numbers, and two of them
reached the board on adjacent slides last quarter. Each disagreement costs an analyst a day to reconcile.

## 3. Scope
- Domain: sales pipeline. Data: CRM and billing, query history, the board pack and dashboards
- Golden set: at least 20 sealed in Phase 1; more added before launch that the builders never saw; sealed by the eval owner and two graders
- Bar: 9 in 10 golden-set questions right, on every run
- Agent architecture: the chat tool as surface; a custom harness built by the agent builder; the model chosen in Phase 0
- Out of scope: bookings forecast, commissions, marketing attribution; why-questions until the numbers are released

## 4. Success criteria
The CRO decides at each gate.

| Gate | Deliverable | How we judge it together | Outcome |
|---|---|---|---|
| Phase 1 | 20 sealed; baseline | the grading rubric; one run per question | pass: baseline 7 of 20 |
| Phase 2 | metrics, scored | every metric witnessed; conflicts resolved | pass: 14 of 20 |
| Phase 3 | fixes from traces; new questions added for the launch test | nothing that passed has broken | pass: 18 of 20 |
| Phase 4 | launch gate on the whole set | at or above 9 in 10 on every run; random pass audit done; out-of-scope refused | go with conditions |

## 5. Roles and open questions
The people table from the before-you-start checklist. Open questions, each with a due date.

## 6. Go / no-go (Phase 4)
Decision: GO WITH CONDITIONS
Conditions: the "created and still open" state built, due two weeks after launch ·
the open conflicts on released questions resolved, due at the first release ·
domain two chosen, due at handover
Signed: CRO
```

```markdown
# Engagement success document: <domain> · signed <date>

## 1. Purpose
<one paragraph: the business problem and why this domain first>

## 2. Shared understanding
<what both sides agree is true today: data, current agent if any, known gaps>

## 3. Scope
- Domain; data in scope; out of scope: <...>
- Golden set: at least 20 sealed in Phase 1; more added before launch that the builders never saw; sealed by <eval owner>
- Bar: <one pass rate for the whole golden set>, on every run
- Agent architecture: <surface>, <harness>, <model>

## 4. Success criteria
<exec sponsor> decides at each gate.

| Gate | Deliverable | How we judge it together | Outcome |
|---|---|---|---|
| Phase 1 | golden set sealed; baseline | <rubric; one run per question> | <your run> |
| Phase 2 | metrics, scored | <metrics witnessed; conflicts resolved> | <your run> |
| Phase 3 | fixes from traces; new questions added for the launch test | <nothing that passed has broken> | <your run> |
| Phase 4 | launch gate on the whole set | <at or above the bar on every run; random pass audit; out-of-scope refused> | <your run> |

## 5. Roles and open questions
<the people table from the before-you-start checklist; open questions, each with a due date>

## 6. Go / no-go (Phase 4)
Decision: GO | NO-GO | GO WITH CONDITIONS
Conditions: <action, due>
Signed: <exec sponsor>
```
:::

::: {.template #r2-11 file="kickoff-agenda.md" title="Kickoff agenda"}
The 90 minutes that end in an agreed checklist. Teach before you ask: show what goes wrong on the company's own data, then walk the checklist.

```markdown
# Kickoff: Sales · 90 min · run by the delivery lead
Room: CRO, RevOps lead, FP&A partner, eval owner, agent builder, platform owner, security lead, delivery lead, context engineer

| Time | Item | Output |
|---|---|---|
| 0:00 | Why pilots stall between the demo and the tenth question | a shared diagnosis |
| 0:10 | The decisions hidden in "What's our Q3 pipeline?", on the company's data | two unwritten rules: some early stages never count; internal and test accounts are out |
| 0:25 | Which domain first | sales pipeline, over finance close and marketing attribution |
| 0:35 | The bar, then how the agent answers | the bar: 9 in 10 golden-set questions right on every run; board numbers governed; slippage, creation and aging exploratory; why deferred |
| 0:50 | Who settles which definitions | RevOps lead: deals, stages, amounts · FP&A partner: who the top 100 customers are |
| 1:00 | Walk the before-you-start checklist | roles filled; architecture chosen |
| 1:15 | Access and what leaves the building | security walks the data-flow diagram; the per-call trace export started |
| 1:25 | Next steps | brief agreed; the clock starts when every access test passes |
```

```markdown
# Kickoff: <domain> · 90 min · run by <delivery lead>
Room: <exec sponsor>, <domain owner(s)>, <eval owner>, <agent builder>, <platform owner>, <security lead>, <context engineer>
Pre-read: the one-page method

| Time | Item | Output |
|---|---|---|
| 0:00 | Why pilots stall between the demo and the tenth question | shared diagnosis |
| 0:10 | One question, the decisions it hides, on your own data | two of your own unwritten rules |
| 0:25 | Which domain first | the domain, and why |
| 0:35 | The bar, then how the agent answers | one pass rate for the whole golden set; which kinds of question are governed |
| 0:50 | Who settles which definitions | the domain owner, and a co-owner if a definition crosses teams |
| 1:00 | Walk the before-you-start checklist | status per item; a date for each gap |
| 1:15 | Access and what leaves the building | security's next step and date |
| 1:25 | Next steps | checklist met, or the date it will be |
```
:::

::: {.template #r2-1 file="before-you-start.md" title="Before-you-start checklist"}
The access and the people that must be in place before Phase 1. Each access item is done when its test passes. The clock starts when every line is met.

```markdown
# Before you start: Sales (pipeline and win rate) · met at the end of Phase 0 · signed by the CRO

## Access
| Item | Test | Status |
|---|---|---|
| Read-only warehouse access for CRM and billing (required) | a query runs under it | done, first week of Phase 0 |
| Query history for sales (required) | the export has rows and a date range | done, first week |
| BI reports and semantic models: board pack, RevOps dashboards, semantic model (required if you have them) | the export opens | done, second week |
| Trace export from the harness (required): context served, every SQL statement, the answer | one trace read end to end | done, last day of Phase 0: the chat tool exported a nightly summary only, so a per-call export was built |
| Where users will ask, named | recorded in the brief | the chat tool sales leadership already uses |

## People
| Role | Time |
|---|---|
| Exec sponsor: the CRO | kickoff, a 30-minute readout in each phase, gates |
| Domain owner: the RevOps lead | 2-3 h/week |
| Co-owner: the FP&A partner | about 1 h/week in Phases 2-3 |
| Eval owner, with a RevOps analyst and an FP&A analyst as graders | 6-8 h in Phase 1, then about 2 h/week |
| Agent builder | about 20 h/week to the baseline, then 4-6 |
| Platform owner, security lead | Phase 0, then on call |
| Context engineer, delivery lead: from the partner; in-house, an analytics engineer and your program lead | dedicated; every session |
```

```markdown
# Before you start: <domain> · met <date> · signed by <exec sponsor>

## Access
| Item | Test | Status |
|---|---|---|
| Read-only warehouse access for the domain's tables (required) | a query runs under it | <date> |
| Query history for the domain (required) | the export has rows and a date range | <date> |
| BI reports and semantic models (required if you have them) | the export opens | <date> |
| Trace export from your harness (required): context served, every SQL statement, the answer | one trace read end to end | <date> |
| Where users will ask, named | recorded in the brief | <surface> |

## People
| Role | Time |
|---|---|
| Exec sponsor | <...> |
| Domain owner, co-owner | <h/week> |
| Eval owner and graders | <h/week> |
| Agent builder | <h/week> |
| Platform owner, security lead | <...> |
| Context engineer, delivery lead | <...> |
```
:::

::: {.template #r2-2 file="domain-brief.yaml" title="Domain brief"}
One page that fixes the domain, its users, its questions, the one bar for the golden set, and which lane the agent answers each kind of question in.

```yaml
# Domain brief: Sales · v1 · agreed at the kickoff
domain:       sales pipeline
fiscal_year:  ends 30 June; every eval answer at the fiscal year-end snapshot
users:        CRO staff, sales leaders, RevOps analysts, FP&A partners, asking in the chat tool they already use
problem:      pipeline numbers disagree with finance; each disagreement costs an analyst a day to reconcile
owners:       RevOps lead (deals, stages, amounts) · FP&A partner (who the top 100 customers are)
graders:      a RevOps analyst and an FP&A analyst

bar:          9 in 10 golden-set questions right, on every run   # one bar for the whole set, set by the sponsor now

governed:     # a metric or no answer
  - open pipeline, any cut
  - win rate, any cut
  - closed-won ARR, any cut
exploratory:  # the agent writes the SQL and shows it, with its sources
  - slippage
  - pipeline creation
  - stage aging
  - rep and territory cuts
deferred:     why-questions, until the numbers are released
out_of_scope: bookings forecast, commissions, marketing attribution

data:         CRM opportunities, snapshots, accounts, stage and close-date history, reps, territories; billing terms
sources:      query history, human authors; the board pack; the RevOps dashboards and semantic model
import:       the RevOps semantic model; no earlier agent, so no instructions
architecture: surface the chat tool · harness custom, built by the agent builder · model the production model, named with its version
```

```yaml
# Domain brief: <domain> · v<n> · agreed <date>
domain:       <domain>
fiscal_year:  <when it ends>; every eval answer at <snapshot>
users:        <roles who will ask, and where they ask today>
problem:      <what goes wrong today, for whom, at what cost>
owners:       <domain owner (what they decide)> · <co-owner, if a definition crosses teams>
graders:      <two people who know the domain>

bar:          <one pass rate for the whole golden set>, on every run   # written now, before any result exists

governed:     # a metric or no answer
  - <kind of question>
exploratory:  # the agent writes the SQL and shows it, with its sources
  - <kind of question>
deferred:     <kinds of question, and why>
out_of_scope: <questions, data, surfaces>

data:         <schemas and tables>
sources:      <query-history window, human authors>; <BI reports and semantic models>
import:       <semantic layer, saved queries or instructions you already have, or none>
architecture: surface <...> · harness <platform-native or custom> · model <the production model, with its version>
```
:::

## Phase 1: the golden set {#r2-week-1}

::: {.template #r2-15 file="question-harvest.md" title="Question-harvest sheet"}
The candidate list the golden set is drawn from, each question traced to where the business already asks it. Collect two or three candidates for every question you will seal.

```markdown
# Question harvest: Sales, Phase 1 · graders: a RevOps analyst, an FP&A analyst · 62 candidates
Sources: 23 from the board pack, 19 from RevOps dashboards, 14 from tickets, 6 from the CRO. Five rows shown.

| # | Question, as a user asks it | Source | Asked by, how often | Verified answer at | Keep? |
|---|---|---|---|---|---|
| 3 | How much open pipeline do we have with our top 100 customers? | board pack, top-accounts page; RevOps "Top accounts" tile | CRO, weekly | board pack. DISPUTED: the tile ranks a different 100 | yes; the FP&A partner picks the source before sealing |
| 7 | How many of the open deals with our top 100 customers slipped from last quarter? | a RevOps analyst's saved query, "deals pushed past quarter end, by rep" | sales leaders, each quarter end | the analyst's query on the snapshot | yes |
| 8 | What is our win rate with the top 100 customers, against everyone else? | RevOps win-rate dashboard | CRO staff, monthly | dashboard; denominator to confirm | yes |
| 19 | Which reps have the most pipeline stuck at one stage for over 60 days? | ticket from a regional sales VP | sales managers, ad hoc | graders compute it from stage history | yes |
| 41 | Why did pipeline with these customers drop in EMEA this quarter? | CRO, year-end review | CRO, once | none | no: deferred until the numbers are released |
```

```markdown
# Question harvest: <domain>, Phase 1 · graders: <names> · <n> candidates
Sources: <n> from <source>, <n> from <source>, ...

| # | Question, as a user asks it | Source | Asked by, how often | Verified answer at | Keep? |
|---|---|---|---|---|---|
| 1 | <question> | <tile, report, ticket, saved query> | <role>, <how often> | <where, or none> | <yes / no: why> |

Candidates drafted by a tool are marked "drafted"; graders rewrite them in the user's words.
A disputed source goes to the definition's owner before sealing, and to the conflict list with no value attached.
```
:::

::: {.template #r2-16 file="coverage-estimate.md" title="Coverage estimate"}
Optional. A first signal of your ceiling: how many harvested questions a trusted past query or an existing metric already answers. The eval owner runs it, so no answer passes to the context engineer. The engagement did not record its counts, so the example shows the shape with "your run" in the cells.

```markdown
# Coverage estimate: Sales, Phase 1
Inputs: 62 harvested questions; query history (a query counts with 2 or more distinct analysts and 5 or more runs)

| Candidates | With a trusted past query | With an existing metric | Neither | Covered |
|---|---|---|---|---|
| 62 | your run | your run | your run | your run |

Reading: <go | hold | re-scope>. Uncovered topics go to the context engineer as topic names only.
```

```markdown
# Coverage estimate: <domain>, Phase 1 · <date>
Inputs: harvested questions; <query-history window; a query counts with at least <n> analysts and <n> runs>

| Candidates | With a trusted past query | With an existing metric | Neither | Covered |
|---|---|---|---|---|
| <n> | <n> | <n> | <n> | <%> |

Reading: <go | hold: mostly uncovered | re-scope>
Any query later used as expected SQL is purged from the context by hash.
```
:::

::: {.template #r2-4 file="grading-rubric.md" title="Grading rubric"}
How every answer is judged, agreed before the first run so no score is argued after it.

```markdown
# Grading rubric: Sales, v1 · agreed in Phase 1, before the first run

## 1. Returned data first
- Counts exact. Amounts within 0.5%. A fraction equals its percentage.
- The pipeline question expects 91 accounts, 340 deals, $412M. A split by region that sums to the total
  (NA $198M, EMEA $161M, APAC $53M) is a valid alternative.

## 2. Then the SQL
- A value inside tolerance reached by the wrong logic is wrong.
- Every question is graded the same way, by code against the sealed answer.

## 3. Verdicts
- The pipeline question at $1.31B (top 100 by deal count, every stage, contract value, each term): wrong.
- "Two definitions of top 100 are in use; which one?" before the conflict is resolved: a correct refusal.
- A run that failed is an error, reported apart, never counted as wrong.

## 4. Runs and judges
- Baseline and Phase 2 score: one run per question. From the first round in Phase 3: three runs. Launch gate: five.
- Score = questions right on every run, against the bar in the brief: 9 in 10.
- An LLM judge checks answer shape only (period, filter and unit stated), after calibration on 20 items.

## 5. Not measured
Why-questions, follow-up turns, entity lookups.
```

```markdown
# Grading rubric: <domain>, v<n> · agreed <date>, before the first run

## 1. Returned data first
- Compare returned values with `expected`; accept any `valid_alternatives` entry.
- Counts: <exact>. Amounts: <tolerance>. A fraction equals its percentage.

## 2. Then the SQL
- Check the SQL against the decisions the question hides.
- A value inside tolerance reached by the wrong logic is wrong.
- Every question is graded the same way, by code against the sealed answer.

## 3. Verdicts
- correct: data within tolerance and the logic holds
- wrong: data outside tolerance, or right data by wrong logic
- refusal: declined, or flagged a conflict. Correct when: <policy>
- error: the run failed; reported separately, never counted as wrong

## 4. Runs and judges
- One run per question until the score passes about 60%; then <3-5> runs; score = right on every run, against the bar in the brief.
- Code checks values first; an LLM judge checks answer shape only, once calibrated on <n> items.

## 5. Not measured
<e.g. why-questions, follow-up turns, entity lookups>
```
:::

::: {.template #r2-3 file="sales-01.yaml" title="Golden-set item"}
One question with its expected answer, the SQL that produced it, and how it is graded. The eval owner and graders draft and seal it. The agent and the context engineer never see it. The first five fields are required; the rest are optional.

```yaml
# required
id:           sales-01
question:     How much open pipeline do we have with our top 100 customers?
source:       finance board pack, top-accounts pipeline page (year-end close)
expected:     {accounts: 91, deals: 340, open_pipeline: 412000000}
expected_sql: |   # a full copy, never a link, so the sealed answer never moves when a metric does
  WITH latest_term AS (
    SELECT account_id, arr, ROW_NUMBER() OVER (PARTITION BY subscription_id ORDER BY start_date DESC) AS rn
    FROM billing.subscription_term WHERE status = 'active' AND start_date <= DATE '2026-06-30'),
  top_accounts AS (
    SELECT account_id FROM latest_term WHERE rn = 1 GROUP BY account_id ORDER BY SUM(arr) DESC LIMIT 100)
  SELECT COUNT(DISTINCT o.account_id) AS accounts, COUNT(*) AS deals, SUM(o.arr) AS open_pipeline
  FROM crm.opportunity_snapshot o
  JOIN top_accounts t ON t.account_id = o.account_id JOIN crm.account a ON a.id = o.account_id
  WHERE o.as_of_date = DATE '2026-06-30' AND o.stage_order >= 2 AND o.type IN ('New Business', 'Upsell')
    AND NOT o.is_closed AND NOT a.is_internal AND NOT a.is_test;

# optional
as_of:              2026-06-30        # the fiscal year-end snapshot
valid_alternatives: ["by region, summing to the total: NA 198M, EMEA 161M, APAC 53M"]
tolerance:          {counts: exact, amounts: within 0.5%}
decisions:          [top 100 by current ARR, some early stages never count, amount is ARR, each deal once]
decoy:              "top 100 by deal count, every stage, contract value, each term -> $1.31B"
sealed_by:          eval owner, with the RevOps and FP&A graders, Phase 1
history:            ["Phase 1: graders disputed the source (dashboard tile vs board pack); the FP&A partner chose the board pack"]
```

```yaml
# required
id:           <domain>-<nn>
question:     <exactly as a user would ask it>
source:       <dashboard, report or analyst work the answer was verified against>
expected:     {<column>: <value>, ...}
expected_sql: |
  <DuckDB SQL that returns expected; a full copy, never a link>

# optional
as_of:              <YYYY-MM-DD>
valid_alternatives: []                 # each with a reason
tolerance:          {counts: exact, amounts: <your setting>}
decisions:          [<the choices the question hides>]
decoy:              <the wrong answer you get when the hidden choices are guessed the obvious way>
sealed_by:          <eval owner, with the graders, when>
history:            []                 # every key correction and source dispute: when, who, why
```
:::

::: {.template #r2-22 file="context-call-and-trace.json" title="Context call and trace record"}
What the harness sends on its one context call, what comes back, and the per-call trace record it exports. Fix this shape before the baseline and keep it, so the baseline and the later scores compare. At baseline the response carries the schema only. The example is the pipeline question after the top-100 conflict was resolved.

```json
{
  "request": {
    "question": "How much open pipeline do we have with our top 100 customers?",
    "domain": "sales",
    "identity": {"user": "a member of the CRO staff", "passthrough": true}
  },
  "response": {
    "call_id": "cc-phase3-sales-01-r1",
    "context_version": "v1.3",
    "lane": "governed",
    "metrics": [
      {
        "name": "open_pipeline_top_accounts",
        "version": 3,
        "owners": ["RevOps lead", "FP&A partner"],
        "provenance": "approved; witnessed in Phase 3; top-100 conflict resolved by both owners",
        "parameters": {"as_of": {"type": "date", "required": true}, "n": {"type": "integer", "default": 100}},
        "dimensions": ["region", "segment", "rep", "stage"],
        "sql": "-- the metric's sql field, complete, as in the metric spec"
      }
    ],
    "trusted_queries": [],
    "rules": [
      {"name": "quarter-means-fiscal", "version": 1, "instruction": "Quarters are fiscal; the fiscal year ends 30 June."}
    ],
    "business_terms": [{"term": "Top accounts", "version": 2, "points_to": "open_pipeline_top_accounts v3"}]
  },
  "trace_record": {
    "trace_id": "sales-01 · Phase 3, round 4 · run 1 of 3",
    "question_id": "sales-01",
    "model": "the chosen model and version",
    "served": [
      {"id": "open_pipeline_top_accounts", "version": 3},
      {"id": "quarter-means-fiscal", "version": 1},
      {"id": "Top accounts", "version": 2}
    ],
    "tool_calls": [
      {"turn": 2, "tool": "context_call", "args": {"domain": "sales"}, "result": "cc-phase3-sales-01-r1", "ok": true},
      {"turn": 3, "tool": "execute_metric", "args": {"metric": "open_pipeline_top_accounts", "version": 3, "as_of": "2026-06-30", "n": 100},
       "identity": "the fixed service identity", "sql": "-- the bound statement, exactly as run", "rows": 1, "ok": true}
    ],
    "outcome": {"kind": "answer", "text": "Open pipeline with our top 100 customers: $412M, 340 deals on 91 accounts."},
    "steps": 4,
    "sql_statements": 1,
    "seconds": "your run",
    "tokens": "your run"
  }
}
```

```json
{
  "request": {
    "question": "<the user's words, unedited>",
    "domain": "<domain>",
    "identity": {"user": "<the asking user's id>", "passthrough": true}
  },
  "response": {
    "call_id": "<unique per call>",
    "context_version": "<v x.y>",
    "lane": "<governed | exploratory>",
    "metrics": [
      {"name": "<metric>", "version": "<int>", "owners": ["<role>"], "provenance": "<status, owners, how it was settled>",
       "parameters": {"<name>": {"type": "<type>", "required": "<true | false>", "default": "<value, or omit>"}},
       "dimensions": ["<name>"], "sql": "<the complete sql field>"}
    ],
    "trusted_queries": [
      {"id": "<query id>", "version": "<int>", "provenance": "<run by N analysts, M runs, last run <when>; witness OK>", "sql": "<complete statement, literals kept>"}
    ],
    "rules": [{"name": "<rule>", "version": "<int>", "instruction": "<one rule, as an instruction>"}],
    "business_terms": [{"term": "<term>", "version": "<int>", "points_to": "<metric or query, with version>"}]
  },
  "trace_record": {
    "trace_id": "<question id · phase, round · run n of k>",
    "question_id": "<id, or unsealed in production>",
    "model": "<model and version>",
    "served": [{"id": "<item>", "version": "<version>"}],
    "tool_calls": [
      {"turn": "<n>", "tool": "<context_call | run_sql | execute_metric>", "args": {}, "identity": "<user | service identity>",
       "sql": "<every statement, failed ones included>", "rows": "<n>", "ok": "<true | false>", "error": "<message, if any>"}
    ],
    "outcome": {"kind": "<answer | refusal: no metric | conflict flagged>", "text": "<what the user saw>"},
    "steps": "<n>",
    "sql_statements": "<n>",
    "seconds": "<n>",
    "tokens": "<in, out>"
  }
}
```
:::

## Phase 2: metrics {#r2-week-2}


::: {.template #r2-14 file="q-pushed-by-rep.yaml" title="Trusted past query"}
A complete analyst query, kept as a worked example for the exploratory lane. The record carries the provenance that earns it a place and the business terms that let a question find it.

```yaml
id: q-pushed-by-rep
title: Deals pushed past quarter end, by rep
owner: a RevOps analyst
domain: sales
version: 1
provenance:
  distinct_analysts: 9
  runs: 120
  last_run: the final week of the fiscal year
  witness: OK                      # re-run read-only in Phase 2
business_terms:                    # linked in Phase 3; before that "slipped" found nothing
  - {term: Slipped deal, alternate_labels: [pushed, rolled, slid]}
rules: [quarter-means-fiscal]
dialect: duckdb
sql: |
  WITH slipped AS (                -- each deal once, however often it was pushed
    SELECT DISTINCT h.opportunity_id
    FROM crm.close_date_history h
    WHERE h.old_close_date >= DATE '2026-01-01' AND h.old_close_date < DATE '2026-04-01'
      AND h.new_close_date >= DATE '2026-04-01'
      AND h.changed_at >= DATE '2026-01-01' AND h.changed_at < DATE '2026-04-01')
  SELECT r.name AS rep, COUNT(*) AS slipped, SUM(o.arr) AS arr
  FROM slipped s
  JOIN crm.opportunity o ON o.id = s.opportunity_id
  JOIN crm.rep r ON r.id = o.owner_id
  GROUP BY r.name
  ORDER BY slipped DESC;
notes: Fiscal Q3 runs January to March; the fiscal year ends 30 June.
```

```yaml
id: <query id>
title: <what the query answers, in the analyst's words>
owner: <analyst or team who wrote it>
domain: <domain>
version: <int>                     # bumps when the author re-issues it
provenance:
  distinct_analysts: <N>
  runs: <M>
  last_run: <when>
  witness: <OK | FAIL>             # re-run read-only against the warehouse
business_terms:                    # the terms linked to this query, with their alternate labels
  - {term: <term>, alternate_labels: [<label>, ...]}
rules: [<rules that apply when it is used>]
dialect: duckdb
sql: |
  <complete statement, literals kept>
notes: <what the analyst's comments say, if any>
```
:::

::: {.template #r2-5 file="open_pipeline_top_accounts.yaml" title="Metric spec"}
The metric's executable definition: one metric per file, governed like code. It stays a candidate until an owner approves it.

Rules the file obeys:

- `sql` is what the harness runs. It fills only declared parameters and adds only declared dimensions. It never retypes the statement.
- `formula`, `filters` and `joins` restate `sql` for reviewers. The witness run checks that they agree.
- Verified examples are executed from `sql`, never hand-written.
- `provenance` records where the metric came from and how its conflicts were settled. The approval label served with the metric is rendered from `status`, `owners` and `provenance`.

```yaml
name: open_pipeline_top_accounts
version: 3                          # v2 ranked customers by deal count; retired when the top-100 conflict was resolved
owners:
  - {role: RevOps lead, owns: deals and amount}
  - {role: FP&A partner, owns: who the top 100 customers are}
status: approved
description: >
  Open new-business and upsell pipeline in ARR, on the 100 customers with the highest current ARR.
  Some early stages never count. Finance ranks the customers; Sales owns the deals.
population: Open new-business and upsell deals past the first stage, on the top N customers by current ARR
grain: One row per customer; each open deal counted once (key opportunity id)
time_rule: The quarter-end snapshot at the as-of date. Quarters are fiscal; the fiscal year ends 30 June.
formula: SUM(o.arr)
exclusions: [first-stage deals, renewals, internal and test accounts, closed deals]
filters:
  - o.stage_order >= 2
  - o.type IN ('New Business', 'Upsell')
  - NOT o.is_closed
  - NOT a.is_internal
  - NOT a.is_test
dimensions:
  - {name: region, sql: a.region}
  - {name: segment, sql: a.segment}
  - {name: rep, sql: o.owner_id}
  - {name: stage, sql: o.stage}
joins:
  - {to: top_accounts (ranked from billing.subscription_term), condition: t.account_id = o.account_id, cardinality: many_to_one}
  - {to: crm.account, condition: a.id = o.account_id, cardinality: many_to_one}
sql: |
  -- dialect: duckdb; parameters: $as_of (date, required), $n (integer, default 100)
  WITH latest_term AS (
    SELECT account_id, arr, ROW_NUMBER() OVER (PARTITION BY subscription_id ORDER BY start_date DESC) AS rn
    FROM billing.subscription_term WHERE status = 'active' AND start_date <= $as_of),
  top_accounts AS (
    SELECT account_id FROM latest_term WHERE rn = 1 GROUP BY account_id ORDER BY SUM(arr) DESC LIMIT $n)
  SELECT COUNT(DISTINCT o.account_id) AS accounts, COUNT(*) AS deals, SUM(o.arr) AS open_pipeline
  FROM crm.opportunity_snapshot o
  JOIN top_accounts t ON t.account_id = o.account_id JOIN crm.account a ON a.id = o.account_id
  WHERE o.as_of_date = $as_of AND o.stage_order >= 2 AND o.type IN ('New Business', 'Upsell')
    AND NOT o.is_closed AND NOT a.is_internal AND NOT a.is_test;
verified_examples:
  - question: How much open pipeline do we have with our top 100 customers?
    parameters: {n: 100, as_of: 2026-06-30}
    result: {accounts: 91, deals: 340, open_pipeline: 412000000}
provenance:
  source: the finance board pack; the ranking lived in a spreadsheet, never in query history
  observed_queries: 0               # 31 queries pasted the list's output as fixed IDs; none computed the ranking
  distinct_analysts: 0
  witnessed: Phase 3 · 1 row · grain check 340 = 340 · by region NA 198M, EMEA 161M, APAC 53M
  conflict: >
    Top 100 by deal count (the sales ops dashboard, the only ranking in query history) against top 100 by
    current ARR (the board pack, ranked in a spreadsheet). Provenance could not weigh a variant it never saw, so both owners decided: ARR.
  approved_by: [RevOps lead, FP&A partner]
  replaces: "v2: top 100 by deal count"
```

```yaml
name: <snake_case>                  # unique; equals the filename stem
version: <int>                      # bumps when sql, formula, filters or joins change
owners:
  - {role: <team>, owns: <what part of the definition>}
status: candidate                   # candidate | approved | deprecated
description: <what a business owner approves, in plain words>
population: <which rows the number counts>
grain: <one row per ...; the key each row is counted once by>
time_rule: <which date, which calendar, snapshot or live>
formula: <aggregate expression>
exclusions: [<what is deliberately left out, in plain words>]
filters: [<SQL predicates, always ANDed in>]
dimensions:
  - {name: <name>, sql: <expression>}
joins:
  - {to: <schema.table>, condition: <condition>, cardinality: <many_to_one>}
sql: |
  -- dialect: duckdb; parameters: $<name> (<type>, <required | default>)
  <the complete executable statement>
verified_examples:
  - question: <text>
    parameters: {<name>: <value>}
    result: {<column>: <value>}
provenance:
  source: <query history | BI | imported | hand-written>
  observed_queries: <n>
  distinct_analysts: <n>
  witnessed: <when · rows · grain check>
  conflict: <what disagreed, and whether provenance or the owner settled it>
  approved_by: []
  replaces: null                    # previous version and why it was retired
```
:::

::: {.template #r2-6 file="top-100-conflict.md" title="Conflict record"}
The record of a conflict between two definitions, and what changed because of it. Most conflicts close on provenance and need only the first two sections. Write the full record when the owner decides, or when the decision changes something already approved.

```markdown
# Conflict: who the top 100 customers are
Status: resolved · Raised by: trace review, Phase 3 · Settled by: the owners, a 20-minute session the next day
Room: RevOps lead (decides: deals) · FP&A partner (decides: top 100) · context engineer (presents, no vote) · eval owner (present, silent on the key)
Prepared the day before: both variants as SQL, witnessed; the pasted list of 100 account IDs traced to the FP&A partner's spreadsheet

## The conflict
When someone asks about "our top 100 customers", which 100 are they?

| Variant | Definition | Where it is used | Provenance |
|---|---|---|---|
| A | most opportunities, any stage | sales ops "Top accounts" dashboard; approved v2 | the only ranking in query history, run often by sales ops |
| B | highest current ARR on the latest active term | finance board pack | none in query history: the ranking lived in a spreadsheet; 31 RevOps queries pasted its output as a fixed list of IDs |

Provenance: cannot settle it. B, the number leadership runs on, never appeared in query history, so history favours A by default. Sent to the owners.

## Decision
B, written as SQL on billing terms, with "some early stages never count" written into the metric's population.
Rationale, FP&A partner: "The board pack is the number leadership runs on. Deal count rewards accounts with many small deals."
RevOps lead: "Agreed. Sales ops keeps its tile, renamed 'most active accounts'."

## Effect
- Context changed: open_pipeline_top_accounts v3; v2 retired, kept on record
- Business term "Top accounts" now points to v3
- Golden-set items affected: the pipeline question and the win-rate question; already sealed to B; resealed: no
- Next: v3 re-witnessed, then the whole set rerun; predicted fixes: the pipeline, slipped-deals and win-rate questions
- Reopen if: finance changes how the board pack ranks customers
```

```markdown
# Conflict: <short name>
Status: open | resolved on provenance | resolved by the owner | escalated · Raised by: <generation | repeated runs | trace review | user correction>, <when>
Room (owner decisions only): <who decides, on what> · <who presents, no vote> · <eval owner, silent on the key>
Prepared: <each variant as SQL, witnessed; any pasted list it touches, traced>

## The conflict
<the question the business had not decided, in one sentence>

| Variant | Definition | Where it is used | Provenance |
|---|---|---|---|
| A | <definition> | <dashboards, teams> | <analysts, runs, last run, matches the warehouse?> |
| B | <definition> | <dashboards, teams> | <analysts, runs, last run, matches the warehouse?> |

Provenance: <settles it: which variant and why | split: sent to the owner>

## Decision
<the variant chosen, or the new definition>
Rationale: <why, in the owner's words, or the provenance that settled it>

## Effect
- Context changed: <metric and new version | rule | business term>; retired: <version>
- Golden-set items affected: <ids>; resealed: <yes / no>
- Next: <re-witness, rerun, predicted fixes>
- Reopen if: <what would reopen it>
```
:::

## Phase 3: the hill climb {#r2-week-3}

::: {.template #r2-7 file="trace-review.md" title="Trace review sheet"}
One row per miss, read from the raw trace. The row decides the next context change. Walk each miss down [Why did this miss?](#c6) first; the kind column takes its branch.

```markdown
# Trace review: Sales, Phase 3, rounds 2 and 3

| Question | Run | Verdict | Expected / returned | Served | Used? | Step where it guessed | Kind of miss | Proposed change |
|---|---|---|---|---|---|---|---|---|
| partner-org count | round 2 · 1 of 3 | wrong; passed in round 1 | sealed count, a partner org included / one org short | new rule "internal and test accounts are out", as an instruction | yes, too widely | turn 3: excluded every account that was not a direct customer | a break: a rule served too widely | scope the rule to the org-type field |
| win rate, fiscal Q3 | round 3 · 2 of 3 | wrong on 1 of 3 | fiscal Q3 / calendar Q3 | win_rate v4; rule quarter-means-fiscal | partly | turn 3: let the metric's period default read "Q3" as July to September | served, parameter bound wrong | make the time parameter required, no default |
| pipeline, top 100 | round 3 · 1 of 3 | wrong, same every run | $412M / a total above the key | open_pipeline_top_accounts v2 | yes | turn 3: the served metric ranked customers by deal count, with no early-stage rule | never written: finance's ranking was nowhere in the context | raise the top-100 conflict; write the stage rule into the metric |
| slipped deals | round 3 · 2 of 3 | wrong | 96 slipped ($118M) / 218 slipped | win_rate v4 (weak match); the trusted query not retrieved | partly | turn 3: "nothing served defines slipped"; counted any close-date change | written, not served | add alternate labels "pushed", "rolled" to "Slipped deal"; link the term to the query |
| pipeline created, by segment | round 3 · 3 of 3 | wrong, same every run | sealed value / wrong | a newly promoted trusted query | yes | none: the warehouse holds no "created and still open" state | the data | escalate to the platform owner |
```

```markdown
# Trace review: <domain>, round <n> · context v<x.y>

| Question | Run | Verdict | Expected / returned | Served | Used? | Step where it guessed | Kind of miss | Proposed change |
|---|---|---|---|---|---|---|---|---|
| <question> | round <n> · <n of k> | <verdict; mark a break if it passed before> | <value> / <value> | <names and versions> | <yes / no / partly> | <turn, and what it assumed> | <key wrong / budget / never written / written, not served / served, ignored / the data / a break> | <one change> |
```
:::

::: {.template #r2-8 file="iteration-ledger.md" title="Iteration ledger"}
One row per round of context changes, with the prediction written before the run, so every gain is traceable and every loss is visible. The stop rule: stop when two rounds in a row move the total by no more than the run-to-run variation (how far the score moves between identical runs), and none of the predicted fixes lands. Cap Phase 3 at five rounds.

```markdown
# Iteration ledger: Sales · golden set of 20 · run-to-run variation: 2 questions (the Phase 2 context run three times unchanged: 14, 13, 15) · score = right on every run

| Round | When | Context | Changes | Predicted fixes | Runs | Score | Fixed / broken | Decision |
|---|---|---|---|---|---|---|---|---|
| 0 | end of Phase 1 | bare schema | none (baseline) | none | 1 | 7 of 20 | none | gate met |
| 1 | end of Phase 2 | v1.0 | six metrics, trusted queries, business terms, two rules | none (first scored run) | 1 | 14 of 20 | +7 / 0 | gate met |
| 2 | Phase 3 | v1.1 | rule "regions roll up to NA, EMEA, APAC"; stage-aging query ranked above a stale one; rule "internal and test accounts are out" as an instruction | stage aging | 3 | 14 of 20 | stage aging / partner-org count, caught by the rerun | keep the first two; rescope the rule |
| 3 | Phase 3, next day | v1.2 | the rule scoped to org type; "pipeline created by quarter" query promoted | partner-org count, pipeline created | 3 | 14 of 20 | partner-org count / win rate, 1 of 3 runs | keep; raise the top-100 conflict; pipeline created goes to the platform owner |
| 4 | Phase 3 | v1.3 | top-100 conflict resolved: metric v3 with the stage rule inside; "Slipped deal" labels and link; win rate's time parameter required | pipeline, slipped deals, both win-rate questions | 3 | 18 of 20 | all four, 3 of 3 / none | keep |
| 5 | Phase 3 | v1.4 | column description on the stage field: "the first stage is not pipeline" | none expected | 3 | 18 of 20 | none / none | revert: the rule already lives in the metric |

Stop rule: not fired. Rounds 2 and 3 held the total but each landed its predicted fix; round 4 moved it by 4; round 5 was the only quiet round.
Phase 3 ended at 18 of 20, which meets the bar of 9 in 10. New questions were then added for the launch test.
```

```markdown
# Iteration ledger: <domain> · golden set of <n> · run-to-run variation: <questions>, from <k> identical runs · score = right on every run

| Round | When | Context | Changes | Predicted fixes | Runs | Score | Fixed / broken | Decision |
|---|---|---|---|---|---|---|---|---|
| <n> | <when> | <v> | <changes> | <questions, written before the run> | <k> | <your run> | <questions> / <questions> | <keep / revert> |

Stop rule: <fired | not fired | five-round cap reached>, and why.
Optional columns: cost and latency per question, from the traces.
```
:::

::: {.template #r2-12 file="sponsor-readout.md" title="Sponsor readout"}
One page the exec sponsor reads in five minutes: the score against the golden set, what changed, and what needs a decision. Once per phase, at its gate.

```markdown
# Sponsor readout: Sales · end of Phase 2 · delivery lead

Status: on track. Gate this phase: metrics published and scored. Met.

## Score against the golden set
Six metrics, one run per question: 14 of 20, up from the bare-schema baseline of 7 of 20. The bar is 9 in 10.

## What changed
- Six metrics approved, each with an owner, a version and its provenance
- Most conflicts settled on provenance; the owners decided the split ones; one escalated to you (below)
- Win rate now excludes disqualified deals: the dashboard version predated that stage, and every recent analyst query excluded it

## Decisions needed from you
- For multi-year deals, is the amount first-year ARR or total contract value? The RevOps lead and the FP&A partner
  disagree. Until you decide, the agent flags the conflict instead of answering. Decided at this readout: first-year ARR.
- Your question on why EMEA dropped waits until the numbers are released. It sits in the backlog with a date.

## Risks
- New questions for the launch test, ones the builders never saw, must be sealed by the end of Phase 3
- The FP&A partner's hour in Phase 3, for any decision on the top 100

## Next phase
Measure run-to-run variation, then fix from traces; the graders add new questions for the launch test.
```

```markdown
# Sponsor readout: <domain> · <phase or gate> · <delivery lead>

Status: on track | at risk | blocked. Gate this phase: <gate>, <met / not yet>

## Score against the golden set
<context version, score against the bar, change since the last readout, inside run-to-run variation or not>

## What changed
<context changes since the last readout, and how each conflict was settled>

## Decisions needed from you
<decision, why it matters, by when>

## Risks
<live rows from the risk log, with their mitigation>

## Next phase
<plan to the next gate>
```
:::

::: {.template #r2-18 file="risk-log.md" title="Risk log"}
The live list of what could stall the engagement. Open it at the kickoff from the [engagement rows in R1](#r1-engagement) and read it at every readout.

```markdown
# Risk log: Sales · opened at the kickoff · delivery lead · as it stood after launch

| # | Risk | Signal to watch | Likelihood, impact | Mitigation | Status |
|---|---|---|---|---|---|
| 1 | No per-call trace export | the chat tool exports a nightly summary only | H, H | build a per-call export; read one trace end to end before Phase 1 | closed in Phase 0 |
| 2 | Security review opens late | no walk-through booked | M, H | walk the data-flow diagram at the kickoff | closed in Phase 0 |
| 3 | Why-questions before the numbers are right | the CRO asked in Phase 2 | M, M | deferred by the brief; dated in the backlog | closed: why-set ran after launch |
| 4 | Pipeline-creation questions cannot pass | the same miss on every run, the data (Phase 3) | H, M | held back by name; build the "created and still open" state | closed after launch |
| 5 | A schema change breaks served queries | a schema-change alert | M, H | the regression set reruns on every alert | fired after launch; fixed by the team alone |

Escalate a High/High to the exec sponsor the same day.
```

```markdown
# Risk log: <domain> · opened <date> · <delivery lead>

| # | Risk (an R1 symptom, or new) | Signal to watch | Likelihood, impact | Mitigation | Status |
|---|---|---|---|---|---|
| 1 | <risk> | <the observable signal> | <H/M/L>, <H/M/L> | <action, due> | open / closed <date> |

Escalate a High/High to the exec sponsor the same day.
```
:::

## Phase 4: release and hand over {#r2-week-4}

::: {.template #r2-9 file="release-note.md" title="Release note"}
What shipped, what it scored against the sealed set, and how to roll it back.

```markdown
# Release: Sales context v1.0 · Phase 4 · signed by the CRO
Launch gate: the golden set at or above the bar of 9 in 10, on every run; everything that passed at Phase 3 still passes;
random pass audit done; every out-of-scope question refused

| Type | Name | Version | Change | Settled by |
|---|---|---|---|---|
| metric | open_pipeline_top_accounts | v3 | added; v2 retired, kept on record | both owners (top-100 conflict) |
| metric | win_rate | v4 | added: won / (won + lost), by close date, disqualified out | provenance (recency) |
| metrics | closed_won_arr, open_pipeline, avg_deal_size, stage_conversion | v1 | added | provenance |
| business terms | Slipped deal (pushed, rolled, slid); Top accounts; 10 more | 2; 2; 1 | added; linked | none needed |
| rules | quarter-means-fiscal; regions-roll-up; flag-conflicts | 1 | added | RevOps lead |
| trusted queries | 38 | 1 | added | provenance |

Held back by name: pipeline-creation questions, until the "created and still open" state exists
Known limits: why-questions, follow-up turns and entity lookups are not measured
Rollback: repoint to the previous context version with the previous harness build
Next: the open conflicts on released questions, then the why-layer
```

```markdown
# Release: <domain> context v<x.y> · <date> · signed by <exec sponsor>
Launch gate: <your run> on the sealed set against the bar of <bar>, on every run; regression <held / not>; random pass audit <done>; out-of-scope <refused / not>

| Type | Name | Version | Change | Settled by |
|---|---|---|---|---|
| <metric / rule / business term / trusted query> | <name> | <v> | <added / changed / retired> | <provenance / owner> |

Held back by name: <kinds of question, and what brings them back>
Known limits: <unmeasured question types; open conflicts>
Rollback: <previous context version and harness build>
Next: <next-version backlog>
```
:::

::: {.template #r2-19 file="handover-checklist.md" title="Handover checklist"}
The Phase 4 test that the company runs the loop without the delivery team.

```markdown
# Handover checklist: Sales · Phase 4
- [x] Every metric (6) has an owner on the company's side and a version; every rule (3) and business term (12) has a version
- [x] The golden set is sealed and versioned; the questions right on every run form the regression set
- [x] The conflict records and the iteration ledger are edited by the company's team, not by the delivery team
- [x] One pass run together: the open conflicts resolved, the regression set passing in full
- [ ] One pass run alone within two weeks (done after launch: a schema change, rerun and fixed by the team)
- [x] Production traces reach the company's log store per call; user corrections reach the conflict list as proposed changes
- [x] A rerun fires on every context change (the full set) and on every schema change (the regression set)
- [x] The next-version backlog and the domain-two plan agreed
- [x] Postmortem and pattern write-up drafted and reviewed
Open: pipeline-creation questions wait on the new data state; the arbiter for words finance and sales both own
```

```markdown
# Handover checklist: <domain> · Phase 4 · <date>
- [ ] Every metric has an owner on your side and a version; every rule and business term has a version
- [ ] The golden set is sealed and versioned; the questions right on every run form the regression set
- [ ] The conflict records and the iteration ledger are edited by your team
- [ ] One pass run together
- [ ] One pass run alone within two weeks (due <date>)
- [ ] Production traces reach your log store per call; user corrections reach the conflict list as proposed changes
- [ ] A rerun fires on every context change and every schema change
- [ ] Next-version backlog and domain-two plan agreed
- [ ] Postmortem and pattern write-up drafted and reviewed
Open: <what waits, and on whom>
```
:::

::: {.template #r2-20 file="pattern-write-up.txt" title="Pattern write-up"}
A short, anonymised account of what the engagement showed, for whoever owns the platform it ran on. The delivery lead drafts it within a week of launch:

1. Collect the decisions log (the conflict records), the iteration ledger and the postmortem.
2. Describe the domain's shape: industry, which kinds of question are governed, estate size, and whether an agent already existed.
3. List what moved the score and what did not.
4. Sort every fix into two piles: keep the fixes the next engagement will need, throw away the ones that fitted only this estate.
5. Name each missing capability in one line, with the trace or decision that showed it.
6. Have the anonymisation checked, then send it.

```text
Pattern: a definition kept in a spreadsheet hid a conflict until Phase 3
Domain shape: B2B software, sales pipeline; board numbers governed, diagnostics exploratory; CRM and billing; no agent at the start
What happened: graders disputed the top-100 source in Phase 1; the FP&A partner chose the board pack, and the choice stayed on the item.
  Finance's ranking lived in a spreadsheet, so the only ranking in query history was the deal-count tile.
  The 31 queries that pasted finance's list were set aside as a hard-coded list, which raised no conflict.
  Phase 2 approved the deal-count ranking; the Phase 3 raw trace exposed it; the owners resolved it in 20 minutes.
What moved / what did not: a rule served too widely broke one question, caught by the rerun and fixed the next day;
  the top-100 fix, a term link and a required time parameter took the score from 14 to 18 of 20; a column description moved nothing and was reverted
Platform: a set-aside list of IDs with no known source should ask the owners where it came from
Throw away: the "created and still open" state was specific to this warehouse
Missing capability: a sealing dispute should also reach the conflict list, with no sealed value attached
Reviewed for anonymisation by: the RevOps lead
```

```text
Pattern: <one line>
Domain shape: <industry, kinds of question and which are governed, estate size, starting point>
What happened: <the conflict, miss or result, and the round that showed it>
What moved / what did not: <from the ledger>
Platform: <fixes the next engagement will need too>
Throw away: <fixes specific to this estate>
Missing capability: <one line each>
Reviewed for anonymisation by: <domain owner>, <date>
```
:::

::: {.template #r2-21 file="postmortem.md" title="Field postmortem"}
A blameless review that examines the system, never a person. Run it at the end of every engagement, and whenever a gate slips by more than a week, a wrong number reaches a governed-lane user, the score drops after a release, a context change is rolled back, or the engagement stops before launch.

Write it about conditions. "The domain owner was slow to decide" is blame. "Decisions waited a week because the owner's hours were agreed in Phase 0 and never put on a calendar" is a condition, and a condition has a fix. Run it in five steps:

1. Collect the record: decisions, the iteration ledger, risks and readouts.
2. Write the timeline in order, with no interpretation yet.
3. For each problem, find what in the plan, the roster or the tooling made it likely.
4. Write actions with dates. Each changes a checklist, a template, a runbook step or the platform. "Be more careful" is not an action.
5. Review it with the domain owner and the sponsor in one 45-minute session, then feed it forward to the next engagement.

```markdown
# Postmortem: Sales · Phase 4
Trigger: engagement end · Author: delivery lead · Reviewed with: RevOps lead, CRO

## Timeline
Phase 1: graders disputed the source for the pipeline question; the FP&A partner chose the board pack; recorded on the item only
Phase 1: 20 sealed; by design, the context side never saw the item's history
Phase 2: generation set aside 31 queries with a pasted list of 100 account IDs; no conflict raised
Phase 2: the top-100 metric was approved in a batch of six, ranking customers by deal count
Phase 3: the raw trace of the pipeline question showed the ranking
Phase 3: the owners resolved the conflict the next day; the rerun fixed three questions on every run

## Conditions
The wall between the key and the context protected the key and also hid a conflict.
A set-aside list is not a conflict, so it never reached the owner.
Nobody approving the batch asked where the top-100 ranking came from.
Gate 2 passed the metric with its stage rule served only as an instruction, outside its SQL.

## Actions
| Action | Due |
|---|---|
| A sealing dispute about a definition also goes to the conflict list, with no sealed value | domain two's Phase 0 |
| Every pasted list of IDs is traced to its source before the concept it touches is approved | domain two's Phase 2 |
| Gate 2 reads each metric's SQL for the house rules that apply before approval | domain two's Phase 2 |
New R1 row: symptom "graders disagree on a source"; cause "a conflict settled at sealing, never resolved"; fix "send it to the conflict list as well"
```

```markdown
# Postmortem: <domain> · <date>
Trigger: <engagement end | gate slipped | wrong governed number | a break | rollback | stopped early>
Author: <delivery lead> · Reviewed with: <domain owner>, <exec sponsor>

## Timeline
<when>: <what happened>, in order, no interpretation

## Conditions
<what in the plan, roster or tooling made each problem likely>

## Actions
| Action | Due |
|---|---|
| <a checklist, template, runbook step or platform change> | <date> |
New R1 rows: <symptom, cause, fix>
```
:::

## After release {#r2-after}

::: {.template #r2-13 file="sales-subgraph.yaml" title="Ontology fragment and business changes"}
The slice of the business graph a why-question needs. Every entity is bound to its tables and metrics. The business changes list holds the dated changes the agent can test as causes. Build it after the numbers are released.

```yaml
ontology: sales subgraph · imported from the company glossary (entities, vocabulary) and the BI semantic model (bindings), after launch
entities:                           # five, cut to what the why-questions touch
  - {name: Opportunity, tables: [crm.opportunity, crm.opportunity_snapshot], key: id, metrics: [open_pipeline_top_accounts, win_rate]}
  - {name: Account, tables: [crm.account], key: id, metrics: [open_pipeline_top_accounts]}
  - {name: Rep, tables: [crm.rep], key: id, metrics: []}
  - {name: Territory, tables: [crm.territory], key: id, metrics: []}
  - {name: Stage history, tables: [crm.stage_history], key: opportunity_id, metrics: []}
relationships:                      # the two the EMEA answer turned on
  - {from: Territory, to: Rep, name: owned by, rule: a new rep re-qualifies the territory's deals, binding: crm.territory.owner_rep_id}
  - {from: Opportunity, to: Stage history, name: re-signing on new terms returns a deal to the first stage, rule: a re-signed deal sits outside open pipeline until re-qualified, binding: crm.stage_history.opportunity_id}
business_changes:
  - {date: 2026-05-01, change: EMEA territory realignment; many top-100 accounts changed owning rep, owner: Sales Ops, entities: [Territory, Rep, Opportunity], testable_by: deals whose owner changed that day and have not moved since}
  - {date: 2026-05-15, change: enterprise pricing change; open deals re-signed on new terms, owner: Finance, entities: [Opportunity, Stage history], testable_by: enterprise deals back at the first stage after that date}
# The EMEA why-question: pipeline fell $53M. $31M sat in deals stuck after the territory realignment;
# $19M was re-signed on new terms after the pricing change. The one why-set miss traced to a comp-plan change nobody wrote down.
```

```yaml
ontology: <domain> subgraph · <sources it was imported or written from>, <date>
entities:
  - {name: <Entity>, tables: [<schema.table>], key: <column>, metrics: [<metrics>]}
relationships:
  - {from: <Entity>, to: <Entity>, name: <verb phrase>, rule: <what it means for the numbers>, binding: <join or column>}
business_changes:                         # written by the owning team as events happen
  - {date: <YYYY-MM-DD>, change: <what changed>, owner: <team>, entities: [<Entity>], testable_by: <the SQL signal>}
```
:::
