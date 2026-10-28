---
for: agent builder, context engineer
produces: the retrieval architecture, the ranking rules, the three trace checks
---

# Serve per question {#ch-retrieval}

> [!RULE]
> One context call per question, before any SQL: exact lookup first, search second, served live over MCP.

::: {.tldr}
- **Short version.** Metrics and trusted past queries only help when the right one reaches the question. Serve them live, per question, from one store that every agent calls over MCP. Don't load the whole layer into the prompt.
- **Do this.** Stand up one MCP server over the context layer, make the agent call it before any SQL, and check in the traces that it does.
- **Skip if** your only agent is a platform-native one that reads context pushed into the platform. Read [Wire the agent](#ch07-paths) instead.
:::

[]{#ch-retrieval-why}Building the context layer is half the job. The other half is getting the one metric or query that settles a question in front of the agent at the moment it needs it. The obvious first build pastes everything into the agent's instructions. It is simple and it fails. Loaded in full into every prompt, the layer scored 52.3%, and 72.0% with past queries added. Retrieved per question, the same kind of layer scored 83.2% and cost less than half as much per right answer <!-- E11 -->. A long prompt buries the decisive item among near-variants, and the agent picks the closest-looking one. Retrieval per question also keeps the layer live: an agent that searches on every question reads the version approved this morning.

## The retrieval architecture {#ch-retrieval-arch}

::: {.diagram #retrieval}
One question, end to end. The agent makes one context call before any SQL. The MCP server searches the context layer live and returns a handful of labelled items, each with complete SQL. The tool name is an example.
:::

Three parts do the work:

- **One store.** Metrics, trusted past queries, rules and business terms live in one place, each with a version. This is the layer you build in [Phase 2](#ch05).
- **One MCP server in front of it.** It exposes a small set of tools, such as a context lookup and a metric fetch, to any agent that speaks MCP. Lyft reaches its metrics through an MCP server in the same way <!-- X05 -->. DoorDash's data agent goes further: it blocks unmodeled or unverified sources at the harness level, and keeps new joins and documents inactive until they meet an eval threshold <!-- X16 -->.
- **One rule in the agent's instructions.** Call for context before writing SQL. If a metric matches, run its SQL as served. If none matches, say so. For a governed question, stop there; otherwise explore and show the SQL.

## Why MCP {#ch-retrieval-mcp}

| How context reaches the agent | What happens | Our view |
|---|---|---|
| Pasted into the prompt | The whole layer rides along with every question | Don't. It scored lower and cost more per right answer |
| Pushed into the platform | Semantic views, metric views or instructions inside the warehouse's own agent | Works for that one agent. It stays inside the platform's governance and permissions, with no extra service to run. You push again on every release |
| Live search over MCP | The agent calls one server on each question; the server searches the context layer | Our design preference, not measured against pushing into the platform. One store serves every agent, each call shows up in the traces, and a change reaches every agent at once |
| Your own API | Your harness calls a context endpoint before it writes SQL | Same design as MCP, for a harness you own. Expose the same tools |

The case for MCP isn't the protocol. It is that every agent, whether it's a warehouse agent, an IDE assistant or a Slack bot, reads the same copy through one door you can trace. When the next harness arrives, connecting it is only wiring.

## What the search should match {#ch-retrieval-match}

1. **Exact lookup first.** When a metric covers the question, return it at the top, labelled as a metric, so the agent runs it instead of rewriting it.
2. **Match on field names and business terms.** Ranking past queries by the tables, columns and terms they share with the question beat ranking by embedding similarity, 68.2% to 55.1% <!-- E61 -->. Words in a question rarely match the words in a query's title. Business terms bridge that gap.
3. **Return a handful, whole.** Return the top five or so, with complete SQL. Cap by the number of items, never by characters. Past queries served whole instead of cut short added 9.4 points <!-- E12 -->.
4. **Don't stack retrievers.** A second, sharper retriever on top of the metrics added nothing <!-- E09 -->, because near-variants compete with the item that settles the question.
5. **Judge retrieval by answers, not recall.** Better table search lifted recall from 59.8% to 86.4% and accuracy didn't move <!-- E21 -->. Finding more candidates is not the same as serving the decisive one.

> [!NOTE]
> **Business terms are the index.** "Slipped" appears in neither the trusted query's title nor its SQL. A business term with "slipped" as an alternate label, linked to the query, is how the search finds it. Write terms for the words people actually type, including the acronyms and jargon a new hire wouldn't know.

## Check it in the traces {#ch-retrieval-check}

Retrieval fails quietly. The agent still answers, so read the traces for three things:

- **The call happens.** Every question shows a context call before the first SQL statement. An agent wired to MCP but not told to call it often skips it.
- **The decisive item comes back.** For every miss in the golden set, check whether the metric or query that would have settled it was returned. If it wasn't, the miss is "written, not served": fix the term, the alternate labels or the ranking, not the metric. [Phase 3](#ch06) sorts every miss this way.
- **The agent uses what came back.** If the right item was returned and the agent wrote its own SQL anyway, tighten the instruction to run a metric's SQL as served.

Read more: [Phase 2: serve it per question](#ch05-serve)
