---
for: domain owner, eval owner, agent builder, platform owner, exec sponsor, delivery lead
produces: the production loop, drift triggers, the domain-two plan, the ceremonies and the gates
---

# Keep it running {#ch-run}

> [!RULE]
> Feed real usage back into the context, or it goes stale within a quarter.

::: {.tldr}
- **Short version.** After launch, real questions and corrections flow back into the context every week, a schema change triggers a regression run before it reaches users, and the next domain starts from what this one built. Once the numbers hold, the sponsor's why-questions get a second kind of context, kept small. That part is practice, not yet measured. Whoever runs the program keeps the calendar and never decides a definition.
- **Do this.** Book a weekly trace hour and decide the queue in it.
- **Skip if** you haven't launched yet, except [Run the ceremonies](#ceremonies): book that calendar at the kickoff.
:::

Launch is where the agent meets questions nobody wrote down. From here the job changes: keep the context true as the business moves, use what domain one built to start the next one faster, and run the whole thing on gates rather than dates. Your team runs all of it, with no outside help.

## Run the production loop {#ch07-loop}

Your users will ask hundreds of questions the golden set never held. Each one comes with a trace, and the ones that recur are golden-set candidates. Two events in the first weeks after launch show the two halves of the loop.

A regional VP asked for open pipeline with the top customers in EMEA, then replied, "Wrong. My tracker is well above that." The trace showed the metric's SQL, matching the board pack. The VP's tracker counted renewals and early stages the metric leaves out. The correction became a proposed change for the metric's owners, never applied on its own. In ten minutes they kept the board number, added a note under every answer ("excludes renewals and early stages"), and put a renewal-pipeline metric in the backlog.

Then a schema alert fired: billing would retire a deal-amount column. The regression set ran on a staging copy first, and two questions failed. Both leaned on past queries that read the dying column. The agent had rewritten them from the schema and lost the rule about early stages. No user would have seen an error, only a plausible wrong number. The queries were re-issued against the new column, and the rerun came back clean.

