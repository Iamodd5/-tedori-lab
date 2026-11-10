# Validation

## 1. Hand calculations

Each household's 2026 disposable income was worked out by hand, step by step, from the rule files (`tests/hand_calcs/H1.md` … `H8.md`). `tests/test_baseline.py` checks that the engine matches them exactly, to the yen.

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

Caveat: the hand calculations and the engine were written by the same author from the same rule files. They catch arithmetic and coding slips, not misreadings of the law. The official checks in section 2 are the independent ones. A later check found two misreadings that both had missed (section 11): the resident-tax rounding and the earner count in the NHI reduction test.

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

Same salaries, each run as a single person in OpenFisca-Japan with the calculation date 2026-12-01 (OpenFisca-Japan computes every value for a given day; `scripts/crosscheck_openfisca.py`; `make all` rebuilds the numbers into `outputs/openfisca_check.json`, and a test checks this table against it). Differences are expected: OpenFisca-Japan has the 2025 basic deduction but not the 2025 change to the employment-income deduction or any 2026 change, and it uses a flat health-insurance rate (docs/COVERAGE.md).

| Household | Person | Salary | Social ins. (ours) | (OF-J) | Income tax (ours) | (OF-J) | Resident tax (ours) | (OF-J) |
|---|---|---|---|---|---|---|---|---|
| H1 | a | 1,250,000 | 183,348 | 183,125 | 0 | 0 | 5,000 | 11,188 |
| H3 | a | 4,500,000 | 669,564 | 659,250 | 74,000 | 82,739 | 208,500 | 212,075 |
| H3 | b | 3,000,000 | 457,728 | 439,500 | 26,600 | 35,761 | 115,600 | 117,550 |
| H8 | a | 9,000,000 | 1,285,188 | 1,280,700 | 603,700 | 623,178 | 530,800 | 538,930 |
| H8 | b | 7,000,000 | 1,039,644 | 1,025,500 | 276,100 | 287,309 | 375,500 | 379,450 |

Each person is run as an employee in 厚生年金. OpenFisca-Japan assumes everyone pays National Pension unless told otherwise
(its input 国民年金保険に加入している defaults to yes), so the comparison now says no for employees. An earlier version
left it at yes: OpenFisca-Japan then deducted <!-- history -->210,120<!-- /history --> yen of National Pension that employees don't pay, and its resident
tax came out <!-- history -->12,882–19,937<!-- /history --> yen lower than ours (OPEN_QUESTIONS Q27, now explained).

Remaining differences, traced step by step:
- Social insurance: OF-J works out health insurance at a 10% rate and employee pension at 18.3%, both on pay ÷ 12 rather than the pay band (標準報酬月額) that sets the real premium, and has no 子ども・子育て支援金. The pay band is the larger part of the gap for H3 b and H8 b. The lower premiums also lower OF-J's insurance deduction, which raises its income tax and resident tax a little.
- Income tax: OF-J uses the 2025 basic deduction (880,000 for H3, 630,000 and 580,000 for H8, against 1,040,000, 670,000 and 620,000 for 2026) and the employment-income deduction from before 2025 (minimum 550,000: H1's income is 700,000 there, 600,000 under the 2025 rule and 510,000 under 2026's); it doesn't apply the income adjustment deduction for H8 a (salary over 8.5m with a child under 23: 50,000); and it doesn't round to 100 yen.
- Resident tax: OF-J's 調整控除 drops to 0 above taxable income of 2m, where the law keeps a minimum of 5% of 50,000 (地方税法314条の6第2号 for the ward's 3%, 37条第2号 for Tokyo's 2%): 2,500 yen for H3 a and both H8 earners. Together with the social-insurance difference, the missing income adjustment (H8 a) and no rounding, OF-J is 1,950–8,130 yen higher. H1: OF-J's pre-2025 employment-income deduction leaves 86,875 yen taxable where ours leaves nothing, so OF-J charges 6,188 yen of 所得割 (under the 2025 rule there would be none either).
- These OF-J differences (the National Pension default for employees, the 調整控除 minimum, the income adjustment deduction, and the out-of-date deduction amounts) are candidates for upstream fixes (docs/COVERAGE.md).

## 4. Outside calculator

Not done yet: take-home pay for H1, H3 and H8 at three incomes compared with a reputable public calculator.

## 5. Designs (history: the first Daiwa reading, superseded by section 9)

<!-- history -->

| Check | Ours | Published | Why they differ |
|---|---|---|---|
| Daiwa: single employee, salary 5,000,000 (age 30) | −40,700 yen/year | −13,000 (Daiwa p.7) | Daiwa used 2025 rules (basic deduction 680,000 for this worker). Under 2026 rules the deduction is 1,040,000, so losing it costs more. Q19; see §9. |
| Daiwa: H1, H3, H7 | +40,200 / −18,300 / −20,700 | hand calculations, `tests/hand_calcs/daiwa.md` | match to the yen |

<!-- /history -->

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

The H4 wall was <!-- history -->−281,926 at first, −280,126<!-- /history --> after the resident-tax limit was corrected (section 8) and −258,226 since the higher earner deducts the spouse's national pension (wall_H4.md). The website shows the current value.

