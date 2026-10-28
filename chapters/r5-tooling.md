# R3. Tooling and sources {#r5}

> [!RULE]
> The method runs by hand. Tooling changes the upkeep, never who decides.

This page holds how to run every step on your own stack, the context-call contract, the external sources behind the book, and how the book itself changes.

## Running it on your own stack {#r5-tooling}

Keep one file per context object in version control, in the formats of [the templates](#r2), with a required approver. Generate and witness candidates under a read-only identity with a script, keep conflicts in a spreadsheet with each variant's provenance, and give the harness a retrieval function it calls before any SQL. Log every call with what was served and its version. Grade with a value-matching script, then read the SQL of every item that passes. Keep the iteration ledger in a shared sheet, tag each release with its eval results, and rerun the regression set on every context change and schema change. The method and the gates are the same either way.

### The context-call contract {#r5-contract}

This is the shape between a harness and a context layer, whoever builds either side. It is a design we have not benchmarked. [The builder's minimum harness](#c4) puts a harness around it, and [the templates](#r2-22) have a filled example.

::: {.diagram #contract}
One call per question, before any SQL. The shape stays fixed from the baseline on, so the scores compare.
:::

The call goes in with the question text unedited, the domain to search, and the user's identity, passed through. It comes back with metrics (name, version, complete SQL, owner, provenance), the top trusted past queries as complete SQL, the rules that apply, the business terms the question matched, and which lane the question falls in. On a governed question with no matching metric, the harness refuses: no metric, no answer. When a metric answers, the harness runs its SQL as served, filling only declared parameters. The case for that is consistency: the same number on every run, and no long statement broken in the retyping.

## Sources {#r5-sources}

Every external source the book draws on. Any number quoted is the source's own.

| Source | What to take from it |
|---|---|
| [Uber, QueryGPT](https://www.uber.com/us/en/blog/query-gpt/) | Scope agents to curated domain workspaces and build the eval from real query logs. |
| [LinkedIn, Practical text-to-SQL for data analytics](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics) | Many questions have more than one valid answer, so grade for alternatives. |
| [Pinterest, text-to-SQL at Pinterest](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff) (numbers via [this summary](https://www.getdot.ai/blog/pinterest-text-to-sql-querybook)) | Table documentation lifted table-search hit rate. It measured retrieval; in our runs better table search did not raise accuracy. |
| [Vanna, AI SQL accuracy](https://ask.vanna.ai/blog/ai-sql-accuracy.html) | Relevant examples beat schema alone by a wide margin. A vendor blog on a small set. |
| [Spider 2.0](https://spider2-sql.github.io/) ([paper](https://arxiv.org/html/2411.07763v2)) | Enterprise workflows break models that do well on academic sets. Date any leaderboard figure. |
| [BIRD](https://bird-bench.github.io/) ([paper](https://arxiv.org/abs/2305.03111)) | External knowledge helps. Its hints are written per question, not kept as a definitions library. |
| [Databricks, production-ready Genie spaces](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way) and [Genie best practices](https://docs.databricks.com/aws/en/genie/best-practices) | A worked climb with a gate before user testing, and example SQL over text instructions. Its perfect score is on 13 questions. |
| [Snowflake, semantic views for Cortex Analyst](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/) | Start with a small set of verified queries; compare its production checklist with ours. |
| [DoorDash, Inside Vera, DoorDash's data agent](https://careersatdoordash.com/blog/inside-vera-doordashs-data-agent/) | An in-house data agent graded on 1,900 contributed questions across 19 business areas. Harness and context work mattered more than the model. Graded by a model judge, not by code. Checked 2026-10-02. |
| [Hex, DataBench](https://hex.tech/databench/) | A public benchmark for data agents that reports cost, tokens and latency beside each score, and publishes example tasks with their grades. A pattern for showing results. Checked 2026-10-02. |
| [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Build tasks from real failures, split capability from regression, and read transcripts. |
| [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Serve the smallest set of high-signal context, retrieved just in time. |
| [OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | Run evals for a baseline first, then reach the target, then cut cost; keep tools few and well defined. |
| [OpenAI, AI in the Enterprise](https://cdn.openai.com/business-guides-and-resources/ai-in-the-enterprise.pdf) | Start with evals. Its case studies give no denominators. |
| [Looker, Conversational Analytics best practices](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices) | A placement rule: what belongs in the semantic model and what in agent instructions. |
| [Snowflake semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/overview), [CREATE SEMANTIC VIEW](https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view) | Metrics are named per logical table and bounded by the view; verified queries sit at view level. Checked 2026-10-27. |
| [Databricks metric views](https://docs.databricks.com/aws/en/uc-semantics/metric-views/), [Genie](https://docs.databricks.com/aws/en/genie/) | A metric view is rooted on one source table and can join several levels deep; a Genie Agent (formerly a Genie space) holds up to 50 tables, views or metric views. Checked 2026-10-27. |
| [Looker LookML](https://docs.cloud.google.com/looker/docs/lookml-terms-and-concepts), [drill_fields](https://docs.cloud.google.com/looker/docs/reference/param-field-drill-fields) | Measures in views, joins in explores, drill paths on the measure; joins named once. Checked 2026-09-29. |
| [dbt MetricFlow](https://docs.getdbt.com/docs/build/metrics-overview), [entities](https://docs.getdbt.com/docs/build/entities) | A top-level ratio metric can combine metrics from different semantic models. Checked 2026-10-27. |
| [Malloy sources](https://docs.malloydata.dev/documentation/language/source), [Cube data modeling](https://docs.cube.dev/docs/data-modeling/overview), [Cube joins](https://docs.cube.dev/docs/data-modeling/joins), [Apache Ossie (formerly OSI) core specification](https://github.com/apache/ossie/blob/main/core-spec/spec.md) | Where each puts the metric: in a source; in a cube that reaches other cubes over multi-hop joins; in a dataset or beside datasets in one model. Checked 2026-10-27. |
| [Google SRE book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) | Blameless postmortems with an explicit trigger list. |

## Contributing {#r5-changes}

The playbook is versioned like the context it describes. Published by Atlan. Maintained by Atlan AI Labs, who approve every merge and keep the source evidence current.

### How to propose a change

1. Open a pull request against the chapter file in `chapters/`, one topic each.
2. Source every number. An internal benchmark number names its ledger arm, n and run date. A field result is anonymised and says so. An external claim carries its URL. The maintainers assign evidence IDs; contributors never mint one.
3. Keep to the method. A new phase, framework or practice needs a source: our own work, or an external guide cited with an X-ID and labelled external.
4. Keep the conventions. Chapter shape, callouts and roles follow the authoring guide, and the [glossary](#r4) is the vocabulary. All SQL runs on DuckDB.
5. Keep the invariants. No customer, system or people names. The company owns and runs the harness and the model. No page carries product status labels.
6. Keep the method map in step. The map on [the lifecycle page](#lc-tasks) restates each phase's steps, owners, templates and cards in short form. If your change renames, adds, removes or reorders any of them, or changes a section the map links to, update `diagrams/method-map.html` in the same pull request. The build checks the map's links, not its words, so a stale map still passes.
7. Rebuild with `python3 build.py --check`, read the changed chapter, and add a line to `CHANGELOG.md` in the repository.

Report a field result that contradicts the playbook the same way, with its evidence. Negative results are as welcome as positive ones.
