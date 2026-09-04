# Expected result: secod-payments-billing

`run_fixtures.py` exits `0` and emits JSON with `tests_run: 13`, `failures: 0`, `errors: 0`,
`expectations_reproduced: true`, `controls_exercised` containing PB-1 through PB-10, and
`production_evidence: false`.

Expected findings from unsafe cases:

- PB-1 and PB-5: client-controlled price, tenant or paid state is `Do not ship`.
- PB-2: raw card collection without an intentional compliance decision is `Do not ship`.
- PB-3, PB-7, PB-8 and PB-9: duplicate money writes, missing delivery recovery, silent partial mapping or missing lifecycle correction are `Fix before launch`.
- PB-4 and PB-6: unexpected versions or forged webhooks accepted are `Do not ship`; an unbacked capability row remains `Not verified`.
- PB-10: client-exposed live credentials are `Do not ship`; missing stage/rotation evidence remains `Not verified`.
- Missing adapter, direct provider source, provider state or production evidence remains `Not verified` and is inherited as a blocker by `secod-ship-check`.

Passing local fixture expectations never become application or production `Passed with evidence`.