The list of walls on the website uses 10,000-yen steps and leaves out the step from income 0 (a full-time employee paid nothing is not a real case). The "extra ¥100,000" chart uses 100,000-yen steps, so a wall narrower than 100,000 yen may not go below zero there; the website says so under the chart and marks the listed walls on the take-home chart. The chart also leaves out income 0, as the list does.

### Two baseline rules corrected after the wall map exposed them

1. **NHI low-income reduction test.** It must count the householder's income even when the householder is on employee insurance ("世帯主と被保険者全員の前年中の総所得金額等", Shinjuku reduction page). Before the fix, H4's spouse at 1.3m was wrongly given a 50% cut (<!-- history -->59,349<!-- /history --> instead of 101,786). No reference household was affected.
2. **Resident-tax burden-relief band.** Just above the income-levy exemption line, the income levy is capped at the excess over the line (MIC p.18 figure; 地方税法附則3条の3). Before the fix, H3's head at salary 2.21m → 2.22m lost 85,000 on a 10,000 raise. No reference household was affected.

## 7. Government's own figures (cross-check only)

| Check | Ours | Government | Note |
|---|---|---|---|
| Pay at which take-home recovers after the 1.3m wall (spouse becomes a category-1 pension member) | 1,640,000 (H4, first salary on the 10,000 grid where take-home ≥ the 1,290,000 level) | about 1,600,000 (outline p.10, 第三 一 2(1)③) | The government's figure is rounded and its household is not stated; ours is a Shinjuku household with the head on 5.0m. Same order of size. An earlier version of this row said 1,650,000 (the value before the H4 revision in section 6). |

## 8. Corrections found by our own checks

| Fix | Effect at reference incomes | Effect on wall maps |
|---|---|---|
| Elderly spouse (70+) deduction now used: income tax 480,000 (NTA p.55), resident tax 380,000, 調整控除 difference 100,000 | none (H6 head is below the resident-tax line) | H6 at higher head pensions pays less tax |
| Higher-earning partner claims the spouse and children; a partner can be the dependant of an employee-insured spouse (Q23) | none | H3/H8 at low head pay: no NHI or national pension when the spouse is an employee; spouse deduction claimed by the earner (hand calc `claimant.md`: 26,600 → 7,200) |
| Resident-tax spouse/dependant income limit 480,000 → 580,000 (MIC p.28) | none | H4's 1.3m wall: <!-- history -->−281,926 → −280,126<!-- /history --> (superseded: now −258,226, section 6) |

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

