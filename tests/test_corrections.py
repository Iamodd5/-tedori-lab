"""Corrections log (docs/CORRECTIONS.yaml, spec 10 page 8): every entry complete, and every checked number matches
the published versions it names. Skips the git checks in a clone without history."""
import json
import pathlib
import subprocess

import pytest
import yaml

from scripts.build_report import walls

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG = yaml.safe_load((ROOT / "docs" / "CORRECTIONS.yaml").read_text(encoding="utf-8"))


def git_json(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        pytest.skip(f"git history not available for {commit}")
    return json.loads(r.stdout)


def value(commit, c):
    if "household" in c:
        pts = git_json(commit, "outputs/wall_map.json")["households"][c["household"]]["designs"][c["design"]]
        if "income" in c:  # take-home pay at one income on the wall map
            return next(p[1] for p in pts if p[0] == c["income"])
        return next(w for w in walls(pts) if w["from"] == c["from"])[c["field"]]
    by = git_json(commit, "outputs/population.json")["designs"][c["population"]]["by_decile"]
    return round(next(x for x in by if x["decile"] == c["decile"])["mean_change"])


def test_entries_complete_newest_first():
    assert [e["date"] for e in LOG] == sorted((e["date"] for e in LOG), reverse=True)
    for e in LOG:
        assert e["previous"] and all(e[k]["ja"] and e[k]["en"] for k in ("what", "why"))
        for n in e.get("numbers", []):
            assert n["label"]["ja"] and n["label"]["en"] and n["before"] != n["after"]
            assert "check" not in n or "published" in e


@pytest.mark.parametrize("entry,n", [(e, n) for e in LOG for n in e.get("numbers", []) if "check" in n])
def test_numbers_match_published_versions(entry, n):
    assert value(entry["previous"], n["check"]) == n["before"]
    assert value(entry["published"], n["check"]) == n["after"]

