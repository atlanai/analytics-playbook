---
for: context engineer, agent builder, domain owner, eval owner
produces: trace reviews, approved context changes, the iteration ledger, a score ready for the launch gate
---

# Phase 3: hill-climb from traces {#ch06}

> [!RULE]
> Read the raw trace of every miss. The summary hides the step where the agent guessed.

::: {.tldr}
- **Short version.** Open the raw trace of every wrong answer and find the step where the agent guessed. Each miss is a definition never written, written but never served, or served and ignored. Make the smallest fix, rerun, and stop when the score stops moving.
- **Do this.** Write the stop rule down before the first round.
- **Skip if** the score already clears your launch bar on fresh questions. Go to [Phase 4](#ch07).
:::

::: {.scene week="Phase 3"}
The summary for the pipeline question said the agent had used the metric. That was true. The context engineer opened the raw trace anyway. One line of the metric's SQL ranked the top 100 customers by number of deals. Finance ranks them by current ARR. Finance's list lived in a spreadsheet, so no query history had ever shown it. Phase 2 had no way to see it: the generator drafted from query history, and the one place the ranking had surfaced was a Phase 1 sealing dispute. That dispute should have crossed the wall to the conflict list, with no sealed value. It stayed on the item instead. The FP&A partner and the RevOps lead settled it in a 20-minute session the next morning. The metric now ranks by ARR. The stage rule from kickoff, until then served as a separate instruction, went into the metric's SQL too. Gate 2 should have held the metric until the rule was in its SQL. Nobody had checked. One change broke another question, the regression run caught it, and they fixed it the next day. Phase 3 closed at 18 of 20.
:::

Phase 3 starts from the metrics and the Phase 2 score. The misses left are decisions nobody raised, and the trace is where they show. The phase ends when the score stops moving or clears the bar set in the brief. The work is one loop, run in short rounds. Each round changes the context a little, reruns the golden set and reads what happened. Meanwhile the graders grow the golden set to 50 questions for the launch gate. The context engineer never sees the new questions.

## The loop {#ch06-loop}

::: {.diagram #wave}
One round: freeze the context, predict what will change, run, grade, read every miss, make the smallest fix, rerun everything and record it. The stop rule is the only way out.
:::

Teams skip two steps most often.

- **Predict before you run.** Write down which questions each change should fix. A round that moves the total without landing its predictions did something other than you meant.
- **Rerun the whole set.** A change aimed at one question can break another. The sales team's did: a rule meant to drop internal accounts also dropped a partner account the golden set counts. Only the full rerun caught it.

Two habits keep the scores honest. First, before the first round, run the unchanged context two or three times. The score moves a little between identical runs. Call that spread the run-to-run variation. A round that moves the total by less than that proves nothing on its own. Second, once the score is past about 60%, ask each question three to five times per round. Count a question as right only when it is right on every run.

Record every round in the [iteration ledger](#r2-8): what changed, what you predicted, what moved, and what you kept or reverted.

## Read the raw trace {#ch06-trace}

A summary tells you what the agent says it did. The trace shows what it actually did, step by step. Read the trace of every miss before you change anything. Here is the pipeline question, cut to the lines that matter:

```text
trace · the pipeline question · run 1 of 3
context call   returned: the metric "open pipeline, top customers", version 2, owner RevOps lead
ran metric     the metric's SQL, as served
               WITH top_accounts AS (... ORDER BY COUNT(*) DESC LIMIT 100)   <- ranked by number of deals
               ... WHERE NOT o.is_closed AND o.type IN ('New Business', 'Upsell')   <- every stage counts
answer         "Open pipeline with the top 100 customers: [a total well above the golden answer]"   wrong on 3 of 3 runs
```

The agent made no mistake of its own. It ran the statement it was given, the same way on every run. Both wrong decisions were inside the metric. Asking the question several times would never have exposed this, because a metric that is wrong the same way every time never disagrees with itself. Only the statement in the trace shows it.

A trace is worth reading when it carries, for every run:

- the prompt, with every served item by name and version
- each tool call, with its arguments and result
- every SQL statement, failed ones included
- the answer or the refusal
- tokens, steps and time

If your export lacks any of these, fix it before the next round.

## The three kinds of miss {#ch06-miss}

::: {.diagram #miss-tree}
Walk every miss through the tree before you fix anything. Each kind has one fix and one owner.
:::

Check two things first, because adding context makes both worse. Is the golden answer wrong? Then the eval owner re-verifies and reseals it, and nobody edits the question to fit the agent. Did the agent run out of steps? Then read what the steps were spent on.

Then place the miss in one of three kinds:

| Kind | What the trace shows | Smallest fix | Who |
|---|---|---|---|
| Never written | The decision exists nowhere in the context | Write the definition; the owner decides it | Context engineer drafts, domain owner decides |
| Written, not served | The definition exists and never reached the agent | Fix retrieval: a term link, alternate labels, a rank | Context engineer |
| Served, ignored | The definition was in front of the agent and it took a simpler path | Make it a rule the agent must follow, or make the SQL a metric | Context engineer and agent builder |

Phase 3 found the first two kinds in the running example. The top-100 ranking was never written: finance's definition lived nowhere the pipeline could see it. The slipped-deals question was written and not served. A trusted past query already answered it, but the question said "slipped", and neither the query nor its title used that word, so the agent invented its own definition.

A miss that persists with its definition served and used is not a context problem. The warehouse has no table in the shape the question needs. Take it to the platform owner.

[]{#ch06-instruments}When a miss won't sort cleanly, ask the question several times with everything else fixed and compare the SQL. Where the runs split, two definitions compete. Resolve it as a conflict. This check needs no golden set, so it keeps working after launch.

## The smallest fix that closes a miss {#ch06-fix}

The climb stalls when a team writes new definitions for misses whose definitions already exist. Search the context before you write anything. Then make the smallest change that closes the miss: a versioned edit to one metric, rule, business term or trusted query's rank.

- **Target the rule, never the answer.** The change states the business rule. It should make sense to someone who has never seen the golden set.
- **Keep sealed values out.** No change may contain a golden answer or a literal copied from the set.
- **Use the form that runs.** Definitions go in as SQL, rules as instructions, vocabulary as term links.
- **Give it an owner and a version.** Each round gets a new context version, so rolling back is one step.

The slipped-deals fix shows the size to aim for. It was two edits to one business term. "Slipped deal" gained the alternate labels "pushed" and "rolled", and it was linked to the analyst's query. Nobody wrote a new definition, because none was missing.

The top-100 fix needed a decision. The context engineer prepared both rankings as witnessed SQL, with who uses each. The two owners chose ARR in 20 minutes and agreed to co-own the metric. The RevOps lead also moved "some early stages never count" out of a separate instruction and into the metric's SQL. A harness runs a metric as written, so a rule has to be in the statement to count.

::: {.diagram #a1-before-after}
The pipeline question before and after the fix. Without context: $1.31B, from four reasonable guesses. With the metric: $412M, 340 deals on 91 of the top 100 customers.
:::

Record the changes that do nothing as carefully as the ones that work. The sales team added a description to the stage column, hoping the agent would apply the early-stage rule in its own SQL. Nothing moved across three runs, because the rule already lived in the metric, so they reverted it. The next domain reads that line in the iteration ledger before it spends a round on descriptions.

## When to stop {#ch06-stop}

Write the stop rule down before the first round, so nobody bends it later. Ours: stop when two rounds in a row move the score by no more than the run-to-run variation, and none of the fixes you predicted works. Count predicted fixes as well as the total, because a round can land its one fix while something else flickers. Cap the phase at five rounds. If the bar is still not cleared, report the ceiling honestly and take the gap to the sponsor.

> [!STOP]
> **Stop adding context and escalate when:**
>
> - A miss persists with its definition served and used. The platform owner fixes the table or its grain.
> - A conflict has no owner willing to decide. More examples only teach the agent to pick a side. The sponsor names an owner.
> - A new example fixes one question and breaks others. Make the definition a metric instead.
> - A golden answer is disputed. The eval owner freezes that question until the dispute is settled.

## Don't raise the step budget to cut refusals {#ch06-budget}

When the agent gives up too often, a bigger step budget looks like the easy answer. It turns refusals into confident wrong answers. <!-- E42 --> A refusal tells you a decision is missing. Read the trace, find the decision and supply it. Keep the step budget where it was at the baseline.

## Gate 3 {#ch06-gate}

The sponsor sees the score after each round, what broke and what was fixed, and the golden set grown to 50. The decision is to move to the launch gate.

> [!DONE]
> - [ ] Run-to-run variation measured on the unchanged context before the first round
> - [ ] Each question asked three to five times per round once past about 60%
> - [ ] Predicted fixes written down before every run
> - [ ] The raw trace of every miss read and classified
> - [ ] Every change approved by its owner and versioned; no sealed value in the context
> - [ ] The whole set rerun after every change; nothing that passed before is broken
> - [ ] Iteration ledger complete, reverted changes included
> - [ ] Step budget unchanged since the baseline
> - [ ] The golden set grown to 50 for the launch gate
> - [ ] Remaining gaps escalated with an owner, or the ceiling reported

Card: [Why did this miss?](#c6)