The tax comparators are not tax actually collected. They are the 2024 全国家計構造調査's own estimate of income tax and resident tax, which the Statistics Bureau works out from the incomes people reported (table 第3-32-1, summed over the cells the model uses). They come from the same table the model is built on, so this is a consistency check, not an independent one. The survey's estimate takes off the one-off flat-rate tax cut of 2024 (定額減税: income tax 30,000 and resident tax 10,000 a person, dependants included, up to each person's tax; the income-tax cut was for people whose 2024 total income was ¥18.05m or less; National Tax Agency, 定額減税と確定申告, `sources/tax/nta_teigakugenzei_kakutei.html`) and adds tax on interest and dividends (Statistics Bureau, 年間非消費支出の推計方法, `sources/stats/zkk2024_hisyouhi2024.pdf` p.1, ④⑤). In a normal year the comparator would be higher, so the model's shortfall against a normal year is larger than shown, not smaller. The model also leaves out interest and dividends.

| Check | Model | Official | Gap | Why |
|---|---|---|---|---|
| Households | 53,536,652 (+254,087 in cells the survey hides) | 55,058,000 (国民生活基礎調査 2025) | −2.8% | different survey and year; the hidden cells are too small to model |
| People aged 65+ | 26,897,965 | 33,376,907 (全国家計構造調査 2024, the table the model is built from, Σ 65歳以上人員) | −19% | older people who work are modelled in work households at age 64 or under |
| Income tax | 9.13 trillion (2026 rules) | 11.64 trillion (the survey's own estimate of tax, 2024, after the 2024 flat tax cut) | −21.5% | 2025–26 tax cuts (larger basic deduction), averages taxed instead of individuals, too few high earners, rent, interest and dividends not modelled; the 2024 flat cut in the comparator works the other way. The parts have not been measured separately |
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
| Total (sum of the rows) | 62,057,850 | 51,630,593 | | +20% |

The NTA's own total is one more than the sum of its rows (51,630,594), because each cell is rounded separately. The official counts leave out public servants, so the model should be higher in total. At ¥1m or less the model (6.92 million) now lies between the full-year count (3.70 million) and the count including part-year workers (9.69 million). It has too many people earning ¥1m–3m (24.97 million against 14.49 million including part-year workers) and too few earning ¥10m or more. Averaging within a cell squeezes pay towards the middle. Too few high earners and 19% too few people aged 65+ matter for a plan that raises tax at the top.

**Earners other than the head (Q33, changed 2026-11-04).** Earlier versions gave the survey's "other members' earnings" to every adult child and relative in every household, which made <!-- history -->15.28 million<!-- /history --> earners at ¥1m or less (1.6 times the official count including part-year workers). Now the survey's number of earners per household decides how many spouses and other adults earn: the earners left after the heads of households living on work are spread evenly over the spouses in those households and over other adults, and those who earn get the cell's average divided by that share (`tests/hand_calcs/population.md` section 5). Effects:
- Earners: 66.15 → 62.06 million (the survey's own count, earners per household × households: 62.69 million).
- Income tax: <!-- history -->10.13 → 9.12 trillion<!-- /history --> (9.13 after the fixes in §14). Before, in cells with another adult, almost no room was left for working spouses, so the few spouses who worked took nearly all of the household's work income (in the cell of the hand calculation, a spouse salary of about 4.46 million and almost nothing for the head). Now more couples split their pay between two earners, and two moderate salaries pay less progressive tax than one large one: heads' income tax <!-- history -->9.21 → 8.72 trillion, spouses' 0.91 → 0.34<!-- /history -->. Other adults who work now earn more each and pay more (0.02 → 0.07), and fewer spouses and other adults count as dependants.
- Daiwa's refunds: <!-- history -->0.58 → 0.38 trillion<!-- /history --> (0.40 after §14), mostly because fewer other adults earn too little to use the credit.

The "before" figures are from the previous build, which also lacked the two deductions below; with only the earner split changed the moves are <!-- history -->0.59 → 0.38 (refunds), 0.93 → 1.09 (net) and −85,274 → −101,548 (top group), within 0.01 trillion<!-- /history --> of the figures above. The new split matches the survey's own earner counts much better, but against the NTA pay bands it is not better overall: ¥2m–3m earners went from −2% to +63% of the official count, and earners on ¥10m or more from −50% to −66%.

**Dependants aged 70 and over (Q32, 2026-11-04).** The model now gives the larger deduction for a dependant aged 70+ (income tax 480,000, or 580,000 for a parent living with the taxpayer; resident tax 380,000 or 450,000). Every relative aged 70+ in the model is treated as a parent of the head or spouse living with them (labelled approximation). People with both salary and pension income now get the income adjustment deduction (Q41). Together these lowered income tax by <!-- history -->less than 0.01 trillion<!-- /history --> at the time. No model member has income of both kinds above zero (the salaries and pensions of relatives aged 70 are small), so the salary-and-pension deduction changes no all-household number.

**Decile boundaries** (highest cell average in each model decile vs the survey's own decile upper limits, 第1-21表): 1.74m / 1.86m, 2.69m / 2.59m, 3.22m / 3.28m, 4.14m / 4.00m, 4.73m / 4.83m, 5.74m / 5.77m, 7.17m / 6.99m, 8.69m / 8.50m, 11.15m / 11.00m. All within 7%.

**Daiwa cost** (2026 rules): income tax +1.47 trillion, refunds 0.40 trillion, net: the government collects 1.07 trillion more (the result pages round these to 0.1 trillion: 1.5, 0.4 and 1.1). Daiwa's own estimate (2025 rules, credit 56,500; p.7): income tax +0.7 trillion, refunds 0.7 trillion, net about zero. Most of the gap has the same cause as in §9: under 2026 rules the basic deduction that the design removes is larger (1,040,000 at incomes up to 4.89 million), so removing it raises more tax. Daiwa built its estimate from MIC tax-assessment statistics, not household-survey averages.

**How uncertain the national totals are.** One change in how earners are split (above) moved the refunds by a third and the net by about 0.15 trillion (the published builds before and after it differ by 0.152; they also added the two deductions below, which moved it by less than 0.01 trillion). The known calibration gaps all push the same way: too many people earning ¥1m–3m make the cash paid out too large, and too few earning ¥10m or more (and too few people aged 65+) make the extra tax too small. So the net gain is more likely above the modelled 1.07 trillion than below. A rough check: scaling each earner's part of the result by the official count for their pay band (full-year plus part-year workers) gives a net of about 1.8 trillion; this overstates, because the same scaling also pushes the model's income tax above official totals, so it is an upper guide, not a central figure. Group averages are less certain still: the top group's average moved by 19% under the same change.

**Method changed during development.** The first version split each cell by the share of people aged 65+. Its first run counted <!-- history -->35.8 million<!-- /history --> earners at 1 million yen or less, because it gave pensioners small salaries. It was replaced by the pension/work split before anything was published. The test and hand calculation were rewritten with it (`tests/hand_calcs/population.md`, revision note), and an arithmetic slip in the first hand calculation is recorded there too.

## 11. Corrections after checking the published site

Checking the published site found errors that the checks above had missed. Each fix below was checked against a primary source saved in `sources/`. For the rounding, NHI-earner and wage-test fixes the hand calculation was corrected first and the test was watched failing before the rule was changed. For the 令和9年度 limits this was not true at first: no hand calculation or test depended on 620,000 or 890,000, so the tests still passed with the old limits. A second check found this (section 12), and the 890,000 limit now has a hand calculation and a test; the 620,000 limit has a hand calculation (`wall_H4.md`) and a test too, which fails if the limit goes back to 580,000 (Q40).

| Fix | Source | Effect |
|---|---|---|
| Resident tax: 特別区民税 (6%) and 都民税 (4%) each rounded down to 100 yen, not the 10% once (Q14) | 地方税法20条の4の2第3項・第8項; 大田区 worked example | H3, H5 and H8 take-home +100; several walls move by 100 yen |
| Resident tax for 令和9年度: spouse/dependant income limit 580,000 → 620,000; working-student limit 750,000 → 890,000; 特定親族特別控除 added; every amount now cited to the law, so the "fiscal 2025 guide" approximation is gone (Q13) | 地方税法292条1項7号・9号, 314条の2 (令和8年法律第2号); 所得税法2条1項32号 | H2's wall at 1.5m: <!-- history -->−97,172 →<!-- /history --> −75,572 (back at 1,590,000), plus a separate −18,458 wall at 1.63m; H3 at the head's pay and H4 at the spouse's pay of 1.33m–1.36m; population view |
| NHI reduction: an earner is someone with salary over 550,000, or pension over 600,000 (under 65) / 1,250,000 (65+); the 65+ 150,000 comes off pension income only (Q25) | 国民健康保険法施行令29条の7第6項第1号, 附則5条 | H6's walls 100,000 yen lower (1.78m → 1.68m, 2.4m → 2.3m); no change at reference incomes |
| Part-time wage test (88,000 a month) applied January–September only; from 2026-10-01 part-timers working 20+ hours at a 51+ firm are in employee insurance at any wage. **Withdrawn in section 12**: it missed the 特定減額特例 rule | 令和8年政令第275号; 日本年金機構 notice 2026-10-01 | H1 below 1,056,000 (e.g. 1,050,000: <!-- history -->814,839 → 834,858<!-- /history -->); population view |
| National pension ages 20–59 now read from parameters (Q30) | 国民年金法7条1項1号 | none |

Tests changed with these fixes, all after correcting the hand calculation: `expected.yaml` (H3, H5, H8 +100); `test_h1_baseline_walls_match_hand_calculation` (<!-- history -->+90,013 → +69,994<!-- /history -->); `test_keep_per_100000` (income 0 left out of the chart); `test_resident_tax_relief_band_matches_mic_figure` kept and marked as an expected failure (section 2); `test_incomplete_designs_say_why` (Rengo also needs household food spending, because its plan abolishes the reduced 8% rate on food: Rengo 税制改革構想 PDF p.33).

## 12. Corrections after a second check

A second check went over the fixes in section 11 against the law and the published site. What it found, and what changed:

| Fix | Source | Effect |
|---|---|---|
| The October split of section 11 is withdrawn. From October 2026, a part-timer on 20+ hours paid under 88,000 a month can only be a worker paid below the minimum wage with an exception (the lowest rate in force from October to December is 1,023 yen: 20 hours a week pays 88,660 a month), and such a worker (特定減額特例対象者) joins company insurance only if they ask. We assume they don't, so the 88,000 line decides for all 12 months again | 厚生年金保険法附則4条の6, 健康保険法附則8条の3の2; 厚生労働省 令和8年度地域別最低賃金 全国一覧 | H1 at 1,050,000: <!-- history -->834,858 →<!-- /history --> 809,595; the step to 1,060,000: <!-- history -->+69,994 →<!-- /history --> +95,257 (`wall_H1.md`, revision 2). Population view: nobody changes scheme in October, which also removes a fault where the Daiwa cash cap missed October joiners' premiums |
| Employment insurance is charged to every non-student wage earner on 20+ hours, in or out of company insurance (Q24 answered) | 雇用保険法6条 | H1 below 1,056,000: −5,244 a year (437 × 12 at 1,050,000); population view |
| Rengo's cost of 1.5–2 trillion yen was paired with "about 6 million people", which is Rengo's count for the taper band only; it is for about 21 million employees | 連合「税制改革構想」 pp.27–28 | text only |
| The ministry figure in section 2 is a match before rounding, not a conflict | MIC 資料３ p.18; 地方税法20条の4の2第3項 | text only; the expected-failure test now says why it fails |
| Official pay-band counts now read from the table's 計 rows (adding men and women was off by 1 in nine cells) | 民間給与実態統計調査 令和7年分 第3表 | section 10 table |
| Household NHI counts toward the head's Daiwa cash cap whenever the head works (before, not when the head was in company insurance) | Daiwa p.4 | none (the head's own premiums already exceed the credit) |

Tests changed, each after the hand calculation: `test_h1_baseline_walls_match_hand_calculation` (<!-- history -->+69,994 →<!-- /history --> +95,257, plus take-home 809,595 at 1,050,000). New: `test_h2_walls_match_hand_calculation` (`H2.md`, wall map points; it fails if the working-student limit goes back to 750,000) and `test_wall_map_section_matches_engine` (the "Engine" column of section 6).

## 13. Rules added before release

Rules that were listed as missing are now in the calculation, each from a hand calculation written first and tested.

| Rule | Source | Effect |
|---|---|---|
| Single-parent allowance (児童扶養手当): 48,050 a month for the first child and 11,350 for each further one, reduced above an income limit and stopped at a higher one; a public pension of the parent is taken off month by month | 児童扶養手当法, 施行令2条の2, 2条の4, 4条, 6条の5 | H5 receives 443,400 a year: take-home <!-- history -->2,208,436 →<!-- /history --> 2,651,836 (`tests/hand_calcs/H5.md`). A new wall where it stops (salary 3.85m) |
| Long-term-care premium for people 65 and over (Shinjuku, fiscal 2026) | 新宿区 table; 介護保険法施行令38条 | H6 pays 51,480 + 19,800: take-home <!-- history -->2,683,201 →<!-- /history --> 2,611,921 (`tests/hand_calcs/H6.md`). A new wall where the head starts to pay resident tax (pension 2.12m) |
| Resident-tax spouse deduction for earners with total income above 9m (220,000 / 110,000) | 地方税法314条の2第1項第10号・第10号の2, 314条の6 | none of H1–H8 at their reference incomes, and no wall-map point or calculator setting. For such earners resident tax is 11,000 / 22,000 higher than before when the spouse's income is 620,000 or less (12,000 / 25,000 for a spouse aged 70+), and 1,000–22,000 lower when it is 620,001–1,330,000 (`tests/hand_calcs/spouse_rt.md`) |
| Student pension deferral only while the student's income after insurance is at most 1,280,000 | 国民年金法90条の3; 施行令6条の9, 6条の12 | H2's wall map: national pension 215,040 from a salary of about 2.2m (step −174,798, `tests/hand_calcs/H2.md`) |
| Dependants aged 70+: income tax 480,000 (580,000 for a parent or grandparent living with the taxpayer), resident tax 380,000 (450,000), 調整控除 differences 100,000 (130,000) | NTA 年末調整のしかた pp.12, 56; 地方税法314条の2第1項第11号・第4項, 314条の6第1号イ表(8)(iii)・(9) | none of H1–H8; in the all-household estimate, relatives aged 70+ (treated as parents living with the household, labelled approximation) (`tests/hand_calcs/elderly_dependant.md`) |
| Income adjustment deduction for people with both salary and pension income: min(salary income, 100,000) + min(pension income, 100,000) − 100,000 | NTA No.1411 (措法41条の3の11第2項); 大田区 計算のしくみ 注釈2(2) for resident tax | none of H1–H8, and no member of the all-household estimate has income of both kinds above zero (`tests/hand_calcs/salary_and_pension.md`). The 65+ care premium adds it back (介護保険法施行令22条の2第4項第1号) |

The all-household numbers moved a little with these rules (for example the Daiwa plan's net effect on government revenue, <!-- history -->0.95 → 0.93 trillion; it later became 1.09 trillion<!-- /history --> with the change in §10, and 1.07 with §14). Not modelled, by decision: the National Pension exemption for low incomes, which has to be applied for and lowers the future pension; nobody is assumed to apply (Q20).

The wall list also names the rule that starts or stops at a wall where one does: the student deferral's income limit (H2 at 2.19m), resident tax starting (H5 at 2.09m; at H6's 2.11m it also moves the 65+ care premium bands), and the single-parent allowance stopping (H5 at 3.85m). Tested in `tests/test_site.py`.

Tests changed with these rules, each after the hand calculation: `expected.yaml` H5 <!-- history -->2,208,436 →<!-- /history --> 2,651,836 and H6 <!-- history -->2,683,201 →<!-- /history --> 2,611,921; the H6 NHI-earner test now runs without the 65+ premium (its band is set from a first pass without it, so take-home 2,414,941 is checked there); the H4 wall-cause test lists the two new parts (65+ premium, single-parent allowance).

## 14. Fixes before public release

A check of the published site before its announcement found the following; each was checked against the cited source.

| Fix | Source | Effect |
|---|---|---|
| The first income adjustment deduction (salary over 8.5m) needs a 扶養親族 under 23, so a child whose own income is above 620,000 doesn't count | 措法41条の3の11第1項; NTA No.1411 | none of H1–H8; modelled income tax 9.12 → 9.13 trillion, gap −21.6% → −21.5% (`tests/hand_calcs/salary_and_pension.md`) |
| No resident-tax 調整控除 above total income of 25m | 地方税法314条の6, 37条 | none of H1–H8; a few all-household members pay 2,500 more (`tests/hand_calcs/adjustment_credit_25m.md`) |
| Single-parent allowance: a dependant aged 70+ raises the limits by 480,000, not 380,000 | 児童扶養手当法施行令2条の4第1項第2号ロ | none of H1–H8 or the all-household estimate (`tests/hand_calcs/H5.md`, last section) |
| Daiwa plan: the 65+ care premium counts toward the cash limit for people who work, as Daiwa's note lists it | Daiwa p.4 図表3 (注1); daiwa.yaml `contributions_counted` | none of H1–H8; refunds 0.38 → 0.40 trillion, net 1.09 → 1.07 (`tests/hand_calcs/daiwa_care_premium.md`) |
| The Compare calculators read a precomputed ¥10,000 grid. An amount between two grid points with a wall (or a jump up) between them now shows both points instead of the nearest one, which could be on the other side of the wall | – | e.g. H4's spouse at ¥1,295,000: shown at ¥1,290,000 and ¥1,300,000 with a warning, not at ¥1,300,000 alone (`tests/test_site.py`) |
| §10: the survey's tax estimate already takes off the 2024 flat tax cut, so the shortfall against a normal year is larger, not smaller | Statistics Bureau, 年間非消費支出の推計方法 | text only |
| §13: the 9m–10m spouse rule raises resident tax for a spouse with income up to 620,000; §11: the 620,000 limit has a test | 地方税法314条の2第1項第10号 | text only |

New tests, each after its hand calculation: `test_first_adjustment_needs_a_dependant_under_23`, `test_no_adjustment_credit_above_25m`, `test_allowance_limit_for_a_dependant_aged_70_plus`, `test_daiwa_cash_limit_counts_the_65_plus_care_premium`, `test_typed_amounts_and_walls_between_grid_points`. Two existing tests changed: the list of numbers kept in the parameter files but not read (the 25m limit is read now), and the expected wording of H6's wall reason, which now says the 79,200 is the 65+ premiums of two people together (head band 3 → 6, spouse band 1 → 4, `tests/hand_calcs/H6.md`).

Also fixed, in text only: the plan descriptions now quote the bill's review clauses with their conditions (第36条第4項・第5項) and its financing rules (第21条, 第39条), describe the top-up's target as the outline does (pages 9–10: joining company insurance or moving into National Health Insurance and National Pension), and use the same rule for every plan in the one-line summaries; the report, press summary and All households page say which way the known calibration gaps push the national totals; the press charts carry the plan's full name and a line on what they leave out; the 65+ care-premium note names the national fiscal-2026 rule (介護保険法施行令附則24条・25条); and `make fetch-sources` now stops at a failed download instead of failing later at the fingerprint check.

**Pages that publishers replace.** The build downloads 25 pages that can't be stored in git (sources/EXTERNAL.tsv). Publishers replace some of them each year, which would make a fresh build fail its fingerprint check. Copies saved at the Internet Archive are now listed next to the publisher's address; `scripts/fetch_sources.py` uses the copy only when the publisher's file no longer matches, and stops with a message if neither does (`tests/test_fetch_sources.py`). 18 of the 25 pages have a checked copy. Three 協会けんぽ web pages (HTML; its PDFs are checked) differ on every download because of a code embedded in the page, so no copy can be checked against a fingerprint; they are used as downloaded, without a fingerprint check (`sources/SHA256SUMS.volatile`). The other 4, on the Shinjuku, Ota and Chuo city websites, have no copy listed yet, because so far no copy matching the saved fingerprint has been downloaded from the Internet Archive. If one of them is replaced, the build stops and names it (`tests/test_fetch_sources.py`). The new page is then compared by hand with the figures cited from it: if they are all still there, its fingerprint is updated; if not, a fresh build can't get that source, and this is recorded in OPEN_QUESTIONS.md.

## 15. Checks added

These checks were added before any of the fixes they lead to, so each fix below them can be traced to the check that found it.

| Check | What it catches |
|---|---|
| `tests/test_number_provenance.py` | a number in public text (site pages, report, press summary, these documents, household and plan files) that is not in outputs/ or parameters/ and is not listed with its source in `tests/number_sources.yaml` |
| `tests/test_languages_match.py` | a number carried by the Japanese version of a text but not the English one, or the other way round |
| `tests/test_calculator_grid.py`, `site/grid.js` | a calculator that shows the nearer grid point for an amount between two points, when a wall can lie between them |
| `tests/test_plan_quotes.py` | a sentence describing a plan that no exact quote from the plan's own document backs |
| `make pinned` (`scripts/check_parameters_pinned.py`) | a parameter whose value can change without any rule test failing (exceptions listed with their reason in `tests/unpinned_ok.yaml`) |
| `scripts/check_changes_logged.py` | a change to outputs/, report/ or press/ with no record of why in this file or `docs/CORRECTIONS.yaml` |

`test_household_matches_hand_calculation` in `tests/test_baseline.py` now requires each household to match its hand calculation to the yen. It used to allow a tolerance wide enough for a small change to a deduction to pass unnoticed. All eight households already matched exactly (section 1), so no number changed.

### Fix 1: calculators show both grid points

Both Compare calculators read a precomputed grid in ¥10,000 steps. Before, an amount between two grid points was shown at the nearer point ("rounded to ¥10,000") unless a wall was found between them. Now any amount between two grid points shows the result at both points and says the exact amount isn't calculated; when take-home pay falls, or rises by more than the step, between them, the page also says it depends on which side of that line the amount falls. Above the top of the grid the result is still shown at ¥10m and says so. `site/grid.js` holds the input reading (`readYen`), the choice of grid points (`gridPoints`) and the jump test (`jumpBetween`); the earlier `gridPoint` and `readYen` in `site/walls.js` are removed. `test_typed_amounts_and_walls_between_grid_points` in `tests/test_site.py` now calls the same checks through `site/grid.js` with the same households and amounts; `tests/test_calculator_grid.py` passes. No published number changed.

### Fix 2: every number in public text is traced

`tests/test_number_provenance.py` listed the numbers in public text that are not in outputs/ or parameters/. Each one is now handled one of three ways:

- **Old values kept on purpose** (for example the H4 wall before two corrections, earlier versions of the all-household model, and the first Daiwa reading in section 5) are marked as history in this file and in OPEN_QUESTIONS.md. They stay visible; the check skips them.
- **Figures from a source or a hand calculation** (official worked examples, the plans' own estimates, steps in `tests/hand_calcs/`) are listed in `tests/number_sources.yaml`, each with its source and, where the engine gives the same number, the test that pins it.
- **Figures the engine produces but that were typed by hand** are worked out again by `tests/test_listed_numbers.py`: H2's salary where the student deferral ends, the largest OpenFisca-Japan resident-tax gap, and the earner counts in section 10.

Two figures needed more than a source:

- The rough check in section 10 (each earner's part of the Daiwa result scaled to the official count for their pay band) was not produced by the build. The build now writes it to `outputs/population.json` (`calibration.daiwa_net_scaled_to_official_earners`), and it gives the same "about 1.8 trillion". To do this, `engine/reforms.py` now works out the Daiwa result member by member (`daiwa_members`) and adds it up; every household and all-household total is unchanged.
- <!-- history -->Section 10 said one change in the earner split moved the net "by about 0.15 trillion". The two figures it refers to (0.93 and 1.09 trillion, kept above as history) differ by 0.16 trillion, so the text now says 0.16.<!-- /history --> (Reversed later: see "Fixes from a third check" below.)

The provenance check itself was corrected: it read written numbers without their sign but compared them with signed values in outputs/, so a figure written as −16,100 was reported as untraced although outputs/ holds −16100. It now compares sizes, as it already did for amounts in 万, 億 and trillions.

Every direction word in the Checks page's comparison with official figures (household count below, income tax and resident tax lower, too many earners on ¥1m–3m, too few on ¥10m or more, too few people aged 65+) matches the sign worked out from `outputs/population.json`, in both languages; `test_checks_page_directions_match_the_signs` in `tests/test_validation_doc.py` keeps it so.

### Fix 3: Japanese and English carry the same numbers

`tests/test_languages_match.py` found two household notes where the languages differed. H1: the English said "paid less" where the Japanese gives the amount (月給8.8万円未満); it now says "paid less than ¥88,000 a month", and so do the same sentence on the Home page and in the all-household assumptions. H2: the Japanese wrote the salary as 219万6,000円, which reads as two numbers; it now writes 2,196,000円, as the English does. Text only; no number changed.

### Fix 4: every plan sentence backed by the plan's own words

`tests/test_plan_quotes.py` found plan descriptions (the one-line and paragraph texts in `parameters/designs/*.yaml`, shown on Home, Compare, All households and in the report) that no quote backed. Each plan file now has a `quotes:` list: every sentence, in both languages, with the exact words from the plan's own document and the PDF page. Where no quote said what a sentence said, the sentence was rewritten to say what the quote says. Two sentences that only say why this site can't calculate the Rengo plan yet are kept as the site's own words, with that reason. Three documents were added as sources for the government plans: the bill's 要綱 (siryou2, 2026-10-09), the 社会保障国民会議 index page that records the Cabinet decision and submission on 2026-10-09, and the points from the Prime Minister's press conference of 30 July 2026 (siryou3, 2026-08-05).

What changed in substance (text only; no number changed):

- **Government plans.** Children: the extra is for supported relatives under 19 living in Japan (under 16 in fiscal 2027–28), as the outline defines 扶養児童. The conditions name the pension income that is subtracted from tax and insurance paid. The spouse test applies to a spouse on 1 January of the year the fiscal year starts. Earned income includes miscellaneous income from work as well as business income. The income-wall top-up is described as the outline does: for people facing the wall and people with a similar insurance burden, time-limited "until the wall is removed" in the outline's own words, and only for people who paid premiums equal to company insurance. Older people who don't work are named as not covered in the government's own words (press conference points). The bill's review clause says 疾病等 (illness and similar reasons). Statements that no saved document backs were removed: that the bill was still being debated on a given date, that no nationality condition is written, that no total cost has been published, and that amounts "haven't been decided" (now: the bill leaves them to be set by Cabinet order).
- **Daiwa.** The credit is for every taxpayer; the cash cap counts social insurance on income from work (wages and business income are examples, not the full list); National Health Insurance, National Pension, the 65+ care premium and late-stage elderly medical premiums count only for people with income from work; people who live *mainly* on a pension, asset income or savings get no cash; the eight versions differ by the special top-up above the old basic deduction, not a "recent" one.
- **Rengo.** Named as the Japanese Trade Union Confederation; amounts are "refunded", not "paid in cash"; the consumption-tax refund is *mainly* for people below the income-tax threshold; the work-support credit is for employees who pay social and employment insurance (the earlier text said the self-employed were excluded, which neither document says); the reduced rate is described with Rengo's own definition.

The same facts were brought in line in `docs/METHODS.md`, `docs/METHODS.ja.md`, the report template and the press summary template (the Daiwa "living on a pension" sentence, and "not decided" for amounts the bill leaves to Cabinet order).

### Fix 5: every parameter pinned by a test

`make pinned` changes each parameter a little and runs the rule tests; a parameter whose change no test noticed was not checked by any hand calculation. Most were limits and ages that no example household reaches (for example the single-parent deduction and its income limit, the working-student deduction, the dependant age bands, the elderly-spouse amounts, the employment-income table's first row, and the National Health Insurance reduction lines). Each now has a small case in `tests/hand_calcs/parameter_edges.md`, worked out by hand at the limit or the age itself, and a test in `tests/test_parameter_edges.py`. The rest are listed in `tests/unpinned_ok.yaml` with the reason: four numbers the engine doesn't read (the same four as in `tests/test_parameters_used.py`), one the engine reads but that can never decide its test (the working-student deduction inside the student pension deferral test), Daiwa's zero basic deduction (the check's one-yen change is lost in the credit's rounding), and the parameters of the three plans that can't be calculated yet. No rule changed and no number changed.

### Fixes from the check before publishing

- **Single-parent allowance cases in `tests/hand_calcs/parameter_edges.md`.** Cases 27 and 28 counted no supported child, but a child under 16 whom the parent supports raises each income limit by 380,000 (児童扶養手当法施行令2条の4; a child aged 16 to 18 who is a dependant for income tax adds 530,000), and the engine counts it. Both cases now include it (stop limit 2,940,000 and full limit 1,550,000 in case 27; full limit 1,450,000 in case 28) and their tests were changed after the hand calculation. They pin the same parameters, and now also the 380,000 per child.
- **Case 23** now treats the pensioner as an earner, as the reduction test does for a pension over the 65+ line; with one member this gives the same 49,406.
- **The government plan's review clause** (第36条第4項): "who are left out of this payment" now covers both low earners and people who find it hard to work because of illness, as in the bill outline (p.6), in both languages.
- **Section 10** <!-- history -->says "about 0.16 trillion"<!-- /history -->, since both figures it comes from are rounded, and marks those two old figures as history (reversed later: see below).
- **The 2027–28 government plan's label and names** no longer call it a "bridge" (つなぎ) in the site's own voice; that is the government's word, and the plan description says so. Its label is now 政府案（2027〜28年度：食料品の消費税1%＋給付）/ Government plan (FY2027–28: 1% tax on food + payment), here and in METHODS. Text only; no number changed.

### Fixes from a second check of everything since the release check

- **Compare, "Try your own household's shape":** the count of plans not shown included "2026 rules", so it said one more plan than there is. It now counts the plans only, as Home does. The note on the earner below the company-insurance line now says the spouse pays National Pension whenever the spouse isn't in company insurance, which includes a spouse who works part-time.
- **Report and press summary:** the Daiwa figures for the example households (the change at the H4 wall and the table of changes) now carry the （近似）/(Approximation) label, as on Home and Compare.
- **Direction of the national total:** the known calibration gaps make the Daiwa plan's net gain more likely above the model's own figure (1.07 trillion), not above the rounded 1.1 shown on the pages. The Checks page, All households page, report and press summary now say "above this estimate's figure", and section 10 says "above the modelled 1.07 trillion".
- **Numbers that passed the provenance check by coincidence:** the 2024 flat tax cut amounts in section 10 now cite the National Tax Agency's page, and the Q37 household count is recomputed by `tests/test_listed_numbers.py`.
- **Corrections record (`docs/CORRECTIONS.yaml`), entry of 2026-11-06:** it listed only two income groups; it now lists every group whose average changed, each checked against the two published versions by `tests/test_corrections.py`, and says the shares of households better off and unchanged moved too. Two entries were added: one for the plan descriptions and the section 10 figure published on 2026-11-09, and one for these fixes.
- **Press charts:** the Daiwa line in the H4 wall chart and the title of the example-household chart carry （近似）, as the all-household chart already did.

One published number changed: the Compare page's count of plans not shown, from 4 to 3.

### Fixes from a third check

- **Section 10 is back to "about 0.15 trillion".** The two published builds before and after the change in how earners are split give a net gain of 0.936 and 1.088 trillion: 0.152 apart (they also added two deductions, which moved the net by less than 0.01 trillion). The "0.16" came from rounding two figures to 0.01 before subtracting them; one of them, 0.93, is from a build that was not kept. `tests/test_listed_numbers.py` now recomputes the figure from the two published builds.
- **The 2024 flat tax cut:** the ¥18.05m limit is now stated for the income-tax cut only, as the National Tax Agency's page gives it, and the figure is listed with that page in `tests/number_sources.yaml`.
- **Corrections record:** the 2026-11-06 entry now says it lists each group whose average changed; the 2026-11-09 entry no longer lists the calculator change, which was a change of design (the earlier calculator marked the nearer point as rounded and showed both points when take-home pay jumped between them), and the 2026-11-10 entry records the return to 0.15.
