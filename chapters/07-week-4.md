---
for: sponsor, domain owner, eval owner, agent builder, platform owner
produces: launch decision, release note, handover
---

# Phase 4: release and hand over {#ch07}

> [!RULE]
> Launch on questions nobody climbed against, and hand over only what your team has run alone.

::: {.tldr}
- **Short version.** Test on fresh questions nobody climbed against, let the business decide go or no-go, choose how the agent reaches users, then hand over with one pass together and one your team runs alone.
- **Do this.** Have the graders add questions the builders never see, and run the launch gate on them.
- **Skip if** you're still climbing. Come back when the score holds.
:::

::: {.scene week="Phase 4"}
By the start of Phase 4 the golden set had grown to 50. The graders drafted the new questions from dashboard tiles and the CRO's own asks. The context engineer never saw them. The governed questions came back right on every run, and the exploratory ones cleared their bar. One question type failed for a reason no context could fix: the warehouse kept no record of pipeline created this quarter. The CRO signed the launch and held that type back by name. A few days after launch, a regional VP told the agent it was wrong. Soon after, a billing column was retired. The team handled both without calling the delivery team.
:::

Phase 4 has two jobs. It proves the agent holds up on questions nobody climbed against. It also leaves a team that keeps the context true after the delivery team goes, so the score still holds next quarter.

## Gate 4: is it ready to launch? {#ch07-launch-gate}

A score earned on the questions you tuned against flatters the agent. That is why the graders grew the golden set to 50 during Phase 3, with questions from outside the climb: new dashboard tiles, recent tickets, the sponsor's own asks. Now run all 50 three to five times each. Tick this checklist at the gate review.

> [!DONE]
> - [ ] The golden set has grown to 50, and the new questions were sealed without the context engineer seeing them
> - [ ] All 50 ran three to five times each on the release configuration
> - [ ] Governed questions are right on every run
> - [ ] Exploratory questions clear the bar set in Phase 0, on the overall set
> - [ ] Everything that passed at the last gate still passes
> - [ ] Every miss was checked against its golden answer before anyone blamed the context
> - [ ] Five passing questions, chosen at random, were re-graded by hand
> - [ ] A governed question with no metric gets "no metric", never a guess
> - [ ] Traces from the production surface reach a store the team can read
> - [ ] The sponsor signed go, no-go, or go with conditions, and each condition has an owner and a date

If something falls short, you have three moves: ship without it and name it, move it to the exploratory lane with the sponsor's agreement, or run one more round of the hill climb. The engagement's launch readout fit in five lines:

```markdown
# Launch readout: Sales · end of Phase 4 · CRO, RevOps lead, FP&A partner, eval owner, delivery lead
Governed: right on every run, and "no metric" on every out-of-scope probe · CLEARED
Exploratory: above the Phase 0 bar on every run, after one golden answer was corrected · CLEARED
Pipeline created this quarter: wrong on every run; the warehouse holds no "created and still open" record · HELD BACK
Decision: GO WITH CONDITIONS · the held-back type returns once the platform owner builds the record · traces must flow on launch day, or the launch waits
```

Read more: [Is it ready to launch?](#c12)

## Wire the agent to where users ask {#ch07-paths}

You chose the architecture and the surface in Phase 0. Phase 4 wires the release path to the context layer and checks it on launch day. Each path reaches the same context layer; they differ in how the context gets to the agent.

::: {.diagram #agent-architectures}
The same context layer behind every release path. A platform-native agent reads context pushed into the platform or calls the context layer over MCP or API. A custom harness makes the context call itself.
:::

| Release path | How context reaches the agent | What to watch |
|---|---|---|
| Platform-native agent | Pushed into the platform as semantic views, metric views or instructions | Stays inside the platform's governance and permissions, with no extra service to run. Push again on every release. |
| Platform agent plus MCP | Called over MCP on each question | Name the connection in the agent's instructions, and check the traces to confirm the call happens. |
| Custom harness | Your harness calls for context first, then runs read-only SQL | You own the tools, the step budget and the traces. |

Keep every definition in one store any harness can read, so the next harness change is only a wiring job. Four things must hold on launch day:

1. The agent asks for context before it writes any SQL. Confirm it in the traces.
2. Governed questions run the metric's SQL as served. When no metric matches, the agent says so.
3. Governed answers run under a fixed service identity, so a board number is the same for every asker. Exploratory queries run under the user's own identity.
4. Traces reach a store the review team can read: every context call, what it returned, every SQL statement and the answer.

The fourth slips most often. Without traces there is no loop, so the launch waits.

## Hand over: one pass together, one alone {#handover}

An agent that clears its bar is half the job. The other half is a team that can produce the next score alone. Each thing left behind needs an owner on your side and a version.

| What stays | Owner after handover | Reused as |
|---|---|---|
| Metrics | The owning team for each | The one definition every later agent and domain calls |
| Golden set of 50 | Eval owner | The full rerun on every context change. The questions it gets right on every run form the regression set, rerun on every schema change |
| Decisions log | Domain owner | Precedent: the next conflict on the same concept starts here |
| Rules and business terms | Domain owner | Shared by every domain that uses the same words |
| Trusted past queries | Their authors, approved by the domain owner | The exploratory lane's library |
| Trained owners | Exec sponsor | The people who run domain two |

The decisions log outlasts the rest. It records every place two defensible definitions were in use, who decided, and when. It survives a model swap or a harness rewrite.

The handover takes three steps:

1. Walk the assets. Each owner uses their own asset while the context engineer watches.
2. Run one pass together. The team runs a full improvement round end to end: it decides the open conflicts, reruns the golden set and records the result. The context engineer only watches.
3. Run one pass alone within two weeks. The context engineer is on call and nobody calls. Your team writes the record.

::: {.diagram #handover}
The two handover passes side by side: who triggered, decided, ran, graded and recorded each one, and where the context engineer was.
:::

In the running example, a schema change after launch forced the solo pass early, a harder test than a planned one ([Keep it running](#ch-run) tells the story). Test the handover with one question: could your team run the next round with the delivery team gone? If the answer depends on a script, a notebook or a person the delivery team brought, move it into your repository, give it an owner, or throw it away.

Card: [Is it ready to launch?](#c12)
