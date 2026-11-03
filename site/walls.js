// Wall charts shared by Home and Build your own: take-home pay, and how much of an extra ¥100,000 you keep.
// Data: points [[income, take-home, ...], ...] at 10,000-yen steps from outputs/wall_map.json.
const WALL = { step: 100000, ranges: [3e6, 6e6, 1e7], minDrop: 10000 };

// How much more take-home pay (yen) an extra ¥100,000 of income brings; below 0 is a wall.
// 100,000 rather than 10,000 so rounding of tax to 100 yen does not show as noise.
// Starts at 100,000: income 0 is left out here and in the wall list (see bigWalls).
function keepSeries(pts) {
  const at = new Map(pts.map(p => [p[0], p[1]]));
  return pts.filter(p => p[0] > 0 && p[0] % WALL.step === 0 && at.has(p[0] + WALL.step)).map(p => [p[0], at.get(p[0] + WALL.step) - p[1]]);
}

const KEEP_FLOOR = -200000;  // lower values are drawn at the floor and marked ▼; the tooltip gives the real amount
// signed short yen for the keep axis: 5万 / −20万, ¥50k / −¥200k
const keepTick = v => v === 0 ? "0" : lang === "ja" ? `${v < 0 ? "−" : ""}${Math.abs(v) / 1e4}万` : `${v < 0 ? "−" : ""}¥${Math.abs(v) / 1e3}k`;

// Places where earning ¥10,000 more lowers take-home pay by WALL.minDrop or more, and where it gets back.
// Income 0 is skipped: a full-time employee with almost no pay still owes the minimum premiums, which is not a real case.
function bigWalls(pts) {
  const out = [];
  let small = 0;
  pts.forEach((p, i) => {
    const n = pts[i + 1];
    if (!n || p[0] === 0 || n[1] >= p[1]) return;
    if (p[1] - n[1] < WALL.minDrop) { small++; return; }
    const back = pts.find(q => q[0] > p[0] && q[1] >= p[1]);
    out.push({ from: p[0], at: n[0], drop: p[1] - n[1], back: back ? back[0] : null });
  });
  return { walls: out, small };
}

// Short money labels for chart axes: 300万 / ¥3m
// rounded, for labels: 120万円 / ¥1.2m
const axisMoney = x => lang === "ja" ? `${(x / 1e4).toLocaleString("ja-JP")}万` : `¥${+(x / 1e6).toFixed(2)}m`;

