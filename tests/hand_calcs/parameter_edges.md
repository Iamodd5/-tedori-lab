# Parameter edges: one small case per rule value that no household reached

Each case below is chosen so the value matters: a test at an age limit uses the age itself, a test at an
income limit uses an income just past it, and an amount is read off as a difference between two cases that
differ only in the condition. Amounts and limits are those in `parameters/baseline_2026/` (each cites the law
or table). Tests: `tests/test_parameter_edges.py`.

Deductions: "income-tax deductions" and "resident-tax deductions / 調整控除 difference" are the totals the head
claims (basic + social insurance + personal deductions). Two cases that differ in one condition have the same
basic deduction and insurance, so their difference is the personal deduction alone.

## Income tax

1. **Employment income table starts at 2,191,000** (年末調整のしかた 別表第五). Salary 2,250,000 is in the table:
   2,250,000 ÷ 4 = 562,500, rounded down to the thousand: 562,000; 562,000 × 2.8 − 80,000 = **1,493,600**.
   (The minimum-deduction rule would give 2,250,000 − 740,000 = 1,510,000.)
2. **Income adjustment cap 10,000,000** (No.1411): salary 11,000,000 with a dependant under 23:
   (10,000,000 − 8,500,000) × 10% = **150,000**.
3. **Income adjustment needs a dependant under 23**: head on 9,000,000 with a child aged 22 (no income):
   (9,000,000 − 8,500,000) × 10% = **50,000**; with the child aged 23: **0**.
4. **Public pension income table from age 65** (No.1600): pension 2,000,000 at 65 is in the row from 1,100,001:
   2,000,000 × 100% − 1,100,000 = **900,000**.
5. **Elderly spouse from 70** (earner income ≤ 9m): spouse aged 70 with no income **480,000**; aged 69 **380,000**.
6. **Dependant from age 16**: head on 5,000,000, child aged 16 vs 15: income tax **+380,000**; resident tax
   **+330,000**, 調整控除 difference **+50,000**.
7. **Specific dependant from 19**: child aged 19 vs 18: income tax 630,000 − 380,000 = **+250,000**; resident tax
   450,000 − 330,000 = **+120,000**; difference 180,000 − 50,000 = **+130,000**.
8. **Specific dependant under 23**: child aged 22 vs 23: the same **+250,000 / +120,000 / +130,000**.
9. **Specific dependant amounts**: child aged 19 vs no child: income tax **+630,000**, resident tax **+450,000**,
   difference **+180,000**.
10. **Elderly dependant from 70** (not living with them as a parent): aged 70 vs 69: income tax 480,000 − 380,000 =
    **+100,000**; resident tax 380,000 − 330,000 = **+50,000**; difference 100,000 − 50,000 = **+50,000**.
11. **Dependant income limit 620,000**: a child aged 16 with business income 620,000 is still a dependant: income tax
    **+380,000** against no child. With 630,000 they are not: **+0** (at 16 there is no 特定親族 deduction either).
12. **Single-parent deduction 350,000, income limit 5,000,000**: a single parent with business income 5,000,000:
    single parent vs not, income tax **+350,000**; with 5,000,001: **+0**.
13. **Working-student deduction 270,000, income limit 890,000**: a student, salary 1,540,000 (not 20 hours, so no
    insurance through work), total income 1,540,000 − 740,000 = 800,000: student vs not, income tax **+270,000**,
    resident tax **+260,000**, difference **+10,000**. Salary 1,631,000 (total income 891,000): **+0** for each.

## Resident tax (Shinjuku: ward 6%, Tokyo 4%; 調整控除 3% and 2%; per-capita 3,000 + 1,000 + 1,000 = 5,000)

14. **Elderly spouse 380,000, its difference 100,000, from age 70** (earner ≤ 9m): spouse aged 70 → **(380,000, 100,000)**;
    aged 69 → **(330,000, 50,000)**.
15. **Single person's line 450,000**: total income 460,000, deductions 430,000, difference 50,000.
    Taxable 30,000; 調整控除 base min(50,000, 30,000) = 30,000; ward 30,000 × 6% − 30,000 × 3% = 900;
    Tokyo 30,000 × 4% − 30,000 × 2% = 600; total **900 + 600 + 5,000 = 6,500**.
