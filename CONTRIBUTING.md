# Contributing

Customers act on this guide. Every line has to hold up to a skeptical reader.

## Evidence
- **IDs.** Every number that is evidence carries a maintainer-assigned ID, written as a hidden comment beside it, e.g. `31.8% <!-- E03 -->`. The `audit_ids` list in `evidence.json` validates these identifiers; it stores no evidence records. Figures from the running example and procedural defaults (time boxes, proposed hours) do not.
- **Adding or changing a number.** Give the value, n, date, caveat and source in the PR description. A maintainer checks it against the internal store of record before merging and adds any new audit ID to `evidence.json`.
- **How to quote results.** Keep numbers few and simple. Quote the configuration you ship, never the best run, and give the range of variants next to it. The same setup run twice moved by six questions and eight changed verdict, so don't claim a gap under about seven points.
- **Field results** are anonymised before they enter the guide.

## Method
- **Changes that need review.** Phase 0 to Phase 4, the gates, the two lanes, the three kinds of miss and the stop rule are the method. Changing them needs a maintainer's review. Improving how a step is explained does not.
- **The harness.** The customer owns and runs the harness and the model. Atlan never runs or takes on either.
- **Atlan.** The book describes the method, not a product. It carries no product pages, product names or status labels.
- **The method map.** `diagrams/method-map.html` restates every phase, step, owner, template and card in short form. A pull request that renames, adds, removes or reorders any of them, or changes a section the map links to, updates the map too. The build checks the map's links, not its words, so reviewers check that the two still agree.

## Writing
- Second person, direct, short sentences (average under 18 words).
- Each chapter opens with its rule line. Part II chapters open with a story scene and close with a Definition of done and a card link.
- Don't use:
  - "not X but Y" contrasts
  - one-line closers
  - decorative bold
  - em dashes in prose
  - hype words
- No customer names, no internal system or project names, and no named individuals.
- SQL in examples runs on DuckDB.
