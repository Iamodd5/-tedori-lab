# Validation

## 1. Hand calculations

Each household's 2026 disposable income was worked out by hand, step by step, from the rule files (`tests/hand_calcs/H1.md` … `H8.md`). `tests/test_baseline.py` checks the engine against them with a 1,000-yen tolerance.

| Household | Hand calculation (yen) | Engine (yen) | Gap |
|---|---|---|---|
| H1 | 1,061,652 | 1,061,652 | 0 |
| H2 | 1,000,000 | 1,000,000 | 0 |
| H3 | 6,248,008 | 6,248,008 | 0 |
| H4 | 4,961,316 | 4,961,316 | 0 |
| H5 | 2,208,436 | 2,208,436 | 0 |
| H6 | 2,683,201 | 2,683,201 | 0 |
| H7 | 2,170,281 | 2,170,281 | 0 |
| H8 | 12,009,068 | 12,009,068 | 0 |

Caveat: the hand calculations and the engine were written by the same author (Claude, an AI) from the same rule files. They catch arithmetic and coding slips, not misreadings of the law. The official checks in section 2 are the independent ones. The persona review of 2026-11-03 found two misreadings that both had missed (section 11): the resident-tax rounding and the earner count in the NHI reduction test.

## 2. Official worked examples and tables

| Check | Source | Result |
|---|---|---|
| Employment income for salary 8,970,000 = 7,020,000; income-adjustment deduction 47,000 | NTA 令和8年分 年末調整のしかた p.58 | match |
| Basic deduction 620,000; spouse deduction 380,000; 特定親族特別控除 410,000 | same, p.59 | match |
| Tax on 2,146,000 taxable = 117,100; ×102.1% rounding to 100 yen | same, p.59 | match |
| Employment-income table rows (6 points incl. band edges) | same, pp.3, 48 | match |
| Shinjuku NHI, one member, incomes 1.1m / 2.0m / 3.0m, under 40 and 40–64 | 新宿区 令和8年度 国民健康保険料 概算早見表 | match (all 6) |
| 協会けんぽ Tokyo premium lookups | 令和8年3月分からの保険料額表 | match |
| Resident tax rounded separately for 特別区民税 and 都民税: taxable 3,334,000 → 201,500 + 133,300 | 大田区 住民税の計算のしくみ (worked example) | match |
| Resident-tax 特定親族特別控除, 令和9年度 bands | 大田区 所得控除 table; 地方税法314条の2第1項第12号 | match |
| Just above the income-levy exemption line (income 1,124,200, line 1,120,000) | MIC 資料３ p.18 figure | **conflict**: the figure shows one combined levy of 4,200; the law caps each tax in proportion and rounds each, giving 2,500 + 1,600 = 4,100. The engine follows the law; the test from the figure is kept and marked as an expected failure (Q22) |

## 3. Comparison with OpenFisca-Japan (commit 1f8d13d)

Same salaries, each run as a single person in OpenFisca-Japan with the calculation date 2026-12-01 (OpenFisca-Japan computes every value for a given day; `scripts/crosscheck_openfisca.py`; `make all` rebuilds the numbers into `outputs/openfisca_check.json`, and a test checks this table against it). Differences are expected because OpenFisca-Japan has not been updated for the 2025–2026 tax changes and uses a flat health-insurance rate (docs/COVERAGE.md).

| Household | Person | Salary | Social ins. (ours) | (OF-J) | Income tax (ours) | (OF-J) | Resident tax (ours) | (OF-J) |
|---|---|---|---|---|---|---|---|---|
| H1 | a | 1,250,000 | 183,348 | 183,125 | 0 | 0 | 5,000 | 5,000 |
| H3 | a | 4,500,000 | 669,564 | 659,250 | 74,000 | 72,013 | 208,500 | 188,563 |
| H3 | b | 3,000,000 | 457,728 | 439,500 | 26,600 | 25,034 | 115,600 | 96,538 |
| H8 | a | 9,000,000 | 1,285,188 | 1,280,700 | 603,700 | 580,271 | 530,800 | 517,918 |
| H8 | b | 7,000,000 | 1,039,644 | 1,025,500 | 276,100 | 244,403 | 375,500 | 358,438 |

Likely causes, not yet traced line by line:
- Social insurance: OF-J uses a 10% health rate on actual pay instead of the Tokyo 9.85% rate on banded pay, and has no 子ども・子育て支援金.
- Income tax: OF-J's results are not rounded to 100 yen, and it uses 2025 employment-income rules.
- Resident tax: for the four people above the flat per-person levy, OF-J is 12,882–19,937 yen lower (H1 is the same). The cause is not yet found (Q27).
- Corrections: until 2026-11-02 the line above said "about 17,000–20,000 yen lower", and the website repeated it; H8 a was 12,982 lower, so the range was wrong. On 2026-11-03 our resident tax for H3 b and H8 a fell by 100 yen (section 11), so the range is now 12,882–19,937. Both are in the website's corrections log.

