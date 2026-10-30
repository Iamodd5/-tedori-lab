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
