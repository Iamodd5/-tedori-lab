"""Check that every number in parameters/ is pinned by a test.

For each scalar parameter (a mapping with a numeric `value`), change the value a little, run the rule
tests (snapshot and page-text tests left out), and record whether any test failed. A parameter whose
change fails no rule test is not checked by any hand calculation or worked example.

Usage: python scripts/check_parameters_pinned.py [--only income_tax,resident_tax]
Exit code 1 if a parameter is unpinned and not listed in tests/unpinned_ok.yaml (with a reason).
Takes a few minutes: one test run per parameter. The parameter files are changed while it runs and put back after
each run; don't edit them, or run anything that reads them, at the same time.
"""
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = sorted((ROOT / "parameters" / "baseline_2026").glob("*.yaml")) + sorted((ROOT / "parameters" / "designs").glob("*.yaml"))
# tests that compare against committed files or page text, not against a hand calculation or worked example
NOT_RULE_TESTS = ["not snapshot_is_current", "--ignore=tests/test_validation_doc.py", "--ignore=tests/test_report.py",
                  "--ignore=tests/test_press.py", "--ignore=tests/test_corrections.py",
                  "--ignore=tests/test_number_provenance.py", "--ignore=tests/test_languages_match.py",
                  "--ignore=tests/test_plan_quotes.py", "--ignore=tests/test_calculator_grid.py"]


def leaves(node, path=()):
    if isinstance(node, dict):
        v = node.get("value")
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            yield path
        for k, child in node.items():
            if k != "value":
                yield from leaves(child, path + (k,))
    elif isinstance(node, list):
        for i, child in enumerate(node):
            yield from leaves(child, path + (i,))


def nudged(v):
    if isinstance(v, int) and abs(v) < 200:      # ages, counts, hours
        return v + 1
    if v == 0:
        return 1
    return type(v)(v * 1.05) if isinstance(v, float) else round(v * 1.05)


def rule_tests_pass():
    cmd = [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-k", NOT_RULE_TESTS[0], *NOT_RULE_TESTS[1:], "tests"]
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).returncode == 0


def main():
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    assert rule_tests_pass(), "the rule tests must pass before the check starts"
    ok = yaml.safe_load((ROOT / "tests" / "unpinned_ok.yaml").read_text(encoding="utf-8")) if (ROOT / "tests" / "unpinned_ok.yaml").exists() else {}
    ok = ok or {}
    unpinned = []
    for f in FILES:
        if only and f.stem not in only:
            continue
        original = f.read_bytes()
        data = yaml.safe_load(original.decode("utf-8"))
        for path in list(leaves(data)):
            changed = yaml.safe_load(original.decode("utf-8"))
            node = changed
            for k in path:
                node = node[k]
            node["value"] = nudged(node["value"])
            f.write_text(yaml.safe_dump(changed, allow_unicode=True, sort_keys=False), encoding="utf-8")
            try:
                if rule_tests_pass():
                    unpinned.append(f"{f.relative_to(ROOT)}: {'.'.join(map(str, path))}")
            finally:
                f.write_bytes(original)
    missing = [u for u in unpinned if u not in ok]
    for u in unpinned:
        print(("  ok (listed)  " if u in ok else "  UNPINNED     ") + u + (f"  — {ok[u]}" if u in ok else ""))
    print(f"{len(unpinned)} unpinned, {len(missing)} not listed in tests/unpinned_ok.yaml")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
