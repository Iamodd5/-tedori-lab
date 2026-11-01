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
  - What you pay in tax and social insurance, minus any public pension you receive, must be above a set level. This lets working older people qualify. The government also names who is left out for now: low earners below the minimum, and older people who do not work. Both are to be looked at again later (Aug 5 explanation slide, 資料3 p.3). Our pensioner couple H6 has no work income, so it would get nothing from this payment.
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

## Milestone 4 — 2026-11-01: wall map and comparison table

**Decision recorded.** H-10: A. Daiwa's plan is applied exactly as published, on 2026 rules. Every Daiwa number on the site carries a note (in Japanese and English) saying Daiwa designed it for 2025 rules, so our results differ from theirs.

**The comparison table** (`outputs/household_comparison.csv`). For each household and each design, how much take-home pay changes in a year, and why: income tax, resident tax, social insurance, money paid out, consumption tax. Designs whose numbers are not published yet say "incomplete" instead of showing a number.

**The wall map** (`outputs/wall_map.json`).
- We raise one person's income in 10,000-yen steps from 0 to 10 million.
- At each step we ask: of the next 10,000 yen earned, how much is lost to tax, insurance and lost benefits? That share is the "effective marginal rate".
- If it is more than 100%, earning more leaves you with less money. That is a "wall".

Walls the map shows for 2026 rules:
- **H2 (student), at 1.5 million.** Above it the student can no longer be on the parents' health insurance.
- **H2 and H7, at total income 4.89 million.** The basic deduction drops from 1.04 million to 670,000 here. Daiwa's plan removes this cliff because it removes the basic deduction.
- **H5 (single parent), at salary 2.09 million.** The single-parent exemption from resident tax ends.
- **Every employee, small steps.** Insurance premiums are charged on "bands" of monthly pay, so moving up a band costs more than the raise.

**A surprise worth knowing.** H1 is called "near the 1.3 million wall", but as we modelled H1 (living alone), that wall does not hit them. The 1.06m and 1.3m walls only apply to someone who could otherwise be covered as a dependant on a parent's or spouse's insurance for free. A single person below that line already pays National Health Insurance and the national pension (about 235,000 yen a year), which is more than the employee premiums at that pay. So joining employee insurance actually *raises* H1's take-home pay by about 90,000 yen. Whether to redefine H1 is an open question (Q21).

**What is not done yet.**
- Wall maps for the four households with two incomes (H3, H4, H6, H8) need a decision on whose income moves (H-11).
- A preview page, `site/wallmap.html`, draws both charts and the table straight from `outputs/`.

### Milestone 4 completed — 2026-11-01

**Decision recorded.** H-11: D. In households with two incomes, the wall map moves:
- H4: the part-time spouse's pay (to show the spouse walls);
- H3 and H8: the main earner's pay;
- H6: the main pensioner's pension.

**H4 shows the famous 1.3 million wall.** When the spouse's pay goes from 1,290,000 to 1,300,000, the spouse can no longer be covered for free on the main earner's insurance. The household must now pay:
- national pension, 215,040 a year;
- National Health Insurance, 101,786 a year.
Taxes fall a little, but take-home pay still drops by 281,926 yen for earning 10,000 more. Every step is in `tests/hand_calcs/wall_H4.md`.

**Two rules fixed because the wall map exposed them.** Neither changes the eight reference households.
1. *National Health Insurance discount for low-income homes.* Shinjuku decides who gets it by adding up the incomes of the insured people **and** the head of the household, even if the head has work insurance. We had left the head out.
2. *Resident-tax "soft landing".* Just above the income level where resident tax starts, the law limits the tax to the amount by which your income is over that level. This stops a 10,000-yen raise from costing 85,000 yen in tax. The Ministry's own example: line 1,120,000, income 1,124,200, tax 4,200.

**Why there are spikes every 240,000 yen.** Employee insurance is charged on "standard monthly pay" in steps of 20,000 a month at middle incomes. Crossing a step raises a whole year's premiums at once, so for that 10,000 yen the marginal rate is about 300%. These steps are real. They look sharp only because we use 10,000-yen steps.

**Checks.** 83 tests pass. `make all` rebuilds the outputs, and the preview page draws all eight households.

## Milestone 5 — 2026-11-01: adversarial self-review (spec 12.3)

Two independent reviewers read the whole project. Each took three of the six roles in spec 12.3 and could only read, not change, anything. Below is each finding, whether we confirmed it, and what we did about it.

