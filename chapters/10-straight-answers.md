# Straight answers {#ch10}

> [!RULE]
> Say what you measured, and what it means for your warehouse.

::: {.tldr}
- **Short version.** The same skeptic questions come up in every room. The replies say what was measured and where it applies. The chapter also covers what score to expect, cost and latency, and what to do on Monday.
- **Do this.** Quote every number with its scope.
- **Skip if** nobody in the room needs convincing.
:::

The hardest reader of this book runs a data platform, has built text-to-SQL before and distrusts vendor numbers, with reason. Our numbers come from one warehouse, graded against keys our own analysts wrote. [How we measured](#r3) explains the benchmark and its limits.

## The skeptic's questions {#ch10-questions}

The same questions come up in almost every room: a better model, few-shot retrieval, scale, and who pays for the owners' time. The card [Replies for the skeptic](#c13) has a reply to each, plus semantic layers, row-level security and lock-in.

## What score should we expect? {#ch10-score}

Quote no score before your baseline exists. Our ladder shows the order of what helped on one warehouse: past SQL beat documentation, metrics beat past SQL alone, and more prose on top added little. We expect that order to transfer. We don't expect our absolute numbers to, because yours depend on how many of your business's questions your analysts have already answered in SQL and in BI reports.

After the baseline, quote three scores: the baseline at the end of Phase 1, the metrics score at the end of Phase 2, and the launch gate at the end of Phase 4.

Read more: [What moved the score](#ch02-ladder)

## Cost and latency, dated {#ch10-cost}

These figures are from July to September 2026, on one model through one reference harness, and nobody optimised for speed. Expect them to date within a quarter.

| Measure | What we saw |
|---|---|
| Time per question | 22 to 45 seconds <!-- E56 --> |
| Best configuration | about 30 seconds and about 4¢ per right answer <!-- E07 --> |
| What drives cost | model price: one frontier model cost far more per right answer on identical context |

Three habits keep the numbers honest:

1. Report cost per right answer. Cost per call hides the most expensive thing an agent produces: a cheap wrong answer.
2. Measure latency and cost on your own harness, at the baseline and again after Phase 2. Your harness and model set most of both.
3. Price one full rerun of the golden set before Phase 3. The hill climb repeats it on every change, and so does the production loop.

## What to do on Monday {#ch10-monday}

You don't need a budget or a vendor to start. You need an hour and one question.

1. Take one question your leadership asks every week and list the decisions a correct answer needs, with the exercise in [The tenth question](#ch01-decisions). Find two unwritten rules.
2. Pull 20 real questions with known answers for one domain, and run whatever agent you have against them. That is your baseline.
3. Export the last quarter of query history for that domain. The rules your agent is missing are mostly already in it.
4. Name the domain owner who will settle definitions, and ask for their hours in writing.

If the baseline is low and the rules are real, you have a context problem, and this book is the plan for fixing it.

> [!DONE]
> - [ ] Every number you quote has its scope, its model and its date next to it
> - [ ] The sponsor has heard the limits: one warehouse, the question types measured
> - [ ] Governed questions answer from a metric, or refuse
> - [ ] Cost per right answer and latency are measured on your own harness