::: {.diagram #production-loop}
After launch, two loops keep the context current. Real use turns into proposed changes, decided each week. A schema change triggers a regression run before it reaches production.
:::

Run the loop every week, in one trace hour:

1. Read the raw traces of every flagged answer and a sample of the rest.
2. Pull every step where the agent logged that its context was not enough, and classify each miss.
3. Ask the most common real questions several times. A split between runs means a decision nobody made. File it as a conflict.
4. Decide the queue: corrections, conflicts and gap fixes.
5. Batch the approved changes into the next release and run the gate.

Corrections are the richest signal and the easiest to mishandle. Each arrives sounding like a bug, and often the user simply holds a different definition.

## Rerun the set on every drift trigger {#ch07-drift}

The business moves under the context, and nothing announces the move. A realignment, a pricing change or a retired column changes no line of the context. So handle drift with triggers. A context version with no eval run behind it is still a draft.

| Trigger | What reruns |
|---|---|
| A schema change on any table the context touches | The regression set: the golden-set questions already right on every run. Run it on staging first if you can |
| Any context change: a metric, rule, term or trusted query | The full golden set |
| Any harness change, including its model or instructions | The full golden set |
| A business event: a reorg, a pricing change, a new fiscal rule | The questions on what it changed; the change is recorded with its date |
| A new kind of question in the traces | Nothing yet; it becomes a golden-set candidate |

Keep the previous release deployable, so rollback takes one decision.

## Domain two {#domain-two}

Domain two inherits what domain one built: house rules, shared entities, business terms, the grading method and the release process. Plan it while the knowledge is still in the room.

::: {.diagram #domain-two}
What finance inherits from sales with no new decision, what it builds itself, and the shared words that still need an arbiter.
:::

1. Pick the next domain from those that share tables, entities and words with the first.
2. List what it inherits with no new decision, and what it must build.
3. List the words both domains use, and mark each as settled or contested.

In the engagement, finance came next. It inherited "top 100 customers", the fiscal quarter and the rule on early stages. It still built its own golden set, metrics and queue. Two words were contested. Sales reads "ARR" as the latest term's value, and finance reads it as recognised ARR at period end. Sales counts a customer by an active term, and finance by a paid invoice. Each owner could decide for their own domain, and neither could overrule the other. Name an arbiter before the new domain starts: one executive with authority over both functions. Until then, freeze the contested words, so neither domain changes them alone.

## Answer why {#ch08}

[]{#ch08-order}"Why did pipeline drop in EMEA?" is what an executive asks as soon as the number lands, often at the first readout. An agent with only metrics restates the drop. To explain it, the agent has to know how your business works and what changed in it this quarter. That is a second kind of context, and it is built only after the numbers hold: a why-answer explains a movement in a number, and if the number is wrong, the explanation is a confident story about a figure nobody should trust. Write the why-question down with its date and finish the what-questions first.

> [!NOTE]
> **Practice, not measured.** The benchmark behind this book covers what-questions only. What follows on why-questions is judgment from building the method, and no score backs it yet. Measuring why-answers is the problem we aim to tackle next as practitioners. Until then, treat this as a starting point and test it on your own why-questions.

### A map of the business, and a record of what changed {#ch08-ontology}

The first piece is an ontology: your business drawn as a graph and tied to your data. Its entities are the things the business talks about, such as rep, deal, customer, territory and stage history. The links between them carry rules the agent can reason with: a territory is owned by a rep, and when it changes hands the new rep re-qualifies its deals; a deal re-signed on new terms goes back to an early stage. Each entity points to the tables that hold it and to the metric that measures it, so the agent knows where to compute instead of guessing.

The second piece is a dated record of what changed in the business: a territory realignment, a pricing change, a reorg, a new comp plan, each tied to the entity it touched. Without this, the agent can list every way pipeline might fall and still cannot say which one happened this quarter. A stronger model does not fix that. It can reason about causes, but it cannot test a change nobody wrote down.

::: {.diagram #ontology key="1"}
The slice of the business behind the EMEA answer: five entities tied to their tables, two business rules, two dated changes, and the two causes the agent measured in SQL.
:::

### The EMEA question, worked through {#ch08-emea}

Without this context, the agent summed open amounts by country and returned a percentage. With it, the agent worked in three steps:

1. **Find the possible causes.** The metric showed EMEA down while North America and APAC held. The graph listed what this pipeline moves with: new deals, owner changes, deals re-signed on new terms, and the season.
2. **Rule some out.** New deals were flat, and last year's numbers ruled out the season. The two causes left each matched a dated change: the territory realignment and the pricing change.
3. **Measure the rest in SQL.** Using a trusted past query on days since a deal last changed stage, the agent counted the deals behind each cause.

```text
EMEA pipeline with the top 100 customers fell $53M. North America and APAC held.
New deals were flat, and last year rules out the season.
$31M sits in deals that changed owner in the territory realignment and have not moved since.
$19M sits in Enterprise deals re-signed on new terms after the pricing change, which sent them back to the first stage.
The remaining $3M has no single cause.
```

The one why-answer that fell short in the running example traced to a comp-plan change nobody had written down. Have each change recorded when it happens, by the team that makes it, as part of the weekly work.

### Build it only where systems or history need linking {#ch08-worth}

Metrics carry most of a why-answer. The ontology adds the most where one entity has to be linked across two systems, or where the answer turns on a deal's history. It is the wrong tool for what-questions, and it is one more thing to keep current.

> [!STOP]
> **Don't build an ontology when:**
>
> - The what-questions still fail. Finish the hill climb first.
> - The domain lives in one system with one set of keys. Write the business rules down as rules and stop.
> - Nothing needs linking across systems and no answer turns on history.
> - No team will record what changes in the business, with dates.

If you do build it, keep it small: seal five to ten real why-questions, each with its list of expected findings; import what exists first (the glossary, BI semantic models, any existing ontology) and cut it down to what those questions touch; approve every link an answer depends on; tie each entity to its tables and metric and check each tie runs; serve it for why-questions only, and rerun the what-question regression set on every release.

Card: [Is an ontology worth it?](#c8)

## Run the ceremonies {#ceremonies}

[]{#ch09}The delivery lead, whether a forward-deployed engineer, a partner consultant or an internal program lead, runs the calendar and the ceremonies. The sponsor decides at each gate. The delivery lead never decides a definition and never grades an answer. If the delivery lead makes those calls, the numbers stop belonging to the business, and nobody keeps them accurate after the delivery lead leaves.

Each phase ends at a gate, and each gate is one decision: pass, hold or stop. [What the sponsor sees at each gate](#c10) lists what passes each one. A stop is a legitimate result. Four ceremonies carry the engagement. Book all of them through Phase 4 before the kickoff ends. Each one produces something written.

::: {.diagram #ceremonies}
The four ceremonies on one calendar, from the kickoff in Phase 0 to the launch gate at the end of Phase 4.
:::

| Ceremony | When | Who | What it produces |
|---|---|---|---|
| Kickoff, 90 minutes | Phase 0 | Sponsor, domain owner, eval owner, agent builder, platform owner, security, the delivery lead | Each checklist item agreed, or given a date |
| Working session, 60 minutes | Each phase, weekly if a phase runs longer | Domain owner, agent builder, eval owner, context engineer, the delivery lead | Decisions on conflicts and changes, and the latest score |
| Readout, 30 minutes | Each phase | Sponsor, domain owner, the delivery lead | One page and one decision |
| Gate review, 45 minutes | End of each phase | Sponsor, domain owner, eval owner, the delivery lead | The sponsor's pass, hold or stop, written down |

At the kickoff, teach before you ask. Open with one real question from their business and let the room find the rules hidden in it, using the exercise in [Why it is hard](#ch01-decisions). Then walk the checklist; the full agenda is the [kickoff agenda](#r2-11) template. The working session is where decisions happen, and its agenda is fixed: the score since the last session, the misses read from traces, changes waiting for approval, and conflicts waiting for a decision. The sponsor will ask for things the plan deferred. Log each one in the backlog with a date, and say when it comes back. "Go with conditions" is a pass with debts: check each condition on its date, because one that slips past unchecked has quietly lowered the bar.

## What to do when things stall {#ch09-stalls}

A stall usually shows up first as a date that slips. Treat the slip as the signal, whatever caused it, and make the same four moves: log it the day you see it, with a date; keep working on everything that does not depend on it; take it to the sponsor at the next readout, or the same day if it is both likely and serious; and hold the gate it affects, without absorbing the stall by deciding yourself or starting the next phase early.

| Stall | First sign | Your move |
|---|---|---|
| The domain owner disappears | Conflicts wait a week undecided | Ask for their time back, or a deputy who can decide |
| Access is blocked | A request sits unanswered | Log it; in Phase 0 the clock waits |
| The sponsor moves the bar | A new target in a readout | Record the new bar and its date; score the last run against both |
| Someone asks the delivery team to host the agent | "Just for the pilot" | Decline; the agent runs in the company's environment |
| Scope creeps into a second domain | New questions from another team | Log them for domain two; keep them out of the golden set |
| Security review stretches Phase 0 | Weeks pass on one approval | Start the review early; keep the gates, stretch the calendar |

In our engagements, the stall that cost the most time was a decider who could spare only minutes a week. Decisions queued, and the gates slipped behind them. Ask for the time back as soon as the queue starts to grow.

[]{#ch09-partner}[]{#ch09-writeup}[]{#ch09-postmortem}Three more things the delivery lead owes the company, each on one page: the boundaries that hold when a partner firm delivers, [Deliver as a partner](#c14); the anonymised note on what moved the score, so the next engagement costs less, [Pattern write-up](#r2-20); and a blameless postmortem at the end of each engagement and whenever a gate slips or a wrong governed number reaches a user, [Field postmortem](#r2-21).

> [!DONE]
> - [ ] A weekly trace hour is on the calendar, and the queue is decided in it
> - [ ] Every user correction becomes a proposed change, never an automatic one
> - [ ] Each drift trigger reruns the right set
> - [ ] The previous release stays deployable
> - [ ] Domain two is named, with what it inherits, what it builds, the contested words and an arbiter
> - [ ] Why-questions are written down with their dates, and no ontology is built before the what-questions hold
> - [ ] The four ceremonies are booked through Phase 4, and every gate decision is written down
> - [ ] Every condition on a "go with conditions" has a date, checked on that date

Card: [What to do when things stall](#c9)
