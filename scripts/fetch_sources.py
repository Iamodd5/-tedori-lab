"""Download the sources not kept in git (sources/EXTERNAL.tsv) and check each against sources/SHA256SUMS.

EXTERNAL.tsv: path under sources/ <TAB> publisher URL [<TAB> Internet Archive copy]. A file already present is left
alone (`make check-sources` checks it). The publisher's file is tried first; if it can't be downloaded or no longer
matches its fingerprint (publishers replace pages when their year rolls over), the archived copy is used instead."""
import hashlib
import pathlib
import sys
import urllib.request

UA = "Mozilla/5.0"


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def fetch(root):
    src = root / "sources"
    sums = dict(reversed(line.split("  ", 1)) for line in (src / "SHA256SUMS").read_text().splitlines()
                if line.strip() and not line.startswith("#"))
    for line in (src / "EXTERNAL.tsv").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        path, *urls = line.split("\t")
        target = src / path
        if target.exists():
            continue
        tried = []
        for url in urls:
            try:
                body = download(url)
            except Exception as e:  # unreachable or refused: try the next copy
                tried.append(f"{url}: {e}")
                continue
            # No fingerprint: the page embeds a per-request token (SHA256SUMS.volatile), so the publisher's file is used.
            if path not in sums or hashlib.sha256(body).hexdigest() == sums[path]:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(body)
                print(f"downloaded {path}" + ("" if url == urls[0] else " (Internet Archive copy; the publisher's file has changed)"))
                break
            tried.append(f"{url}: different from the saved fingerprint")
        else:
            sys.exit(f"could not get {path}:\n  " + "\n  ".join(tried))


if __name__ == "__main__":
    fetch(pathlib.Path(__file__).resolve().parents[1])
