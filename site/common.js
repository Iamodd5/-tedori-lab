// Shared by every page: language (Japanese default, English toggle), header, footer, helpers.
const PAGES = [
  ["index.html", { ja: "ホーム", en: "Home" }],
  ["compare.html", { ja: "案の比較", en: "Compare plans" }],
  ["population.html", { ja: "全世帯で見ると", en: "All households" }],
  ["methods.html", { ja: "計算方法", en: "How it works" }],
  ["validation.html", { ja: "検証", en: "Checks" }],
  ["sources.html", { ja: "出典とコード", en: "Sources & code" }],
];
let lang = "ja";
try { lang = localStorage.getItem("tedori-lang") === "en" ? "en" : "ja"; } catch (e) { /* storage blocked: stay Japanese */ }

const t = o => (o && (o[lang] ?? o.ja)) ?? "";
const yen = n => n == null ? "—" : Math.round(n).toLocaleString("ja-JP");
const loadJSON = u => fetch(u, { cache: "no-cache" }).then(r => r.json());
// joins several reasons in the page language
const joinT = list => list.map(t).join(lang === "ja" ? "。" : "; ");
const li = (ul, text) => { const x = document.createElement("li"); x.textContent = text; ul.append(x); };

function applyLang() {
  document.documentElement.lang = lang;
  document.documentElement.dataset.lang = lang;
  const b = document.getElementById("lang-toggle");
  if (b) b.textContent = lang === "ja" ? "English" : "日本語";
  document.querySelectorAll("header nav a").forEach((a, i) => a.textContent = t(PAGES[i][1]));
}

// onLangChange: pages with charts or generated text redraw themselves
function setupPage(onLangChange = () => {}) {
  const here = location.pathname.split("/").pop() || "index.html";
  const header = document.createElement("header");
  header.innerHTML = `<a class="brand" href="index.html">手取りラボ / Tedori Lab</a><nav aria-label="Pages"></nav>
    <button id="lang-toggle" type="button" aria-label="Switch language / 言語を切り替え"></button>`;
  for (const [href] of PAGES) {
    const a = document.createElement("a"); a.href = href;
    if (href === here) a.setAttribute("aria-current", "page");
    header.querySelector("nav").append(a);
  }
  document.body.prepend(header);
  const footer = document.createElement("footer");
  footer.innerHTML = `<span lang="ja">数字はすべて試算です。制度が変わっても、人々の働き方は変わらないものとして計算しています。このサイトは特定の案・政党・政治家を支持するものではありません。</span>
    <span lang="en">All numbers are estimates. They assume people don't change how much they work when the rules change. This site doesn't support any plan, party or politician.</span>`;
  document.body.append(footer);
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
