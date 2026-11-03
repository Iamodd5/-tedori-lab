# OpenFisca-Japan coverage map

Inspected: `project-inclusive/OpenFisca-Japan`, commit `1f8d13dbe735b064373fe67377859454dd750b9c` (2026-08-26), by reading the source (not yet installed or run).
Variable and parameter names are in Japanese in the upstream code; they are quoted as-is.

Legend: ✅ implemented and looks usable · ⚠️ implemented but needs checking or updating for 2026 · ❌ not implemented

## Baseline rules Tedori Lab needs

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
| Single-parent allowance (児童扶養手当) | `児童扶養手当` (variables/福祉/育児/児童扶養手当.py) | ⚠️ | Exists, with open TODOs for the partial-payment formula (施行令2条の4) and the public-pension offset (施行令6条の5). Tedori Lab implements both (`engine/baseline.py` `child_rearing_allowance`, tested from `tests/hand_calcs/H5.md`): a ready upstream contribution. |
| Long-term care premium, 65+ (介護保険 第1号) | – | ❌ | Set by each municipality. Tedori Lab implements Shinjuku's fiscal 2026 table (`parameters/baseline_2026/ltc_65.yaml`). |
| Student pension deferral and low-income exemptions (国民年金) | – | ❌ | Tedori Lab implements the deferral's income limit (施行令6条の9); the exemptions are not modelled (Q20). |
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

Opening any issue or PR upstream is for the project owner.

## Decision taken in Milestone 2 (2026-10-30) — confirmed by the project owner

OpenFisca-Japan installs only on Python 3.11 (its numpy pin), and does so now (`requirements.txt`). But for the 2026 baseline nearly every rule we need had to change: employment-income deduction (2025 and 2026 reforms), basic deduction amounts, the Tokyo health rate and band table, the new 子ども・子育て支援金, the national pension amount, NHI (missing), public-pension income (missing), resident-tax exemption limits and 調整控除. So the baseline is written as a small standalone engine (`engine/baseline.py`, one function per rule, every number read from `parameters/baseline_2026/`). OpenFisca-Japan is used as a cross-check (docs/VALIDATION.md §3). Each corrected rule is a candidate upstream fix.

## First upstream-ready contribution (identified in Milestone 3, 2026-10-31)

**Update `国民年金保険料` to FY2026.** Upstream file `openfisca_japan/parameters/社会保険料/国民年金保険料.yaml` has one value, 17,510 yen from 2015-01-01. The FY2026 amount is 17,920 yen a month (Japan Pension Service, `sources/social/nenkin_kokumin_hokenryo.html`; our `parameters/baseline_2026/social_insurance.yaml` line 59). Proposed change, adding one dated value and keeping the old one:

```yaml
values:
  2015-01-01:
    value: 17510
  2026-04-01:          # 令和8年度 (April 2026 – March 2027)
    value: 17920
```

Small, self-contained, and backed by a national primary source, so it is a good first pull request. Opening it is for the project owner; it is not urgent.
