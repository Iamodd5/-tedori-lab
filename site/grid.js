// Which points of a precomputed grid to show for an amount typed into a box.

// An amount typed into a box ("1300000", "1,300,000", "130万", full-width digits): null when empty, NaN when not a number.
function readYen(text) {
  let s = String(text).normalize("NFKC").replace(/[,\s円¥]/g, ""), mul = 1;
  if (s.endsWith("万")) { mul = 10_000; s = s.slice(0, -1); }
  if (s === "") return null;
  if (!/^\d+(\.\d+)?$/.test(s)) return NaN;  // no signs, exponents, "Infinity" or "NaN"
  return Number(s) * mul;
}

// Returns null when the text isn't an amount of yen (empty, negative, letters).
// Off the grid, both neighbouring points are returned (never the nearer one: a wall can lie between them).
// Above the top, the top point is returned with capped: true.
function gridPoints(text, step, top) {
  const raw = readYen(text);
  if (raw === null || !Number.isFinite(raw)) return null;
  if (raw > top) return { lo: top, hi: top, exact: false, capped: true };
  const lo = Math.floor(raw / step) * step, hi = Math.min(top, Math.ceil(raw / step) * step);
  return { lo, hi, exact: lo === hi, capped: false };
}
if (typeof module !== "undefined") module.exports = { readYen, gridPoints };
