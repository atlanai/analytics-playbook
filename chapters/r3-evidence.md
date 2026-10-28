# How we measured {#r3}

[]{#method}

> [!RULE]
> A score means something only when the questions are real, the answers are sealed and the grader is code.

Every number in this book comes from one benchmark we built on our own go-to-market warehouse. This page says what it is, how a run works, how an answer is graded and what it cannot tell you. Use it to judge our numbers, and as a pattern for the golden set you build in [Phase 1](#ch04).

## No hand-written context {#method-automated}

The benchmark had one rule from the start: no person writes the context. From bare schema to the configuration we ship, every metric, past query, join and term the agent saw was built by our own systems from what the warehouse already had: the analyst query log, the catalog and existing documentation. The pipeline mined the definitions, merged the duplicates, ran each metric against the warehouse to check it, and ranked what it kept by how often analysts used it. Where two definitions with the same name disagreed, it held both back. Nobody picked a winner.

People did two things: they wrote the questions and sealed the answers. The one exception is a comparison: the semantic-view setup ran on 40 semantic model files written by hand, because that is how such a layer is built. It scored 38.3% <!-- E76 -->, well below the layer our systems built.

We set the rule because hand-written context doesn't scale. An analyst can tune one domain's context until the score looks good, and the next domain starts from zero. So the scores show what automation reaches on its own. In the benchmark, each metric was mined, checked by running it and ranked by use, with no person approving it. In an engagement, each metric is also reviewed and approved, as in [Phase 2](#ch05). We have not measured what that review adds.

## The questions {#method-questions}

We started from 120 questions our own teams had asked of the data: dashboard tiles, questions from business reviews, and requests that came to analysts. Each one has a single right answer, usually a number, a count or a date. We set thirteen aside because they needed knowledge that sits in no table, query or document the agent could reach, such as the meaning of a list kept only in an event brief. That leaves 107.

They span five areas of a go-to-market business: marketing events and campaigns, sales pipeline and leaderboards, customer success, account and product-usage dashboards, and sales operations. Most ask "how much" or "which ones". None asks "why".

Each question hides at least one decision the schema doesn't state. Six examples, paraphrased:

| The question | The decision it hides |
|---|---|
| As of the date of last quarter's business review, how much open new-business and upsell pipeline did we have? | Rebuild every deal's stage and amount as they stood on that date. Today's values give a different answer. |
| How many customer accounts churned this quarter? | Churn is an event: the account's type changed from customer this quarter. The current type field can't tell you when. |
| What share of agent tool requests were reads? | The business divides reads by reads plus writes, not by every request. |
| How many customer contacts registered for our spring event? | Leave out deleted records and our own employees. |
| How much pipeline did the summit influence? | Count each account once before you sum, or one account's deals are counted several times. |
| How many opportunities entered the first stage after the event? | Use the dated stage-entry field. Creation date and the "after event" flag both give the wrong count. |

Every answer key was written by running the correct SQL against the frozen warehouse and checking the result against the source the business trusts, such as the dashboard or the review deck.

## How a run works {#method-run}

::: {.diagram #bench-flow}
One run, end to end. The agent sees only the question, the tables and the context under test. The grader alone sees the sealed answer.
:::

- **A frozen warehouse.** Every run queries the same read-only copy of the warehouse, so the right answer never moves.
- **One agent, one tool.** The agent gets the question, the context being tested, and one read-only SQL tool. It explores, queries and answers within a fixed step budget.
- **Only the context changes.** Between arms of a comparison, the model, the tool, the budget and the questions stay the same. Only the context in front of the question changes: bare schema, descriptions, past queries, metrics.
- **A firewall.** Each question is split in two. The agent's half holds the question and the table names. The grader's half holds the answer, the correct SQL and the hidden decision. The grader checks the exact prompt of every run and flags any that saw part of the answer.

## How an answer is graded {#method-grading}

Code grades every answer. Nobody reads an answer and decides it is close enough.

- **Numbers** match when they agree within half a percent, so rounding doesn't fail a correct answer. A percentage given as a fraction, or the other way round, still matches.
- **Dates** match on the day, and on the minute when both sides carry a time.
- **A refusal is a miss.** "I can't determine this" scores the same as a wrong number. An agent that refuses often looks careful and still fails the business.
- **One boundary case** gets a small band: a trailing 90-day window where three start dates are defensible.

## How to read the numbers {#method-reading}

- **Runs vary.** The same setup run twice moved by six questions out of 107, and eight questions changed verdict. Treat a gap under about seven points as unresolved.
- **We quote the configuration we ship.** Results for other configurations are separate comparisons.
- **One model by default.** Most comparisons use GLM-5.2. The model chart in [Why analytics agents are hard](#ch01-models) and the Sonnet ablation chart name their models.
- **Cost and time are recorded.** Every run logs tokens, cost and seconds per question, so a better score can be weighed against what it costs.

## What it can't tell you {#method-limits}

It is one warehouse, in one business, with our own analysts' questions. Expect your absolute numbers to differ, and the order of what helps to hold: past SQL beats documentation, and metrics add to both. The questions are about what happened, not why, and the set does not measure why-questions.
