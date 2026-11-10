"""Milestone 11: the press kit (spec 11), from outputs/ only: a one-page Japanese summary and three SVG charts.
Summary template: press/summary.ja.md with {name} fields filled from scripts/build_report.facts(), so every number
matches the report and the site. Charts are plain SVG written here (no plotting library), text kept as text."""
import json
import math
import pathlib
from xml.sax.saxutils import escape

from scripts import build_report as br

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "press"
INK, INK2, RULE, GRID = "#16243A", "#4E5B70", "#D3DAE3", "#E4E8EE"
DAIWA, LOSS, GAIN = "#B87A00", "#B3261E", "#0B6E4F"  # the site's colours: plan line, a loss, a gain
FONT = "Hiragino Sans, 'Hiragino Kaku Gothic ProN', 'BIZ UDPGothic', 'Noto Sans JP', 'Yu Gothic', sans-serif"
W, H = 720, 470
SOURCE = "出典：手取りラボ（2026年11月版）https://iamodd5.github.io/-tedori-lab/site/"
APPROX = "（近似）計算に含まれる近似は、サイトの「レポート」の「近似の一覧」にあります"
ADAPTED = "大和総研の算式を2026年の制度に当てはめた計算で、大和総研自身の試算とは異なります。"


def man(v):
    """Yen in 万 (10,000) for axis labels: 1500000 -> 150万."""
    x = v / 1e4
    if x == 0:
        return "0"
    return ("−" if x < 0 else "") + (f"{abs(x):,.0f}" if x == int(x) else f"{abs(x):,.1f}") + "万"


def ticks(lo, hi, n=5):
    raw = (hi - lo) / n
    step = min((m * 10 ** math.floor(math.log10(raw)) for m in (1, 2, 5, 10)), key=lambda s: abs(s - raw))
    return [step * k for k in range(math.floor(lo / step), math.ceil(hi / step) + 1)], step


def text(x, y, s, size=12, fill=INK2, anchor="start", weight="normal"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>'


def frame(title, subtitle, body, notes=()):
    """notes: lines printed above the source line, so the chart keeps its context when it travels alone."""
    foot = [text(24, H - 34 - 16 * (len(notes) - 1 - i), n, 11) for i, n in enumerate(notes)]
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
                      f'<rect width="{W}" height="{H}" fill="#fff"/>', f'<rect width="{W}" height="4" fill="{INK}"/>',
                      text(24, 38, title, 17, INK, weight="bold"), text(24, 60, subtitle, 12), *body, *foot,
                      text(24, H - 14, SOURCE, 11), "</svg>\n"])


def wall_chart(wm, f):
    """Figure 1: H4's take-home pay as the spouse's pay rises, 2026 rules and the calculated plan."""
    h4 = wm["households"]["H4"]["designs"]
    series = [(h4["baseline"], INK, "2026年の制度"), (h4["daiwa"], DAIWA, "（近似）" + f["daiwa_label"])]
    x0, x1, top = 0, 3_000_000, 3_000_000
    pts = {k: [(x, d) for x, d, *_ in s if x <= top] for k, (s, _, _) in enumerate(series)}
    ys = [d for p in pts.values() for _, d in p]
    yt, _ = ticks(min(ys), max(ys))
    L, R, T, B = 84, W - 44, 96, H - 112
    sx = lambda x: L + (x - x0) / (x1 - x0) * (R - L)
    sy = lambda y: B - (y - yt[0]) / (yt[-1] - yt[0]) * (B - T)
    body = [f'<line x1="{L}" x2="{R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{GRID}"/>' + text(L - 8, sy(v) + 4, man(v), 11, anchor="end") for v in yt]
    body += [text(sx(v), B + 18, man(v), 11, anchor="middle") for v in range(x0, x1 + 1, 500_000)]
    body.append(text((L + R) / 2, B + 38, "配偶者の給与（年、税引き前）", 11, anchor="middle"))
    body.append(f'<line x1="{L}" x2="{R}" y1="{B}" y2="{B}" stroke="{RULE}"/>')
    for k, (_, colour, _) in enumerate(series):
        path = " ".join(f"{sx(x):.1f},{sy(d):.1f}" for x, d in pts[k])
        body.append(f'<polyline points="{path}" fill="none" stroke="{colour}" stroke-width="2.2" stroke-linejoin="round"/>')
    for k, (_, colour, label) in enumerate(series):  # legend
        lx = L + k * 170
        body.append(f'<line x1="{lx}" x2="{lx + 18}" y1="80" y2="80" stroke="{colour}" stroke-width="2.2"/>' + text(lx + 24, 84, label, 11, INK))
    at = int(f["lead_at"].replace(",", ""))
    y_at = next(d for x, d in pts[0] if x == at)
    body.append(f'<polygon points="{sx(at) - 5:.1f},{sy(y_at) + 6:.1f} {sx(at) + 5:.1f},{sy(y_at) + 6:.1f} {sx(at):.1f},{sy(y_at) + 14:.1f}" fill="{LOSS}"/>')
    body.append(text(sx(at) + 10, sy(y_at) + 28, f"{f['lead_from']}円→{f['lead_at']}円で年{f['lead_drop']}円減る", 12, LOSS, weight="bold"))
    return frame("例の世帯H4：配偶者の給与と世帯の手取り",
                 f"東京都新宿区、会社員の夫または妻の給与が年{f['h4_earner']}円、子どもなし。手取り（年）。{f['grid_step']}きざみで計算", body,
                 ["配偶者は週20時間未満の勤務で、勤め先の健康保険には入っていません。ほかの案は、まだ計算できないため描いていません。", APPROX])


