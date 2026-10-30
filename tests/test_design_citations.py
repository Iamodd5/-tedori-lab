"""Milestone 1 acceptance check: every design parameter is cited or marked unresolved (CLAUDE.md rules 1-2)."""
import pathlib

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGNS = sorted((ROOT / "parameters" / "designs").glob("*.yaml"))
REQUIRED_TOP = {"name_ja", "name_en", "source", "start_year", "parameters", "status", "notes"}


def leaves(params, path=""):
    """Yield (path, node) for every parameter node, i.e. a dict that has a 'status' key."""
    for key, node in params.items():
        p = f"{path}.{key}" if path else key
        if isinstance(node, dict) and "status" in node:
            yield p, node
        elif isinstance(node, dict):
            yield from leaves(node, p)
        else:
            raise AssertionError(f"{p}: parameter must be a mapping with a 'status' key")


@pytest.mark.parametrize("design", DESIGNS, ids=lambda d: d.stem)
def test_design_parameters_are_cited_or_unresolved(design):
    d = yaml.safe_load(design.read_text(encoding="utf-8"))
    assert REQUIRED_TOP <= d.keys(), f"missing top-level fields: {REQUIRED_TOP - d.keys()}"
    sources = d["source"]
    for key, s in sources.items():
        for field in ("title", "url", "published"):
            assert s.get(field), f"source {key} lacks {field}"
    nodes = list(leaves(d["parameters"]))
    assert nodes, "design has no parameters"
    for path, node in nodes:
        status = node["status"]
        assert status in {"resolved", "unresolved", "user_input"}, f"{path}: bad status {status}"
        if status == "resolved":
            assert "value" in node and node["value"] is not None, f"{path}: resolved but no value"
            cite = node.get("cite")
            assert cite and cite.get("source") in sources and cite.get("page"), f"{path}: resolved needs cite.source + cite.page"
        if status == "unresolved":
            assert node.get("value") is None, f"{path}: unresolved must not carry a value"
            assert node.get("question"), f"{path}: unresolved needs a question id from OPEN_QUESTIONS.md"
    any_unresolved = any(n["status"] == "unresolved" for _, n in nodes)
    assert d["status"] == ("unresolved" if any_unresolved else "resolved"), "top-level status disagrees with parameters"


def test_all_five_designs_exist():
    assert {d.stem for d in DESIGNS} == {"government_final", "rengo", "daiwa", "food_tax_cut", "custom_template"}
