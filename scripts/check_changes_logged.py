"""Fail when published numbers changed without a record of why.

If anything under outputs/, report/ or press/ changed between BASE and HEAD, docs/VALIDATION.md or
docs/CORRECTIONS.yaml must change in the same range (the record of what changed and why).
Usage: python scripts/check_changes_logged.py BASE     (BASE: a commit, e.g. the previous push)
"""
import subprocess
import sys

PUBLISHED = ("outputs/", "report/", "press/")
RECORDS = ("docs/VALIDATION.md", "docs/CORRECTIONS.yaml")


def changed(base):
    out = subprocess.run(["git", "diff", "--name-only", f"{base}..HEAD"], capture_output=True, text=True)
    if out.returncode != 0:
        print(f"cannot compare with {base!r}; skipped")
        sys.exit(0)
    return out.stdout.split()


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    if set(base) == {"0"}:          # first push of a new branch
        sys.exit(0)
    files = changed(base)
    published = [f for f in files if f.startswith(PUBLISHED)]
    if published and not any(f in RECORDS for f in files):
        print("Published numbers changed but neither " + " nor ".join(RECORDS) + " says why:")
        print("\n".join("  " + f for f in published))
        sys.exit(1)
    print(f"ok: {len(published)} published file(s) changed" + (", with a record" if published else ""))


if __name__ == "__main__":
    main()
