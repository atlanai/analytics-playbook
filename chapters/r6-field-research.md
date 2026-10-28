# What others found {#r6}

Other teams have shipped analytics agents and written up what worked, and researchers have tested the same ideas on public benchmarks. Read that work for its mechanisms. Each source ran on a different warehouse, with different questions and its own definition of a right answer, so its scores won't transfer to yours. The last section shows what happened when we rebuilt eight of these methods on our own benchmark.

## Past queries and examples {#r6-examples}

**Uber, QueryGPT.** [Uber](https://www.uber.com/us/en/blog/query-gpt/) scopes each agent to a curated workspace for one domain and builds its golden set from real query logs. <!-- X01 --> Both ideas carry over. A small, curated scope beats the whole warehouse, and the questions worth testing are the ones people already ask.

**[Pinterest, text-to-SQL in Querybook](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff).** Pinterest summarises its tables and past queries, embeds the summaries, and retrieves by similarity before writing SQL. It reported that table documentation raised its table-search hit rate from 40% to 90%. <!-- X06 --> That number measures finding the table. In our runs, better table search left accuracy flat <!-- E21 -->, so judge a retriever by the answers it leads to.

**Vanna.** A vendor test found [schema-only prompts about 3% accurate, and about 80%](https://ask.vanna.ai/blog/ai-sql-accuracy.html) with ten relevant example queries. <!-- X04 --> It is a small set run by a vendor. The direction matches our ladder, where past SQL was the largest single step.

**[Automatic metadata extraction (arXiv 2505.19988)](https://arxiv.org/abs/2505.19988).** This paper extracts context three ways: profiling the data, analysing the query log, and having a model describe each past query in plain words. Profiling alone took first place on the BIRD leaderboard, because BIRD ships no query log. <!-- X12 --> For an enterprise, the query log is the part to study, since you have one and BIRD doesn't.

## Governed metrics {#r6-metrics}

**[Lyft, Metric Semantic Layer](https://eng.lyft.com/metric-semantic-layer-how-lyft-governs-and-scales-key-data-definitions-56bee3643c29).** Lyft keeps each widely used metric in one versioned package: a YAML definition, a SQL template and two owning teams. A business owner answers for the definition, an operational owner for the data behind it, and every change needs both. A metric qualifies only with at least two distinct uses. <!-- X05 --> The same definitions feed dashboards, data quality checks, ML models and an MCP server that hands agents the SQL. Lyft says agents answer metric questions more accurately with it, and publishes no figure. This is the closest public match to the metrics in this book, down to the owners.

**[OpenAI, in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/).** OpenAI describes an internal agent that combines warehouse metadata, business context, table knowledge drawn from code, and memory of past analyses. When an intermediate result looks wrong, the agent investigates and tries again. <!-- X07 --> Read it as a design description of what a production data agent draws on, since it gives no score on a fixed question set.

## Retrieval, evidence and checks {#r6-retrieval}

**[CHESS (arXiv 2405.16755)](https://arxiv.org/abs/2405.16755).** Four agents split the work. One searches an index of the database's actual values and descriptions, one prunes the schema, one writes and revises candidate queries, and one writes unit tests to choose between candidates. It reported 71.10% on the BIRD test set, within 2% of the best proprietary method with about 83% fewer model calls. <!-- X08 --> The value index is the part to borrow: it finds literals such as status codes and tag names that no description mentions.

**[SEED (arXiv 2506.07423)](https://arxiv.org/abs/2506.07423).** BIRD supplies a hand-written hint with each question. SEED has a model read the schema, descriptions and sample values and write those hints itself. Its authors report a clear gain over no hints, and sometimes over BIRD's own. <!-- X13 --> The risk for a practitioner is that a generated hint reads as fact whether or not it matches the data.

**[Anthropic, context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).** Anthropic's guidance for agents is to serve the smallest set of high-signal context the task needs, retrieved when the agent needs it, instead of loading everything up front. <!-- X14 --> Our runs agree: loading the whole metrics layer into every prompt scored 52%, and serving a handful of items per question scored 83% at under half the cost per right answer <!-- E11 -->.

## How to measure {#r6-eval}

**[Anthropic, evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).** Build eval tasks from real failures, keep a capability suite apart from a regression suite, and read the transcripts instead of trusting a pass rate. <!-- X15 --> This is the golden set, the regression rerun and the raw trace of this book, arrived at from the agent side.

**LinkedIn.** [About 60% of more than 130 questions](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics) had more than one valid answer. <!-- X02 --> Write answer keys that accept the alternatives, or you will grade correct answers as misses.

**[BIRD](https://bird-bench.github.io/).** 12,751 question and SQL pairs over 95 databases, with a hint of outside knowledge written for each question. At release, ChatGPT scored 40.08% against 92.96% for people. <!-- X10 --> Its hints are written once per question. A library of definitions your team maintains is a different thing, and BIRD scores say little about it.

**[Spider 2.0](https://spider2-sql.github.io/).** 632 tasks drawn from enterprise workflows. The best agent at release solved 21.3%, against 91.2% on Spider 1.0 and 73.0% on BIRD. <!-- X09 --> Enterprise warehouses are much harder than academic sets, so put a date on any leaderboard figure you quote.

**[Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards (PVLDB 2026, arXiv 2601.08778)](https://arxiv.org/abs/2601.08778).** Experts re-checked samples and found annotation errors in 52.8% of BIRD Mini-Dev and 62.8% of Spider 2.0-Snow. Correcting them moved system scores by as much as 31% in relative terms, and ranks by up to 9 places. <!-- X11 --> Check your own answer keys before you trust a ranking.

## The overall picture {#r6-picture}

- **Real past SQL is the strongest single input.** Uber, Vanna and Pinterest build on it, and it was the largest step on our ladder <!-- X01 X04 E05 -->.
- **Less context, chosen well, beats more.** Anthropic's guidance and our runs agree: a few high-signal items per question beat the whole layer in every prompt <!-- X14 E11 -->.
- **Generated context helps from a weak start and hurts from a strong one.** SEED and profiling report gains over bare or hint-free baselines. Added on top of our strong context, every method that injected a claim lost accuracy <!-- E74 E75 -->.

## On our benchmark {#r6-results}

We rebuilt each method and ran it once on 107 questions from our own go-to-market warehouse. Most methods ran on top of our metrics layer, so each row measures what the method adds to an already strong setup. That is a harder test than the papers set themselves. Treat a gap under about seven points as unresolved.

| Approach | Source | How it works | Accuracy | Cost per run | Seconds per question |
|---|---|---|---|---|---|
| Intent-embedding retrieval | Pinterest | Past queries retrieved by embedding a model-written description of each query's intent, in place of matching field names. | 66.4% <!-- E71 --> | $5.24 <!-- E71 --> | 68 <!-- E71 --> |
| Metric groups | Lyft | The agent picks a governed metric by name and a renderer writes the SQL. Pilot domains only. | 64.5% <!-- E72 --> | $2.12 <!-- E72 --> | 43 <!-- E72 --> |
| Value index and cross-check | CHESS | An index of every column value, several candidate queries, and unit tests to pick one. | 57.9% <!-- E73 --> | $11.29 <!-- E73 --> | 222 <!-- E73 --> |
| Fused candidates | CHESS, SEED and Companion Agents | Parallel candidate generation from the three papers, combined with unit testing. | 57.0% <!-- E74 --> | $8.14 <!-- E74 --> | 134 <!-- E74 --> |
| Generated evidence | SEED | A model writes hints about the data, served to the agent as fact. | 50.5% <!-- E75 --> | $6.15 <!-- E75 --> | 142 <!-- E75 --> |
| Semantic views | Hand-written semantic models (OSI format) | 40 hand-written semantic model files and no schema. | 38.3% <!-- E76 --> | $4.87 <!-- E76 --> | 146 <!-- E76 --> |
| Data profiling | arXiv 2505.19988 | Column statistics, sample values and inferred joins on top of bare schema. | 34.6% <!-- E20 --> | $2.48 <!-- E20 --> | 64 <!-- E78 --> |
| Ontology in SPARQL | Ontop and R2RML | The agent queries a business ontology in SPARQL, translated to SQL at run time. No schema. | 33.6% <!-- E77 --> | $8.14 <!-- E77 --> | 317 <!-- E77 --> |

For scale, our metrics layer, metric SQL plus trusted past queries served per question, scored 83.2% <!-- E52 -->, and bare schema scored 31.8% <!-- E03 -->. No rebuilt method came close to the metrics layer, and profiling and the ontology landed near bare schema.

Read more: [What we found](#results)
