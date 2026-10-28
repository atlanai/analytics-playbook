## What and why

<!-- One topic per PR. Which chapter files change, and why. Link the issue if there is one. -->

## Kind of change

- [ ] Wording or explanation only
- [ ] A number or result
- [ ] The method: a phase, gate, lane, kind of miss or the stop rule (needs a source and a maintainer's review)
- [ ] Site, diagrams or build

## Evidence (for a new or changed number, or a method change)

<!-- Fill one block per number. Leave the evidence ID to the maintainers; don't add one yourself. -->

- Value:
- n:
- Date:
- Caveat: <!-- What could stop this holding elsewhere. Give the range across variants if you ran more than one. -->
- Source: <!-- Internal benchmark: ledger arm and run date. External: URL. Field result: say it is anonymised. Method change: our own work, or the external guide. -->

## Checklist

- [ ] `python3 build.py --check` passes, and I read the changed chapter.
- [ ] No customer, internal system, person or product is named, and no page carries a product status label.
- [ ] The company owns and runs the harness and the model throughout. Any SQL runs on DuckDB.
- [ ] `diagrams/method-map.html` is updated if a phase, step, owner, template or card was renamed, added, removed or reordered.
- [ ] `CHANGELOG.md` has a line for this change.