16. **Single parent with total income up to 1,350,000 pays none**: at 1,350,000 → **0**. At 1,400,000 (one dependant,
    deductions 430,000 + 300,000 = 730,000, difference 50,000 + 50,000 = 100,000): per-capita line
    350,000 × 2 + 310,000 = 1,010,000 and income-levy line 350,000 × 2 + 420,000 = 1,120,000 are both passed;
    taxable 670,000; base 100,000; ward 40,200 − 3,000 = 37,200; Tokyo 26,800 − 2,000 = 24,800; the burden-relief
    band does not apply (62,000 < 1,400,000 − 1,120,000); total **37,200 + 24,800 + 5,000 = 67,000**.
17. **No 調整控除 above 25,000,000**: total income 25,500,000, no deductions, difference 50,000: taxable 25,500,000;
    ward 1,530,000, Tokyo 1,020,000; total **2,555,000** (with the 調整控除 it would be 2,552,500).

## Social insurance

18. **Employee LTC premium to age 64, pension to 69**: at 65 the health premium is the one without LTC (the same
    as at 39); at 70 the pension premium is **0**, at 69 the same as at 30.
19. **Dependant limit 1,800,000 from age 60**: an employee's spouse aged 60 on salary 1,750,000 (part-time, not
    insured through work) is a dependant; on 1,850,000 they are in National Health Insurance.
20. **National Pension to age 59**: a self-employed head aged 60 pays **0**; aged 59 pays 17,920 × 12 = **215,040**.
21. **Earners in the NHI reduction test** (国保令29条の7第6項第1号, 附則5条): salary 560,000 (over 550,000) → earner;
    pension 610,000 at 64 (over 600,000) → earner; pension 1,260,000 at 65 (over 1,250,000) → earner.
22. **100,000 more per extra earner in the reduction line**: two NHI members aged 30, both earners, total incomes
    532,000 and 0. Line 430,000 + 100,000 = 530,000 < 532,000, so not the 70% cut; 532,000 ≤ 530,000 + 310,000 × 2,
    so the 50% cut. Base 102,000. Medical 47,600 × 2 × 50% + 102,000 × 7.51% = 47,600 + 7,660.2; support
    17,600 + 102,000 × 2.8% = 17,600 + 2,856; child levy 1,873 + 102,000 × 0.27% = 1,873 + 275.4.
    Total 77,864.6 → **77,864**.
23. **150,000 off a 65+ pensioner's income in the reduction test**: one member aged 65, pension income 580,001 (pension
    received 1,680,001, over the 1,250,000 line of case 21, so an earner; with one member the line has no extra earner). Test income 580,001 − 150,000 = 430,001 > 430,000, so not the 70% cut; ≤ 430,000 + 310,000, so the
    50% cut. Base 150,001. Medical 23,800 + 11,265.0751; support 8,800 + 4,200.028; child levy 936.5 + 405.0027.
    Total 49,406.6058 → **49,406**.
24. **65+ long-term-care premium from 65**: a person aged 65 pays the same premium as one aged 66 with the same
    pension (the band depends on income, not age), and more than 0.

## Allowances

25. **Child allowance to 18**: one child aged 18 → 10,000 × 12 = **120,000**; aged 19 → **0**.
26. **Single-parent allowance for children to 18**: a single parent with one child aged 19 gets **0**; with the child
    aged 18, more than 0.
27. **Limit +480,000 for a dependant aged 70+**: one child (a supported child, +380,000 to each limit) and one
    elderly dependant: stop limit 2,080,000 + 380,000 + 480,000 = 2,940,000, so income 2,940,000 gets **0**. Income
    2,930,000: full limit 690,000 + 380,000 + 480,000 = 1,550,000; withheld (2,930,000 − 1,550,000) × 0.0264029 =
    36,436.0 → 36,440 + 10 = 36,450; 48,050 − 36,450 = 11,600 a month, **139,200** a year.
28. **Further-child rate 0.0040719**: two children (supported children, +380,000 each), so the full limit is
    690,000 + 760,000 = 1,450,000 and the stop limit 2,840,000. Income 2,450,000 (1,000,000 above the full limit): first child
    withheld 26,402.9 → 26,400 + 10 = 26,410; further child 4,071.9 → 4,070 + 10 = 4,080;
    (48,050 − 26,410) + (11,350 − 4,080) = 28,910 a month, **346,920** a year.
