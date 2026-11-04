"""Milestone 9: the short report (spec 3, 11), in Japanese and English, from outputs/ only.
Templates: report/report.{ja,en}.md with {name} fields. Every number comes from `facts()`; tests/test_report.py
checks that the templates contain no numbers of their own and that outputs/report.*.md are current."""
import json
import pathlib

import yaml

from engine import reforms as r

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
LANGS = ("ja", "en")


def walls(pts, min_drop=10_000):
    """Same rule as site/walls.js bigWalls: earning 10,000 more cuts take-home by min_drop or more (income 0 skipped)."""
    out = []
    for (x, d, *_), (x2, d2, *_) in zip(pts, pts[1:]):
        if x and d - d2 >= min_drop:
            back = next((q[0] for q in pts if q[0] > x and q[1] >= d), None)
            out.append({"from": x, "at": x2, "drop": d - d2, "back": back})
    return out


def yen(n):
    return f"{round(n):,}"


def signed(n):
    return ("+" if n > 0 else "−" if n < 0 else "±") + yen(abs(n))


def facts():
    wm = json.loads((OUT / "wall_map.json").read_text())
    cmp = json.loads((OUT / "household_comparison.json").read_text())
    pop = json.loads((OUT / "population.json").read_text())
    f = {l: {} for l in LANGS}
    both = {}

    # lead finding: the biggest wall for H4 under 2026 rules, and the same step under each calculated design
    h4 = wm["households"]["H4"]["designs"]
    lead = max(walls(h4["baseline"]), key=lambda w: w["drop"])
    both.update(lead_from=yen(lead["from"]), lead_at=yen(lead["at"]), lead_drop=yen(lead["drop"]), lead_back=yen(lead["back"]))
    cause = next(c for c in wm["households"]["H4"]["wall_causes"] if c["from"] == lead["from"])["change"]
    assert cause["employee_insurance"] == 0 and cause["income_tax"] <= 0 and cause["resident_tax"] <= 0, "rewrite the lead's reason"
    sc = yaml.safe_load((ROOT / "parameters" / "baseline_2026" / "social_insurance.yaml").read_text(encoding="utf-8"))["part_time_coverage"]
    both.update(lead_np=yen(cause["national_pension"]), lead_nhi=yen(cause["nhi"]), lead_tax_cut=yen(-cause["income_tax"] - cause["resident_tax"]),
                hours_min=sc["hours_min"]["value"], employer_min=sc["employer_size_min"]["value"])
    f["ja"]["grid_step"], f["en"]["grid_step"] = f"{wm['step'] // 10_000}万円", f"¥{yen(wm['step'])}"
    daiwa_step = next(w for w in walls(h4["daiwa"]) if w["from"] == lead["from"])
    both.update(lead_daiwa_drop=yen(daiwa_step["drop"]), lead_daiwa_back=yen(daiwa_step["back"]),
                h4_earner=yen(next(m["salary"] for m in wm["households"]["H4"]["incomes"] if m["role"] == "head")),
                n_households=len(wm["households"]))

    # the designs: which can be calculated, and why the others cannot
    first = [x for x in cmp if x["household"] == "H1"]
    done = [x for x in first if x["status"] == "complete"]
    both.update(n_plans=len(first), n_done=len(done), n_blocked=len(first) - len(done), full_year=r.design("government_final")["start_year"])
    for l in LANGS:
        sep = "：" if l == "ja" else ": "
        f[l]["done_labels"] = "、".join(x["label"][l] for x in done) if l == "ja" else ", ".join(x["label"][l] for x in done)
        f[l]["plan_list"] = "\n".join(f"- **{wm['labels'][d][l]}**{sep}{wm['shorts'][d][l]}" for d in wm["shorts"])
        f[l]["blocked_list"] = "\n".join(f"- {x['label'][l]}{sep}{(('。' if l == 'ja' else '; ').join(b[l] for b in x['blocked_by']))}{'。' if l == 'ja' else '.'}"
                                         for x in first if x["status"] != "complete")

    # example households under the calculated design
    daiwa = {x["household"]: x for x in cmp if x["design"] == "daiwa"}
    for l in LANGS:
        name = "name_ja" if l == "ja" else "name_en"
        f[l]["household_rows"] = "\n".join(
            f"| {hid} | {wm['households'][hid][name]} | {yen(x['baseline_disposable'])} | {signed(x['disposable_change'])} |"
            for hid, x in daiwa.items())
    ch = [x["disposable_change"] for x in daiwa.values()]
    both.update(hh_up=sum(c > 0 for c in ch), hh_down=sum(c < 0 for c in ch), hh_same=sum(c == 0 for c in ch))
    best, worst = max(daiwa.values(), key=lambda x: x["disposable_change"]), min(daiwa.values(), key=lambda x: x["disposable_change"])
    both.update(hh_best=best["household"], hh_best_change=signed(best["disposable_change"]),
                hh_worst=worst["household"], hh_worst_change=signed(worst["disposable_change"]))

    # all households (approximate)
    d = pop["designs"]["daiwa"]
    by = d["by_decile"]
    up, down = [x for x in by if x["mean_change"] > 0], [x for x in by if x["mean_change"] < 0]
    top_up, top_down = max(up, key=lambda x: x["mean_change"]), min(down, key=lambda x: x["mean_change"])
    for l in LANGS:
        dash = "〜" if l == "ja" else "–"
        f[l]["up_groups"] = f"{up[0]['decile']}{dash}{up[-1]['decile']}"
        f[l]["down_groups"] = f"{down[0]['decile']}{dash}{down[-1]['decile']}"
    both.update(up_top_group=top_up["decile"], up_top=yen(top_up["mean_change"]), down_top_group=top_down["decile"],
                down_top=yen(-top_down["mean_change"]), net=f"{-d['cost_yen'] / 1e12:.1f}",  # rough estimates: 0.1 trillion
                it_up=f"{d['cost_components_yen']['income_tax'] / 1e12:.1f}", cash=f"{d['cost_components_yen']['credit'] / 1e12:.1f}")
    pct_range = lambda k: (lambda v: f"{min(v)}" if min(v) == max(v) else f"{min(v)}{{dash}}{max(v)}")([round(x[k] * 100) for x in up])
    for l in LANGS:
        dash = "〜" if l == "ja" else "–"
        f[l]["up_win"] = pct_range("winners_share").replace("{dash}", dash)
        f[l]["up_same"] = pct_range("unchanged_share").replace("{dash}", dash)
    lose = [(x["decile"], round(x["losers_share"] * 100)) for x in up if round(x["losers_share"] * 100) > 0]
    f["ja"]["up_lose"] = "".join(f"グループ{g}では{p}%の世帯で手取りが減ります。" for g, p in lose)
    f["en"]["up_lose"] = "".join(f" In group {g}, {p}% of households are worse off." for g, p in lose)
    assert d["cost_yen"] < 0, "the report text says the government takes in more; rewrite it if this changes"
    pub = d["published_estimates"]
    both.update(pub_it=pub["headline_variant_with_refund"]["income_tax_increase_trillion_yen"],
                pub_cash=pub["headline_variant_with_refund"]["refund_payments_trillion_yen"],
                credit_2025=yen(pub["tax_credit_under_2025_rules"]), credit_2026=yen(r.daiwa_credit()))

    # calibration gaps (docs/VALIDATION.md section 10)
    cal = pop["calibration"]
    gap = lambda a, b: f"{abs(a - b) / b * 100:.1f}"
    both.update(gap_households=gap(cal["households"]["model"], cal["households"]["official_kiso_2025"]),
                gap_income_tax=gap(cal["income_tax"]["model_baseline_2026"], cal["income_tax"]["survey_estimate_2024"]),
                gap_resident_tax=gap(cal["resident_tax"]["model_baseline_2026"], cal["resident_tax"]["survey_estimate_2024"]))

    # every approximation behind the numbers in the report (project rule 3)
    for l in LANGS:
        lab = "（近似）" if l == "ja" else "(Approximation) "
        f[l]["approx_baseline"] = "\n".join(f"- {a[l]}" for a in wm["baseline_approximations"])
        f[l]["approx_daiwa"] = "\n".join(f"- {lab}{a[l]}" for a in daiwa["H1"]["approximations"])
        f[l]["approx_population"] = "\n".join(f"- {lab}{a[l]}" for a in pop["approximations"])
        f[l]["daiwa_note"] = daiwa["H1"]["site_note"][l]
        f[l]["daiwa_label"] = daiwa["H1"]["label"][l]
    return {l: {**both, **f[l]} for l in LANGS}


def render():
    fs = facts()
    return {l: (ROOT / "report" / f"report.{l}.md").read_text(encoding="utf-8").format_map(fs[l]) for l in LANGS}


if __name__ == "__main__":
    for l, text in render().items():
        (OUT / f"report.{l}.md").write_text(text, encoding="utf-8")
    print("wrote outputs/report.ja.md, outputs/report.en.md")
