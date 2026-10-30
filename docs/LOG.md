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