| Role | Finding | Checked? | What we did |
|---|---|---|---|
| Tax accountant | Spouse aged 70+ never got the larger "elderly spouse" deduction. The number was in the YAML, but no code used it. | Confirmed (NTA p.55) | Fixed; test added |
| Tax accountant | Only the person labelled "head" could claim the spouse or children, or be covered on the other partner's insurance. | Confirmed (H3 at low head pay) | Fixed: the higher earner claims (Q23, labelled approximation) |
| Tax accountant | Resident-tax income limit for a spouse or dependant was 480,000. It is 580,000 from 令和8年度. | Confirmed (MIC p.28) | Fixed; whether it rises to 620,000 for 令和9年度 is still open (Q13) |
| Tax accountant | Part-timers below 88,000 a month pay no employment insurance here. | Plausible, but the rule is not in our sources | Recorded (Q24) |
| Tax accountant | Who counts as an "earner" for the NHI discount | Not in our sources | Recorded (Q25) |
| Tax accountant | Who deducts the spouse's national pension changes H4's wall | True; it is a choice | Recorded (Q26), asked the human |
| Maintainer | Some policy numbers are written in the code, not the YAML (breaks rule 1) | Confirmed | Recorded (Q28); proposed as its own task |
| Maintainer | Hand calculations come from the same author, so tests can be circular; no snapshot test; no outside calculator check | Partly | Snapshot test added; outside check still to do (spec 12.2); 17–20k gap with OpenFisca-Japan recorded (Q27) |
| Maintainer | `sources/text` is out of date | Not confirmed (17 text files for 19 tax files; the other 2 are images) | No change |
| Economist | Approximations not shown on the page (rule 3) | Confirmed | The page now lists every baseline approximation, each household's notes, and Daiwa's Q11/Q18 approximations |
| Economist | Daiwa shown as "complete" although its file has an open item | Confirmed | Shown with its approximations; human asked to approve them (H-12) |
| Economist | Daiwa's 56,500 comes from a formula that gives 52,000 under 2026 rules | Confirmed (Daiwa p.5 注1, p.6) | Recorded (Q29); H-10 reopened for the human (H-12) |
| Ruling-party staffer | The chart showed only Daiwa, with no word that the other designs were missing | Confirmed | A banner now names each design not drawn and why |
| Ruling-party staffer | One label, "incomplete parameters", hid three different reasons | Confirmed | Each design now shows its own reason: "waiting for Cabinet order", "this tool's data not ready", or "documents not obtained" |
| Ruling-party staffer | The government's 2027–28 package was labelled "Food tax cut" only | Confirmed | Labelled as the government's bridge package (food 1% + payment) |
| Ruling-party staffer | Red for the government design | Confirmed | Switched to a colour-blind-safe palette that carries no meaning |
| Ruling-party staffer | Daiwa's own estimates were kept for checking; the government's were not | Confirmed | Government's own figures added; its 1.6m recovery point is checked against our 1.65m (VALIDATION §7) |
| Opposition staffer | Name said "full refundable credit", which the source calls only a "first step" | Confirmed (outline p.1) | Renamed after the documents' own term (支援金制度の本格導入) |
| Opposition staffer | Who the government leaves out was not stated | Confirmed (Aug 5 資料3 p.3) | Stated in the design file and this log; H6 gets nothing |
| Opposition staffer | Food rate returns to 8% in FY2029 | True | Noted; FY2027–28 and FY2029 will be shown separately once numbers exist |
| Journalist | Axis cut at 300% hid the size of the big walls | Confirmed | Cut points are marked ▲ and show their true value on hover or tap |
| Journalist | H1's name promises a wall it does not face | Confirmed (Q21) | A note on the page; renaming H1 is the human's choice |
| Journalist | "Expensive" was an opinion word | Confirmed | Reworded with the numbers |

**Neutrality check:** no text recommends a design, party or politician.

**A lead that is true and checked (for later, not yet published).** Under 2026 rules, a part-time spouse in Shinjuku (H4) keeps about 280,000 yen less by earning 1,300,000 instead of 1,290,000. Their take-home pay does not get back to the 1,290,000 level until they earn 1,650,000. The government's own outline puts that recovery point at about 1.6 million. No design can be compared on this yet, because the government's amounts are not published.

**Results.** 88 tests pass. None of the eight households changed at their reference incomes; the fixes change only the wall maps.
