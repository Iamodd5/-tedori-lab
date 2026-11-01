# make all = check sources, rebuild derived files, run tests. Later milestones add outputs and the site.
PY = .venv/bin/python

all: check-sources text tables test outputs

check-sources:
	cd sources && shasum -a 256 -c --quiet SHA256SUMS

text:
	$(PY) -I scripts/pdf_to_text.py sources > /dev/null

tables:
	$(PY) -I scripts/extract_tables.py

test:
	$(PY) -m pytest -q tests

outputs:
	PYTHONPATH=. $(PY) scripts/build_outputs.py

.PHONY: all check-sources text tables test outputs
