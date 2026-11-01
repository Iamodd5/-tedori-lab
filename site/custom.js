// Custom credit for the design builder. Python twin: custom_people / custom_population in engine/reforms.py;
// tests/test_custom.py runs both on the same cases. Hand calculation: tests/hand_calcs/custom_credit.md.
// people: [[kind, earnings, pensions], ...], kind k = child (child-allowance age), p = head or spouse, o = other.
function customCredit(people, p) {
  let kids = 0, claimant = -1;  // claimant: the partner with the higher earnings, the head if equal
  people.forEach(([k, earn], i) => {
    if (k === "k") kids++;
    if (k === "p" && (claimant < 0 || earn > people[claimant][1])) claimant = i;
  });
  let total = 0;
  people.forEach(([, earn, pension], i) => {
    if (earn <= 0) return;
    let c = Math.min(p.phase_in_rate * earn, p.maximum) + (i === claimant ? kids * p.child_addition : 0);
    c -= p.phase_out_rate * Math.max(0, earn + pension - p.plateau_end);
    total += Math.max(0, Math.floor(Math.round(c * 1e6) / 1e6));  // 0.05 × 1,000,000 must not floor to 49,999
  });
  return total;
}

// Wall map with the credit: baseline is [[income, take-home, rate], ...] from outputs/wall_map.json.
function customWall(h, baseline, p) {
  const [who, slot, rest] = h.vary, step = baseline[1][0] - baseline[0][0];
  const disp = baseline.map(([x, d]) => {
    const ppl = h.people.map(q => q.slice());
    ppl[who][slot] = rest + x;
    return d + customCredit(ppl, p);
  });
  return baseline.map(([x], j) => [x, disp[j], j + 1 < disp.length ? Math.round((1 - (disp[j + 1] - disp[j]) / step) * 1e4) / 1e4 : null]);
}

function populationResults(builder, p) {
  const credit = builder.population.rows.map(x => customCredit(x, p)), pieces = builder.population.pieces;
  const mean = Array(10).fill(0), share = Array(10).fill(0), weight = Array(10).fill(0);
  let cost = 0;
  for (const [i, d, w] of pieces) {
    weight[d - 1] += w; mean[d - 1] += credit[i] * w; cost += credit[i] * w;
    if (credit[i] > 0) share[d - 1] += w;
  }
  return { mean: mean.map((m, k) => m / weight[k]), share: share.map((s, k) => s / weight[k]), cost };
}

if (typeof module !== "undefined") module.exports = { customCredit, customWall, populationResults };
