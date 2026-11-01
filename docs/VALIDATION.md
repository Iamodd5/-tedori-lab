# Validation

## 1. Hand calculations (Milestone 2 acceptance)

Each household's 2026 disposable income was worked out by hand, step by step, from the rule files (`tests/hand_calcs/H1.md` … `H8.md`). `tests/test_baseline.py` checks the engine against them with a 1,000-yen tolerance.

| Household | Hand calculation (yen) | Engine (yen) | Gap |
|---|---|---|---|
| H1 | 1,061,652 | 1,061,652 | 0 |
| H2 | 1,000,000 | 1,000,000 | 0 |
| H3 | 6,247,908 | 6,247,908 | 0 |
| H4 | 4,961,316 | 4,961,316 | 0 |
| H5 | 2,208,336 | 2,208,336 | 0 |
| H6 | 2,683,201 | 2,683,201 | 0 |
| H7 | 2,170,281 | 2,170,281 | 0 |
| H8 | 12,008,968 | 12,008,968 | 0 |

Caveat: the hand calculations and the engine were written by the same author (Claude) from the same rule files. They catch arithmetic and coding slips, not misreadings of the law. The official checks in section 2 and the outside calculator check (section 4) are the independent ones.

## 2. Official worked examples and tables

| Check | Source | Result |
|---|---|---|
| Employment income for salary 8,970,000 = 7,020,000; income-adjustment deduction 47,000 | NTA 令和8年分 年末調整のしかた p.58 | match |
| Basic deduction 620,000; spouse deduction 380,000; 特定親族特別控除 410,000 | same, p.59 | match |
| Tax on 2,146,000 taxable = 117,100; ×102.1% rounding to 100 yen | same, p.59 | match |
| Employment-income table rows (6 points incl. band edges) | same, pp.3, 48 | match |
| Shinjuku NHI, one member, incomes 1.1m / 2.0m / 3.0m, under 40 and 40–64 | 新宿区 令和8年度 国民健康保険料 概算早見表 | match (all 6) |
| 協会けんぽ Tokyo premium lookups | 令和8年3月分からの保険料額表 | match |

## 3. Comparison with OpenFisca-Japan (commit 1f8d13d)

Same salaries, run as a single person in OpenFisca-Japan on 2026-12-01. Differences are expected because OpenFisca-Japan has not been updated for the 2025–2026 tax changes and uses a flat health-insurance rate (docs/COVERAGE.md).

| Household | Person | Salary | Social ins. (ours) | (OF-J) | Income tax (ours) | (OF-J) | Resident tax (ours) | (OF-J) |
|---|---|---|---|---|---|---|---|---|
| H1 | a | 1,250,000 | 183,348 | 183,125 | 0 | 0 | 5,000 | 5,000 |
| H3 | a | 4,500,000 | 669,564 | 659,250 | 74,000 | 72,013 | 208,500 | 188,563 |
| H3 | b | 3,000,000 | 457,728 | 439,500 | 26,600 | 25,034 | 115,700 | 96,538 |
| H8 | a | 9,000,000 | 1,285,188 | 1,280,700 | 603,700 | 580,271 | 530,900 | 517,918 |
| H8 | b | 7,000,000 | 1,039,644 | 1,025,500 | 276,100 | 244,403 | 375,500 | 358,438 |

Likely causes, not yet traced line by line:
- Social insurance: OF-J uses a 10% health rate on actual pay instead of the Tokyo 9.85% rate on banded pay, and has no 子ども・子育て支援金.
- Income tax: OF-J's results are not rounded to 100 yen, and it uses 2025 employment-income rules.
- Resident tax: OF-J is about 17,000–20,000 yen lower. The cause is not yet found; to be checked in Milestone 3 when choosing the first upstream contribution.

## 4. Outside calculator (spec 12.2)

Not done yet. Planned for Milestone 4: take-home pay for H1, H3 and H8 at three incomes compared with a reputable public calculator.

## 5. Designs (Milestone 3)

| Check | Ours | Published | Why they differ |
|---|---|---|---|
| Daiwa: single employee, salary 5,000,000 (age 30) | −40,700 yen/year | −13,000 (Daiwa p.7) | Daiwa used 2025 rules (basic deduction 580,000). Under 2026 rules the deduction is 1,040,000, so losing it costs more. Open as Q19. |
| Daiwa: H1, H3, H7 | +40,200 / −18,300 / −20,700 | hand calculations, `tests/hand_calcs/daiwa.md` | match to the yen |

