---
for: context engineer, domain owner, agent builder, sponsor
produces: what a metric is, where each kind of knowledge goes, which lane a question takes
---

# The metric is the unit {#ch02}

> [!RULE]
> Write each business rule into a metric's SQL.

::: {.tldr}
- **Short version.** A metric is every decision a number depends on, sealed into one statement that runs, with an owner and a version. Each kind of knowledge has one place to live, and SQL beats a sentence wherever both would do. Keep the semantic layer you have; organize the agent's context around the metric. Some questions need one governed number, others need exploration, so the agent works in two lanes.
- **Do this.** For each business rule, decide where it lives: in a metric's SQL, in a trusted past query, or in a one-line rule.
- **Skip if** you've decided to build metrics and want the steps. Go to [Phase 2](#ch05).
:::

[]{#ch02-metric}A metric is every decision a number depends on, sealed into one statement that runs. A formula such as `SUM(amount)` is one part of it. On its own, that formula produced the wrong $18.4M in [Why it is hard](#ch01-query).

::: {.diagram #closure}
A metric. Population, grain, time rule, formula and exclusions each settle one decision, and each points at the clause in the SQL that carries it.
:::

Leave any part out and the agent guesses it. Take the engagement's pipeline question: "How much open pipeline do we have with our top 100 customers?" The metric that answers it settles five things no table states:

- Top 100 means the highest current ARR.
- Some early stages never count toward pipeline.
- The amount is ARR, not total contract value.
- Each open deal counts once, however many contract terms it spans.
- The number is taken at the quarter-end snapshot.

Before the metric existed, the agent guessed each of these and returned $1.31B. With the metric, it returned $412M: 340 deals on 91 of the top 100 customers.

A metric has one more advantage: the business already understands it. A sales leader can read "open pipeline with the top 100 customers, by current ARR" and say "that's wrong, we rank by bookings." Nobody can say that about a table description or a prompt. When the unit of context is a metric, the business can correct and approve it directly, so the feedback loop stays short. That review time is the real cost of this method, which is one reason to work one domain at a time.

Metrics also change. Stage names move and fiscal rules get redefined. So every metric carries an owner and a version, and every agent reads the same copy.

## SQL, not a sentence {#ch02-form}

The same rule can reach the agent in two forms. As a sentence:

> Open pipeline is the value of new and upsell deals that are still open, leaving out the earliest stages and internal or test accounts, taken at the end of the quarter.

And as SQL, where each line settles one part of that sentence:

```sql
-- taken at the end of the quarter
WHERE o.as_of_date = :quarter_end
-- leaving out the earliest stages
  AND o.stage_order >= 2
-- new and upsell deals that are still open
  AND o.type IN ('New Business', 'Upsell')
  AND o.is_closed = FALSE
-- no internal or test accounts
  AND a.is_internal = FALSE
  AND a.is_test = FALSE
```

::: {.diagram #sql-vs-prose}
The same metric served as SQL and as prose, on the same multi-table questions. Only the form changed. In a single run of each, the SQL scored 16 points higher. <!-- E14 -->
:::

On single-table questions the two forms tied. The more decisions a question carries, the more a sentence leaves the agent to translate, and every translation is another guess.

## Where does each kind of knowledge go? {#ch02-placement}

Find the knowledge you are holding in the first column. Put it where the second column says.

| Knowledge | Where it goes | Example |
|---|---|---|
| A number the business runs on | Metric: SQL, owner, provenance | Open pipeline with the top 100 customers, with "some early stages never count" written inside |
| How analysts actually answered a long-tail question | Trusted past query, with provenance: who ran it, how often, when | "Deals pushed past quarter end" |
| A house rule that applies across many metrics | Rule: one short line the agent must follow, also written into each metric it touches | "Quarter means fiscal quarter"; "top 100 customers means highest current ARR" |
| Internal names and jargon | Business term | Project names such as "Project Alpha", internal product names, team codenames |
| What a table is and what one row means | The DDL itself | `CREATE TABLE` plus a comment on the grain |
| Why a number moved | Ontology plus a dated record of business changes | A territory realignment, a pricing change |

Two rules settle most ties. If a fact could go in two places, use the one that can run: SQL beats a sentence. A rule that touches one metric goes inside that metric; a rule that touches many is served as a rule and also written into the SQL of every metric it touches.

Provenance is what makes a past query trustworthy. In the engagement, the slipped-deals question had no metric. It was answered by a RevOps analyst's "deals pushed past quarter end", which many analysts had run many times, recently. That record is why the agent could trust it. A business term then linked the user's word "slipped" to the query, though the two share no words.

> [!STOP]
> **Don't write it as prose.** If you catch yourself writing a paragraph so the agent will understand a table, stop and sort the fact.
>
> - A decision that fits in SQL goes in the metric.
> - A house rule becomes a one-line rule, and goes into the SQL of every metric it touches.
> - What a row means goes in the DDL.

[]{#ch02-jargon}

> [!NOTE]
> **Write down the jargon a new hire wouldn't know.** If your business runs on acronyms, codenames and house shorthand, such as "T1" for the top tier of accounts or "Project Alpha" for a product, the model can't infer them either. Collect them on day one, from the golden-set questions and from what analysts type. Write each as a business term: the word, its spellings and alternate labels, one line on what it means, and a link to the metric, query or entity it names. Its job is to route the user's word to the right item, so don't paste the definitions onto columns as prose. A full set of glossary definitions served that way made no measurable difference <!-- E19 -->.

## Why a metric, and not a view {#ch-sv}

[]{#ch-sv-gap}[]{#ch-sv-needs}Most teams arrive with a semantic layer of some kind: Snowflake semantic views, Databricks metric views or a Genie Agent, LookML, or a homegrown metric store. Every layer holds the same four parts: what each table and column means, how tables join, metrics, and the dimensions a metric is grouped by. The question is how to organize them so an agent can use them. An agent puts three demands on that storage: a script with no model in the loop can compile a definition to the same SQL every time; the right item can be found by exact lookup when a metric covers the question and by search when it doesn't; and a fix changes the definition itself instead of piling up beside it as notes.

[]{#ch-sv-layouts}The four parts get organized one of three ways, and each repeats something.

| Organized by | How it works | What gets repeated | Where a question starts |
|---|---|---|---|
| Per table | Each table carries its own description, keys, and any joins or metrics that touch it. A catalog works this way | Joins and metrics that span tables | A table name, which the business does not speak |
| Per logical table | Tables are grouped into one business-facing view, such as "Orders", with its own joins, metrics and dimensions. Snowflake semantic views and Genie Agents work this way | Table meanings, joins and metrics, across views | An entity; the agent answers only inside the view it was given |
| Per metric | The metric is the unit. Its formula, filters, joins, dimensions and verified SQL are stored together, and tables are referenced from it | Joins and dimensions, never the metric | The metric, which is where the question starts |

Per logical table is the default today, because it is what the major platforms ship. Its costs show up once agents are asking: a metric that two views need is often defined in each, a question that spans two views has nowhere to go, and a wrong answer gets patched with a note beside the view that the agent reinterprets on every question. On our benchmark, semantic views as the only way in scored 38.3% <!-- E76 -->. On multi-table questions they scored 16%, against about 61% on the same questions for past queries with complete SQL <!-- E18 -->. A view states a join; a past query shows it worked.

[]{#ch-sv-metric}Business questions start with a metric. People ask how many orders came in last week or what churn did last quarter; they rarely start from a table or a view. A per-metric layer stores context in the shape the questions arrive in: the business can read a metric and correct it, the same definition serves every agent and BI tool, and it compiles to the same SQL every time. Its costs are real too. Questions no metric covers fall back to exploration, so coverage builds over time, and without review, metrics sprawl into near-duplicates such as revenue, net revenue and recognized revenue.

::: {.diagram #sv-start}
Logical-table first asks the agent to pick a view, and the same metric lives in several. Metric-first starts at the one definition the question names, with its formula, verified SQL, named joins, dimensions and drills.
:::

[]{#ch-sv-start}If you have semantic views, keep them. They keep working for the analysts who use them, and in [Phase 2](#ch05) they are a source: their measures and filters become candidate metrics alongside past SQL, witnessed and approved like any other. Five questions show quickly whether a layer will hold up once agents are asking:

1. When a metric definition changes, how many places have to change with it?
2. Can an agent answer a question that spans two of your views?
3. For a question your metrics cover, does the layer compile the SQL, or does the agent write it fresh?
4. Does the same request compile to the same SQL, with no model in the loop?
5. When someone corrects a wrong answer, does the fix change the model, or get added beside it as text?

Read more: [Semantic layers compared](#r7), the tools side by side and one model in six syntaxes

## Two lanes {#ch02-lanes}

The placement table says where knowledge goes. The lanes say how the agent may use it. For each kind of question, ask one thing: if this answer is wrong and nobody notices, where does it land?

::: {.diagram #lanes}
The two lanes. Numbers the business runs on take the governed lane: a metric or no answer. The long tail and diagnostics take the exploratory lane: the agent writes SQL grounded in trusted past queries and shows its sources.
:::

In the governed lane, the agent serves a metric or gives no answer. The number must be exact, every time. The pipeline question took this lane and returned $412M, the number in the board pack.

In the exploratory lane, the agent writes its own SQL from trusted past queries and business terms. It shows the SQL and what it assumed. The answer has to point the right way. The slipped-deals question took this lane: 96 deals had slipped, and the win rate with these customers was 31% against 24% elsewhere.

Good context alone doesn't make a board number safe. Even the best run still got some answers wrong, and it stated them as plainly as right ones. In the exploratory lane, a reader can see the SQL and catch a miss before acting. A board number has no such reader, so it needs the governed lane. A kind of question can move lanes later: when two people publish different numbers for an exploratory question, write the metric and move it to the governed lane.

Card: [Which lane?](#c7)
