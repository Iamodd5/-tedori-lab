# 手取りラボ / Tedori Lab

**どの案でも、あなたの世帯で、同じ方法で。** Every proposal, your household, one method.

Japan is designing a refundable tax credit (給付付き税額控除) and a temporary food consumption tax cut. Tedori Lab compares the published designs on the same eight model households, with the same data and the same method, and shows the "income walls" (年収の壁) in each.

- Website: `site/index.html` (Japanese, with an English button)
- How it works: [`docs/METHODS.ja.md`](docs/METHODS.ja.md) (日本語), [`docs/METHODS.md`](docs/METHODS.md) (English)
- Checks: [`docs/VALIDATION.md`](docs/VALIDATION.md); open questions: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md)

The site states findings only. It does not recommend any design, party or politician.

## Rebuild every number

Needs Python 3.11, [uv](https://docs.astral.sh/uv/) and Node.js (the tests run the site's JavaScript).

```bash
uv venv --python 3.11 .venv && VIRTUAL_ENV=.venv uv pip install -r requirements.txt
make all
```

`make all` downloads any source document that is not stored in this repository (listed in `sources/EXTERNAL.tsv`), checks every source file against `sources/SHA256SUMS`, runs the tests and rebuilds `outputs/`.

## License

The code and the documents written for this project are under the GNU Affero General Public License v3.0 (see [`LICENSE`](LICENSE)). The files in `sources/` were published by others and keep their own terms. Each is listed with its publisher and URL in [`sources/SOURCES.md`](sources/SOURCES.md).
