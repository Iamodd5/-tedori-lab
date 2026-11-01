# Methods (draft, Milestone 2)

## The 2026 baseline

- **Year.** All taxes and contributions are computed on income earned in calendar 2026. Income tax uses 令和8年分 rules (applied at the December 2026 year-end adjustment). Resident tax is the 令和9年度 tax that falls on 2026 income.
- **Place.** Shinjuku ward, Tokyo: 協会けんぽ Tokyo rates for employees, Shinjuku rules for National Health Insurance and resident tax (HUMAN_TODO H-8).
- **Approximations** (each labelled `approximation: true` in the parameter files):
  - Rates that start in March or April 2026 (health, child-support levy, employment insurance, national pension) are applied to all 12 months.
  - NHI uses FY2026 rates on 2026 income, because FY2027 rates are not published.
  - Resident-tax personal deductions use the 令和7年度 Shinjuku table (Q13). Rounding rule source pending (Q14).
  - Salary is paid in 12 equal months with no bonus.
  - A child's age is held fixed for the whole year.
- **Not included in v1:** behaviour changes (static), long-term-care premiums for 65+ (Q15), 児童扶養手当 (Q17), the parents of the student household (Q16), consumption tax (added with household spending in Milestone 3).

## Policy designs (Milestone 3)

Each design is a reform in `engine/reforms.py` that reads only its own file in `parameters/designs/`. It runs the same household through the baseline twice, once unchanged and once with the reform, and reports the difference in five parts: income tax, resident tax, social insurance, credit or payment received, and consumption tax.

- **Daiwa (headline variant).** Income-tax basic deduction set to 0; each person gets a 56,500-yen tax credit. Credit left after income tax is paid in cash up to the person's labour social insurance (employee health + pension; NHI + national pension for the self-employed). *Approximation:* the credit comes off before the 2.1% reconstruction surtax, as existing tax credits do (Q11). See also Q18, Q19.
- **Government final** and the **payment part of the food tax cut.** The shape (flat, rising, flat, child add-on, phase-out, rounded up to 1,000 yen) is coded and tested with made-up numbers (`tests/hand_calcs/credit_shape.md`). Every real amount awaits a Cabinet order (Q9), so these show "incomplete parameters" and no number.
- **Food tax cut, tax side.** Saving = food spending × (8% − 1%) ÷ 1.08 × pass-through (100%, with a 50% sensitivity). *Approximation:* full pass-through to prices. Household food spending is not yet loaded (Q8), so no number yet.
- **Rengo.** No documents yet (Q3); shown as "incomplete parameters".

## Wall map and household comparison (Milestone 4)

- **Household comparison** (`outputs/household_comparison.csv`, `.json`): for every household and design, the change in take-home pay at the reference income, split into income tax, resident tax, social insurance, money received, and consumption tax. Designs with unpublished numbers show `incomplete` and list what is missing.
- **Wall map** (`outputs/wall_map.json`): one member's income moves from 0 to 10,000,000 yen in 10,000-yen steps; everything else about the household stays fixed (including "works 20+ hours at a 51+ firm"). At each step we record take-home pay and the **effective marginal rate**: 1 − (take-home at the next step − take-home here) ÷ 10,000. Above 100% means earning 10,000 more leaves you with less. In two-income households the moving income is set in the household file (`wall_map`, HUMAN_TODO H-11: D): H4 the spouse's salary; H3 and H8 the head's salary; H6 the head's pension.
- Built by `make outputs` (part of `make all`). Preview page: `site/wallmap.html` (serve the repository root, e.g. `python3 -m http.server`).