## 4. Outside calculator

Not done yet: take-home pay for H1, H3 and H8 at three incomes compared with a reputable public calculator.

## 5. Designs (history: the first Daiwa reading, superseded by section 9)

| Check | Ours | Published | Why they differ |
|---|---|---|---|
| Daiwa: single employee, salary 5,000,000 (age 30) | −40,700 yen/year | −13,000 (Daiwa p.7) | Daiwa used 2025 rules (basic deduction 680,000 for this worker). Under 2026 rules the deduction is 1,040,000, so losing it costs more. Q19, answered 2026-11-01; see §9. |
| Daiwa: H1, H3, H7 | +40,200 / −18,300 / −20,700 | hand calculations, `tests/hand_calcs/daiwa.md` | match to the yen |

Correction 2026-11-03: this table said "basic deduction 580,000". Under 2025 rules a single employee on 5,000,000 has total income 3,560,000 and a basic deduction of 680,000 (NTA No.1199; 580,000 applies only above 6,550,000).

## 6. Wall map

| Check | Engine | Hand calculation |
|---|---|---|
| H1, salary 1,110,000 → 1,120,000 (premium band 88,000 → 98,000) | marginal rate 170.88% | 170.88% (`tests/hand_calcs/wall_H1.md`) |
| H1, salary 1,050,000 → 1,060,000 (in employee insurance from January rather than October) | take-home +69,994 | +69,994 (wall_H1.md, revision 2026-11-03) |
| H5, salary 2,090,000 → 2,100,000 | resident tax +31,100 | Shinjuku single-parent exemption ends at total income 1,350,000 (`resident_tax.yaml` non_taxable) |
| H4, spouse salary 1,290,000 → 1,300,000 (the 1.3m wall) | take-home −258,226; marginal rate 2,682% | −258,226 (`tests/hand_calcs/wall_H4.md`, revision 2026-11-01) |
| H4, the same step: why | national pension +215,040, NHI +101,786, income tax −16,100, resident tax −32,500 | same (wall_H4.md) |
| H6, head's pension 1,700,000 | take-home 2,414,941 | 2,414,941 (`tests/hand_calcs/H6.md`, revision 2026-11-03) |

A test written first expected a wall at 1,056,000 for H1. It was wrong: H1 is single, so joining employee insurance replaces the more expensive NHI + national pension (see Q21). The test was replaced, before any commit, by the documented hand calculation above.

The H4 wall was −281,926 at first, −280,126 after the resident-tax limit was corrected (section 8) and −258,226 since 2026-11-01, when the higher earner deducts the spouse's national pension (wall_H4.md). The website shows the current value.

The list of walls on the website uses 10,000-yen steps and leaves out the step from income 0 (a full-time employee paid nothing is not a real case). The "extra ¥100,000" chart uses 100,000-yen steps, so a wall narrower than 100,000 yen may not go below zero there; the website says so under the chart and marks the listed walls on the take-home chart. Since 2026-11-03 the chart also leaves out income 0, as the list does.

### Two baseline rules corrected after the wall map exposed them

1. **NHI low-income reduction test.** It must count the householder's income even when the householder is on employee insurance ("世帯主と被保険者全員の前年中の総所得金額等", Shinjuku reduction page). Before the fix, H4's spouse at 1.3m was wrongly given a 50% cut (59,349 instead of 101,786). No reference household was affected.
2. **Resident-tax burden-relief band.** Just above the income-levy exemption line, the income levy is capped at the excess over the line (MIC p.18 figure; 地方税法附則3条の3). Before the fix, H3's head at salary 2.21m → 2.22m lost 85,000 on a 10,000 raise. No reference household was affected.

## 7. Government's own figures (cross-check only)

| Check | Ours | Government | Note |
|---|---|---|---|
| Pay at which take-home recovers after the 1.3m wall (spouse becomes a category-1 pension member) | 1,640,000 (H4, first salary on the 10,000 grid where take-home ≥ the 1,290,000 level) | about 1,600,000 (outline p.10, 第三 一 2(1)③) | The government's figure is rounded and its household is not stated; ours is a Shinjuku household with the head on 5.0m. Same order of size. This row said 1,650,000 until 2026-11-03 (the value before the 2026-11-01 revision). |

## 8. Corrections from the first self-review (2026-11-01)

