"""Extract text from every PDF under sources/ into sources/text/ (one .txt per PDF, pages marked)."""
import pathlib, sys
from pypdf import PdfReader

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "sources")
out = root / "text"
out.mkdir(exist_ok=True)
for pdf in sorted(root.rglob("*.pdf")):
    r = PdfReader(pdf)
    pages = [f"=== page {i} ===\n{p.extract_text() or ''}" for i, p in enumerate(r.pages, 1)]
    (out / (pdf.stem + ".txt")).write_text("\n".join(pages), encoding="utf-8")
    print(f"{pdf.relative_to(root)}\t{len(r.pages)} pages")