## 6. Wall map (Milestone 4)

| Check | Engine | Hand calculation |
|---|---|---|
| H1, salary 1,110,000 → 1,120,000 (premium band 88,000 → 98,000) | marginal rate 170.88% | 170.88% (`tests/hand_calcs/wall_H1.md`) |
| H1, salary 1,050,000 → 1,060,000 (joins employee insurance) | take-home +90,013 | +90,013 |
| H5, salary 2,090,000 → 2,100,000 | resident tax 0 → 31,200 | Shinjuku single-parent exemption ends at total income 1,350,000 (`resident_tax.yaml` non_taxable) |

A test written first expected a wall at 1,056,000 for H1. It was wrong: H1 is single, so joining employee insurance replaces the more expensive NHI + national pension (see Q21). The test was replaced, before any commit, by the documented hand calculation above.
| H4, spouse salary 1,290,000 → 1,300,000 (the 1.3m wall) | take-home −281,926; marginal rate 2,919% | −281,926 (`tests/hand_calcs/wall_H4.md`) |

### Two baseline rules corrected after the wall map exposed them (Milestone 4)

1. **NHI low-income reduction test.** It must count the householder's income even when the householder is on employee insurance ("世帯主と被保険者全員の前年中の総所得金額等", Shinjuku reduction page). Before the fix, H4's spouse at 1.3m was wrongly given a 50% cut (59,349 instead of 101,786). No reference household was affected.
2. **Resident-tax burden-relief band.** Just above the income-levy exemption line, the income levy is capped at the excess over the line (MIC p.18 figure: line 1,120,000, income 1,124,200, levy 4,200). Before the fix, H3's head at salary 2.21m → 2.22m lost 85,000 on a 10,000 raise. No reference household was affected. Law text still to add (Q22).

## 7. Government's own figures (cross-check only)

| Check | Ours | Government | Note |
|---|---|---|---|
| Pay at which take-home recovers after the 1.3m wall (spouse becomes a category-1 pension member) | 1,650,000 (H4, first salary on the 10,000 grid where take-home ≥ the 1,290,000 level) | about 1,600,000 (outline p.10, 第三 一 2(1)③) | The government's figure is rounded and its household is not stated; ours is a Shinjuku household with the head on 5.0m. Same order of size. |

## 8. Corrections from the Milestone 5 review (2026-11-01)

| Fix | Effect at reference incomes | Effect on wall maps |
|---|---|---|
| Elderly spouse (70+) deduction now used: income tax 480,000 (NTA p.55), resident tax 380,000, 調整控除 difference 100,000 | none (H6 head is below the resident-tax line) | H6 at higher head pensions pays less tax |
| Higher-earning partner claims the spouse and children; a partner can be the dependant of an employee-insured spouse (Q23) | none | H3/H8 at low head pay: no NHI or national pension when the spouse is an employee; spouse deduction claimed by the earner (hand calc `claimant.md`: 26,600 → 7,200) |
| Resident-tax spouse/dependant income limit 480,000 → 580,000 (MIC p.28) | none | H4's 1.3m wall: −281,926 → **−280,126** (`wall_H4.md`, correction note) |

The H4 wall test's expected value was changed from 29.1926 to 29.0126. That was done by correcting the hand calculation first, with the source for the change, and watching the test fail before the parameter was fixed; it is listed here so the change is visible (CLAUDE.md rule 5).

A snapshot test (spec 12.1) now fails if any household × design result changes without `make outputs` being rerun.

## 9. Daiwa after H-12: B (credit from Daiwa's formula, 52,000)

| Check | Ours | Published / hand calc | Note |
|---|---|---|---|
| Formula on 2025 rules (minimum 650,000) | 56,500 | 56,500 (Daiwa p.1) | our formula reproduces Daiwa's number exactly |
| Formula on 2026 rules | 52,000 | (1,780,000 − 740,000) × 5% | used for all results |
| H1, H3, H7 | +35,700 / −27,500 / −25,200 | `tests/hand_calcs/daiwa.md` (revision) | match to the yen |
| Single employee, salary 5,000,000 | −45,300 | −13,000 (Daiwa p.7) | most of the gap: under 2026 rules this worker loses a 1,040,000 basic deduction, against 680,000 under the 2025 rules Daiwa used |

The §5 rows above (56,500 credit) are kept as history; they are superseded by this section.
