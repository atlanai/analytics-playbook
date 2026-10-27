---
for: context engineer, domain owner, agent builder, eval owner
produces: metrics, trusted past queries, resolved conflicts, the Gate 2 score
---

# Phase 2: generate metrics {#ch05}

> [!RULE]
> Write each business rule into a metric's SQL. The agent follows a query and skims a paragraph.

::: {.tldr}
- **Short version.** Generate candidate metrics from the SQL your analysts already run, settle the conflicts with the domain owner, have the owner approve what survives and serve it to the agent per question. Bring in the definitions you already have; nothing needs to start from zero.
- **Do this.** Get the metrics behind your golden-set questions approved first.
- **Skip if** your metrics are already approved by their owners and served. Go to [Phase 3](#ch06).
:::

::: {.scene week="Phase 2"}
On the first morning of Phase 2, the context engineer pointed a metrics agent, a script with a language model that drafts candidate metrics, at the analysts' past SQL and the sales dashboards. By the afternoon it had proposed candidate metrics, each with the real queries behind it. Every candidate then ran read-only against the warehouse. Most conflicts settled on provenance: the version most analysts ran, recently, that matched the warehouse. The RevOps lead decided the rest in short sessions. One would not settle. For multi-year deals, did the amount mean first-year ARR or total contract value? It went to the CRO, who answered two days later: ARR, the figure the board pack uses. By the end of Phase 2 the owners had approved six metrics, and the agent scored 14 of 20, up from 7.
:::

Most of what your company knows about its numbers is already written down. It sits in the SQL your analysts ran and in the reports and semantic models your BI tool serves. You rarely write a metric from scratch. You generate candidates from those sources, prove each one runs, settle the conflicts and have the owner approve what survives. Then you score the result on the same sealed questions.

## Five steps from past SQL to metrics {#ch05-pipeline}

::: {.diagram #metrics-pipeline}
From what your company already has to metrics: gather the sources, generate candidates, witness each one against the warehouse, resolve conflicts, approve.
:::

### Gather the sources

Use two kinds of source, always together. Past SQL shows how analysts actually answered questions, including the filters nobody wrote down. BI reports and semantic models show what the business agreed to put on a dashboard. Either one alone misses things. Query history has no record of a ranking kept in a spreadsheet. A dashboard has no record of the one-off question an analyst answered last month.

Pull the executed statements on the domain's tables, read-only, far enough back to cover a full business cycle, with who ran each one, when and how often. Leave out the agent's own queries and machine traffic such as scheduled loads. Keep dashboard queries, because a person chose their filters. Export the domain's BI reports, measures and semantic models alongside.

### Generate candidates

Hand both sources to a metrics agent. It groups statements that share one shape, keeps one complete statement per shape with its literals intact, and names the metrics inside it. Each candidate comes out with a population, exclusions, a grain, a time rule, joins and dimensions, plus the real SQL it came from. Whatever does not become a metric stays as a trusted past query, with its provenance, for the exploratory lane.

You don't need a product for this step. A script can normalise each statement, stripping literals and ordering clauses, and group statements by shape; a language model then names and describes each group without touching its SQL. Two rules keep the output honest. The generator never sees the golden set. And every candidate's SQL is cut from a real statement: the generator names and describes, but writes no new SQL.

::: {.diagram #metrics-agent}
What the metrics agent does, and where your people take over: it drafts candidates from what you already have; your people witness, settle conflicts, approve and serve.
:::

### Witness every candidate

Nothing is approved until it has run. Run each candidate under a read-only identity and record five things:

- did it run, and how long did it take
- how many rows came back
- does each row count once (`COUNT(*) = COUNT(DISTINCT key)`)
- does the prose agree with the SQL
- is there any literal nobody can attribute to a rule

Hold back any candidate that fails its run or carries a predicate you cannot explain. A hard-coded list of account IDs is the common case. Trace the list to its source before you move on. This is where a fork can hide. A definition kept in a spreadsheet or a board pack never shows up in query history, so at most it surfaces as an unexplained list.

Keep uncertain candidates out of the served context entirely. An agent cannot weigh a warning. A metric marked "unverified" is still a complete, confident statement, and the agent will use it.

### Resolve conflicts

A conflict is two witnessed candidates that claim the same number with different rules. Two versions of win rate is the classic case. The sales dashboard counted disqualified deals in the denominator. The analysts' queries did not.

In our engagements, most conflicts settled on provenance, without a meeting. Line up the evidence for each version.

| Signal | What it tells you |
|---|---|
| Who ran it | Analysts in the owning team outrank a one-off from another function |
| How often | The version run most is the working definition |
| How recently | A version nobody has run since a process change is probably stale |
| Does it match the warehouse | The version whose filters fit the current schema and data is usually right |

Win rate settled on recency. The dashboard version predated the "Disqualified" stage, and every recent analyst query excluded it. The RevOps lead confirmed it in a minute.

When the evidence splits, the domain owner decides. Prepare each conflict the day before: both versions as SQL, both results on the same snapshot, the literals that differ, and who uses each. When a definition spans two functions, both owners sign. If they cannot agree, the conflict goes to the sponsor, and the agent serves neither version until then. Take on only the conflicts the owner can decide in the time booked, most-used numbers first. The rest wait, unserved.

### Approve

Send every witnessed metric with no open conflict for approval. Each one gets an owner, a version, its provenance and its SQL. The domain owner approves them, usually in one batch, and only approved metrics are served on the governed lane.

Before you approve, check that every house rule that applies is written into the SQL. A rule that lives only in a description, or in a separate instruction, never reaches the statement the harness runs.

## What one metric holds {#ch05-spec}

A metric is a file, governed like code. Here is win rate after its conflict was resolved, cut to the fields a reviewer reads.

::: {.template #ch05-metric-preview file="win_rate.yaml" title="Metric spec, short form"}
The exclusion of disqualified deals is in the SQL, where the harness will run it, and in the prose, where a reviewer will read it. The witness run checks that the two agree.

```yaml
name: win_rate
version: 4                          # v3 was the dashboard version; retired, kept on record
owners:
  - {role: RevOps lead, owns: the definition}
status: approved
description: Deals won as a share of deals won or lost in the period. Disqualified deals are out.
population: Deals closed won or closed lost in the period
exclusions: [disqualified deals, internal and test accounts]
grain: One row per deal (key opportunity id)
time_rule: Close date, fiscal quarters; the fiscal year ends 30 June
dimensions: [region, segment, rep]
joins:
  - {to: crm.account, condition: a.id = o.account_id, cardinality: many_to_one}
sql: |
  SELECT 100.0 * COUNT(CASE WHEN o.stage = 'Closed Won' THEN 1 END) / COUNT(*) AS win_rate
  FROM crm.opportunity o JOIN crm.account a ON a.id = o.account_id
  WHERE o.close_date BETWEEN $start AND $end
    AND o.stage IN ('Closed Won', 'Closed Lost')
    AND NOT a.is_internal AND NOT a.is_test
verified_examples:
  - question: What was our win rate last quarter?
    result: 24.3                    # executed against the warehouse
provenance:
  source: query history and the sales dashboard
  distinct_analysts: 6
  runs: 140
  witnessed: Phase 2 · 1 row · grain check passed
  conflict: dashboard version counted disqualified deals; settled on recency, confirmed by the RevOps lead
  approved_by: [RevOps lead]
```
:::

Read more: [the full metric spec template](#r2-5)

## Serve it per question {#ch05-serve}

How you serve decides whether the agent uses what you built. [Serve per question](#ch-retrieval) has the architecture and the ranking rules: one context call per question, a handful of complete statements, metrics first and labelled. Two more rules matter here:

1. **Keep the literals.** `'Closed Won'` and `stage_order >= 2` are the definition. Mask the names of people and customers, and keep the business values.
2. **Serve rules as instructions.** A house rule that holds for every question, such as "quarter means fiscal quarter", goes to the agent as a short instruction with the name of whoever set it. If a metric depends on the rule, write it into the metric's SQL as well.

## Bring in what you already have {#ch05-path-b}

Most teams already hold some context: a semantic layer (semantic views, metric views, LookML or dbt metrics), saved queries, instructions written for an earlier agent. Treat all of it as a source, put it through the same witness and conflict steps, and sort it by what it can do.

| What you bring in | Treat it as | Why |
|---|---|---|
| Saved or verified queries | Candidate trusted past queries | Complete, human-approved SQL transfers well |
| Metric views and measures with filters | Candidate metrics | The filter is a decision, and it runs the same every time |
| Instructions such as "exclude test tenants" | Candidate rules | A rule the agent must follow |
| Column descriptions and synonyms | The floor, for finding tables | A dictionary says what exists. It says nothing about how to count |

Give every imported object an owner and a version before it is served.

## Gate 2 {#ch05-gate2}

The sponsor sees the score on the same sealed questions, the change since the baseline, the conflicts resolved and anything escalated. The decision is to start the hill climb. Hold the gate if anything served is unowned, unversioned or unwitnessed.

A gate can only check what somebody raised. A metric can pass every check here and still carry a definition nobody questioned, because the other definition never appeared in any source. Phase 3 finds those in the traces.

> [!DONE]
> - [ ] Past SQL and BI reports gathered, the agent's own queries excluded
> - [ ] Candidates generated without sight of the golden set, each with SQL cut from a real statement
> - [ ] Every candidate witnessed read-only, with a row count and a grain check
> - [ ] Every unexplained literal traced to its source, and nothing unexplained served
> - [ ] Conflicts resolved on provenance or by the owner; any deadlock on the sponsor's agenda
> - [ ] Every metric has an owner, a version, provenance and SQL, with its house rules inside the SQL
> - [ ] Everything served arrives through one traced context call, per question
> - [ ] Anything brought in from existing models or saved queries is owned, versioned and witnessed
> - [ ] Gate 2: metrics scored on the sealed questions, change since the baseline recorded

Card: [How to resolve a conflict](#c5)
