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
