# Rules for this repository

1. Every policy parameter lives in a YAML file under `parameters/` and cites its source:
   document title, URL, page number, and the date the document was published.
2. Never invent, round, or "reasonably assume" a policy number. If a value is missing
   or ambiguous, add it to OPEN_QUESTIONS.md and mark the parameter `status: unresolved`.
3. Any approximation (for example consumption-tax incidence or population weighting)
   must be labelled `approximation: true` with a one-line explanation, and the label
   must be shown wherever the number appears on the website.
4. Tests come before rules. Each rule needs at least one test built from an official
   worked example or a hand calculation documented in `tests/hand_calcs/`.
5. Never edit a test to make it pass. Fix the rule, or record the conflict in OPEN_QUESTIONS.md.
6. Each policy design is its own reform file. The 2026 baseline is never edited to model a reform.
7. Every number on the website must be reproducible with `make all` from a clean clone.
8. Neutrality: the same households, data and method for every design. Outputs state
   findings only. No text recommends a design, party, or politician.
9. Prefer contributing to OpenFisca-Japan over duplicating it. If a needed rule is missing
   there, implement it in a way that can be offered upstream as a pull request.
10. After each milestone, write a plain-language summary in `docs/LOG.md` that a high school
    student could use to explain every rule implemented, without reading code.
11. Whenever human input or action is needed, stop and follow the Human handoff protocol
    in SPEC.md Section 13: add the task to docs/HUMAN_TODO.md, then end your turn with a
    HUMAN ACTION REQUIRED block. Never bury a request for the human inside a long summary.
