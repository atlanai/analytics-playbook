# What we found {#results}

> [!RULE]
> Trust a number only when you can see the questions, the misses and the cost behind it.

Every number in this book comes from one benchmark: 107 real questions our own teams asked of our go-to-market warehouse, each with a sealed answer, graded by code. We ran it more than 150 times <!-- E90 -->, changing one thing at a time. No person wrote the context behind these scores, apart from the semantic-view comparison: our systems built it from the query log, the catalog and existing documentation. [Why that rule matters](#method-automated). The rest of the book quotes a handful of those results. This page shows the rest, including what failed and what each answer cost. [How we measured](#r3) explains the method.

## The scoreboard {#results-board}

Every setup on the same model and the same questions, ranked, with what each answer cost.

::: {.diagram #scoreboard}
Accuracy, cost per run of all 107 questions, seconds per question and cost per right answer, on GLM-5.2. <!-- E03 E04 E05 E11 E20 E21 E52 E70 E71 E73 E74 E75 E76 E77 E80 E81 -->
:::

Three things stand out:

- **Context moved the score; the method of reasoning didn't.** On the same model, the setups span 32% to 83%. All but one of the published methods we rebuilt on top of the metrics layer, from candidate generation and unit tests to model-written evidence, scored lower than the layer alone and cost three to five times as much per right answer <!-- E73 E74 E75 E81 -->. The exception, intent-embedding retrieval, came out 1.9 points ahead, inside the noise, at twice the cost <!-- E71 -->.
- **Curation is cheap.** Past queries deduplicated and ranked by how many analysts ran them scored 75.7% at 1.3¢ per right answer, the cheapest right answers on the board <!-- E80 -->.
- **Structure alone didn't help.** Semantic views and a business ontology, each as the only way in, scored near bare schema, and the ontology took over five minutes a question <!-- E76 E77 -->.

## What teams try first {#ch02-didnt-work}

Most teams build the prose forms first. We did too. None of it gave the agent a decision it lacked.

| What teams try | What happened | What worked instead |
|---|---|---|
| Table and column descriptions | Accuracy barely moved <!-- M43 --> | The table's own definition, its DDL |
| Semantic views or a join graph | Questions across several tables stayed mostly wrong <!-- E17 E18 --> | Past queries that show the join working |
| Better table search | The agent found the right tables more often; its answers did not improve <!-- E21 --> | Past queries served alongside the tables <!-- E70 --> |
| Embedding search | Worse than plain keyword matching, 55.1% to 68.2% <!-- E61 --> | Ranking on the field names themselves |
| Profiling the data | Twice the cost, and more confident wrong answers <!-- E20 --> | Serving past queries whole instead of cut short <!-- E12 --> |
| Loading everything into the prompt | Lower accuracy at twice the cost <!-- E11 --> | A handful of relevant items per question |

More documentation, glossary prose and a sharper retriever on top of metrics added little or nothing <!-- E16 E19 E09 -->.

## Where context matters: joins {#results-joins}

::: {.diagram #table-split}
Accuracy on questions one table can answer against questions that need a join, for six setups. <!-- E82 -->
:::

Every setup does well when one table holds the answer. Bare schema already got 64% of those. The setups separate on the 61 questions that need a join. With no context, the agent refused 31 of them outright <!-- E92 -->. Semantic views and the ontology barely moved that. Worked SQL did: past queries reached 61%, and the metrics layer 82%. In a single run of each, the same metrics served as prose instead of SQL lost 16 points on joins and nothing on single tables <!-- E14 -->.

Adding context also broke nothing. In a single run of each, every question bare schema got right, the metrics layer got right too <!-- E91 -->.

## By business area {#results-areas}

::: {.diagram #areas}
Questions answered correctly in each business area, on three setups. The grouping into five areas is ours. <!-- E83 -->
:::

The gap is widest where the business has the most private rules. Marketing questions hinge on event rules that no table states: which campaign counts, which touch gets the credit, which contacts are staff. Bare schema solved 1 of 40. Account and usage dashboards read almost straight off the tables, and bare schema already got 17 of 22.

## Worked examples {#results-examples}

Four questions, and how four setups answered them. They show the pattern behind the averages, including where the metrics layer lost.

::: {.diagram #examples}
Four benchmark questions, paraphrased, with the decision each one hides and how each setup did. <!-- E84 -->
:::

The first example is the uncomfortable one. The rule that early-stage deals don't count was in the context three times, and the agent dropped it while adapting the query. A layer can serve the right rule and still lose it to a near-variant, which is why [Phase 3](#ch06) reads traces instead of only adding context. The last example is a gap in the layer: there is no churn metric yet, so every setup counted the wrong field.

## Why the last answers still fail {#results-misses}

The configuration we ship missed 18 of 107: 17 wrong answers and 1 refusal <!-- E55 -->.

::: {.diagram #misses}
The 18 misses of the shipping configuration, by the decision the agent was missing and by how far off it was. <!-- E84 -->
:::

Most misses are rules about which rows belong: a cohort, an exclusion, a population. None came from a wrong literal such as a stage name, because the metric SQL carries those. Four misses landed within 1% of the key, and all four trace to one missing rule that leaves out internal contacts. One added rule would fix four answers, which is how [Phase 3](#ch06) works: find the decision behind the miss, write it once, and score again.

## What each part is worth {#results-parts}

To find what carries the weight, we took the layer apart one piece at a time.

::: {.diagram #ablations}
Accuracy with one layer removed, and with one part removed from each metric. <!-- E85 E86 -->
:::

Removing the metrics or the past queries cost the most. The glossary terms, dimensions and join notes could go with almost no loss. Inside each metric, the SQL carried the value: with the prose stripped out, the score didn't drop, and with the SQL stripped out it fell 8 points.

No single ingredient explains a rescue. Of the 21 questions that SQL turned from wrong to right, none was fixed by literal values alone. The SQL supplied the business values, the right column and the shape of the aggregation together <!-- E87 -->. That is why this book serves whole statements.

## How much to trust a gap {#results-noise}

::: {.diagram #noise}
How much results move between runs. <!-- E88 E90 E42 -->
:::

The same setup run twice moved by six questions, and eight questions changed verdict. So we treat a gap under about seven points as unresolved, and quote the configuration we ship rather than its best run. DoorDash reports a run-to-run spread of about four points on its own data agent benchmark <!-- X16 -->. Some movement is the price of an agent that writes its own SQL.

The union is a warning about cherry-picking. Across all our runs, 105 of 107 questions were answered correctly at least once. A team that keeps the best answer from many runs can report almost any number. Score one run, the way users will meet the agent.

## What others found {#results-others}

Our numbers are from one warehouse. The direction matches what others report:

- **DoorDash's Vera** rose from 43% to 90% on about 1,900 questions across 19 business areas. Its team credits harness and data work over new models, and on 100 questions with the same model, Vera passed 73% where a general coding agent with the same tools passed 48% <!-- X16 -->.
- **Uber** built its agents on [curated workspaces and a golden set drawn from real logs](https://www.uber.com/us/en/blog/query-gpt/) <!-- X01 -->.
- **LinkedIn** found that [about 60% of its questions](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics) had more than one valid answer, which is why grading needs care <!-- X02 -->.
- **Vanna** reported [schema-only accuracy near 3% against about 80%](https://ask.vanna.ai/blog/ai-sql-accuracy.html) with ten relevant example queries <!-- X04 -->.
- **Hex's DataBench** reports cost and latency beside every score, the practice this page follows <!-- X17 -->.

[What others found](#r6) covers the published methods we rebuilt and how they did on our questions.
