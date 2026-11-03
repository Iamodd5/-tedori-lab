"""Every number in parameters/baseline_2026/*.yaml is read by the engine (project rule 1, OPEN_QUESTIONS Q28).

The test wraps params() so each read is recorded, runs every household (at its reference income and across a
coarse wall-map grid) plus three made-up households that reach the remaining branches, then lists the numbers
nobody read. Reading a list (a band table) counts as reading every number in it.
"""
import pathlib

import yaml

from engine import baseline as b
from engine import household as h
from engine import wall_map as w

HOUSEHOLDS = sorted(p.stem for p in (pathlib.Path(__file__).parents[1] / "households").glob("H*.yaml"))

# Numbers kept in the YAML for the record but not used by any rule. Each needs a reason.
NOT_READ = {
    ("income_tax", "public_pension_income", "age65_plus", 0, "floor_zero_until"): "restates the next row, which starts at 1,100,001",
    ("income_tax", "dependent_deduction", "elderly_70_plus_not_living_together", "value"): "not modelled: no household has a dependant aged 70+",
    ("resident_tax", "basic_deduction", "amount", "value"): "the taper's first band holds the same 430,000",
    ("resident_tax", "adjustment_credit", "income_limit", "value"): "not modelled: no household or wall-map point reaches 25m",
    ("social_insurance", "part_time_coverage", "employer_size_min", "value"): "household files state this test as yes/no (employer_51_plus)",
    ("social_insurance", "part_time_coverage", "hours_min", "value"): "household files state this test as yes/no (hours_20_plus)",
    ("social_insurance", "nhi_shinjuku_fy2026", "preschool_flat_reduction", "value"): "not modelled: no household has a preschool child in NHI",
}


class _Tracked(dict):
    def __init__(self, d, path, seen):
        super().__init__(d)
        self.path, self.seen = path, seen

    def __getitem__(self, k):
        return _wrap(super().__getitem__(k), self.path + (k,), self.seen)

    def get(self, k, default=None):
        return self[k] if k in self else default


def _wrap(v, path, seen):
    if isinstance(v, dict):
        return _Tracked(v, path, seen)
    if isinstance(v, list):
        return [_wrap(x, path + (i,), seen) for i, x in enumerate(v)]
    seen.add(path)
    return v


def _numbers(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            if k not in ("cite", "source"):
                yield from _numbers(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _numbers(v, path + (i,))
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        yield path


def _scenarios():
    for hid in HOUSEHOLDS:
        hh = h.load(hid)
        yield hh
        mid, field = w.varying_member(hh)
        for income in range(0, 10_000_001, 100_000):
            x = {"members": [dict(m, **({field: income} if m["id"] == mid else {})) for m in hh["members"]]}
            yield x
    full = {"full_time": True}
    yield {"members": [{"id": "a", "role": "head", "age": 45, "salary": 5_000_000, "work": full},  # dependants 16-22,
                       {"id": "b", "role": "spouse", "age": 43},                                    # a third child
                       {"id": "c1", "role": "child", "age": 17}, {"id": "c2", "role": "child", "age": 20},
                       {"id": "c3", "role": "child", "age": 21, "salary": 1_600_000},
                       {"id": "c4", "role": "child", "age": 5}, {"id": "c5", "role": "child", "age": 1}]}
    yield {"members": [{"id": "a", "role": "head", "age": 62, "salary": 5_000_000, "work": full},  # dependant aged 60+
                       {"id": "b", "role": "spouse", "age": 61, "salary": 500_000}]}
    yield {"members": [{"id": "a", "role": "head", "age": 45, "salary": 50_000_000, "work": full}]}  # top tax band
    for age, salary in ((45, 11_000_000), (45, 11_500_000), (72, 11_000_000)):  # resident-tax spouse deduction above 9m
        yield {"members": [{"id": "a", "role": "head", "age": age, "salary": salary, "work": full}, {"id": "b", "role": "spouse", "age": age}]}


def test_every_baseline_number_is_read(monkeypatch):
    seen = set()
    real = b.params
    monkeypatch.setattr(b, "params", lambda name: _wrap(real(name), (name,), seen))
    for hh in _scenarios():
        h.compute(hh)
    numbers = {p for f in sorted(b.P.glob("*.yaml"))
               for p in _numbers(yaml.safe_load(f.read_text(encoding="utf-8")), (f.stem,))}
    assert set(NOT_READ) <= numbers, "NOT_READ names a number that is not in the YAML"
    assert numbers - seen == set(NOT_READ), "numbers never read (fix the engine, or add to NOT_READ with a reason)"
