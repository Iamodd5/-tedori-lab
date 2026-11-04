# Hand calculation: building model households from one survey cell, and splitting into deciles

Method: `population/population.yaml` (assumptions `income_split`, `older_age`, `work`). Data: `population/cells.csv`,
row `single,04`, which comes from 令和6年全国家計構造調査 所得 第3-32-1表, column 2_単身世帯, band 04_200～250万円.

## 1. The cell (single people with annual income 2.0–2.5 million yen)

| Item | Survey value |
|---|---|
| Households | 2,440,457 |
| Average age of the household head | 63.7 |
| Earnings of the head (勤め先収入) | 811,000 |
| Business income (農林漁業 + 農林漁業以外の事業 + 内職) | 90,000 |
| Pensions of the head (公的年金・恩給 + 企業年金・個人年金) | 1,208,000 |

## 2. Split into a pension household and a work household

Modelled income per household: work income E = 811,000 + 90,000 = 901,000; pensions P = 1,208,000; total T = 2,109,000.
Each part of the cell keeps the cell's total income T, so it stays in its income band.

Share of households that live on pensions: π = P / T = 1,208,000 / 2,109,000 = **0.572783**.

Pension household (weight 2,440,457 × 0.572783 = **1,397,853.04**), age 70:
- pension = T = **2,109,000**; no salary, no business income

Work household (weight 2,440,457 × 0.427217 = **1,042,603.96**):
- work income = T = 2,109,000, split 811 : 90 → salary 2,109,000 × 811/901 = **1,898,334**, business 2,109,000 × 90/901 = **210,666**
- age = (63.7 − 0.572783 × 70) / 0.427217 = 23.605168 / 0.427217 = 55.25 → **55**

Check that the cell's averages are kept: salary 0.427217 × 1,898,334.07 = 811,000.0; pension 0.572783 × 2,109,000 = 1,208,000.0.

## 3. Splitting households into deciles

Three model households, already sorted by annual income: weights 6, 4 and 10 (total 20, so each decile holds 2).

| Household | Covers cumulative weight | Deciles (weight in each) |
|---|---|---|
| 1 | 0–6 | 1 (2), 2 (2), 3 (2) |
| 2 | 6–10 | 4 (2), 5 (2) |
| 3 | 10–20 | 6, 7, 8, 9, 10 (2 each) |

A household that straddles a decile boundary is split between the two deciles in proportion.

## 4. A couple cell: how many spouses earn

Row `couple_2children,10` (夫婦と未婚の子供が２人の世帯, band 500–550万円): 247,009 households, 1.54 children under 18,
1.88 earners per household, head aged 45.6 on average; head earnings 3,101,000, spouse earnings 668,000,
business 724,000, pensions head 194,000 + spouse 56,000. Two children under 18 (1.54 rounds to 2), so nobody else
can take the other members' earnings (202,000, left out and counted in the check of income not modelled).

- Work income 4,493,000 + pensions 250,000 = T = 4,743,000; π = 250,000 / 4,743,000 = 0.052709
- Earners per work household = 1.88 / (1 − 0.052709) = 1.984607, so the share of work households where the spouse
  also earns is q = 1.984607 − 1 = **0.984607** (it must also be at least spouse earnings / work income = 0.1487; it is)

| Household | Weight | Head | Spouse |
|---|---|---|---|
| Pension | 247,009 × 0.052709 = **13,019.66** | age 70, pension 4,743,000 × 194/250 = **3,680,568** | age 70, pension 4,743,000 × 56/250 = **1,062,432** |
| Work, one earner | 247,009 × 0.947291 × 0.015393 = **3,601.76** | age 44, salary 4,743,000 × 3,101/3,825 = **3,845,240**, business **897,760** | age 44, no earnings |
| Work, two earners | 247,009 × 0.947291 × 0.984607 = **230,387.58** | age 44, salary (4,743,000 − 716,193) × 3,101/3,825 = **3,264,609**, business **762,198** | age 44, salary 668,000 / (0.947291 × 0.984607) = **716,193** |

