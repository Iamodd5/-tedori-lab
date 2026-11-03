"""Wall map (spec 9.2): disposable income and effective marginal rate across an income grid, 10,000-yen steps.

Only one member's income moves; everyone else stays at the reference income. In a household with two incomes
the household file names the member (`wall_map`, chosen by the human: HUMAN_TODO H-11: D).
"""
import copy

from engine import household as h
from engine import reforms as r

STEP = 10_000
INCOME_FIELDS = ("salary", "business_income", "public_pension")


def varying_member(hh):
    """(member id, income field): the household's `wall_map` choice, else the only member with income, else None."""
    if "wall_map" in hh:
        return hh["wall_map"]["member"], hh["wall_map"]["income"]
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


def at_income(hh, income):
    """The household with the wall map's moving income set to `income`."""
    mid, field = varying_member(hh)
    x = copy.deepcopy(hh)
    next(m for m in x["members"] if m["id"] == mid)[field] = income
    return x


def parts(hh, income):
    """What the household pays and receives at one income on the wall map (2026 rules), to explain a wall."""
    res = h.compute(at_income(hh, income))
    ms = res["members"].values()
    total = lambda *ks: sum(o[k] for o in ms for k in ks)
    return {"income_tax": total("income_tax"), "resident_tax": total("resident_tax"),
            "employee_insurance": total("health", "child_levy", "pension", "employment"),
            "national_pension": total("national_pension"), "nhi": total("nhi"),
            "child_allowance": res["child_allowance"], "scheme": res["members"][varying_member(hh)[0]]["scheme"]}


def wall_causes(hh, walls):
    """For each wall {from, at, ...}: the change in each tax, premium and benefit, and the moving member's scheme before and after."""
    out = []
    for wl in walls:
        a, b = parts(hh, wl["from"]), parts(hh, wl["at"])
        out.append({"from": wl["from"], "scheme": [a["scheme"], b["scheme"]],
                    "change": {k: b[k] - a[k] for k in a if k != "scheme"}})
    return out
