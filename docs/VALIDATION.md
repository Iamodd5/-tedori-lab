# Validation

## 1. Hand calculations

Each household's 2026 disposable income was worked out by hand, step by step, from the rule files (`tests/hand_calcs/H1.md` … `H8.md`). `tests/test_baseline.py` checks the engine against them with a 1,000-yen tolerance.

| Household | Hand calculation (yen) | Engine (yen) | Gap |
|---|---|---|---|
| H1 | 1,061,652 | 1,061,652 | 0 |
| H2 | 1,000,000 | 1,000,000 | 0 |
| H3 | 6,248,008 | 6,248,008 | 0 |
| H4 | 4,961,316 | 4,961,316 | 0 |
| H5 | 2,651,836 | 2,651,836 | 0 |
| H6 | 2,611,921 | 2,611,921 | 0 |
| H7 | 2,170,281 | 2,170,281 | 0 |
| H8 | 12,009,068 | 12,009,068 | 0 |

Caveat: the hand calculations and the engine were written by the same author from the same rule files. They catch arithmetic and coding slips, not misreadings of the law. The official checks in section 2 are the independent ones. A later review found two misreadings that both had missed (section 11): the resident-tax rounding and the earner count in the NHI reduction test.

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
| 児童扶養手当: full amount 48,050; partial range down to 11,340 just below the stop limit | こども家庭庁「児童扶養手当制度の概要」 (2026-04-08) | match |
| 65+ long-term-care premium: 18 bands, base 79,200; the 826,500 line | 新宿区 介護保険料の決まり方 (令和8年度); 介護保険法施行令38条1項 | match (the table's own amounts) |
| Just above the income-levy exemption line (income 1,124,200, line 1,120,000) | MIC 資料３ p.18 figure | match before rounding: the figure plots the income levy as a continuous line, 4,200 (2,520 + 1,680 by 地方税法附則3条の3), as the engine has it. The law then rounds each tax down to 100 yen (20条の4の2第3項): 2,500 + 1,600 = 4,100. A test written from the figure compared 4,200 with the rounded amount; it is kept as an expected failure so that going back to one combined rounding would be caught (Q22). An earlier version of this row wrongly called the figure a conflict with the law |

## 3. Comparison with OpenFisca-Japan (commit 1f8d13d)

Same salaries, each run as a single person in OpenFisca-Japan with the calculation date 2026-12-01 (OpenFisca-Japan computes every value for a given day; `scripts/crosscheck_openfisca.py`; `make all` rebuilds the numbers into `outputs/openfisca_check.json`, and a test checks this table against it). Differences are expected because OpenFisca-Japan has not been updated for the 2025–2026 tax changes and uses a flat health-insurance rate (docs/COVERAGE.md).

| Household | Person | Salary | Social ins. (ours) | (OF-J) | Income tax (ours) | (OF-J) | Resident tax (ours) | (OF-J) |
|---|---|---|---|---|---|---|---|---|
| H1 | a | 1,250,000 | 183,348 | 183,125 | 0 | 0 | 5,000 | 11,188 |
| H3 | a | 4,500,000 | 669,564 | 659,250 | 74,000 | 82,739 | 208,500 | 212,075 |
| H3 | b | 3,000,000 | 457,728 | 439,500 | 26,600 | 35,761 | 115,600 | 117,550 |
| H8 | a | 9,000,000 | 1,285,188 | 1,280,700 | 603,700 | 623,178 | 530,800 | 538,930 |
| H8 | b | 7,000,000 | 1,039,644 | 1,025,500 | 276,100 | 287,309 | 375,500 | 379,450 |

Each person is run as an employee in 厚生年金. OpenFisca-Japan assumes everyone pays National Pension unless told otherwise
(its input 国民年金保険に加入している defaults to yes), so the comparison now says no for employees. An earlier version
left it at yes: OpenFisca-Japan then deducted 210,120 yen of National Pension that employees don't pay, and its resident
tax came out 12,882–19,937 yen lower than ours (OPEN_QUESTIONS Q27, now explained).

Remaining differences, traced step by step:
- Social insurance: OF-J uses a 10% health rate on actual pay instead of the Tokyo 9.85% rate on banded pay, and has no 子ども・子育て支援金.
- Income tax: OF-J uses the 2025 basic deduction (880,000 for H3, 630,000 and 580,000 for H8, against 1,040,000, 670,000 and 620,000 for 2026) and the 2025 employment-income deduction (H1: income 700,000 against 510,000); it doesn't apply the income adjustment deduction for H8 a (salary over 8.5m with a child under 23: 50,000); and it doesn't round to 100 yen.
- Resident tax: OF-J's 調整控除 drops to 0 above taxable income of 2m, where the law keeps a minimum of 5% of 50,000 (地方税法314条の6第2号): 2,500 yen for H3 a and both H8 earners. Together with the social-insurance difference, the missing income adjustment (H8 a) and no rounding, OF-J is 1,950–8,130 yen higher. H1: OF-J's 2025 employment-income rules leave 86,875 yen taxable where ours leave nothing, so OF-J charges 6,188 yen of 所得割.
- These OF-J differences (the National Pension default for employees, the 調整控除 minimum, the income adjustment deduction) are candidates for upstream fixes (docs/COVERAGE.md).

## 4. Outside calculator

Not done yet: take-home pay for H1, H3 and H8 at three incomes compared with a reputable public calculator.

## 5. Designs (history: the first Daiwa reading, superseded by section 9)

| Check | Ours | Published | Why they differ |
|---|---|---|---|
| Daiwa: single employee, salary 5,000,000 (age 30) | −40,700 yen/year | −13,000 (Daiwa p.7) | Daiwa used 2025 rules (basic deduction 680,000 for this worker). Under 2026 rules the deduction is 1,040,000, so losing it costs more. Q19; see §9. |
| Daiwa: H1, H3, H7 | +40,200 / −18,300 / −20,700 | hand calculations, `tests/hand_calcs/daiwa.md` | match to the yen |

Correction: an earlier version of this table said "basic deduction 580,000". Under 2025 rules a single employee on 5,000,000 has total income 3,560,000 and a basic deduction of 680,000 (NTA No.1199; 580,000 applies only above 6,550,000).

## 6. Wall map

| Check | Engine | Hand calculation |
|---|---|---|
| H1, salary 1,110,000 → 1,120,000 (premium band 88,000 → 98,000) | marginal rate 170.88% | 170.88% (`tests/hand_calcs/wall_H1.md`) |
| H1, salary 1,050,000 → 1,060,000 (joins employee insurance at 88,000 a month; employment insurance at both) | take-home +95,257 | +95,257 (wall_H1.md, revision 2) |
| H5, salary 2,090,000 → 2,100,000 | resident tax +31,100 | Shinjuku single-parent exemption ends at total income 1,350,000 (`resident_tax.yaml` non_taxable) |
| H4, spouse salary 1,290,000 → 1,300,000 (the 1.3m wall) | take-home −258,226; marginal rate 2,682% | −258,226 (`tests/hand_calcs/wall_H4.md`) |
| H4, the same step: why | national pension +215,040, NHI +101,786, income tax −16,100, resident tax −32,500 | same (wall_H4.md) |
| H6, head's pension 1,700,000 | take-home 2,343,661 | 2,343,661 (`tests/hand_calcs/H6.md`, with the 65+ long-term-care premiums) |

A test written first expected a wall at 1,056,000 for H1. It was wrong: H1 is single, so joining employee insurance replaces the more expensive NHI + national pension (see Q21). The test was replaced, before any commit, by the documented hand calculation above.

The H4 wall was −281,926 at first, −280,126 after the resident-tax limit was corrected (section 8) and −258,226 since the higher earner deducts the spouse's national pension (wall_H4.md). The website shows the current value.

The list of walls on the website uses 10,000-yen steps and leaves out the step from income 0 (a full-time employee paid nothing is not a real case). The "extra ¥100,000" chart uses 100,000-yen steps, so a wall narrower than 100,000 yen may not go below zero there; the website says so under the chart and marks the listed walls on the take-home chart. The chart also leaves out income 0, as the list does.

### Two baseline rules corrected after the wall map exposed them

1. **NHI low-income reduction test.** It must count the householder's income even when the householder is on employee insurance ("世帯主と被保険者全員の前年中の総所得金額等", Shinjuku reduction page). Before the fix, H4's spouse at 1.3m was wrongly given a 50% cut (59,349 instead of 101,786). No reference household was affected.
2. **Resident-tax burden-relief band.** Just above the income-levy exemption line, the income levy is capped at the excess over the line (MIC p.18 figure; 地方税法附則3条の3). Before the fix, H3's head at salary 2.21m → 2.22m lost 85,000 on a 10,000 raise. No reference household was affected.

## 7. Government's own figures (cross-check only)

| Check | Ours | Government | Note |
|---|---|---|---|
| Pay at which take-home recovers after the 1.3m wall (spouse becomes a category-1 pension member) | 1,640,000 (H4, first salary on the 10,000 grid where take-home ≥ the 1,290,000 level) | about 1,600,000 (outline p.10, 第三 一 2(1)③) | The government's figure is rounded and its household is not stated; ours is a Shinjuku household with the head on 5.0m. Same order of size. An earlier version of this row said 1,650,000 (the value before the H4 revision in section 6). |

## 8. Corrections from an internal review

| Fix | Effect at reference incomes | Effect on wall maps |
|---|---|---|
| Elderly spouse (70+) deduction now used: income tax 480,000 (NTA p.55), resident tax 380,000, 調整控除 difference 100,000 | none (H6 head is below the resident-tax line) | H6 at higher head pensions pays less tax |
| Higher-earning partner claims the spouse and children; a partner can be the dependant of an employee-insured spouse (Q23) | none | H3/H8 at low head pay: no NHI or national pension when the spouse is an employee; spouse deduction claimed by the earner (hand calc `claimant.md`: 26,600 → 7,200) |
| Resident-tax spouse/dependant income limit 480,000 → 580,000 (MIC p.28) | none | H4's 1.3m wall: −281,926 → −280,126 (superseded: now −258,226, section 6) |

The H4 wall test's expected value was changed from 29.1926 to 29.0126, and later to 26.8226. Each time the hand calculation was corrected first, with the source for the change, and the test was watched failing before the parameter was fixed. Changes to tests are listed here so they are visible.

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

The tax comparators are not tax actually collected. They are the 2024 全国家計構造調査's own estimate of income tax and resident tax, which the Statistics Bureau works out from the incomes people reported (table 第3-32-1, summed over the cells the model uses). They come from the same table the model is built on, so this is a consistency check, not an independent one. We have not confirmed whether the survey's 2024 tax estimate takes off the one-off flat-rate tax cut of 2024 (定額減税); if it does, the official figures are lower than in a normal year and the model's gap is smaller than shown.

| Check | Model | Official | Gap | Why |
|---|---|---|---|---|
| Households | 53,536,652 (+254,087 in cells the survey hides) | 55,058,000 (国民生活基礎調査 2025) | −2.8% | different survey and year; the hidden cells are too small to model |
| People aged 65+ | 26,897,965 | 33,376,907 (全国家計構造調査 2024, the table the model is built from, Σ 65歳以上人員) | −19% | older people who work are modelled in work households at age 64 or under |
| Income tax | 9.12 trillion (2026 rules) | 11.64 trillion (the survey's own estimate of tax, 2024) | −21.6% | 2025–26 tax cuts (larger basic deduction), averages taxed instead of individuals, rent and interest not modelled |
| Resident tax | 12.17 trillion | 12.81 trillion (the survey's own estimate of tax) | −5.0% | as above, smaller because resident tax changed less |
| Income modelled | 297.5 trillion | 316.9 trillion (survey 年間収入) | −6% | rent, interest, transfers left out; 4.3 trillion of other members' earnings had nobody to go to |
| Food at 8%, per household per month | 54,832 (Oct–Nov 2024) | 57,177 (家計調査 2025 full year) | −4% | season; not used by any number yet (the food tax cut cannot be calculated yet) |

**Wage earners by pay band** (people with any salary, model vs 民間給与実態統計調査 令和7年分: private-sector earners who worked the full year, and, separately, those who worked part of the year). Each band is separate: "1–2m" means over 1m up to 2m.

| Pay | Model | Official, full year | Official, part of the year | Gap to full year |
|---|---|---|---|---|
| up to 1m | 6,916,206 | 3,703,056 | 5,982,206 | +87% |
| 1–2m | 12,404,620 | 5,824,931 | 929,310 | +113% |
| 2–3m | 12,568,392 | 6,745,640 | 986,586 | +86% |
| 3–4m | 9,746,749 | 7,986,672 | 621,454 | +22% |
| 4–5m | 7,082,389 | 7,917,759 | 276,016 | -11% |
| 5–6m | 5,392,662 | 6,144,924 | 136,777 | -12% |
| 6–7m | 3,244,262 | 4,035,252 | 64,794 | -20% |
| 7–8m | 1,965,479 | 2,776,867 | 44,854 | -29% |
| 8–9m | 938,648 | 1,833,950 | 30,897 | -49% |
| 9–10m | 625,624 | 1,266,070 | 20,872 | -51% |
| 10–15m | 847,754 | 2,422,426 | 53,697 | -65% |
| 15–20m | 272,693 | 609,530 | 13,450 | -55% |
| 20–25m | 52,372 | 167,273 | 1,985 | -69% |
| over 25m | 0 | 196,243 | 1,987 | -100% |
| Total | 62,057,850 | 51,630,593 | | +20% |

The official counts leave out public servants, so the model should be higher in total. At ¥1m or less the model (6.92 million) now lies between the full-year count (3.70 million) and the count including part-year workers (9.69 million). It has too many people earning ¥1m–3m (24.97 million against 14.49 million including part-year workers) and too few earning ¥10m or more. Averaging within a cell squeezes pay towards the middle. Too few high earners and 19% too few people aged 65+ matter for a plan that raises tax at the top.

**Earners other than the head (Q33, changed 2026-11-04).** Earlier versions gave the survey's "other members' earnings" to every adult child and relative in every household, which made 15.28 million earners at ¥1m or less (1.6 times the official count including part-year workers). Now the survey's number of earners per household decides how many spouses and other adults earn: the earners beyond the head are spread evenly over spouses and other adults, and those who earn get the cell's average divided by that share (`tests/hand_calcs/population.md` section 5). This also gives working spouses more realistic pay: before, in cells with an adult child, all the room for extra earners went to the child, so only a few spouses earned, at high pay. Effects: earners 66.15 → 62.06 million; income tax 10.13 → 9.12 trillion (lower pay for spouses and other adults, and more of them claimed as dependants); Daiwa's refunds 0.58 → 0.38 trillion (fewer people with too little tax to use the credit).

**Dependants aged 70 and over (Q32, 2026-11-04).** The model now gives the larger deduction for a dependant aged 70+ (income tax 480,000, or 580,000 for a parent living with the taxpayer; resident tax 380,000 or 450,000). Every relative aged 70+ in the model is treated as a parent of the head or spouse living with them (labelled approximation). People with both salary and pension income now get the income adjustment deduction (Q41). Together these lower income tax by less than 0.01 trillion.

**Decile boundaries** (highest cell average in each model decile vs the survey's own decile upper limits, 第1-21表): 1.74m / 1.86m, 2.69m / 2.59m, 3.22m / 3.28m, 4.14m / 4.00m, 4.73m / 4.83m, 5.74m / 5.77m, 7.17m / 6.99m, 8.69m / 8.50m, 11.15m / 11.00m. All within 7%.

**Daiwa cost** (2026 rules): income tax +1.47 trillion, refunds 0.38 trillion, net: the government collects 1.09 trillion more (the result pages round these to 0.1 trillion: 1.5, 0.4 and 1.1). Daiwa's own estimate (2025 rules, credit 56,500; p.7): income tax +0.7 trillion, refunds 0.7 trillion, net about zero. Most of the gap has the same cause as in §9: under 2026 rules the basic deduction that the design removes is larger (1,040,000 at incomes up to 4.89 million), so removing it raises more tax. Daiwa built its estimate from MIC tax-assessment statistics, not household-survey averages, and the model has too few high earners (above). The refund total depends on how many people earn little, which the survey averages can't pin down: it moved from 0.58 to 0.38 trillion when the split of other earners changed (above). So the second decimal place should not be relied on.

**Method changed during development.** The first version split each cell by the share of people aged 65+. Its first run counted 35.8 million earners at 1 million yen or less, because it gave pensioners small salaries. It was replaced by the pension/work split before anything was published. The test and hand calculation were rewritten with it (`tests/hand_calcs/population.md`, revision note), and an arithmetic slip in the first hand calculation is recorded there too.

## 11. Corrections after review

A review of the published site reported errors that the checks above had missed. Each fix below was checked against a primary source saved in `sources/`. For the rounding, NHI-earner and wage-test fixes the hand calculation was corrected first and the test was watched failing before the rule was changed. For the 令和9年度 limits this was not true at first: no hand calculation or test depended on 620,000 or 890,000, so the tests still passed with the old limits. The second review found this (section 12), and the 890,000 limit now has a hand calculation and a test; the 620,000 limit is checked against the law text only (Q40).

| Fix | Source | Effect |
|---|---|---|
| Resident tax: 特別区民税 (6%) and 都民税 (4%) each rounded down to 100 yen, not the 10% once (Q14) | 地方税法20条の4の2第3項・第8項; 大田区 worked example | H3, H5 and H8 take-home +100; several walls move by 100 yen |
| Resident tax for 令和9年度: spouse/dependant income limit 580,000 → 620,000; working-student limit 750,000 → 890,000; 特定親族特別控除 added; every amount now cited to the law, so the "fiscal 2025 guide" approximation is gone (Q13) | 地方税法292条1項7号・9号, 314条の2 (令和8年法律第2号); 所得税法2条1項32号 | H2's wall at 1.5m: −97,172 → −75,572 (back at 1,590,000), plus a separate −18,458 wall at 1.63m; H3 at the head's pay and H4 at the spouse's pay of 1.33m–1.36m; population view |
| NHI reduction: an earner is someone with salary over 550,000, or pension over 600,000 (under 65) / 1,250,000 (65+); the 65+ 150,000 comes off pension income only (Q25) | 国民健康保険法施行令29条の7第6項第1号, 附則5条 | H6's walls 100,000 yen lower (1.78m → 1.68m, 2.4m → 2.3m); no change at reference incomes |
| Part-time wage test (88,000 a month) applied January–September only; from 2026-10-01 part-timers working 20+ hours at a 51+ firm are in employee insurance at any wage. **Withdrawn in section 12**: it missed the 特定減額特例 rule | 令和8年政令第275号; 日本年金機構 notice 2026-10-01 | H1 below 1,056,000 (e.g. 1,050,000: 814,839 → 834,858); population view |
| National pension ages 20–59 now read from parameters (Q30) | 国民年金法7条1項1号 | none |

Tests changed with these fixes, all after correcting the hand calculation: `expected.yaml` (H3, H5, H8 +100); `test_h1_baseline_walls_match_hand_calculation` (+90,013 → +69,994); `test_keep_per_100000` (income 0 left out of the chart); `test_resident_tax_relief_band_matches_mic_figure` kept and marked as an expected failure (section 2); `test_incomplete_designs_say_why` (Rengo also needs household food spending, because its plan abolishes the reduced 8% rate on food: Rengo 税制改革構想 PDF p.33).

## 12. Corrections after a second review

A second review checked the fixes in section 11 against the law and the published site. What it found, and what changed:

| Fix | Source | Effect |
|---|---|---|
| The October split of section 11 is withdrawn. From October 2026, a part-timer on 20+ hours paid under 88,000 a month can only be a worker paid below the minimum wage with an exception (the lowest rate in force from October to December is 1,023 yen: 20 hours a week pays 88,660 a month), and such a worker (特定減額特例対象者) joins company insurance only if they ask. We assume they don't, so the 88,000 line decides for all 12 months again | 厚生年金保険法附則4条の6, 健康保険法附則8条の3の2; 厚生労働省 令和8年度地域別最低賃金 全国一覧 | H1 at 1,050,000: 834,858 → 809,595; the step to 1,060,000: +69,994 → +95,257 (`wall_H1.md`, revision 2). Population view: nobody changes scheme in October, which also removes a fault where the Daiwa cash cap missed October joiners' premiums |
| Employment insurance is charged to every non-student wage earner on 20+ hours, in or out of company insurance (Q24 answered) | 雇用保険法6条 | H1 below 1,056,000: −5,244 a year (437 × 12 at 1,050,000); population view |
| Rengo's cost of 1.5–2 trillion yen was paired with "about 6 million people", which is Rengo's count for the taper band only; it is for about 21 million employees | 連合「税制改革構想」 pp.27–28 | text only |
| The ministry figure in section 2 is a match before rounding, not a conflict | MIC 資料３ p.18; 地方税法20条の4の2第3項 | text only; the expected-failure test now says why it fails |
| Official pay-band counts now read from the table's 計 rows (adding men and women was off by 1 in nine cells) | 民間給与実態統計調査 令和7年分 第3表 | section 10 table |
| Household NHI counts toward the head's Daiwa cash cap whenever the head works (before, not when the head was in company insurance) | Daiwa p.4 | none (the head's own premiums already exceed the credit) |

Tests changed, each after the hand calculation: `test_h1_baseline_walls_match_hand_calculation` (+69,994 → +95,257, plus take-home 809,595 at 1,050,000). New: `test_h2_walls_match_hand_calculation` (`H2.md`, wall map points; it fails if the working-student limit goes back to 750,000) and `test_wall_map_section_matches_engine` (the "Engine" column of section 6).

## 13. Rules added before release

Four rules that were listed as missing are now in the calculation, each from a hand calculation written first and tested.

| Rule | Source | Effect |
|---|---|---|
| Single-parent allowance (児童扶養手当): 48,050 a month for the first child and 11,350 for each further one, reduced above an income limit and stopped at a higher one; a public pension of the parent is taken off month by month | 児童扶養手当法, 施行令2条の2, 2条の4, 4条, 6条の5 | H5 receives 443,400 a year: take-home 2,208,436 → 2,651,836 (`tests/hand_calcs/H5.md`). A new wall where it stops (salary 3.85m) |
| Long-term-care premium for people 65 and over (Shinjuku, fiscal 2026) | 新宿区 table; 介護保険法施行令38条 | H6 pays 51,480 + 19,800: take-home 2,683,201 → 2,611,921 (`tests/hand_calcs/H6.md`). A new wall where the head starts to pay resident tax (pension 2.12m) |
| Resident-tax spouse deduction for earners with total income above 9m (220,000 / 110,000) | 地方税法314条の2第1項第10号・第10号の2, 314条の6 | none of H1–H8 at their reference incomes; resident tax 11,000–22,000 lower than before for such earners (`tests/hand_calcs/spouse_rt.md`) |
| Student pension deferral only while the student's income after insurance is at most 1,280,000 | 国民年金法90条の3; 施行令6条の9, 6条の12 | H2's wall map: national pension 215,040 from a salary of about 2.2m (step −174,798, `tests/hand_calcs/H2.md`) |

The all-household numbers moved a little with these rules (for example the Daiwa plan's net effect on government revenue, 0.95 → 0.94 trillion; it later became 1.09 trillion with the change in §10). Still not modelled: the National Pension exemption for low incomes, which has to be applied for and lowers the future pension (Q20).