| Fix | Effect at reference incomes | Effect on wall maps |
|---|---|---|
| Elderly spouse (70+) deduction now used: income tax 480,000 (NTA p.55), resident tax 380,000, 調整控除 difference 100,000 | none (H6 head is below the resident-tax line) | H6 at higher head pensions pays less tax |
| Higher-earning partner claims the spouse and children; a partner can be the dependant of an employee-insured spouse (Q23) | none | H3/H8 at low head pay: no NHI or national pension when the spouse is an employee; spouse deduction claimed by the earner (hand calc `claimant.md`: 26,600 → 7,200) |
| Resident-tax spouse/dependant income limit 480,000 → 580,000 (MIC p.28) | none | H4's 1.3m wall: −281,926 → −280,126 (superseded: −258,226 since 2026-11-01, section 6) |

The H4 wall test's expected value was changed from 29.1926 to 29.0126, and on 2026-11-01 to 26.8226. Each time the hand calculation was corrected first, with the source for the change, and the test was watched failing before the parameter was fixed. Changes to tests are listed here so they are visible.

A snapshot test now fails if any household × design result changes without `make outputs` being rerun.

## 9. Daiwa: the credit from Daiwa's formula on 2026 rules (52,000)

| Check | Ours | Published / hand calc | Note |
|---|---|---|---|
| Formula on 2025 rules (minimum 650,000) | 56,500 | 56,500 (Daiwa p.1) | our formula reproduces Daiwa's number exactly |
| Formula on 2026 rules | 52,000 | (1,780,000 − 740,000) × 5% | used for all results |
| H1, H3, H7 | +35,700 / −27,500 / −25,200 | `tests/hand_calcs/daiwa.md` (revision) | match to the yen |
| Single employee, salary 5,000,000 | −45,300 | −13,000 (Daiwa p.7) | most of the gap: under 2026 rules this worker loses a 1,040,000 basic deduction, against 680,000 under the 2025 rules Daiwa used |

## 10. Population view — calibration against official statistics

Numbers from `outputs/population.json` → `calibration` (rebuilt by `make all`). The model is a 2024 survey run under 2026 rules, so a perfect match is not expected; the gaps are listed so readers can judge them.

The tax comparators are not tax actually collected. They are the 2024 全国家計構造調査's own estimate of income tax and resident tax, which the Statistics Bureau works out from the incomes people reported (table 第3-32-1, summed over the cells the model uses). They come from the same table the model is built on, so this is a consistency check, not an independent one.