// Two linked wall charts with zoom. ids: { panel, disp, rate, ranges, nav }.
// Zoom: drag across a chart (mouse), pinch with two fingers (touch), drag or resize the frame in the overview strip,
// arrow keys and +/− on the frame, or the range buttons. Double-click a chart to go back to the starting view.
// Both charts always show the same incomes, and the vertical axis fits what is shown.
function wallCharts(ids) {
  const MAX = 1e7, MIN_SPAN = 200000, SNAP = 10000;
  let view = null, home = null, last = null, frame = 0;
  const panel = document.getElementById(ids.panel);
  const make = (id, yTicks, pointLegend) => new Chart(document.getElementById(id), { type: "line", data: { datasets: [] },
    options: { animation: false, maintainAspectRatio: false, parsing: false,
      interaction: { mode: "nearest", axis: "x", intersect: false },
      plugins: { legend: { labels: pointLegend ? { usePointStyle: true, pointStyleWidth: 18, boxHeight: 8 } : { boxWidth: 18, boxHeight: 2 } } },  // lines show as lines
      scales: { x: { type: "linear", ticks: { callback: axisMoney, maxTicksLimit: 7 }, title: { display: true } },
                y: { ticks: { callback: yTicks }, title: { display: true } } } } });
  const disp = make(ids.disp, axisMoney, true), rate = make(ids.rate, keepTick, false);  // rate's ▼ markers are not a legend symbol

  // toolbar: range buttons, what is shown, enlarge
  const bar = document.getElementById(ids.ranges);
  const chips = WALL.ranges.map(r => {
    const b = document.createElement("button"); b.type = "button"; b.dataset.r = r;
    b.onclick = () => setView(0, r);
    bar.append(b); return b;
  });
  const viewing = document.createElement("span"); viewing.className = "viewing"; viewing.setAttribute("aria-live", "polite"); bar.append(viewing);
  // zoom buttons for one-pointer and keyboard use (A17): − widens, ＋ narrows around the middle of the view
  const zoom = f => { const span = view.max - view.min, mid = (view.min + view.max) / 2; setView(mid - span * f / 2, mid + span * f / 2); };
  const zoomOut = document.createElement("button"), zoomIn = document.createElement("button");
  zoomOut.type = zoomIn.type = "button"; zoomOut.textContent = "−"; zoomIn.textContent = "＋";
  zoomOut.onclick = () => zoom(2); zoomIn.onclick = () => zoom(.5);
  bar.append(zoomOut, zoomIn);
  const big = document.createElement("button"); big.type = "button"; big.className = "btn enlarge";
  big.onclick = () => toggleBig(); bar.parentElement.append(big);
  function toggleBig(force) {
    panel.classList.toggle("big", force);
    const on = panel.classList.contains("big");
    document.body.style.overflow = on ? "hidden" : "";
    if (on) { panel.setAttribute("role", "dialog"); panel.setAttribute("aria-modal", "true"); } else { panel.removeAttribute("role"); panel.removeAttribute("aria-modal"); }
    for (let n = panel; n !== document.body; n = n.parentElement)  // everything outside the panel is inert while it fills the screen
      for (const sib of n.parentElement.children) if (sib !== n) sib.inert = on;
    big.setAttribute("aria-expanded", on);
    label(); requestAnimationFrame(() => { disp.resize(); rate.resize(); nav.resize(); placeFrame(); });
    big.focus();
  }
  addEventListener("keydown", e => { if (e.key === "Escape" && panel.classList.contains("big")) toggleBig(false); });

  // overview strip: the whole 0–10m line with a frame for what is shown
  const navBox = document.getElementById(ids.nav);
  navBox.innerHTML = `<canvas></canvas><div class="nav-window" tabindex="0" role="group"><span class="grip l"></span><span class="grip r"></span></div>`;
  const nav = new Chart(navBox.querySelector("canvas"), { type: "line", data: { datasets: [] },
    options: { animation: false, maintainAspectRatio: false, parsing: false, events: [], onResize: () => requestAnimationFrame(placeFrame),
      plugins: { legend: { display: false }, tooltip: { enabled: false } }, layout: { padding: { left: 8, right: 8 } },
      scales: { x: { type: "linear", min: 0, max: MAX, ticks: { callback: axisMoney, maxTicksLimit: 6, font: { size: 11 } }, grid: { display: false } },
                y: { display: false } } } });
  const win = navBox.querySelector(".nav-window");
  function placeFrame() {
    if (!view || !nav.chartArea) return;
    const s = nav.scales.x, a = s.getPixelForValue(view.min), b = s.getPixelForValue(view.max);
    Object.assign(win.style, { left: a + "px", width: Math.max(8, b - a) + "px", top: nav.chartArea.top + "px", height: (nav.chartArea.bottom - nav.chartArea.top) + "px" });
  }
  const navValue = x => nav.scales.x.getValueForPixel(x - navBox.getBoundingClientRect().left);
  navBox.addEventListener("pointerdown", e => {
    const part = e.target.closest(".grip")?.classList.contains("l") ? "l" : e.target.closest(".grip") ? "r" : e.target.closest(".nav-window") ? "move" : "jump";
    const v0 = navValue(e.clientX);
    if (part === "jump") { const span = view.max - view.min; setView(v0 - span / 2, v0 + span / 2, true); }
    const start = { v0, min: view.min, max: view.max };
    navBox.setPointerCapture(e.pointerId);
    const move = ev => {
      const d = navValue(ev.clientX) - start.v0;
      if (part === "l") setView(Math.min(start.min + d, start.max - MIN_SPAN), start.max);
      else if (part === "r") setView(start.min, Math.max(start.max + d, start.min + MIN_SPAN));
      else setView(start.min + d, start.max + d, true);
    };
    const up = () => { navBox.removeEventListener("pointermove", move); navBox.removeEventListener("pointerup", up); navBox.removeEventListener("pointercancel", up); };
    navBox.addEventListener("pointermove", move); navBox.addEventListener("pointerup", up); navBox.addEventListener("pointercancel", up);
    e.preventDefault();
  });
  win.addEventListener("keydown", e => {
    const span = view.max - view.min, mid = (view.min + view.max) / 2;
    const act = { ArrowLeft: () => setView(view.min - span / 10, view.max - span / 10, true), ArrowRight: () => setView(view.min + span / 10, view.max + span / 10, true),
      "+": () => setView(mid - span * .4, mid + span * .4), "=": () => setView(mid - span * .4, mid + span * .4),
      "-": () => setView(mid - span * .625, mid + span * .625), Home: () => setView(home.min, home.max) }[e.key];
    if (act) { act(); e.preventDefault(); }
  });

  // zoom on the charts themselves: drag with a mouse, pinch with two fingers, double-click to go back
  for (const ch of [disp, rate]) {
    const c = ch.canvas, sel = document.createElement("div"); sel.className = "zoom-sel"; c.parentElement.append(sel);
    const valueAt = x => ch.scales.x.getValueForPixel(x - c.getBoundingClientRect().left);
    const touches = new Map(); let drag = null, pinch = null;
    c.addEventListener("pointerdown", e => {
      if (e.pointerType === "mouse") { if (e.button === 0) { drag = e.clientX; c.setPointerCapture(e.pointerId); } return; }
      touches.set(e.pointerId, e.clientX);
      if (touches.size === 2) { const [a, b] = touches.values(); pinch = { d0: Math.abs(a - b), at: valueAt((a + b) / 2), min: view.min, max: view.max }; }
    });
    c.addEventListener("pointermove", e => {
      if (drag !== null) {
        const r = c.getBoundingClientRect(), area = ch.chartArea, clamp = x => Math.max(area.left, Math.min(area.right, x - r.left));
        const a = clamp(drag), b = clamp(e.clientX);
        Object.assign(sel.style, { display: Math.abs(b - a) > 4 ? "block" : "none", left: Math.min(a, b) + "px", width: Math.abs(b - a) + "px", top: area.top + "px", height: (area.bottom - area.top) + "px" });
      } else if (touches.has(e.pointerId)) {
        touches.set(e.pointerId, e.clientX);
        if (pinch && touches.size === 2) {
          const [a, b] = touches.values(), span = (pinch.max - pinch.min) * pinch.d0 / Math.max(24, Math.abs(a - b));
          const f = (pinch.at - pinch.min) / (pinch.max - pinch.min);
          setView(pinch.at - f * span, pinch.at + (1 - f) * span);
        }
      }
    });
    const end = e => {
      if (drag !== null && e.pointerType === "mouse") {
        const a = valueAt(drag), b = valueAt(e.clientX);
        sel.style.display = "none"; drag = null;
        if (Math.abs(b - a) >= 3 * SNAP) setView(Math.min(a, b), Math.max(a, b));
      }
      touches.delete(e.pointerId); if (touches.size < 2) pinch = null;
    };
    c.addEventListener("pointerup", end); c.addEventListener("pointercancel", end);
    c.addEventListener("dblclick", () => setView(home.min, home.max));
  }

  // keep the view inside 0–10m and at least MIN_SPAN wide; keepSpan: move without resizing
  function setView(min, max, keepSpan) {
    let span = Math.min(MAX, Math.max(MIN_SPAN, max - min));
    if (keepSpan) span = view ? view.max - view.min : span;
    min = Math.max(0, Math.min(MAX - span, min));
    view = { min: Math.round(min / SNAP) * SNAP, max: Math.round((min + span) / SNAP) * SNAP };
    if (!frame) frame = requestAnimationFrame(() => { frame = 0; render(); });
  }

  function label() {
    chips.forEach(b => {
      b.textContent = lang === "ja" ? `0〜${axisMoney(+b.dataset.r)}円` : `¥0–${axisMoney(+b.dataset.r).slice(1)}`;
      b.setAttribute("aria-pressed", !!view && view.min === 0 && view.max === +b.dataset.r);
    });
    if (view) viewing.textContent = lang === "ja" ? `表示中：${axisMoney(view.min)}〜${axisMoney(view.max)}円` : `Showing ${axisMoney(view.min)}–${axisMoney(view.max).slice(1)}`;
    big.textContent = panel.classList.contains("big") ? (lang === "ja" ? "閉じる" : "Close") : (lang === "ja" ? "全画面で見る" : "Full screen");
    panel.setAttribute("aria-label", lang === "ja" ? "年収の壁のグラフ" : "Income wall charts");
    zoomOut.setAttribute("aria-label", lang === "ja" ? "縮小（広い範囲を見る）" : "Zoom out");
    zoomIn.setAttribute("aria-label", lang === "ja" ? "拡大（狭い範囲を見る）" : "Zoom in");
    win.setAttribute("aria-label", lang === "ja" ? "表示する範囲。左右の矢印で移動、＋と−で拡大・縮小" : "Range shown. Arrow keys move it, + and − zoom");
  }

  // series: [{label, color, points}], the first is 2026 rules; ref: the moving member's current income; who: whose income moves
  function draw(o, newHousehold) {
    last = o;
    if (newHousehold || !view) {
      const r = WALL.ranges.find(r => r >= 2 * o.ref) || MAX;
      home = { min: 0, max: r }; view = { ...home };
    }
    nav.data.datasets = [{ data: o.series[0].points.map(p => ({ x: p[0], y: p[1] })), borderColor: "#4E5B70", borderWidth: 1.2, pointRadius: 0 }];
    nav.update();
    render();
  }

  function render() {
    const o = last, { min, max } = view;
    label(); placeFrame();
    const shown = pts => pts.filter(p => p[0] >= min && p[0] <= max);
    const base = new Map(o.series[0].points.map(p => [p[0], p[1]]));
    disp.data.datasets = o.series.map(s => ({ label: s.label, borderColor: s.color, backgroundColor: s.color, pointRadius: 0, pointStyle: "line",
      borderWidth: 2.5, data: shown(s.points).map(p => ({ x: p[0], y: p[1] })) }));
    const at = new Map(o.series[o.marksOn || 0].points.map(p => [p[0], p[1]]));  // marksOn: the series the walls were found in
    const marks = (o.marks || []).filter(w => w.from >= min && w.at <= max);
    if (marks.length) disp.data.datasets.push({ label: lang === "ja" ? "壁（上の一覧）" : "Walls (listed above)", showLine: false, pointRadius: 6,
      pointStyle: "triangle", rotation: 180, borderColor: "#B3261E", backgroundColor: "#B3261E", data: marks.map(w => ({ x: w.at, y: at.get(w.at) })) });
    const here = o.series[0].points.find(p => p[0] >= o.ref);
    if (here && o.ref >= min && o.ref <= max) disp.data.datasets.push({ label: lang === "ja" ? "この世帯の今の収入" : "This household now", showLine: false,
      pointRadius: 6, pointStyle: "circle", borderColor: "#16243A", backgroundColor: "#fff", borderWidth: 2, data: [{ x: o.ref, y: here[1] }] });
    disp.options.plugins.tooltip = { callbacks: {
      title: c => !c.length ? "" : (lang === "ja" ? `${o.who} ${yen(c[0].raw.x)}円` : `${o.who[0].toUpperCase() + o.who.slice(1)}: ¥${yen(c[0].raw.x)}`),
      label: c => `${shortName(c.dataset.label)}: ${lang === "ja" ? yen(c.raw.y) + "円" : "¥" + yen(c.raw.y)}`,
      afterLabel: c => c.datasetIndex > 0 && c.datasetIndex < o.series.length
        ? (lang === "ja" ? "  2026年の制度との差：" : "  vs 2026 rules: ") + (c.raw.y >= base.get(c.raw.x) ? "+" : "−") + yen(Math.abs(c.raw.y - base.get(c.raw.x))) : "" } };
    rate.data.datasets = o.series.map(s => {
      const data = keepSeries(s.points).filter(([x]) => x >= min - WALL.step && x <= max).map(([x, v]) => ({ x, y: Math.max(KEEP_FLOOR, v), raw: v }));
      return { label: s.label, borderColor: s.color, backgroundColor: s.color, borderWidth: 2.5, stepped: "before", data, pointStyle: "triangle",
        rotation: 180, pointRadius: data.map(q => q.raw !== q.y ? 5 : 0) };
    });
    rate.data.datasets.push({ label: lang === "ja" ? "0円（ここより下が壁）" : "¥0 (below this is a wall)", borderColor: "#B3261E",
      borderDash: [6, 4], borderWidth: 1.5, pointRadius: 0, pointStyle: "line", data: [{ x: min, y: 0 }, { x: max, y: 0 }] });
    // the dotted ¥0 line is filtered out, so the tooltip can have no items
    rate.options.plugins.tooltip = { filter: c => c.datasetIndex < o.series.length, callbacks: {
      title: c => !c.length ? "" : lang === "ja" ? [`${o.who}が`, `${yen(c[0].raw.x)}円→${yen(c[0].raw.x + WALL.step)}円に増えると`]
                                : [`If ${o.who} goes`, `from ¥${yen(c[0].raw.x)} to ¥${yen(c[0].raw.x + WALL.step)}`],
      label: c => { const v = c.raw.raw;
        return lang === "ja" ? `${shortName(c.dataset.label)}：手取りは${yen(Math.abs(v))}円${v < 0 ? "減る（壁）" : "増える"}`
                             : `${shortName(c.dataset.label)}: ${v < 0 ? "down" : "up"} ¥${yen(Math.abs(v))}${v < 0 ? " (a wall)" : ""}`; } } };
    rate.options.scales.y.suggestedMax = WALL.step;
    if (ids.table) table(o, min, max);
    for (const [ch, y] of [[disp, lang === "ja" ? "手取り（円／年）" : "Take-home pay (yen per year)"], [rate, lang === "ja" ? "手取りが増える額" : "Extra take-home pay"]]) {
      Object.assign(ch.options.scales.x, { min, max });
      ch.options.scales.x.title.text = o.axis;
      ch.options.scales.y.title.text = y;
      ch.update();
    }
  }
  // the charted numbers as a table, every ¥100,000 of the range shown (for keyboard and screen-reader users)
  function table(o, min, max) {
    const tb = document.getElementById(ids.table), ja = lang === "ja";
    const rows = o.series.map(s => new Map(s.points.map(p => [p[0], p[1]])));
    const head = [incomeHead(o), ...o.series.map((s, i) => i ? `${shortName(s.label)}${ja ? "（2026年の制度との差）" : " (vs 2026 rules)"}` : `${s.label}${ja ? "：手取り" : ": take-home"}`)];
    tb.innerHTML = "";
    const hr = tb.createTHead().insertRow();
    head.forEach(h => { const th = document.createElement("th"); th.textContent = h; hr.append(th); });
    const body = tb.createTBody();
    for (let x = Math.ceil(min / WALL.step) * WALL.step; x <= max; x += WALL.step) {
      const r = body.insertRow(), base = rows[0].get(x);
      r.insertCell().textContent = yen(x);
      rows.forEach((m, i) => { const v = m.get(x); r.insertCell().textContent = i ? `${yen(v)}（${v >= base ? "+" : ""}${yen(v - base)}）` : yen(v); });
    }
  }
  const incomeHead = o => lang === "ja" ? `${o.who}（円）` : `${o.who[0].toUpperCase() + o.who.slice(1)} (yen)`;
  return { draw };
}

