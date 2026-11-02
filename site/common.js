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
let lang = "ja";
try { lang = localStorage.getItem("tedori-lang") === "en" ? "en" : "ja"; } catch (e) { /* storage blocked: stay Japanese */ }

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
const li = (ul, text) => { const x = document.createElement("li"); x.textContent = text; ul.append(x); };

function applyLang() {
  document.documentElement.lang = lang;
  document.documentElement.dataset.lang = lang;
  const b = document.getElementById("lang-toggle");
  if (b) b.textContent = lang === "ja" ? "English" : "日本語";
  document.querySelectorAll("header nav a").forEach((a, i) => a.textContent = t(PAGES[i][1]));
  document.querySelectorAll("footer nav a").forEach((a, i) => a.textContent = t(ABOUT[i][1]));
}

// onLangChange: pages with charts or generated text redraw themselves
function setupPage(onLangChange = () => {}) {
  const here = location.pathname.split("/").pop() || "index.html";
  const header = document.createElement("header");
  header.innerHTML = `<a class="brand" href="index.html">手取りラボ<small>Tedori Lab</small></a><nav aria-label="Main pages"></nav>
    <button id="lang-toggle" type="button" aria-label="Switch language / 言語を切り替え"></button>`;
  const links = (nav, pages) => pages.forEach(([href]) => {
    const a = document.createElement("a"); a.href = href;
    if (href === here) a.setAttribute("aria-current", "page");
    nav.append(a);
  });
  links(header.querySelector("nav"), PAGES);
  document.body.prepend(header);
  const footer = document.createElement("footer");
  footer.innerHTML = `<nav aria-label="About this site"></nav><span lang="ja">数字はすべて試算です。制度が変わっても、人々の働き方は変わらないものとして計算しています。このサイトは特定の案・政党・政治家を支持するものではありません。</span>
    <span lang="en">All numbers are estimates. They assume people don't change how much they work when the rules change. This site doesn't support any plan, party or politician.</span>`;
  links(footer.querySelector("nav"), ABOUT);
  document.body.append(footer);
  if (window.Chart) {  // charts use the page's font and colours
    Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
    Chart.defaults.font.size = 13;
    Chart.defaults.color = "#5A6676";
    Chart.defaults.borderColor = "#E3E9EF";
  }
  header.querySelector("#lang-toggle").onclick = () => {
    lang = lang === "ja" ? "en" : "ja";
    try { localStorage.setItem("tedori-lang", lang); } catch (e) { /* not saved; fine */ }
    applyLang(); onLangChange();
  };
  applyLang();
}

// Document pages render the project's own Markdown files, so the site and the docs never drift apart.
function renderDoc(el, urls) {
  const url = typeof urls === "string" ? urls : t(urls);
  fetch(url, { cache: "no-cache" }).then(r => r.text()).then(md => { el.innerHTML = marked.parse(md); });
}
