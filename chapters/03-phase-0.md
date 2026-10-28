---
for: sponsor, domain owner, platform owner, security lead, delivery lead
produces: the domain brief, the access list proved, the agent architecture, a working trace export
---

# Phase 0: before the clock {#ch03}

> [!RULE]
> Start with one domain. It is small enough to finish, and its open questions have someone who can settle them.

::: {.tldr}
- **Short version.** Pick one domain, write a one-page brief with the bar the agent must clear, and prove every access item works before the clock starts. Then build the smallest harness that records every step the agent takes.
- **Do this.** Write the brief, with one bar for the whole golden set: a pass rate, on every run.
- **Skip if** the domain, the bar and access are already settled. Go to [Phase 1](#ch04) once the minimum harness exists.
:::

::: {.scene week="Phase 0"}
The CRO asked for one thing: a pipeline number for the top accounts that matches Finance every time. In a 90-minute kickoff, the team chose sales as the domain and wrote a one-page brief with the RevOps lead and the FP&A partner.

Getting access took the next two weeks. Warehouse access and query history arrived within days. The slow part was recording what the agent does on each question: the chat tool kept only a daily summary, so the team added a record of every step. Phase 1 started once one question could be followed from start to finish.
:::

An answer is only right against a bar set before any result exists. Phase 0 picks the domain, writes the bar down and opens the access every later fix depends on. The work is small and the waiting is long. Plan for about two weeks.

> [!NOTE]
> **Building in-house, or with a partner?**
> Phase 0 is written so it works either way. If your own team builds the agent on your own systems, three parts are optional:
>
> - **The security review of what leaves the building.** It matters when a vendor or outside team handles your data or runs part of the stack.
> - **A separate delivery lead and context engineer.** In-house, your program lead runs the sessions and an analytics engineer generates and tests the metrics.
> - **The signed checklist.** Prove each access item with its test either way; the formal sign-off is for engagements with an outside team.
>
> Access takes longest when an outside team needs it. In-house, Phase 0 can take days.

Pick one domain: a bounded set of questions, asked by known users, over known tables. Sales pipeline, finance close and support analytics are good first domains. Choose the one with real questions the business already asks, past SQL or dashboards on its tables, and someone with time to settle its definitions. Three domains at once give you three half-built golden sets and nobody with time for any of them.


## The brief {#ch03-brief}

The brief is one page. It fixes the domain, the users, the problem, the bar and which questions need an exact answer. Phase 1 harvests questions only from inside it. It is written at the kickoff, and the sponsor sets the bar in it.

::: {.template #ch03-brief-preview file="domain-brief.yaml" title="Domain brief, short form"}
The sales team's brief, as agreed at the kickoff.

```yaml
domain:       Sales pipeline
fiscal_year:  ends 30 June
as_of:        the last quarter-end snapshot        # every answer in the golden set uses it

users:        CRO staff, sales leaders, RevOps analysts, FP&A partners
asks_in:      the chat tool sales leadership already uses

problem: >
  Leaders get pipeline numbers that disagree with FP&A.
  Each disagreement costs an analyst a day to reconcile.

owners:
  - RevOps lead: deals, stages, amounts
  - FP&A partner: who the top accounts are
graders:      a RevOps analyst and an FP&A analyst
model:        the one expected in production, named with its version

bar:          9 in 10 golden-set questions right, on every run

governed:     open pipeline, win rate, closed-won ARR    # a metric or no answer
exploratory:  slippage, pipeline creation, stage aging   # SQL shown with the answer
deferred:     why-questions, until the numbers are right
out_of_scope: bookings forecast, commissions, marketing attribution

```
:::

[]{#ch03-lanes}The bar is one pass rate for the whole golden set, met on every run. The sponsor writes it down now, before any result exists. The brief also says which kinds of question the agent answers in the governed lane at launch and which in the exploratory lane. That is how the agent answers users; every golden-set question is graded the same way. If another team owns part of a definition, list both owners. When the two meanings of "top 100 customers" collided in Phase 3, both people who could settle it were already in the brief.

Read more: [the full domain brief template](#r2-2)

## What you need before you start {#ch03-checklist}

This is the checklist for Phase 0: the system access. Most delays in Phase 0 come from access, so request every item on the first day. Each item is done when its test passes. A statement that access "should work" is not a pass.

::: {.diagram #access-checklist}
What you need before Phase 1: five access items, each with its test.
:::

Trace export is the item most often left until last, and the one the hill climb depends on. In Phase 3 the trace is where you see which decision the agent guessed. A nightly summary does not count, because it reports what the agent said it did. You need a record of every call, with what was served and what SQL ran.

Read more: [What you need before you start](#c11)

## People and hours {#hours}

[]{#ownership}Each role covers one part of the work. The hours are indicative; adjust them to your domain, but never to zero.

| Role | Its part | Phases 1-4 | After launch |
|---|---|---|---|
| Exec sponsor | Sets the bar; decides at each gate | The kickoff, a 30-minute readout in each phase, the gates | Each release |
| Domain owner | Reviews metrics, past queries and rules; settles the conflicts provenance can't | 2-3 h/week, most of it in one working session | 1-2 h/week |
| Co-owner from another team | Definitions that span both teams | About 1 h/week in Phases 2 and 3 | As conflicts need |
| Eval owner and graders | Seal the golden set; audit the grading | 6-8 h in Phase 1, then about 2 h/week | About 1 h/week |
| Agent builder | The harness and the model | About 20 h/week until the baseline, then 4-6 | Runs the loop |
| Platform owner | Access, trace export, the tables | Phase 0, then on call | On call for schema changes |
| Security lead (if data leaves your environment) | What leaves the building | Phase 0 | Reviews changes to data handling |
| Context engineer (in-house: an analytics engineer) | Generates and tests candidates; never sees an expected answer | Dedicated | Hands over in Phase 4, or stays on |
| Delivery lead (in-house: your program lead) | Runs every session and gate | Every session | Runs the handover |

The co-owner's hour is the line teams forget, and the agent builder's 20 hours is the line they underestimate.

::: {.diagram #swimlane}
Who does what, phase by phase. A gate closes each one.
:::

## The agent architecture {#ch03-architecture}

Every analytics agent has four parts: the surface where people ask, the harness that runs the loop, the model, and the context it reads before it writes SQL. That context lives in a context layer: the store of metrics, trusted past queries, rules and terms that the agent calls once per question. It can be files in a repository behind a small search function, or a product. You choose between two shapes for the rest.

- **Platform-native.** The warehouse vendor supplies the harness and the surface. Databricks Genie and Snowflake CoWork (formerly Snowflake Intelligence) are the common ones. You configure; you do not build.
- **Custom.** You build the harness on a framework such as Google ADK or LangGraph, or write your own. You get full control of the loop, the tools and the traces.

::: {.diagram #agent-architectures}
The four parts of an analytics agent, in both shapes. The surface, harness and model differ. The context layer plugs into the same place in each.
:::

In either shape, the harness runs in your environment and your team owns it after launch. Pick the model you expect to use in production. You can change it later, as long as you rerun the golden set on the new model before you compare scores.

## The minimum harness {#ch03-harness}

Build this and stop.

1. One context call per question, before any SQL. At baseline it returns the schema only.
2. One read-only SQL tool. Exploratory queries run as the asking user; governed answers run under a fixed service identity, so a board number is the same for every asker.
3. A step budget: a fixed cap on tool calls per question. Ten is a sound default. Leave it there; Phase 3 explains why.
4. A per-call trace: everything served, every tool call and SQL statement, the answer or refusal, tokens and time.


Fix the shape of the context call on the first day. In Phase 2 the metrics and trusted past queries arrive behind the same call, and nothing else in the harness changes. That is what keeps the baseline and the later scores comparable.

## What leaves the building {#security}

This section matters when a vendor or outside team handles your data or runs part of the stack. Security will ask what data moves, and where. Walk them through this diagram at the kickoff.

::: {.diagram #data-flows}
What moves and where it goes: result rows go from your warehouse to your harness and model, past SQL is read for context, and definitions and past queries are served to the agent. The metrics agent is any model-driven script that drafts candidate metrics from past SQL in Phase 2.
:::

Result rows never pass through the context layer. Every context call is logged, so security can audit what was served.

## Gate 0 {#ch03-gate}

Brief agreed, every access item proved. The sponsor sees the brief and the access tests, and decides whether to start the clock.

> [!DONE]
> - [ ] One domain chosen, with someone who can settle its open questions
> - [ ] The brief agreed: users, problem, the bar, governed and exploratory questions, out of scope
> - [ ] One bar for the whole golden set, a pass rate on every run, written before any result
> - [ ] Every access item proved by its test, including one trace read end to end
> - [ ] The agent architecture recorded: platform-native or custom, and which model
> - [ ] If data leaves your environment: security has walked the data-flow diagram and approved it
> - [ ] The minimum harness is planned, due before the baseline

Card: [The sponsor's ask](#c2)