// Why take-home falls at one wall, from outputs/wall_map.json wall_causes (2026 rules only):
// "扶養から外れて、国民年金（年215,040円）と国民健康保険（年101,786円）の保険料がかかるためです。税は合わせて年48,600円減ります。"
function wallReason(c) {
  const ja = lang === "ja", m = v => ja ? `年${yen(v)}円` : `¥${yen(v)} a year`;
  const NAMES = { employee_insurance: { ja: "会社の健康保険・厚生年金などの保険料", en: "company health insurance and pension premiums" },
    nhi: { ja: "国民健康保険料", en: "National Health Insurance" }, national_pension: { ja: "国民年金保険料", en: "National Pension" },
    ltc_65: { ja: "65歳以上の介護保険料", en: "long-term care premiums for people aged 65 or over" },
    income_tax: { ja: "所得税", en: "income tax" }, resident_tax: { ja: "住民税", en: "resident tax" } };
  const ch = { ...Object.fromEntries(Object.keys(NAMES).map(k => [k, 0])), ...c.change };  // a part missing from older data counts as 0
  const [before, after] = c.scheme;
  let why;
  if (before !== after && after === "nhi") {
    const paid = ["national_pension", "nhi"].filter(k => ch[k] > 0).map(k => ja ? `${t(NAMES[k])}（${m(ch[k])}）` : `${t(NAMES[k])} (${m(ch[k])})`);
    why = ja ? `${before === "dependant" ? "扶養から外れて、" : ""}${paid.join("と")}がかかるため` : `${before === "dependant" ? "the dependant status ends and " : ""}${paid.join(" and ")} must be paid`;
  } else if (before !== after && after === "employee") {
    why = ja ? `会社の健康保険・厚生年金に入り、保険料（${m(ch.employee_insurance)}）がかかるため` : `company health insurance and pension start (${m(ch.employee_insurance)})`;
  } else {
    // the changes that make the wall: at least ¥1,000 and at least a fifth of the largest (small steady rises are left out)
    const BENEFITS = { child_allowance: { ja: "児童手当", en: "child allowance" }, child_rearing_allowance: { ja: "児童扶養手当", en: "the single-parent allowance (児童扶養手当)" } };
    const fall = k => -(ch[k] || 0);
    const big = Math.max(...Object.keys(NAMES).map(k => ch[k]), ...Object.keys(BENEFITS).map(fall));
    const up = Object.keys(NAMES).filter(k => ch[k] >= Math.max(1000, big / 5)).sort((a, b) => ch[b] - ch[a]);
    up.push(...Object.keys(BENEFITS).filter(k => fall(k) >= Math.max(1000, big / 5)));
    if (!up.length) return "";
    // Japanese: every item but the last ends in 増え/減り, the last in 増える/減る
    const say = (k, last) => k in BENEFITS ? (ja ? `${BENEFITS[k].ja}が${m(fall(k))}${last ? "減る" : "減り"}` : `${BENEFITS[k].en} falls by ${m(fall(k))}`)
      : k === "employee_insurance" && before === "employee" ? (ja ? `会社の保険料が、収入の段階が上がって${m(ch[k])}${last ? "増える" : "増え"}` : `company insurance premiums step up by ${m(ch[k])}`)
      : (ja ? `${t(NAMES[k])}が${m(ch[k])}${last ? "増える" : "増え"}` : `${t(NAMES[k])} goes up by ${m(ch[k])}`);
    why = up.map((k, i) => say(k, i === up.length - 1)).join(ja ? "、" : ", ") + (ja ? "ため" : "");
  }
  const taxCut = -Math.min(0, ch.income_tax) - Math.min(0, ch.resident_tax);
  return ja ? `${why}です。` + (taxCut >= 1000 ? `税は合わせて${m(taxCut)}減ります。` : "")
            : `Why: ${why}.` + (taxCut >= 1000 ? ` Taxes fall by ${m(taxCut)} in all.` : "");
}

