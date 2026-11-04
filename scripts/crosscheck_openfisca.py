"""Cross-check with OpenFisca-Japan (docs/VALIDATION.md section 3): each salaried member of H1, H3 and H8, run as a
single person in OpenFisca-Japan (commit pinned in requirements.txt) with its date set to 2026-12-01.
Writes outputs/openfisca_check.json; tests/test_validation_doc.py checks the table in VALIDATION.md against it."""
import json
import pathlib
import warnings

from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_japan import CountryTaxBenefitSystem

from engine import household as h

warnings.filterwarnings("ignore")
OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
D = "2026-12-01"
FIELDS = {"social_insurance": "社会保険料", "income_tax": "所得税", "resident_tax": "住民税"}

tbs = CountryTaxBenefitSystem()
rows = []
for hid in ["H1", "H3", "H8"]:
    hh = h.load(hid)
    ours = h.compute(hh)["members"]
    for m in hh["members"]:
        if not m.get("salary"):
            continue
        # OF-J's 国民年金保険に加入している defaults to True; employees in 厚生年金 don't pay National Pension (Q27)
        sit = {"世帯員": {"A": {"誕生年月日": {"ETERNITY": f"{2026 - m['age']}-01-01"}, "収入": {D: m["salary"]},
                                "週労働時間20時間以上": {D: True},
                                "国民年金保険に加入している": {D: ours[m["id"]]["scheme"] != "employee"}}},
               "世帯一覧": {"世帯1": {"親一覧": ["A"]}}}
        sim = SimulationBuilder().build_from_entities(tbs, sit)
        rows.append({"household": hid, "person": m["id"], "salary": m["salary"],
                     **{k: {"ours": ours[m["id"]][k], "openfisca": round(float(sim.calculate(v, D)[0]))}
                        for k, v in FIELDS.items()}})
(OUT / "openfisca_check.json").write_text(json.dumps({"date": D, "rows": rows}, ensure_ascii=False, indent=1))
print("wrote outputs/openfisca_check.json")
