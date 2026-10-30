"""Extract text from every PDF and HTML file under sources/ into sources/text/ (one .txt per file, PDF pages marked)."""
import html.parser
import pathlib
import re
import sys

from pypdf import PdfReader


class _Text(html.parser.HTMLParser):
    """Visible text of an HTML page, one block per line; script/style dropped."""

    def __init__(self):
        super().__init__()
        self.parts, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        self._skip += tag in ("script", "style")
        if tag in ("p", "br", "tr", "li", "div", "h1", "h2", "h3", "h4", "table"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        self._skip -= tag in ("script", "style")
        if tag in ("td", "th"):
            self.parts.append(" | ")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_text(path):
    raw = path.read_bytes()
    # some government pages are Shift_JIS; the declared charset is in the first bytes
    m = re.search(rb'(?:charset|encoding)=["\']?([\w-]+)', raw[:2048], re.I)
    p = _Text()
    p.feed(raw.decode(m.group(1).decode() if m else "utf-8", errors="replace"))
    lines = (" ".join(line.split()) for line in "".join(p.parts).splitlines())
    return "\n".join(line for line in lines if line.strip(" |"))


root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "sources")
out = root / "text"
out.mkdir(exist_ok=True)
for f in sorted([*root.rglob("*.pdf"), *root.rglob("*.html")]):
    if out in f.parents:
        continue
    if f.suffix == ".pdf":
        pages = PdfReader(f).pages
        text = "\n".join(f"=== page {i} ===\n{p.extract_text() or ''}" for i, p in enumerate(pages, 1))
    else:
        text = html_text(f)
    # folder + name, so files with the same name in different folders do not overwrite each other
    (out / ("_".join(f.relative_to(root).with_suffix("").parts) + ".txt")).write_text(text, encoding="utf-8")
    print(f.relative_to(root))