| Check | Model | Official | Gap | Why |
|---|---|---|---|---|
| Households | 53,536,652 (+254,087 in cells the survey hides) | 55,058,000 (国民生活基礎調査 2025) | −2.8% | different survey and year; the hidden cells are too small to model |
| People aged 65+ | 26,897,965 | 33,376,907 (same survey, Σ 65歳以上人員) | −19% | older people who work are modelled in work households at age 64 or under |
| Income tax | 10.17 trillion (2026 rules) | 11.64 trillion (the survey's own estimate of tax, 2024) | −12.6% | 2025–26 tax cuts (larger basic deduction), averages taxed instead of individuals, rent and interest not modelled |
| Resident tax | 12.23 trillion | 12.81 trillion (the survey's own estimate of tax) | −4.5% | as above, smaller because resident tax changed less |
| Income modelled | 297.5 trillion | 316.9 trillion (survey 年間収入) | −6% | rent, interest, transfers left out; 4.3 trillion of other members' earnings had nobody to go to |
| Food at 8%, per household per month | 54,832 (Oct–Nov 2024) | 57,177 (家計調査 2025 full year) | −4% | season; not used by any number yet (the food tax cut cannot be calculated yet) |

**Wage earners by pay band** (people with any salary, model vs 民間給与実態統計調査 令和7年分: private-sector earners who worked the full year, and, separately, those who worked part of the year). Each band is separate: "1–2m" means over 1m up to 2m.

| Pay | Model | Official, full year | Official, part of the year | Gap to full year |
|---|---|---|---|---|
| up to 1m | 15,284,541 | 3,703,056 | 5,982,206 | +313% |
| 1–2m | 14,622,271 | 5,824,930 | 929,309 | +151% |
| 2–3m | 7,578,733 | 6,745,640 | 986,585 | +12% |
| 3–4m | 7,617,433 | 7,986,672 | 621,454 | −5% |
| 4–5m | 5,659,320 | 7,917,758 | 276,015 | −29% |
| 5–6m | 4,955,611 | 6,144,924 | 136,777 | −19% |
| 6–7m | 3,782,120 | 4,035,253 | 64,794 | −6% |
| 7–8m | 2,360,337 | 2,776,867 | 44,854 | −15% |
| 8–9m | 1,547,603 | 1,833,950 | 30,897 | −16% |
| 9–10m | 1,007,523 | 1,266,070 | 20,871 | −20% |
| 10–15m | 1,187,905 | 2,422,427 | 53,697 | −51% |
| 15–20m | 492,655 | 609,530 | 13,450 | −19% |
| 20–25m | 52,372 | 167,273 | 1,985 | −69% |
| over 25m | 0 | 196,244 | 1,987 | −100% |
| Total | 66,148,424 | 51,630,594 | | +28% |

The official counts leave out public servants, so the model should be higher in total. Counting part-year workers too, about 9.69 million private-sector employees earned ¥1m or less, so the model's 15.28 million is about 1.6 times too many (it is about 4 times the full-year count alone). The top bands are too empty: averaging within a cell squeezes pay towards the middle, and adult children and relatives share an average salary (Q33). Too few high earners and 19% too few people aged 65+ matter for a plan that raises tax at the top.

**Decile boundaries** (highest cell average in each model decile vs the survey's own decile upper limits, 第1-21表): 1.74m / 1.86m, 2.69m / 2.59m, 3.22m / 3.28m, 4.14m / 4.00m, 4.73m / 4.83m, 5.74m / 5.77m, 7.17m / 6.99m, 8.69m / 8.50m, 11.15m / 11.00m. All within 7%.

**Daiwa cost** (2026 rules): income tax +1.53 trillion, refunds 0.58 trillion, net: the government collects 0.95 trillion more. Daiwa's own estimate (2025 rules, credit 56,500; p.7): income tax +0.7 trillion, refunds 0.7 trillion, net about zero. Most of the gap has the same cause as in §9: under 2026 rules the basic deduction that the design removes is larger (1,040,000 at incomes up to 4.89 million), so removing it raises more tax. Daiwa built its estimate from MIC tax-assessment statistics, not household-survey averages, and the model has too few high earners (above), so the second decimal place should not be relied on.

**Method changed during the milestone.** The first version split each cell by the share of people aged 65+. Its first run counted 35.8 million earners at 1 million yen or less, because it gave pensioners small salaries. It was replaced by the pension/work split before anything was published. The test and hand calculation were rewritten with it (`tests/hand_calcs/population.md`, revision note), and an arithmetic slip in the first hand calculation is recorded there too.

## 11. Corrections after the persona review (2026-11-03)

A simulated review (24 AI personas, docs/COWORK_REVIEW_PROMPT.md) reported errors that the checks above had missed. Each fix below was checked against a primary source saved in `sources/`, the hand calculation was corrected first, and the test was watched failing before the rule was changed.

| Fix | Source | Effect |
|---|---|---|
| Resident tax: 特別区民税 (6%) and 都民税 (4%) each rounded down to 100 yen, not the 10% once (Q14) | 地方税法20条の4の2第3項・第8項; 大田区 worked example | H3, H5 and H8 take-home +100; several walls move by 100 yen |
| Resident tax for 令和9年度: spouse/dependant income limit 580,000 → 620,000; working-student limit 750,000 → 890,000; 特定親族特別控除 added; every amount now cited to the law, so the "fiscal 2025 guide" approximation is gone (Q13) | 地方税法292条1項7号・9号, 314条の2 (令和8年法律第2号); 所得税法2条1項32号 | H2's wall at 1.5m: −97,172 → −75,572 (back at 1,590,000), plus a separate −18,458 wall at 1.63m; H3/H4 at spouse pay 1.33m–1.36m; population view |
| NHI reduction: an earner is someone with salary over 550,000, or pension over 600,000 (under 65) / 1,250,000 (65+); the 65+ 150,000 comes off pension income only (Q25) | 国民健康保険法施行令29条の7第6項第1号, 附則5条 | H6's walls 100,000 yen lower (1.78m → 1.68m, 2.4m → 2.3m); no change at reference incomes |
| Part-time wage test (88,000 a month) applied January–September only; from 2026-10-01 part-timers working 20+ hours at a 51+ firm are in employee insurance at any wage | 令和8年政令第275号; 日本年金機構 notice 2026-10-01 | H1 below 1,056,000 (e.g. 1,050,000: 814,839 → 834,858); population view |
| National pension ages 20–59 now read from parameters (Q30) | 国民年金法7条1項1号 | none |

Tests changed with these fixes, all after correcting the hand calculation: `expected.yaml` (H3, H5, H8 +100); `test_h1_baseline_walls_match_hand_calculation` (+90,013 → +69,994); `test_keep_per_100000` (income 0 left out of the chart); `test_resident_tax_relief_band_matches_mic_figure` kept and marked as an expected failure (section 2); `test_incomplete_designs_say_why` (Rengo also needs household food spending, because its plan abolishes the reduced 8% rate on food: Rengo 税制改革構想 PDF p.33).
