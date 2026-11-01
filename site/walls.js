// Wall charts shared by Home and Build your own: take-home pay, and how much of an extra ¥100,000 you keep.
// Data: points [[income, take-home, ...], ...] at 10,000-yen steps from outputs/wall_map.json.
const WALL = { step: 100000, ranges: [3e6, 6e6, 1e7], minDrop: 10000 };

// How much more take-home pay (yen) an extra ¥100,000 of income brings; below 0 is a wall.
// 100,000 rather than 10,000 so rounding of tax to 100 yen does not show as noise.
function keepSeries(pts) {
  const at = new Map(pts.map(p => [p[0], p[1]]));
  return pts.filter(p => p[0] % WALL.step === 0 && at.has(p[0] + WALL.step)).map(p => [p[0], at.get(p[0] + WALL.step) - p[1]]);
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
const roundMoney = x => lang === "ja" ? `${Math.round(x / 1e4).toLocaleString("ja-JP")}万円` : `¥${(x / 1e6).toFixed(1)}m`;
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
      plugins: { legend: { labels: { boxWidth: 14, usePointStyle: pointLegend } } },
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
  const big = document.createElement("button"); big.type = "button"; big.className = "btn enlarge";
  big.onclick = () => toggleBig(); bar.parentElement.append(big);
  function toggleBig(force) {
    panel.classList.toggle("big", force);
    document.body.style.overflow = panel.classList.contains("big") ? "hidden" : "";
    label(); requestAnimationFrame(() => { disp.resize(); rate.resize(); nav.resize(); placeFrame(); });
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
    win.setAttribute("aria-label", lang === "ja" ? "表示する範囲。左右の矢印で移動、＋と−で拡大・縮小" : "Range shown. Arrow keys move it, + and − zoom");
  }

  // series: [{label, color, points}], the first is 2026 rules; ref: the moving member's current income; who: whose income moves
  function draw(o, newHousehold) {
    last = o;
    if (newHousehold || !view) {
      const r = WALL.ranges.find(r => r >= 2 * o.ref) || MAX;
      home = { min: 0, max: r }; view = { ...home };
    }
    nav.data.datasets = [{ data: o.series[0].points.map(p => ({ x: p[0], y: p[1] })), borderColor: "#5A6676", borderWidth: 1.5, pointRadius: 0 }];
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
    const here = o.series[0].points.find(p => p[0] >= o.ref);
    if (here && o.ref >= min && o.ref <= max) disp.data.datasets.push({ label: lang === "ja" ? "この世帯の今の収入" : "This household now", showLine: false,
      pointRadius: 6, pointStyle: "circle", borderColor: "#1C2633", backgroundColor: "#fff", borderWidth: 2, data: [{ x: o.ref, y: here[1] }] });
    disp.options.plugins.tooltip = { callbacks: {
      title: c => !c.length ? "" : (lang === "ja" ? `${o.who} ` : `${o.who[0].toUpperCase() + o.who.slice(1)} `) + `${yen(c[0].raw.x)}${lang === "ja" ? "円" : " yen"}`,
      label: c => `${c.dataset.label}: ${yen(c.raw.y)}${lang === "ja" ? "円" : " yen"}`,
      afterLabel: c => c.datasetIndex > 0 && c.datasetIndex < o.series.length
        ? (lang === "ja" ? "  2026年の制度との差：" : "  Difference from 2026 rules: ") + (c.raw.y >= base.get(c.raw.x) ? "+" : "") + yen(c.raw.y - base.get(c.raw.x)) : "" } };
    rate.data.datasets = o.series.map(s => {
      const data = keepSeries(s.points).filter(([x]) => x >= min - WALL.step && x <= max).map(([x, v]) => ({ x, y: Math.max(KEEP_FLOOR, v), raw: v }));
      return { label: s.label, borderColor: s.color, backgroundColor: s.color, borderWidth: 2.5, stepped: "before", data, pointStyle: "triangle",
        rotation: 180, pointRadius: data.map(q => q.raw !== q.y ? 5 : 0) };
    });
    rate.data.datasets.push({ label: lang === "ja" ? "0円（ここより下が壁）" : "¥0 (below this is a wall)", borderColor: "#C23B22",
      borderDash: [6, 4], borderWidth: 1.5, pointRadius: 0, pointStyle: "line", data: [{ x: min, y: 0 }, { x: max, y: 0 }] });
    // the dotted ¥0 line is filtered out, so the tooltip can have no items
    rate.options.plugins.tooltip = { filter: c => c.datasetIndex < o.series.length, callbacks: {
      title: c => !c.length ? "" : lang === "ja" ? `${o.who}が${yen(c[0].raw.x)}円から${yen(c[0].raw.x + WALL.step)}円に増えると`
                                : `If ${o.who} goes from ¥${yen(c[0].raw.x)} to ¥${yen(c[0].raw.x + WALL.step)}`,
      label: c => { const v = c.raw.raw;
        return lang === "ja" ? `${c.dataset.label}：手取りは${yen(Math.abs(v))}円${v < 0 ? "減る（壁）" : "増える"}`
                             : `${c.dataset.label}: take-home pay goes ${v < 0 ? "down" : "up"} by ¥${yen(Math.abs(v))}${v < 0 ? " (a wall)" : ""}`; } } };
    rate.options.scales.y.suggestedMax = WALL.step;
    for (const [ch, y] of [[disp, lang === "ja" ? "手取り（円／年）" : "Take-home pay (yen per year)"], [rate, lang === "ja" ? "手取りが増える額" : "Extra take-home pay"]]) {
      Object.assign(ch.options.scales.x, { min, max });
      ch.options.scales.x.title.text = o.axis;
      ch.options.scales.y.title.text = y;
      ch.update();
    }
  }
  return { draw };
}

// Plain-words list of the biggest walls for one series (at most `top`), into a <ul>; the rest are counted
function listWalls(ul, pts, who, top = 3) {
  ul.innerHTML = "";
  const { walls, small } = bigWalls(pts);
  const shown = [...walls].sort((a, b) => b.drop - a.drop).slice(0, top), rest = walls.length - shown.length + small;
  for (const w of shown) li(ul, lang === "ja"
    ? `${who}が${yen(w.from)}円から${yen(w.at)}円に増えると、世帯の手取りは年${yen(w.drop)}円減ります。` + (w.back ? `元の手取りに戻るのは${yen(w.back)}円のときです。` : "")
    : `If ${who} goes from ¥${yen(w.from)} to ¥${yen(w.at)}, the household takes home ¥${yen(w.drop)} less a year.` + (w.back ? ` Take-home gets back to where it was at ¥${yen(w.back)}.` : ""));
  if (!walls.length) li(ul, lang === "ja" ? "1万円多く稼いで手取りが1万円以上減るところはありません。" : "There is no point where earning ¥10,000 more cuts take-home pay by ¥10,000 or more.");
  if (rest) li(ul, lang === "ja" ? `ほかに、手取りが少し減るところが${rest}か所あります（多くは、会社の保険料が収入の段階ごとに上がるため）。グラフで確かめられます。`
                                 : `There are also ${rest} smaller dips, mostly because company insurance premiums go up in steps as pay rises. You can see them in the charts.`);
}

if (typeof module !== "undefined") module.exports = { keepSeries, bigWalls };
