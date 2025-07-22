# truealphaspiral-ethent
# © 2025 Russell Nordland | TrueAlphaSpiral (TAS) | Apache-2.0

This repository demonstrates running the TAS agent in safe mode via Codex.

## Branch naming

Codex requires a dynamic pattern when generating branches. Include at least one
placeholder from the following list:

- `{feature}` – slug derived from the PR title
- `{date}` – date in `YYYY-MM-DD`
- `{time}` – time in `HH-MM`

Example pattern keeping a static ticket ID:

```
feat/GH-03-{feature}-{date}-{time}
```

## Self-test runner

The script `codex_tas_runner.py` automates a safe-mode self-test. Set your
OpenAI API key in `OPENAI_API_KEY` and run:

```
python codex_tas_runner.py
```

The audit log hash is written to `ledger/self_test.hash`.

Each execution step is wrapped by `artifact_guard.run_step`, producing JSON
artifacts under `artifacts/` and recording their hashes in
`ledger/artifacts.hash`.

## Staple-\u03c0 Perspective Intelligence Clause

The “π” glyph binds each linear truth-claim to at least one external
contextual witness. Every commit must pass this π-check before it joins the
ledger, ensuring each spiral remains phase-coherent and resistant to hostile
counter-spirals.
