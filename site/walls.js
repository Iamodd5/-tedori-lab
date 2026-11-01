// Wall charts shared by Home and Build your own: take-home pay, and the share of the next ¥100,000 that is lost.
// Data: points [[income, take-home, ...], ...] at 10,000-yen steps from outputs/wall_map.json.
const WALL = { step: 100000, ranges: [3e6, 6e6, 1e7], minDrop: 10000 };

// Share (%) of the next ¥100,000 lost. 100,000 rather than 10,000 so rounding of tax to 100 yen does not show as noise.
function rateSeries(pts) {
  const at = new Map(pts.map(p => [p[0], p[1]]));
  return pts.filter(p => p[0] % WALL.step === 0 && at.has(p[0] + WALL.step))
    .map(p => [p[0], Math.round((1 - (at.get(p[0] + WALL.step) - p[1]) / WALL.step) * 1000) / 10]);
}

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

function wallCharts(ids) {
  let range = null, last = null;
  const make = (id, yTicks) => new Chart(document.getElementById(id), { type: "line", data: { datasets: [] },
    options: { animation: false, maintainAspectRatio: false, parsing: false,
      interaction: { mode: "nearest", axis: "x", intersect: false },
      plugins: { legend: { labels: { boxWidth: 14 } } },
      scales: { x: { type: "linear", ticks: { callback: axisMoney, maxTicksLimit: 8 }, title: { display: true } },
                y: { ticks: { callback: yTicks }, title: { display: true } } } } });
  const disp = make(ids.disp, axisMoney), rate = make(ids.rate, v => v + "%");

  // range buttons and enlarge buttons
  const box = document.getElementById(ids.ranges);
  for (const r of WALL.ranges) {
    const b = document.createElement("button"); b.type = "button"; b.dataset.r = r;
    b.onclick = () => { range = r; draw(last); };
    box.append(b);
  }
  for (const ch of [disp, rate]) {
    const wrap = ch.canvas.parentElement, b = document.createElement("button");
    b.type = "button"; b.className = "enlarge";
    b.onclick = () => { wrap.classList.toggle("big"); label(); ch.resize(); };
    wrap.prepend(b);
  }
  addEventListener("keydown", e => {
    if (e.key === "Escape") document.querySelectorAll(".chart.big").forEach(w => { w.classList.remove("big"); label(); disp.resize(); rate.resize(); });
  });
  function label() {
    box.querySelectorAll("button").forEach(b => {
      b.textContent = lang === "ja" ? `0〜${axisMoney(+b.dataset.r)}円` : `¥0–${axisMoney(+b.dataset.r).slice(1)}`;
      b.setAttribute("aria-pressed", +b.dataset.r === range);
    });
    document.querySelectorAll(".chart .enlarge").forEach(b => {
      b.textContent = b.parentElement.classList.contains("big") ? (lang === "ja" ? "閉じる" : "Close") : (lang === "ja" ? "拡大する" : "Enlarge");
    });
  }

  // series: [{label, color, points}], the first is 2026 rules; ref: the moving member's current income
  function draw(o, newHousehold) {
    last = o;
    if (newHousehold || range === null) range = WALL.ranges.find(r => r >= 2 * o.ref) || WALL.ranges.at(-1);
    label();
    const inRange = pts => pts.filter(p => p[0] <= range);
    const base = new Map(o.series[0].points.map(p => [p[0], p[1]]));
    disp.data.datasets = o.series.map(s => ({ label: s.label, borderColor: s.color, backgroundColor: s.color, pointRadius: 0,
      borderWidth: 2, data: inRange(s.points).map(p => ({ x: p[0], y: p[1] })) }));
    const here = o.series[0].points.find(p => p[0] >= o.ref);
    if (here && o.ref <= range) disp.data.datasets.push({ label: lang === "ja" ? "この世帯の今の収入" : "This household now", showLine: false,
      pointRadius: 6, pointStyle: "circle", borderColor: "#000", backgroundColor: "#fff", borderWidth: 2, data: [{ x: o.ref, y: here[1] }] });
    disp.options.plugins.tooltip = { callbacks: {
      title: c => (lang === "ja" ? "収入 " : "Income ") + `${yen(c[0].raw.x)}${lang === "ja" ? "円" : " yen"}`,
      label: c => `${c.dataset.label}: ${yen(c.raw.y)}${lang === "ja" ? "円" : " yen"}`,
      afterLabel: c => c.datasetIndex > 0 && c.datasetIndex < o.series.length
        ? (lang === "ja" ? "  2026年の制度との差：" : "  Difference from 2026 rules: ") + (c.raw.y >= base.get(c.raw.x) ? "+" : "") + yen(c.raw.y - base.get(c.raw.x)) : "" } };
    rate.data.datasets = o.series.map(s => {
      const data = rateSeries(inRange(s.points)).map(([x, v]) => ({ x, y: Math.max(-50, Math.min(300, v)), raw: v }));
      return { label: s.label, borderColor: s.color, backgroundColor: s.color, borderWidth: 2, stepped: "before", data,
        pointStyle: "triangle", pointRadius: data.map(q => q.raw !== q.y ? 5 : 0) };
    });
    rate.data.datasets.push({ label: lang === "ja" ? "100%（ここより上が壁）" : "100% (above this is a wall)", borderColor: "#888",
      borderDash: [6, 4], borderWidth: 1, pointRadius: 0, data: [{ x: 0, y: 100 }, { x: range, y: 100 }] });
    rate.options.plugins.tooltip = { filter: c => c.datasetIndex < o.series.length, callbacks: {
      title: c => lang === "ja" ? `${yen(c[0].raw.x)}円から${yen(c[0].raw.x + WALL.step)}円に増えると` : `Earning ${yen(c[0].raw.x + WALL.step)} instead of ${yen(c[0].raw.x)} yen`,
      label: c => lang === "ja" ? `${c.dataset.label}：増えた10万円のうち${c.raw.raw}%を失う` : `${c.dataset.label}: lose ${c.raw.raw}% of the extra ¥100,000` } };
    for (const [ch, y] of [[disp, lang === "ja" ? "手取り（円／年）" : "Take-home pay (yen per year)"], [rate, lang === "ja" ? "失う割合" : "Share lost"]]) {
      ch.options.scales.x.title.text = o.axis;
      ch.options.scales.x.max = range;
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

if (typeof module !== "undefined") module.exports = { rateSeries, bigWalls };
