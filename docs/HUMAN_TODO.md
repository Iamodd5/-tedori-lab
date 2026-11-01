# Human to-do list

| ID | Milestone | Type | What is needed | Status | Answer / notes |
|----|-----------|------|----------------|--------|----------------|
| H-1 | 0 | ACTION | Confirm the test desktop notification arrived (sent 2026-10-29) | done | 2026-10-30: works after running one notification from inside Script Editor and clicking Allow. |
| H-2 | 0 | REVIEW | Milestone 0 CHECKPOINT: look over `sources/SOURCES.md` and `docs/COVERAGE.md` | done | 2026-10-30: "H-2 ok". Milestone 0 complete. |
| H-3 | 0→1 | DECISION | Which government documents count as "government_final", and how to treat the new 就業者負担軽減支援金 (OPEN_QUESTIONS Q1, Q2) | done | 2026-10-30: "H-3: A, C". government_final = Aug 5 Cabinet basic policy, detailed by Jul 29 interim summary. 就業者負担軽減支援金 modelled inside food_tax_cut as a separate component. |
| H-4 | 0→1 | ACTION | Rengo site is under maintenance: retry later, or download the proposal PDF by hand into `sources/rengo/` (Q3) | open | |
| H-5 | 2 | DECISION | Reference municipality for National Health Insurance (Q4) | done | 2026-10-30 via H-8: Shinjuku ward (Tokyo 23-ward standard). |
| H-6 | 0 | ACTION | Start a new Claude Code session in this project folder so the notification hooks load | open | Hooks in `.claude/settings.json` are read when a session starts. |
| H-7 | 1 | REVIEW + DECISION | Milestone 1 CHECKPOINT: review the five design files; choose Daiwa variant(s) (Q10) | done | 2026-10-30: "H-7 ok, A". Milestone 1 checkpoint passed; Daiwa = headline variant only. |
| H-8 | 2 | DECISION | Reference incomes for H1–H8 (Q5) together with the NHI reference municipality (H-5) | done | 2026-10-30: "a, d". NHI = Shinjuku ward; reference incomes as proposed (H1 1.25m; H2 1.0m; H3 4.5m+3.0m; H4 5.0m+1.0m; H5 2.5m; H6 pension 2.0m+0.8m; H7 business income 3.0m; H8 9.0m+7.0m). |
| H-9 | 2→3 | DECISION | Keep the standalone baseline engine (OpenFisca-Japan as cross-check), or rebuild it as an OpenFisca-Japan extension? (docs/COVERAGE.md) | done | 2026-10-31: "H-9: A". Keep the standalone engine; OpenFisca-Japan stays a cross-check and each corrected rule is a candidate upstream fix. |
| H-10 | 3 | DECISION | Daiwa on 2026 rules: model literally, or hold back (OPEN_QUESTIONS Q19) | done | 2026-11-01: "H-10: A". Model literally on 2026 rules; show a visible note wherever Daiwa numbers appear. |
| H-11 | 4 | DECISION | Wall map for two-income households (H3, H4, H6, H8): whose income moves along the grid? | done | 2026-11-01: "H-11: D". H4 spouse's salary; H3 and H8 head's salary; H6 head's pension (`wall_map` in each household file). |
| H-12 | 5 | REVIEW + DECISION | Milestone 5 CHECKPOINT: read the review table in docs/LOG.md; decide how to read Daiwa's credit (Q29); approve or reject the Daiwa approximations Q11 and Q18 | open | |
| H-13 | 5 | DECISION | Who deducts a spouse's national pension when they lose dependant status (Q26) | open | not urgent |
| H-14 | 5 | DECISION | Keep or redefine H1 "near the 1.3m wall" (Q21) | open | not urgent |