Age: (45.6 − 0.052709 × 70) / 0.947291 = 44.24 → 44. Check: spouse earnings 0.947291 × 0.984607 × 716,193.17 = 668,000;
head earnings 0.947291 × (0.015393 × 3,845,240 + 0.984607 × 3,264,608.6) = 3,101,000.

## Correction note (2026-11-01)

The first version of section 2 gave the younger household's salary as 1,898,331 and business income as 210,669.
That was an arithmetic slip: 2,109,000 / 901 = 2,340.7325, and × 811 = 1,898,334.1, × 90 = 210,665.9.
The test was written from the wrong numbers and failed against the code. The code was right. The hand calculation
and the test now use 1,898,334 and 210,666. Nothing else in this file changed.

## Revision (2026-11-01): method changed before first use

The first version split each cell by the share of people aged 65+ (0.59 here): an older household got pensions first,
plus whatever work income was left (salary 55,395), and a younger household got the rest. Run on the whole population,
that gave almost every pensioner a small salary: the model counted 35.8 million people earning up to 1 million yen,
against 3.7 million in the tax agency's count (民間給与実態統計調査). Small salaries also made pensioners look like
workers to Daiwa's refund rule. So the split now follows the income itself (π = pensions / total). The test was
rewritten with this section; nothing had been published from the first version. The arithmetic slip described in
the note above belonged to the first version (it is kept because the same salary split, 1,898,334, is still used).

## 5. A cell with another adult: who else earns (OPEN_QUESTIONS Q33)

Row `couple_1child,10` (夫婦と未婚の子供が１人の世帯, band 500–550万円): 374,101 households, 3.0 people, 0.42 children under 18
(rounds to 0, so the one child is an adult, aged 22), 1.63 earners per household, head aged 57.3 on average; head earnings
2,203,000, spouse earnings 558,000, other members' earnings 477,000, business 556,000, pensions head 804,000 + spouse 338,000.

Before this section the model gave the other members' earnings to every adult child in every household (477,000 each),
which made many small salaries (VALIDATION §10). Now the earners beyond the working heads are spread evenly over the
spouses and the other adults, as the spouses alone were before (assumption `spouse_earnings`):

- Work income 3,317,000 + pensions 1,142,000 = T = 4,459,000; π = 1,142,000 / 4,459,000 = 0.256111; 1 − π = 0.743889
- Places for extra earners: spouses in work households 0.743889 + one other adult = 1.743889
- Extra earners: 1.63 − 0.743889 (the working heads) = 0.886111
- Share that earns: 0.886111 / 1.743889 = **0.508124**, for spouses (q; at least 558,000 / 3,317,000 = 0.168224, and it is)
  and for the other adult (r)

| Household | Weight | Head | Spouse | Adult child |
|---|---|---|---|---|
| Pension, child earns | 374,101 × 0.256111 × 0.508124 = **48,684.08** | age 70, pension 4,459,000 × 804/1,142 = **3,139,261** | age 70, pension **1,319,739** | salary 477,000 / 0.508124 = **938,748** |
| Pension | 374,101 × 0.256111 × 0.491876 = **47,127.39** | as above | as above | none |
| Work, one earner, child earns | 374,101 × 0.743889 × 0.491876 × 0.508124 = **69,554.02** | age 53, salary 4,459,000 × 2,203/2,759 = **3,560,412**, business **898,588** | no earnings | **938,748** |
| Work, one earner | × 0.491876 × 0.491876 = **67,330.00** | as above | none | none |
| Work, two earners, child earns | × 0.508124 × 0.508124 = **71,851.49** | salary (4,459,000 − 1,476,239) × 2,203/2,759 = **2,381,668**, business **601,093** | salary 558,000 / (0.743889 × 0.508124) = **1,476,239** | **938,748** |
| Work, two earners | × 0.508124 × 0.491876 = **69,554.02** | as above | as above | none |

Head age in work households: (57.3 − 0.256111 × 70) / 0.743889 = 52.93 → **53**.
Check: the child's salary averages 0.508124 × 938,748 = 477,000 over the cell; the spouse's 0.743889 × 0.508124 × 1,476,239 = 558,000.
The old split gave q = 0.168224 (the floor), so the few spouses who earned got about 4.46 million each.