// Plain-words list of the biggest walls for one series (at most `top`), into a <ul>; the rest are counted.
// causes: wall_causes for the 2026 series (omitted for other series)
function listWalls(ul, pts, who, top = 3, causes = []) {
  ul.innerHTML = "";
  const { walls, small } = bigWalls(pts);
  const shown = [...walls].sort((a, b) => b.drop - a.drop).slice(0, top), more = walls.length - shown.length;
  for (const w of shown) {
    const c = causes.find(x => x.from === w.from);
    const why = c ? (lang === "ja" ? "" : " ") + wallReason(c) : "";
    li(ul, lang === "ja"
      ? `${who}が${yen(w.from)}円から${yen(w.at)}円に増えると、世帯の手取りは年${yen(w.drop)}円減ります。${why}` + (w.back ? `元の手取りに戻るのは${yen(w.back)}円のときです（1万円きざみで計算）。` : "")
      : `If ${who} goes from ¥${yen(w.from)} to ¥${yen(w.at)}, the household takes home ¥${yen(w.drop)} less a year.${why}` + (w.back ? ` Take-home gets back to where it was at ¥${yen(w.back)} (worked out in ¥10,000 steps).` : ""));
  }
  if (!walls.length) li(ul, lang === "ja" ? "1万円多く稼いで手取りが1万円以上減るところはありません。" : "There is no point where earning ¥10,000 more cuts take-home pay by ¥10,000 or more.");
  if (more) li(ul, lang === "ja" ? `ほかに、手取りが1万円以上減るところが${more}か所あります。グラフで確かめられます。`
                                 : `There ${more === 1 ? "is 1 more place" : `are ${more} more places`} where take-home pay falls by ¥10,000 or more. You can see them in the charts.`);
  if (small) li(ul, lang === "ja" ? `ほかに、手取りが1万円未満だけ減るところが${small}か所あります（税の控除や保険料が、収入の段階ごとに変わるため）。`
                                  : `There are also ${small} places where take-home pay falls by less than ¥10,000 (deductions and premiums change in steps as income rises).`);
  return shown;
}

if (typeof module !== "undefined") module.exports = { keepSeries, bigWalls, wallReason };
