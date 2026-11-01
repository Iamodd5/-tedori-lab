"""Wall map (spec 9.2): disposable income and effective marginal rate across an income grid, 10,000-yen steps.

Only one member's income moves; everyone else stays at the reference income. Which member moves in a household
with two incomes is a human decision (HUMAN_TODO H-11), so those households are skipped until it is made.
"""
import copy

from engine import household as h
from engine import reforms as r

STEP = 10_000
INCOME_FIELDS = ("salary", "business_income", "public_pension")


def varying_member(hh):
    """(member id, income field) when exactly one member has income, else None."""
    earners = [(m["id"], f) for m in hh["members"] for f in INCOME_FIELDS if m.get(f)]
    return earners[0] if len(earners) == 1 else None


def disposable(hh, design):
    base = h.compute(hh)["disposable"]
    if design == "baseline":
        return base
    change = r.run(design, hh)["disposable_change"]
    return None if change is None else base + change


def grid(hh, design, top=10_000_000):
    mid, field = varying_member(hh)
    points = []
    for income in range(0, top + STEP, STEP):
        x = copy.deepcopy(hh)
        next(m for m in x["members"] if m["id"] == mid)[field] = income
        points.append({"income": income, "disposable": disposable(x, design)})
    for a, b in zip(points, points[1:] + [None]):
        ok = b is not None and a["disposable"] is not None and b["disposable"] is not None
        a["emr"] = round(1 - (b["disposable"] - a["disposable"]) / STEP, 4) if ok else None  # share of the next 10,000 lost
    return points
