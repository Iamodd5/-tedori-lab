# Project log (plain language)

## Milestone 0 — 2026-10-29: setup, sources, coverage

**What we did**

1. **Notifications.** Claude Code can run a small command whenever it stops and waits for you. We set two of these "hooks" in `.claude/settings.json`: one for the *Stop* event (Claude finished a turn) and one for the *Notification* event (Claude needs permission or input). Both run macOS's `osascript` to pop up "Tedori Lab: your action is needed. Check the terminal." with the "Glass" sound. A test notification was fired by hand (it ran without error). Hooks load when a session starts, so a fresh session is needed for them to be active.
   - If no pop-up appears: macOS shows `osascript` notifications under the app name **Script Editor**. Open System Settings → Notifications → Script Editor and turn on "Allow notifications". Also check that Focus / Do Not Disturb is off.
2. **Project skeleton.** Saved `SPEC.md` and `CLAUDE.md` (the project rules), started `OPEN_QUESTIONS.md` and `docs/HUMAN_TODO.md`, and made the folder a git repository.
3. **Sources.** Downloaded 50 files (government council papers, Daiwa's report, tax and insurance pages, Tokyo 2026 health-insurance tables, statistics landing pages) into `sources/`, each listed in `sources/SOURCES.md`, with fingerprints (SHA-256) in `sources/SHA256SUMS`. A helper script, `scripts/pdf_to_text.py`, turns every PDF into searchable text in `sources/text/`.
4. **Coverage check.** Read the OpenFisca-Japan code (the open-source Japanese tax-and-benefit calculator we plan to build on) and wrote down in `docs/COVERAGE.md` which rules it already has and which are missing or out of date.

**What we learned**

- The story has moved on since the spec was written. July 13 was only the *draft* interim summary. The government then adopted the interim summary (July 29), the Cabinet approved a basic policy (Aug 5), and in September–October it approved and sent to the Diet a law that (a) cuts the consumption tax on food from 8% to 1% for two years from April 2027, and (b) adds a new cash payment for workers called 就業者負担軽減支援金. Deciding which of these is "the government design" is a human decision (HUMAN_TODO H-3).
- The full refundable credit itself is planned for FY2029 (令和11年度). It is per person (not per household), includes single people, rises with work income up to a level, stays flat, then shrinks and disappears at higher total income, with extra for each child aged 18 or under. Exact numbers are for Milestone 1.
- Rengo's website was under maintenance, so its proposal could not be downloaded.
- OpenFisca-Japan already does income tax, resident tax, employee social insurance and child allowance, but some numbers are placeholders or old (e.g. health insurance rate, national pension amount), and it has no National Health Insurance. We will fix these in our own parameter files and offer the fixes back.

**Tools installed**

- A Python virtual environment in `.venv/` with `pypdf`, `cryptography` (needed to open some government PDFs) and `pyyaml`. Python on this machine is 3.15.

### Audit fixes — 2026-10-30

- `requirements.txt` lists the exact Python packages. A fresh copy is set up with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- File fingerprints moved from hand-copied table columns into `sources/SHA256SUMS`. `cd sources && shasum -a 256 -c SHA256SUMS` checks every file at once.
- The Daiwa report now has its full title in `SOURCES.md` (rule 1).
- `scripts/pdf_to_text.py` names each text file by folder + file name (e.g. `gov_20260713_02_siryou2.txt`), so two PDFs with the same name can't overwrite each other.
- Empty placeholder folders were removed; each folder from SPEC Section 4 is created when its first file is saved.

### Notification fix — 2026-10-30

The first test pop-up did not appear, and "Script Editor" was missing from System Settings → Notifications. macOS only lists an app there after it has asked for permission once. Fix: open Script Editor, run `display notification "Tedori Lab test" with title "Tedori Lab"` there, click **Allow**, and check that Notifications → Script Editor is on. After that, notifications sent from Terminal worked (confirmed by the human, H-1).

## Milestone 1 — 2026-10-30: design parameters

Decision used (H-3): the "government design" is the August 5 Cabinet decision, with details from the July 29 interim summary, the September 15 outline and the October 9 bill. The new worker payment that comes with the food tax cut is part of the food tax cut design.

**What each design file says** (all in `parameters/designs/`)

- **government_final.yaml.** From FY2029 the government will pay each working person (not each household) a yearly cash amount called 就業者負担軽減支援金. The rules so far:
  - You must earn at least a minimum amount from work, and have total income below a maximum.
  - What you pay in tax and social insurance, minus any public pension you receive, must be above a set level. This is how working older people can qualify.
  - If your spouse has a high income, you are excluded.
  - How much you get: a fixed amount at very low earnings. Above that, it rises with each extra yen earned, then stays flat. People earning just past the "income wall", where social insurance starts, get a temporary extra amount. Each child aged 18 or under adds a fixed amount. Above a higher income, the payment shrinks and then disappears.
  - Amounts are rounded up to the next 1,000 yen. It is paid once a year and is not taxed.
  - **None of the yen amounts or rates have been published yet.** The law leaves them to a later Cabinet order, so every number is marked "unresolved" (Q9).
- **food_tax_cut.yaml.** From 1 April 2027 to 31 March 2029, consumption tax on food goes from 8% to 1% (0.78% national plus local tax). "Food" means the same items that get the 8% reduced rate today; newspapers stay at 8%. The same worker payment also starts in FY2027, with three differences: children count only up to age 15, there is no spouse test, and the total cost is capped at roughly what 1% of consumption tax on food raises. Its amounts are also unpublished. Our baseline modelling assumption is that shops pass the whole tax cut on to prices. This is an approximation, and we also show a case where only half reaches shoppers.
- **daiwa.yaml.** Daiwa's idea:
  - Remove the basic deduction from income tax, and give every taxpayer a 56,500-yen tax credit instead. A tax credit is subtracted from the tax bill itself, not from income.
  - If your income tax is smaller than the credit, you get the difference back as cash, but never more than the social insurance you paid on your work income. So people living only on pensions or savings get no cash.
  - Resident tax does not change.

  The report also lists seven other versions. Which to use is your decision (Q10).
- **rengo.yaml.** Empty for now, because Rengo's website was down (Q3).
- **custom_template.yaml.** The five slider settings for the design builder. These have no official values.

**How we check it**

`tests/test_design_citations.py` opens every design file. Each parameter must either have a value plus a source and page number, or be marked "unresolved" with a question ID. Run it with `.venv/bin/python -m pytest -q tests`. Today: 6 passed.

## Milestone 2 — 2026-10-30: the 2026 baseline for H1–H8

Decision used (H-8): National Health Insurance follows Shinjuku ward's rules. Reference incomes as proposed: H1 1.25m; H2 1.0m; H3 4.5m + 3.0m; H4 5.0m + 1.0m; H5 2.5m; H6 pensions 2.0m + 0.8m; H7 business income 3.0m; H8 9.0m + 7.0m.

**How take-home pay is worked out** (`engine/baseline.py`, numbers in `parameters/baseline_2026/`)

1. **Employment income.** From your salary, the law first subtracts a fixed "employment income deduction" (an allowance for work costs). The result is your employment income. For 2026 the minimum deduction rose to 740,000 yen. So:
   - Salary below 741,000 counts as zero income.
   - Up to 2.19 million, income is salary minus 740,000.
   - From there up to 6.6 million, the tax office's official table gives the amount in 4,000-yen steps.
   - Above 6.6 million, a formula is used.

   Earners above 8.5 million with a child under 23 get a further cut of 10% of the salary above 8.5 million (capped at 10 million).
2. **Pension income.** People 65 or older subtract up to 1.1 million from their public pension, and more on a sliding scale at higher pensions.
3. **Social insurance.**
   - **Employees** pay half of each premium, read from Tokyo's 2026 table using "standard monthly pay" bands:
     - health insurance: 9.85%, or 11.47% at ages 40–64, because long-term care is added
     - the new child and childcare support levy: 0.23%
     - pension: 18.3%, with pay counted between 88,000 and 650,000 a month
     - employment insurance: 0.5% for the worker

     A part-timer joins only if all of these hold: they work 20+ hours a week, at a firm with 51+ staff, earn at least 88,000 a month, and are not a student.
   - **A spouse or child who doesn't join** can be a "dependant" with no premiums while their income stays under 1.3 million (1.5 million at ages 19–22). A dependant spouse also pays no pension contribution.
   - **Everyone else** pays National Health Insurance to Shinjuku. For each member there is a flat amount plus a percentage of income above 430,000. Low-income households get the flat amounts cut by 70%, 50% or 20%. People aged 20–59 in this group also pay the national pension, 17,920 yen a month.
4. **Income tax.**
   - From total income, take away the basic deduction (1.04 million for incomes up to 4.89 million, less above that), all social insurance paid, and any personal deductions: spouse, dependants aged 16+, single parent (350,000), working student (270,000).
   - Round the remainder down to 1,000 yen and apply the rate table (5% to 45%).
   - Add 2.1% reconstruction tax, then round down to 100 yen.
5. **Resident tax** (Shinjuku plus Tokyo).
   - Very low incomes pay nothing. For a single person, that means total income of 450,000 or less.
   - Everyone else pays a flat 5,000 yen (ward 3,000, Tokyo 1,000, forest tax 1,000).
   - On top of that, 10% of income after a smaller basic deduction (430,000) and smaller personal deductions, minus a small "adjustment credit" (調整控除) of at least 2,500 yen.
6. **Child allowance.** 15,000 yen a month for each child under 3, and 10,000 for each child from age 3 through high school. The third and later children get 30,000. There is no income limit.
7. **Disposable income** = pay + pensions + child allowance − income tax − resident tax − social insurance.

**Checks.** 28 tests pass (`make all`). They cover:
- the tax office's own worked example
- Shinjuku's health-insurance quick table
- Tokyo's premium table
- all 8 households against step-by-step hand calculations (`tests/hand_calcs/`), which agree to the yen

The table in `docs/VALIDATION.md` also compares our results with OpenFisca-Japan.

**Tools.** The project now runs on Python 3.11, because OpenFisca-Japan needs it. Set up with `uv venv --python 3.11 .venv && VIRTUAL_ENV=.venv uv pip install -r requirements.txt`.

## Milestone 3 — 2026-10-31: the designs as reforms

**Decision recorded.** H-9: A. We keep our own small baseline engine. OpenFisca-Japan stays as a cross-check, and fixes we find are offered back to it.

**How a design is tested against the baseline** (`engine/reforms.py`). We work out a household's take-home pay twice: once under 2026 law, once with the design switched on. The difference is the design's effect. We split it into five parts: income tax, resident tax, social insurance, money paid out by the design, and consumption tax.

**Daiwa's plan.** Today everyone subtracts a "basic deduction" from income before income tax. Daiwa removes it and gives everyone a fixed 56,500 yen off their income tax instead.
- If your tax is smaller than 56,500, the rest is paid to you in cash, but only if you work, and never more than you paid into health insurance and pension.
- Example: H1 (part-timer, 1.25 million) would owe 16,300 yen without the deduction, so 40,200 yen is left over and paid out. H1 gains 40,200 a year.
- Higher earners lose the deduction, which was worth more to them than 56,500 yen, so they pay more. H3's couple pays 18,300 more, H8's couple 148,100 more.
- Problem found: Daiwa sized the 56,500 for 2025 law. In 2026 the basic deduction almost doubled at most incomes, so the same swap costs far more. A single worker on 5 million pays 40,700 more with us, against 13,000 in Daiwa's report. How to handle this is a human decision (H-10).

**The government's payment and the food tax cut.** The law fixes the *shape* of the payment:
- a small flat amount for very low earners,
- then more as you earn more,
- then a flat "basic amount", plus an extra amount per child,
- then it shrinks once total income passes a set level.
That shape is now coded and tested with made-up practice numbers. But every real amount will be set later by a Cabinet order that is not out yet. So the site will show these designs as "incomplete" with no number, instead of a guess. The same goes for the food tax saving until we load food spending by income group (Q8), and for Rengo, whose documents we still cannot download (H-4).

**First contribution for OpenFisca-Japan.** Their national pension amount is 17,510 yen a month, from 2015. For 2026 it is 17,920. The exact change is written in `docs/COVERAGE.md`, ready for the human to submit.

**Checks.** 75 tests pass, including hand calculations for Daiwa (H1, H3, H7), eight practice cases for the payment shape, and a test that every design runs on every household without inventing a number.
