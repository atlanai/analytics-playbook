---
for: eval owner, graders, agent builder, domain owner
produces: at least 20 sealed questions, the grading rules, the baseline score, Gate 1
---

# Phase 1: build the golden set {#ch04}

> [!RULE]
> Seal the questions where the builders can't see them, and grade them by code.

::: {.tldr}
- **Short version.** Harvest real questions from the board pack and dashboards, write the correct SQL for each, check the answers against the source the business trusts, and seal them away from the builders. Then run the bare agent for a baseline.
- **Do this.** Seal at least 20 questions and record the baseline score.
- **Skip if** you already have a sealed, graded answer key for this domain. Go to [Phase 2](#ch05).
:::

::: {.scene week="Phase 1"}
The eval owner started with the board pack and the RevOps dashboards, and within two days had several times as many candidates as the set needed.

The dispute came halfway through. Two graders checked "open pipeline with our top 100 customers" against two trusted sources, the dashboard tile and the board pack. The two lists were not the same hundred accounts. The FP&A partner, who owns the top-100 list, chose the board pack, because that was what the CRO had promised the board. The choice went into the item's history. Nobody sent the dispute across the wall as a conflict.

By the end of Phase 1, twenty questions were sealed. The agent then ran on bare schema, once per question. It got 7 of 20 right. The pipeline question came back as $1.31B, and nothing in the SQL looked wrong.
:::

[Evals first](#ch-evals) makes the case for the golden set; this phase builds it.

## Harvest at least 20 real questions {#ch04-harvest}

Take the questions from what the business already asks and has already answered. An invented question tests work nobody needs done, and it tends to be one the agent can pass. Collect two or three times as many candidates as you will seal. Then pick at least 20 that cover the domain.

Pull the candidates from four places:

- the board pack and the dashboards leaders read
- analyst tickets and requests from the last two quarters
- saved analyst queries on the domain's tables
- the sponsor's own questions

Rewrite each one the way a user would ask it, with no table or column names. Record where its verified answer lives. Then ask the domain owner one question, because it often surfaces the item that matters most: what was the last wrong number that reached a meeting, and how was it caught?

## Write every item in one format {#ch04-item}

Every question goes into the golden set in one format, so any grader can check any item and you can version the set like code. Five fields are required. The rest are optional.

::: {.template #ch04-item-preview file="sales-01.yaml" title="Golden-set item, short form"}
The pipeline question, as sealed.

```yaml
# required
id:               sales-01
question:         How much open pipeline do we have with our top 100 customers?
source:           FP&A board pack, top-accounts pipeline page
expected:         {accounts: 91, deals: 340, open_pipeline: 412000000}
expected_sql:     |
  -- the query that returns expected, run read-only on the as-of snapshot

# optional
valid_alternatives: ["by region, summing to the total"]
tolerance:          {counts: exact, amounts: within 0.5%}
decisions:          [top 100 by current ARR, some early stages never count, amount is ARR, each deal once]
decoy:              "top 100 by deal count, every stage, contract value, each term -> $1.31B"
history:            ["graders disputed the source; FP&A partner chose the board pack"]
```
:::

Two optional fields pay off in Phase 3. `decisions` lists the choices the question hides. `decoy` is the wrong answer you get when those choices are guessed the obvious way. When the agent misses, a grader compares its SQL against the decisions and names the one it guessed.

Read more: [the full golden-set item template](#r2-3)

## Grade the data first, then the SQL {#ch04-grading}

Write the grading rules in this phase, before any result exists. Rules written after the results bend toward them.

::: {.diagram #grading}
One item, graded in order: the returned data within tolerance, then the SQL against its decisions, then the same answer on every run. Each item runs k times. Pass^k means right on all k runs; pass@k means right on at least one. Items right on every run form the regression set. The rest are items the agent can't yet answer reliably.
:::

- **Grade the data first, then the SQL.** The data check is fast and needs no judgment. Then check that the SQL makes the item's decisions. A wrong query can land near the right number by luck, so a near-match on data alone never passes.
- **Allow several valid answers.** A total and a breakdown that sums to it are both right. Record these in `valid_alternatives` when you seal. An alternative that makes a different decision is a conflict. Whoever owns that number settles it before the item is sealed, and it goes to the conflict list too, with no sealed value.
- **Check consistency across runs.** Right every time means the agent knows it. Right some of the time means it is guessing, and on one run you cannot tell the difference. That is why the bar in the brief must hold on every run.
- **Use an LLM as a judge for answer shape.** A model is good at checking what code cannot: did the answer state its period, filter and unit? It should never grade the number itself when code can.

Calibrate the judge before its verdicts count:

1. Two graders grade the same sample blind, with one written rubric.
2. The judge grades the same sample.
3. Look at every disagreement. Most trace to a rule nobody wrote down, so fix the rubric.
4. The judge counts once it agrees with the graders about as often as they agree with each other. Recheck it whenever its model or rubric changes.

## Keep the golden set away from the agent {#ch04-seal}

The golden set and the agent's context draw on the same past SQL. The query behind a dashboard tile can come back as a trusted past query, and then the agent copies the answer instead of working it out. Build guards against three leaks into the pipeline, so nobody has to remember to check:

- **Golden SQL in the context.** Before any context is served, remove every past query that matches an item's expected SQL or returns a sealed answer. Record each removal by hash, so it can be audited without exposing the set.
- **The agent reading its own work.** Exclude the agent's service account from the query history.
- **Answers in served text.** Scan every prompt for sealed values. A hit invalidates the run.

The context engineer never sees an expected answer. The agent sees only the question as a user would ask it.

::: {.diagram #answer-key}
How the golden set is built and sealed. Only two things cross the wall to the context side: a conflict between definitions, with no sealed value, and the hashes used to purge past SQL.
:::

**Seal, then audit.** An item is sealed when its expected SQL has run read-only on the snapshot, the result matches the trusted source and no dispute is open. Commit the set to version control and never edit a question to make the agent pass.

The set will still have errors. When an item fails on every run whatever you change, suspect the item first: re-run its SQL, re-check the source, and correct it if it is wrong. Audit a few passing items too. A wrong item the agent happens to match looks like a pass, and nobody checks a pass.

## Run the bare agent once for a baseline {#ch04-baseline}

Run the agent on the bare schema before you build any context. It shows how far the schema alone gets you, and every later score is read against it. Run each sealed question once, trace every call, and grade the result. For every miss, record which decision the agent guessed.

In the sales baseline, the pipeline question went wrong four ways. The agent ranked the top 100 by deal count, counted every stage, summed contract value, and joined each deal to every subscription term. Each choice was a reasonable reading of the schema, and the SQL ran clean. Each was also one line of the item's decoy. The right answer is $412M.

## Gate 1 {#ch04-tasks}

The sponsor sees the golden set and the baseline, and decides whether to start building context.

> [!DONE]
> - [ ] At least 20 questions sealed, each verified against its source
> - [ ] Every item has its five required fields; disputes settled, recorded in its history and sent to the conflict list
> - [ ] Grading rules written before any result; any LLM judge calibrated against the graders
> - [ ] No sealed answer or expected SQL in the agent's context; removals recorded by hash
> - [ ] The set committed, and stored wherever your runs are recorded
> - [ ] The baseline run once per question, with the guessed decision on every miss

Card: [The eval owner's week](#c3)
