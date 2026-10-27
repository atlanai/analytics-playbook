---
for: eval owner, graders, sponsor, agent builder
produces: what a trustworthy golden set looks like, and how it is graded
---

# Evals first {#ch-evals}

> [!RULE]
> Build the golden set before you build any context. Without it, you can't tell progress from luck.

::: {.tldr}
- **Short version.** A golden set is a fixed list of real questions with sealed answers, scored the same way after every change. Each row has six required fields, four properties make the set worth trusting, grading runs in layers, and the set reruns on every change like a test suite.
- **Do this.** Seal 20 real questions with verified answers before you write any context.
- **Skip if** you already rerun a sealed answer key on every change. [Phase 1](#ch04) has the build steps.
:::

[Why it is hard](#ch-evals-questions) makes the case for a golden set: without one, every claim about the agent is an impression.

::: {.diagram #evals-why}
Four questions only a fixed test can answer. Each one comes up in every phase and after launch.
:::

[]{#ch-evals-noise}A right answer once isn't a capability either. Run each question three to five times and read the pattern. Right every time: the agent knows the decision. Right some of the time: it is guessing at a decision nobody gave it, and the disagreement is a signal in its own right. Never right: something is missing from the context. Whole scores move between identical runs too, so judge a change by its effect on the whole sealed set, never on the question you were looking at, and treat a gap smaller than the run-to-run spread as unresolved: [How much to trust a gap](#results-noise). Every later step in this book is measured against the golden set, so it comes first. This is what a trustworthy one looks like.

## One row of the golden set {#ch-evals-row}

Each row has [six required fields](#r2-3). Three of them do the core work, and each has one job:

| Part | Example | Its job |
|---|---|---|
| The question, in the business's words | "What's open pipeline with our top 100 customers?" | The only part the agent sees |
| The SQL that produced the answer | Reference SQL a grader wrote and verified, with its filters | Graded second, after the result: does the agent's SQL make the same decisions? |
| The sealed answer | $412M | Graded first, within a tolerance |

## What makes an eval worth trusting {#ch-evals-good}

Four properties. Miss one and the score stops meaning what it says.

- **Representative.** Take real questions from the board pack, the dashboards and analyst requests, in the business's words, and keep the hard half. On bare schema, our questions that one table answers scored 64%, and the ones that need a join scored 11.5%. With the metrics layer, they scored 93% and 82% <!-- E82 -->. A set of easy questions hides most of the difference between setups.
- **Not dominated by one fact.** No single rule should be able to swing the headline. In our set, four questions turned on the same missing exclusion rule <!-- E84 -->. Know which questions share a decision, so one fix isn't read as broad progress.
- **Live.** Questions grow out of real use, and the ones that broke before stay in. Anthropic's guidance for agent evals is to build tasks from real failures and read the transcripts, not just the pass rate <!-- X15 -->. Answer keys have errors too: experts re-checking two public benchmarks found errors in more than half the samples they read <!-- X11 -->. Have two graders check every key before it is sealed, and correct a wrong key when you find it.
- **Sealed.** Each answer is computed by running the correct SQL and checked against the source the business trusts. Keep the answers away from whoever builds the context and from anything the agent can reach. If any part of the pipeline can see the answer, the agent will find it.

## Grade the answer, in layers {#ch-evals-grade}

Two different queries can both be right. LinkedIn found [about 60% of its questions](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics) had more than one valid answer <!-- X02 -->. So grade the answer, not the SQL text, and grade it as a stack of checks:

1. **The value.** Code compares the answer with the sealed key, within a tolerance.
2. **The logic.** A grader checks that the SQL makes the item's decisions. A wrong query can land near the right number by luck. Read the trace to see why an answer was right or wrong.
3. **The shape.** A judge checks that the answer is the kind of thing asked for: a number, a list, a date.
4. **Leaks.** Check that no prompt carried any part of the answer.

Count refusals apart from wrong answers, and count both as misses. An agent that refuses often looks careful and still fails the business.

## Evals are the agent's CI/CD {#ch-evals-ci}

An agent changes every time its context changes: a new metric, an edited rule, a renamed column, a new model. Each change can fix one answer and break another. Rerun the golden set on every change, before the change reaches users, and keep the change only if nothing that passed has broken. That is what lets a team keep improving the agent after launch without being afraid to touch it.

The eval's real output is a work queue. Never patch the context for one question. Read each miss as one of three things: a definition never written, one written but never served, or one served and ignored. [Phase 3](#ch06) works through that list.

Read more: [Phase 1: build the golden set](#ch04)
