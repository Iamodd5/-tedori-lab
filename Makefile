# make all = fetch sources not kept in git, check every source, rebuild derived files, run tests, rebuild outputs/.
PY = .venv/bin/python

all: fetch-sources check-sources text tables test outputs

# Documents whose publishers do not allow redistribution are not committed; download them from the publisher.
# sources/EXTERNAL.tsv: path under sources/ <TAB> URL. check-sources then verifies their fingerprints.
fetch-sources:
	@grep -v '^#' sources/EXTERNAL.tsv | while IFS="$$(printf '\t')" read -r path url; do \
	  [ -f "sources/$$path" ] || { mkdir -p "$$(dirname "sources/$$path")" && curl -sfL -A "Mozilla/5.0" "$$url" -o "sources/$$path" && echo "downloaded $$path"; }; \
	done

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

.PHONY: all fetch-sources check-sources text tables test outputs
