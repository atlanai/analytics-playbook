---
for: sponsor, agent builder, delivery lead
produces: the four problems this book solves, and where each fix lives
---

# Why analytics agents are hard {#ch01}

> [!RULE]
> Fix the context before you change the model.

::: {.tldr}
- **Short version.** A query can run clean and still give the wrong number, because it misses a rule nobody wrote down, like the fiscal calendar or which deal stages count. One plain question hides several of these decisions, and a stronger model guesses them better but still guesses. Four problems follow, and the table at the end of this chapter shows where the book fixes each one.
- **Do this.** Take one real question and list every decision an analyst would make that the schema doesn't show.
- **Skip if** you already know why your agent's numbers miss. Go to [The method at a glance](#start).
:::

The talk-to-data pilots we see stall between the demo and the tenth real question. The demo question was picked because it works. The tenth comes from a finance analyst on a Tuesday, touches two tables and a house rule, and gets back a confident number that is wrong. Nothing about the answer looks wrong, so nobody catches it. The business decides whether to trust the agent on misses like that one.

## Five steps, and the hard one {#lc-steps}

::: {.diagram #workload}
What happens between a question and an answer. Writing SQL is easy once the agent knows what the question means. Knowing what it means is the hard part.
:::

Every question an analytics agent answers goes through the same five steps:

1. **Intent.** Read the question as asked.
2. **Context.** Work out what it means, and gather every rule that governs it. *The open problem.*
3. **SQL.** Write the query, probing and rewriting as results come back. Easy once the rules are known.
4. **Execute.** Run it against the warehouse. Solved.
5. **Insight.** Narrate the result. Comes later, and needs good context too.

When the agent lacks a rule at step two, it guesses one your company never wrote down: that fiscal Q3 starts in January, that early stages never count toward pipeline, that test accounts are out of every number. Each guess is a fair reading of the schema, the SQL runs clean, and nobody sees the miss until the number reaches the board. The rest of this chapter shows one such miss, why a better model doesn't fix it, and the four problems that follow.

## The tenth question: a correct query, a wrong answer {#ch01-query}

Take one question: "What's our Q3 sales pipeline?" Any good analyst at this company, whose fiscal year ends 30 June, would write this:

```sql
SELECT SUM(o.amount)
FROM opportunity o
JOIN account a ON a.id = o.account_id
WHERE o.close_date BETWEEN DATE '2026-01-01' AND DATE '2026-03-31'  -- fiscal Q3
  AND o.stage NOT IN ('Closed Won', 'Closed Lost')
  AND a.is_internal = FALSE AND a.is_test = FALSE;  -- internal and test accounts are out
```

It returns $18.4M, and it is wrong. The analyst got the quarter right, because they knew the fiscal calendar, and left out internal and test accounts. They missed a rule nobody told them. At this company the earliest stages never count toward pipeline; Finance treats them as noise and leaves them out of every pipeline number. Add one line and the answer changes:

```sql
  AND o.stage_order >= 2   -- early stages never count toward pipeline
```

Now it returns $11.2M, the number Finance plans on.

The first query has no bug. The rule it misses lives in no table, no column and no description. The company made that decision once and never wrote it down anywhere an agent could reach. A syntax error announces itself. A missing rule produces clean SQL and a plausible number, and a reviewer who didn't know the rule would have written the same query.

The demo never meets this question, because the demo asks what the schema can answer. Real users ask what the business needs, and the hard part of their questions is never in the schema.

## What the question means: the intent problem {#ch01-decisions}

The stage rule is one of five decisions hiding in that short question.

::: {.diagram #five-decisions}
Five decisions hide in "What's our Q3 sales pipeline?" At 80% per guess, an agent with a strong model gets all five right about one time in three.
:::

The agent has to decide which stages count, and which rows are always out, such as internal and test accounts. It has to pick the quarter, fiscal or calendar. It has to find the right amount on the right table, because several look alike. And it has to assemble the rows correctly: deduplicated, joined to the account, as of the right date.

The schema states none of these. An `amount` column doesn't say it is the wrong amount.

Now suppose a strong model guesses each decision right 80% of the time, which is generous for a rule that appears nowhere in the data. All five land about one time in three. That is our arithmetic, not a measurement, but it sits close to what we measured on bare schema: 31.8% <!-- E03 -->.

A smarter model raises the 80% a little. It can't reach 100%, because no model can infer a rule nobody wrote down. Meanwhile the exponent grows with the question: a second table or a comparison period adds hidden decisions. Demo questions hide few. Real questions hide more, and the score falls to match.

[]{#ch01-models}If the problem were the model, a better model would fix it. So we ran the same questions on bare schema across five models, and on three models with past SQL as context. Two models ran both ways.

::: {.diagram #model-chart}
Bare schema and with context, per model, on the same questions. On bare schema, five models landed between 31.8% and 42.1%. With past SQL, every model we ran scored above 66%, and Gemini 3.1 Pro reached 73.8%. <!-- E01 E02 E03 E05 -->
:::

Switching models moved the bare-schema score by about 10 points. Adding context moved both paired models by 26 points or more, and the best model on bare schema still lost to the weakest model with context. Use next year's model when it arrives; it will guess better. It still won't know that your Finance team drops the earliest stages from pipeline, because that rule is in no data it can read. Pick a model that finishes its tasks, then put your effort into context. Written down, owned and versioned, it carries over to the next model. A model swap carries nothing over. On our warehouse, it was not a model problem. It was a context problem.

Not every kind of context closes the gap. Descriptions and documentation barely moved the score; metrics built from the past queries your analysts ran moved it most. [The method at a glance](#ch02-ladder) shows the ladder, and [What teams try first](#ch02-didnt-work) shows what didn't work.

> [!NOTE]
> **Find two of your own unwritten rules**
> Take one question your leadership asks every week. Before anyone writes SQL, list the decisions a correct answer needs:
>
> - which stages or states count
> - which rows are always out
> - which period, and as of when
> - which amount, on which table
> - how the rows are assembled
>
> Next to each, write who decided it and where it is written down. An answer that says "everyone knows", or names a person, is an unwritten rule. You are looking for two.
>
> In the running example, the kickoff team did this exercise in ten minutes and found two rules: the earliest pipeline stages never count, and internal and test accounts are out of every number. Writing a rule down is only the first step. Phase 3 shows how the first of these still slipped through until it was written into the metric's SQL.

## Deciding the same way every time: the format problem {#ch02-sql}

Once a rule is written down, the form it takes decides whether the agent follows it. Written as a sentence, "leave out the earliest stages" still has to be turned into SQL by the agent, on every question, and every translation is another guess. Written as SQL, the decision is made once and runs the same way each time. On multi-table questions, the same metric served as SQL beat the same metric written as a sentence by 16 points <!-- E14 -->: [SQL, not a sentence](#ch02-form) shows both forms.

Most teams build the prose forms first: descriptions, glossaries, documentation. We did too. None of it gave the agent a decision it lacked.

## Knowing you are right: the confidence problem {#ch-evals-questions}

In software, QA decides what ships. For an agent, the eval does. Without one, "it works" is an opinion held by whoever built it. An agent with no eval is a demo: it answers the question it was shown, and nobody can say whether it will answer the next one.

Without a fixed test, every claim gets answered by impression. A sponsor sees three good answers in a demo and believes the agent works. A builder changes a prompt, tries two questions, and believes it improved. Both are guessing, and the agent is usually being tested on questions picked because it already gets them right. One run doesn't settle it either: the same setup run twice gives different scores, so [a single run proves little](#ch-evals-noise).

## Four problems, and where the book fixes them {#ch01-fixes}

| The problem | What fixes it | Where |
|---|---|---|
| A clean query returns the wrong number, and nothing looks wrong | Test the agent against real questions with sealed answers, built before any context | [Evals first](#ch-evals), [Phase 1](#ch04) |
| The question hides decisions the schema doesn't show | Generate metrics from the SQL and reports your analysts already run, and settle conflicts before the agent sees them | [The metric is the unit](#ch02), [Phase 2](#ch05) |
| The agent decides differently each time | Seal each decision into a metric's SQL, serve the few that fit each question, and give board numbers their own lane | [The metric is the unit](#ch02-lanes), [Serve per question](#ch-retrieval) |
| Nobody can tell whether it is right | Rerun the sealed set on every change, and fix each miss from its trace | [Evals first](#ch-evals-ci), [Phase 3](#ch06) |

Read more: [The method at a glance](#start)
