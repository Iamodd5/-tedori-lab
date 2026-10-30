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
| H-9 | 2→3 | DECISION | Keep the standalone baseline engine (OpenFisca-Japan as cross-check), or rebuild it as an OpenFisca-Japan extension? (docs/COVERAGE.md) | open | |