def bar_chart(title, subtitle, rows, notes=()):
    """Horizontal bars, one per row (label, yen); gains green, losses red, values written at the bar end."""
    vals = [v for _, v in rows]
    span = max(0, *vals) - min(0, *vals)
    xt, _ = ticks(min(0, *vals) - (.3 * span if min(vals) < 0 else 0), max(0, *vals) + .15 * span)  # room for the values
    L, R, T, B = 250, W - 70, 84, H - 60 - 16 * len(notes)  # the notes sit under the axis
    gap = (B - T) / len(rows)
    sx = lambda v: L + (v - xt[0]) / (xt[-1] - xt[0]) * (R - L)
    body = [f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{T}" y2="{B}" stroke="{INK if v == 0 else GRID}"/>' + text(sx(v), B + 16, man(v), 11, anchor="middle") for v in xt]
    for i, (label, v) in enumerate(rows):
        y = T + i * gap
        h = min(22, gap * .62)
        x, w = (sx(v), sx(0) - sx(v)) if v < 0 else (sx(0), sx(v) - sx(0))
        colour = LOSS if v < 0 else GAIN
        body.append(f'<rect x="{x:.1f}" y="{y + (gap - h) / 2:.1f}" width="{max(w, 1):.1f}" height="{h:.1f}" fill="{colour}"/>')
        body.append(text(L - 10, y + gap / 2 + 4, label, 12, INK, anchor="end"))
        ex = sx(v) - 6 if v < 0 else sx(v) + 6
        body.append(text(ex, y + gap / 2 + 4, br.signed(v), 11, INK, anchor="end" if v < 0 else "start"))
    return frame(title, subtitle, body, notes)


def charts(f):
    wm = json.loads((ROOT / "outputs" / "wall_map.json").read_text())
    cmp = json.loads((ROOT / "outputs" / "household_comparison.json").read_text())
    pop = json.loads((ROOT / "outputs" / "population.json").read_text())["designs"]["daiwa"]
    names = {hid: h["name_ja"] for hid, h in wm["households"].items()}
    households = [(f"{x['household']} {names[x['household']]}", x["disposable_change"]) for x in cmp if x["design"] == "daiwa"]
    groups = [(f"グループ{x['decile']}", round(x["mean_change"])) for x in pop["by_decile"]]
    return {
        "fig1_wall_h4.svg": wall_chart(wm, f),
        "fig2_households.svg": bar_chart(f"（近似）{f['daiwa_label']}：例の世帯の手取りの変化",
                                         "2026年の制度と比べた変化（円／年）", households, [ADAPTED, APPROX]),
        "fig3_groups.svg": bar_chart(f"（近似）{f['daiwa_label']}：全世帯の手取りの変化",
                                     "年収の低い順に同じ数ずつ10のグループに分けた、1世帯あたりの平均の変化（円／年）。グループ1が最も年収が低い", groups,
                                     [ADAPTED, "グループの平均です。どのグループにも、手取りが変わらない世帯や、平均と逆に動く世帯があります。",
                                      "（近似）2024年の国の調査の平均に合わせた架空の世帯による大まかな試算。働き方は変わらないものとしています"]),
    }


def render():
    f = br.facts()["ja"]
    files = {"summary.ja.md": (ROOT / "press" / "summary.ja.md").read_text(encoding="utf-8").format_map(f)}
    files.update(charts(f))
    return files


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = render()
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote outputs/press/ ({len(files)} files)")
