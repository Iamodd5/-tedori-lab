# Project log (plain language)

## Milestone 0 — 2026-10-29: setup, sources, coverage

**What we did**

1. **Notifications.** Claude Code can run a small command whenever it stops and waits for you. We set two of these "hooks" in `.claude/settings.json`: one for the *Stop* event (Claude finished a turn) and one for the *Notification* event (Claude needs permission or input). Both run macOS's `osascript` to pop up "Tedori Lab: your action is needed. Check the terminal." with the "Glass" sound. A test notification was fired by hand (it ran without error). Hooks load when a session starts, so a fresh session is needed for them to be active.
   - If no pop-up appears: macOS shows `osascript` notifications under the app name **Script Editor**. Open System Settings → Notifications → Script Editor and turn on "Allow notifications". Also check that Focus / Do Not Disturb is off.
2. **Project skeleton.** Created the folders from SPEC Section 4, saved `SPEC.md` and `CLAUDE.md` (the project rules), started `OPEN_QUESTIONS.md` and `docs/HUMAN_TODO.md`, and made the folder a git repository.
3. **Sources.** Downloaded 50 files (government council papers, Daiwa's report, tax and insurance pages, Tokyo 2026 health-insurance tables, statistics landing pages) into `sources/`, each listed with a fingerprint (SHA-256) in `sources/SOURCES.md`. A helper script, `scripts/pdf_to_text.py`, turns every PDF into searchable text in `sources/text/`.
4. **Coverage check.** Read the OpenFisca-Japan code (the open-source Japanese tax-and-benefit calculator we plan to build on) and wrote down in `docs/COVERAGE.md` which rules it already has and which are missing or out of date.

**What we learned**

- The story has moved on since the spec was written. July 13 was only the *draft* interim summary. The government then adopted the interim summary (July 29), the Cabinet approved a basic policy (Aug 5), and in September–October it approved and sent to the Diet a law that (a) cuts the consumption tax on food from 8% to 1% for two years from April 2027, and (b) adds a new cash payment for workers called 就業者負担軽減支援金. Deciding which of these is "the government design" is a human decision (HUMAN_TODO H-3).
- The full refundable credit itself is planned for FY2029 (令和11年度). It is per person (not per household), includes single people, rises with work income up to a level, stays flat, then shrinks and disappears at higher total income, with extra for each child aged 18 or under. Exact numbers are for Milestone 1.
- Rengo's website was under maintenance, so its proposal could not be downloaded.
- OpenFisca-Japan already does income tax, resident tax, employee social insurance and child allowance, but some numbers are placeholders or old (e.g. health insurance rate, national pension amount), and it has no National Health Insurance. We will fix these in our own parameter files and offer the fixes back.

**Tools installed**

- A Python virtual environment in `.venv/` with `pypdf`, `cryptography` (needed to open some government PDFs) and `pyyaml`. Python on this machine is 3.15.
