// Shared by every page: language (Japanese default, English toggle), header, footer, helpers.
// the five main pages go in the header; the pages about the site go in the footer
const PAGES = [
  ["index.html", { ja: "ホーム", en: "Home" }],
  ["compare.html", { ja: "案の比較", en: "Compare plans" }],
  ["population.html", { ja: "全世帯で見ると", en: "All households" }],
  ["builder.html", { ja: "自分で案を作る", en: "Build your own" }],
  ["report.html", { ja: "レポート", en: "Report" }],
];
const ABOUT = [
  ["methods.html", { ja: "計算方法", en: "How it works" }],
  ["validation.html", { ja: "検証", en: "Checks" }],
  ["sources.html", { ja: "出典とコード", en: "Sources & code" }],
  ["corrections.html", { ja: "訂正の記録", en: "Corrections" }],
];
// Japanese unless the visitor chose English, or (first visit) their browser isn't set to Japanese
let lang = /^ja\b/i.test(navigator.language || "ja") ? "ja" : "en";
try { const saved = localStorage.getItem("tedori-lang"); if (saved) lang = saved === "en" ? "en" : "ja"; } catch (e) { /* storage blocked: use the browser's language */ }

const t = o => (o && (o[lang] ?? o.ja)) ?? "";
const yen = n => n == null ? "—" : Math.round(n).toLocaleString("ja-JP");
const loadJSON = u => fetch(u, { cache: "no-cache" }).then(r => r.json());
// joins several reasons in the page language
const joinT = list => list.map(t).join(lang === "ja" ? "。" : "; ");
const FIELDS = { salary: { ja: "給与", en: "salary" }, business_income: { ja: "事業の収入", en: "business income" }, public_pension: { ja: "年金", en: "pension" } };
// whose income moves on a wall map (wall_map.json households entry): "配偶者の給与" / "the spouse's salary"
function whoMoves(h) {
  const who = !h.couple ? null : h.member_role === "spouse" ? { ja: "配偶者の", en: "the spouse's " } : { ja: "世帯主の", en: "the household head's " };
  return lang === "ja" ? (who ? who.ja : "") + FIELDS[h.income_field].ja : (who ? who.en : "the ") + FIELDS[h.income_field].en;
}
function incomeAxis(h) {
  const w = whoMoves(h).replace(/^the /, "");
  return lang === "ja" ? `${w}（税引き前、円）` : `${w[0].toUpperCase() + w.slice(1)} before tax (yen)`;
}
// "世帯主（45歳）：給与5,000,000円 ／ 子ども（10歳）"
function describeIncomes(incomes) {
  const R = { head: { ja: incomes.length > 1 ? "世帯主" : "本人", en: incomes.length > 1 ? "Head" : "The person" }, spouse: { ja: "配偶者", en: "Spouse" },
              child: { ja: "子ども", en: "Child" }, dependant: { ja: "親族", en: "Relative" } };
  return incomes.map(m => {
    const money = Object.keys(FIELDS).filter(k => m[k]).map(k => lang === "ja" ? `${FIELDS[k].ja}${yen(m[k])}円` : `${FIELDS[k].en} ¥${yen(m[k])}`);
    const who = lang === "ja" ? `${t(R[m.role])}（${m.age}歳）` : `${t(R[m.role])} (${m.age})`;
    return money.length ? `${who}${lang === "ja" ? "：" : ": "}${money.join(lang === "ja" ? "、" : ", ")}` : who;
  }).join(lang === "ja" ? " ／ " : " / ");
}
// a plan's name without its bracket, where space is short (tooltips, table rows): 大和総研案（2026年の…） → 大和総研案
const shortName = s => s.replace(/\s*[（(].*$/, "");
const li = (ul, text) => { const x = document.createElement("li"); x.textContent = text; ul.append(x); };

// The household chosen on another page (?hh=H3, or the last one chosen) stays chosen, if it is one of `ids`.
function keptHousehold(ids, fallback) {
  let keep = new URLSearchParams(location.search).get("hh");
  try { keep = keep || localStorage.getItem("tedori-hh"); } catch (e) { /* storage blocked */ }
  if (!ids.includes(keep)) return fallback;
  try { localStorage.setItem("tedori-hh", keep); } catch (e) { /* not kept; fine */ }
  return keep;
}

function applyLang() {
  document.documentElement.lang = lang;
  document.documentElement.dataset.lang = lang;
  const b = document.getElementById("lang-toggle");
  if (b) { b.textContent = lang === "ja" ? "English" : "日本語"; b.lang = lang === "ja" ? "en" : "ja"; }
  const skip = document.querySelector(".skip");
  if (skip) skip.textContent = lang === "ja" ? "本文へ移動" : "Skip to content";
  document.querySelector("header nav")?.setAttribute("aria-label", lang === "ja" ? "主なページ" : "Main pages");
  document.querySelector("footer nav")?.setAttribute("aria-label", lang === "ja" ? "このサイトについて" : "About this site");
  document.querySelectorAll("header nav a").forEach((a, i) => a.textContent = t(PAGES[i][1]));
  document.querySelectorAll("footer nav a").forEach((a, i) => a.textContent = t(ABOUT[i][1]));
}

// onLangChange: pages with charts or generated text redraw themselves
function setupPage(onLangChange = () => {}) {
  const here = location.pathname.split("/").pop() || "index.html";
  // the page's own content goes in <main>, with a link to skip the header
  const main = document.createElement("main"); main.id = "main"; main.tabIndex = -1;
  main.append(...document.body.childNodes); document.body.append(main);
  const header = document.createElement("header");
  header.innerHTML = `<a class="brand" href="index.html">手取りラボ<small lang="en">Tedori Lab</small></a><nav></nav>
    <button id="lang-toggle" type="button"></button>`;
  const links = (nav, pages) => pages.forEach(([href]) => {
    const a = document.createElement("a"); a.href = href;
    if (href === here) a.setAttribute("aria-current", "page");
    nav.append(a);
  });
  links(header.querySelector("nav"), PAGES);
  document.body.prepend(header);
  const skip = document.createElement("a"); skip.className = "skip"; skip.href = "#main"; document.body.prepend(skip);
  const footer = document.createElement("footer");
  footer.innerHTML = `<nav></nav><span lang="ja">数字はすべて試算です。制度が変わっても、人々の働き方は変わらないものとして計算しています。このサイトは特定の案・政党・政治家を支持するものではありません。個人がAIアシスタント（Claude）を使って作っています。</span>
    <span lang="en">Tedori (手取り) means take-home pay. All numbers are estimates. They assume people don't change how much they work when the rules change. This site doesn't support any plan, party or politician. Made by an individual with an AI assistant (Claude).</span>`;
  links(footer.querySelector("nav"), ABOUT);
  document.body.append(footer);
  if (window.Chart) {  // charts use the page's font and colours
    const d = Chart.defaults, ink = "#1D2430";
    d.font.family = getComputedStyle(document.body).fontFamily;
    d.font.size = 12;
    d.color = "#4A5463";
    d.borderColor = "#EEF1F4";
    d.scale.border = { color: "#D9DEE5" };
    d.plugins.legend.align = "start";
    d.datasets.bar.maxBarThickness = 40;
    Object.assign(d.plugins.legend.labels, { boxWidth: 12, boxHeight: 12, padding: 14 });
    Object.assign(d.plugins.tooltip, { backgroundColor: "#fff", titleColor: ink, bodyColor: ink, borderColor: "#D9DEE5", borderWidth: 1,
                                       cornerRadius: 2, padding: 10, titleFont: { weight: "bold" }, boxPadding: 4 });
  }
  header.querySelector("#lang-toggle").onclick = () => {
    lang = lang === "ja" ? "en" : "ja";
    try { localStorage.setItem("tedori-lang", lang); } catch (e) { /* not saved; fine */ }
    applyLang(); onLangChange();
  };
  applyLang();
}

// Document pages render the project's own Markdown files, so the site and the docs never drift apart.
// English-only documents are marked lang="en"; headings move down a level under the page's own h1;
// question numbers such as (Q13) link to the list of open questions.
const QUESTIONS = "https://github.com/Iamodd5/-tedori-lab/blob/main/OPEN_QUESTIONS.md";
function renderDoc(el, urls) {
  const url = typeof urls === "string" ? urls : t(urls);
  el.lang = typeof urls === "string" ? "en" : lang;
  fetch(url, { cache: "no-cache" }).then(r => r.text()).then(md => {
    el.innerHTML = marked.parse(md.replace(/\bQ(\d{1,2})\b(?![^\[]*\])/g, `[Q$1](${QUESTIONS})`));
    const ownH1 = document.querySelectorAll("h1").length > el.querySelectorAll("h1").length;  // the report page has none
    if (ownH1) [...el.querySelectorAll("h1, h2, h3, h4, h5")].forEach(h => {
      const n = document.createElement("h" + (+h.tagName[1] + 1)); n.innerHTML = h.innerHTML; h.replaceWith(n);
    });
  });
}
