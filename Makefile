# make all = fetch sources not kept in git, check every source listed in SHA256SUMS, rebuild derived files, run tests, rebuild outputs/.
PY = .venv/bin/python

all: fetch-sources check-sources text tables test outputs

# Documents whose publishers do not allow redistribution are not committed; download them (sources/EXTERNAL.tsv).
# The publisher's file is tried first, then the Internet Archive copy, where one is listed, if the publisher's no longer
# matches SHA256SUMS; with neither, the build stops naming the page.
fetch-sources:
	$(PY) -I scripts/fetch_sources.py

check-sources:
	cd sources && shasum -a 256 -c --quiet SHA256SUMS

text:
	$(PY) -I scripts/pdf_to_text.py sources > /dev/null

tables:
	$(PY) -I scripts/extract_tables.py
	$(PY) -I scripts/extract_population.py

test:
	$(PY) -m pytest -q tests

outputs:
	PYTHONPATH=. $(PY) scripts/build_outputs.py
	PYTHONPATH=. $(PY) scripts/build_report.py
	PYTHONPATH=. $(PY) scripts/build_press.py
	PYTHONPATH=. $(PY) scripts/crosscheck_openfisca.py

# Every parameter is pinned by a rule test (a few minutes; changes parameter files while it runs).
pinned:
	$(PY) scripts/check_parameters_pinned.py

.PHONY: all fetch-sources check-sources text tables test outputs pinned
