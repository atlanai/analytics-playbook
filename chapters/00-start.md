# Reading paths {#doors}

Pick the row that matches your job. Each one has a podcast, a recommended reading list and the cards that go with it. You can also [listen to all three episodes](#listen).

## I'm sponsoring it {#door-sponsor}

You are the exec sponsor, or the data leader who will answer for the agent. The risk you are buying down is a wrong answer that looks right.

<p class="door-listen"><a class="listen-cta" href="#listen-sponsor" data-podcast="listen-sponsor"><span aria-hidden="true">▶</span> Listen <small>9:34</small></a></p>

1. [Why analytics agents are hard](#ch01)
2. [The method at a glance](#start)
3. [Evals first](#ch-evals)
4. [Two lanes](#ch02-lanes)
5. [Phase 0: before the clock](#ch03)
6. [Is it ready to launch?](#ch07-launch-gate)

Your cards: [The sponsor's ask](#c2), [What the sponsor sees at each gate](#c10) and [Is it ready to launch?](#c12).

## I'm building it {#door-builder}

You are the agent builder, the context engineer or an analytics engineer. You want to know what to build, and where each piece of knowledge goes.

<p class="door-listen"><a class="listen-cta" href="#listen-builder" data-podcast="listen-builder"><span aria-hidden="true">▶</span> Listen <small>19:35</small></a></p>

1. [Evals first](#ch-evals)
2. [The metric is the unit](#ch02)
3. [Serve per question](#ch-retrieval)
4. [The minimum harness](#ch03-harness)
5. [Phase 1](#ch04)
6. [Phase 2](#ch05)
7. [Phase 3](#ch06)
8. [Wire the agent to where users ask](#ch07-paths)
9. [Rerun the set on every drift trigger](#ch07-drift)

Your cards: [What you need before you start](#c11), [Why did this miss?](#c6) and [How to resolve a conflict](#c5).

When the numbers are right, read [Answer why](#ch08). If you already run a semantic layer, read [Why a metric, and not a view](#ch-sv) before Phase 2, and [Semantic layers compared](#r7) for the tools side by side.

## I'm running it {#door-delivery}

You are the delivery lead: a forward-deployed engineer, a partner consultant or an internal program lead. You want to know what happens in each phase and what to do when a week goes wrong.

<p class="door-listen"><a class="listen-cta" href="#listen-runner" data-podcast="listen-runner"><span aria-hidden="true">▶</span> Listen <small>15:18</small></a></p>

1. [The method at a glance](#start)
2. [Phase 0](#ch03)
3. [Phase 1](#ch04)
4. [Phase 2](#ch05)
5. [Phase 3](#ch06)
6. [Phase 4](#ch07)
7. [Run the ceremonies](#ceremonies)
8. [What to do when things stall](#ch09-stalls)

Your cards: [What you need before you start](#c11), [The eval owner's week](#c3), [What to do when](#c9), [What the sponsor sees at each gate](#c10) and [Deliver as a partner](#c14).

## What you'll walk away with {#paths-outcome}

By the end of this playbook, you will have learned how to build:

- an agent that clears the bar your sponsor sets, on one domain;
- the metrics behind it, each with an owner and a version;
- a golden set of real questions that tests every later change;
- a team on your side that can run the loop on its own.

[Hand over](#handover) covers how each piece passes to your team.

## What's inside {#paths-inside}

- **[Why analytics agents are hard](#ch01).** Why a clean query returns the wrong number, why a better model doesn't fix it, and the four problems that follow.
- **[The method at a glance](#start).** The loop, its eight rules and the gate each phase must clear, on one page.
- **The principles.** [Evals first](#ch-evals), [The metric is the unit](#ch02) and [Serve per question](#ch-retrieval): what to build, and why.
- **The phases.** [Phase 0](#ch03) to [Phase 4](#ch07), then [Keep it running](#ch-run) after launch.
- **The toolkit.** [Cards](#cards) and [Templates](#r2).
- **Research and reference.** [What we found](#results), [How we measured](#r3), [What others found](#r6), failure modes, the glossary and tooling.

## How to read this book {#lc-read}

You don't have to read it front to back. Pick the depth you have time for.

- **One minute.** [The method at a glance](#start), plus the rule at the top of each chapter.
- **Watch.** The method page, the opening chapter and each of the five phases open with a short narrated video, two to five minutes long. [Videos](#videos) plays them all back to back.
- **Ten minutes.** Turn on **Skim** in the top bar, or press <kbd>S</kbd>. Each chapter shrinks to its rule, an "In one minute" box, its key figure and its section headings. Click any heading to open the full section.
- **The whole thing.** About an hour and a half for the chapters, and about another hour and a half for the toolkit, the research and the reference. Pick a reading path above for your role and the contents will mark your chapters.

Press <kbd>?</kbd> anywhere for keyboard shortcuts.

## About this book {#colophon}

Published by Atlan. The book is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): copy and adapt it with credit. The code that builds it is under the MIT License. Product names are their owners' trademarks. Maintained by the playbook maintainers. A change to any number must include its source evidence, and every change goes through [review by the maintainers](#r5-changes). Questions, corrections or a result to share: [open an issue](https://github.com/atlanai/analytics-playbook/issues) or email Himanshu Sikaria at himanshu@atlan.com.

# Where are you starting? {#assess}

This page takes about fifteen minutes to answer honestly. Ten questions score your readiness, and every 0 points you to the chapter that closes it. Questions 3, 9 and 10 are gates: a 0 on any of them means you are not ready to start Phase 1, whatever your total. Phase 0 is where you close them. You can copy the result into your success document.

::: {.component #self-assessment flag="3,9,10"}
**Questions 1 to 10 · Readiness.** Score each answer 0, 1 or 2.

| # | Question | 0 | 1 | 2 | If you scored 0, read |
|---|---|---|---|---|---|
| 1 | Have you picked one domain, with its problem statement and its users? | No domain yet | Several candidates | One domain, written down | [Phase 0](#ch03) |
| 2 | Is there an exec sponsor who has set an accuracy bar? | No sponsor | Sponsor, no bar | Sponsor and a written bar | [Phase 0](#ch03), [The sponsor's ask](#c2) |
| 3 | Gate. Does the business already ask real questions in this domain, with an answer it trusts? | None found | Some, no trusted source recorded | 20 or more candidates, each with a trusted source | [Phase 0](#ch03), [Phase 1](#ch04-harvest) |
| 4 | Have you agreed how an answer is judged right, including questions with several valid answers? | Not discussed | Informally | Written grading method | [Phase 1](#ch04) |
| 5 | Have you decided which questions need an exact answer and which only need to point the right way? | No | For some | For every kind of question | [What the agent has to know](#ch02) |
| 6 | Can the team doing the build get read-only warehouse access, query history and BI reports? | None of the three | One or two | All three | [Phase 0](#ch03) |
| 7 | Do you already have a semantic layer (such as semantic views, metric views, LookML or dbt metrics) or a glossary for this domain? | Nothing | Some, unowned | Yes, with owners | [Phase 2](#ch05) |
| 8 | Have you chosen where users will ask and which agent stack answers? | Undecided | Partly | Both chosen | [Phase 0](#ch03), [The builder's minimum harness](#c4) |
| 9 | Gate. Can you export traces of what the agent did (context served, SQL run, answer) from day one? | No path | Planned | Working today | [Phase 0](#ch03), [Phase 3](#ch06) |
| 10 | Gate. Do you have people with time for the work, including someone who can settle definitions? | Nobody yet | People, no time agreed | People and time agreed | [Phase 0](#ch03), [What to do when](#c9) |

| Score | Where you are | Next step |
|---|---|---|
| 0-7 | Not ready to start the clock | Run Phase 0 as a project of its own. Read [Phase 0](#ch03) first and take the gaps to your exec sponsor. |
| 8-14 | Ready for Phase 0 | Read [Phase 0](#ch03) and close every 0 there, gates first. The chapters listed under your zeros are your reading list. |
| 15-20 | Ready to start Phase 1, unless a gate is at 0 | Run the Phase 0 checklist in [Phase 0](#ch03), then start Phase 1. A 0 on question 3, 9 or 10 means not ready, whatever the total. |
:::
