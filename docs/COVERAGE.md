# OpenFisca-Japan coverage map

Inspected: `project-inclusive/OpenFisca-Japan`, commit `1f8d13dbe735b064373fe67377859454dd750b9c` (2026-08-26), by reading the source (not yet installed or run).
Variable and parameter names are in Japanese in the upstream code; they are quoted as-is.

Legend: ✅ implemented and looks usable · ⚠️ implemented but needs checking or updating for 2026 · ❌ not implemented

## Baseline rules Tedori Lab needs (spec Section 3)

| Rule | Upstream variable(s) | Status | Notes |
|---|---|---|---|
| Employment income deduction (給与所得控除) | `給与所得控除額` (variables/所得.py) | ⚠️ | Exists. Need to confirm it uses the 2025 reform (minimum 650,000 yen) for tax year 2026. Amounts are hard-coded in the formula, not in `parameters/`. |
| Basic deduction, income tax (基礎控除) | `基礎控除` | ⚠️ | Has `formula_2025_01_01` and `formula_2027_01_01` tiers (e.g. 950,000 yen up to 1.32 million of total income from 2027). The 2026 values must be checked against NTA No.1199. Hard-coded, not parameters. |
| Spouse / spouse special / dependent deductions | `配偶者控除`, `配偶者特別控除`, `扶養控除` | ⚠️ | Exist. Check 2025 changes (e.g. dependent income limit raised) and the new 特定親族特別控除 (No.1177), which does not appear to be implemented. |
| Income tax rate schedule + reconstruction surtax | `基準所得税額`, `復興特別所得税`, `所得税` | ✅/⚠️ | Exists; check brackets against NTA No.2260. |
| Resident tax (income levy + per-capita levy, 調整控除) | `住民税所得割`, `住民税均等割`, `調整控除`, `住民税` | ⚠️ | Exists. Per-capita parameter `均等割` = 4,000 since 2000; the forest environment tax (1,000) is a separate parameter. Check. |
| Public pension deduction (公的年金等控除) | not found as a separate variable | ❌/⚠️ | Needed for H6 (pensioner couple). Pension income handling must be verified. |
| Health insurance (employee) | `健康保険料`, `標準報酬月額_健康保険料` | ⚠️ | Rate parameter `健康保険料率` is a single **10% placeholder since 2000**, not the 2026 Tokyo rate. Must use the 協会けんぽ Tokyo R8 table. Upstream fix candidate. |
| Long-term care premium (age 40–64) | `介護保険料`, `介護保険料率` | ⚠️ | Exists; check 2026 rate. |
| Employee pension | `厚生年金保険料`, `標準報酬月額_厚生年金保険料` | ✅ | Rate 18.3% (unchanged since 2017-09). Check band table and caps. |
| Employment insurance | `雇用保険料`, `雇用保険料率` | ✅ | Has a 2026-04-01 worker rate of 0.5%. Verify against MHLW page. |
| Coverage thresholds (106万 / 週20時間 / 130万 dependent) | `社会保険料納付条件`, `週労働時間20時間以上`, `扶養者収入基準_*` | ⚠️ | Uses monthly wage ≥ 88,000 yen and 20 hours. Need to check 2026 law changes (wage requirement abolition timing, firm-size rule). |
| National health insurance (self-employed) | – | ❌ | Upstream explicitly skips it ("varies by municipality"). Tedori Lab must implement it for one reference municipality (H7). |
| National pension contribution | `国民年金保険料` | ⚠️ | Parameter is **17,510 yen/month dated 2015** – stale. Must update to the FY2026 amount. Upstream fix candidate. |
| Child allowance (児童手当) | `児童手当` (+ parameters/福祉/育児/児童手当) | ⚠️ | Covers children up to high school. Must confirm the Oct 2024 reform (no income limit, 30,000 yen from 3rd child). |
| Consumption tax | – | ❌ | Not in scope upstream. Tedori Lab computes it outside OpenFisca from household spending (approximation, labelled). |
| Refundable credit / any of the four designs | – | ❌ | To be built as reform files in `engine/`. |

## Structure notes (for upstream fit)

- Entities: `人物` (person) and `世帯` (household). Most variables use `definition_period = DAY`.
- Many 2025/2027 tax amounts live **inside formulas** rather than in `parameters/`. Moving them into parameters would be a clean first upstream contribution (and lets reforms change them).
- `tools/make_tests` exists for generating YAML tests; `simulation/` has sample household CSVs.
- Several parameter references point to municipal web pages rather than national primary sources.

## MCP server

The Code for Japan note (`sources/scrapbox_openfisca_mcp.json`) describes an MCP server that exposes some OpenFisca-Japan Web API calculations to chat apps. It is a wrapper over the existing Web API; nothing in the note indicates it can load custom reforms. Not needed for v1.

## First upstream-ready contributions (candidates, to be confirmed in Milestone 3)

1. Update `国民年金保険料` and `健康保険料率` (prefecture-specific) to 2026 values with national primary-source references.
2. Move hard-coded deduction amounts (基礎控除, 給与所得控除) into dated parameters.
3. Add `特定親族特別控除` if missing.

Opening any issue or PR upstream is a human action (spec Section 13).
