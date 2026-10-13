const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const source = fs.readFileSync("assets/js/scholar-stats.js", "utf8");
const snapshot = JSON.parse(fs.readFileSync("_data/scholar.json", "utf8"));

async function test({ response, cached, rejected = false, status = 200 }) {
  const nodes = Object.fromEntries(["citations", "h_index", "i10_index"].map((key) => [key, { textContent: String(snapshot[key]) }]));
  const date = { replaceChildren(...values) { this.values = values; } };
  const saved = [];
  const container = {
    dataset: { scholarId: snapshot.author_id, updatedAt: snapshot.updated_at, statsUrl: "https://example.com/scholar.json" },
    querySelector(selector) { return selector === "[data-stats-date]" ? date : nodes[selector.match(/data-metric="([^"]+)"/)[1]]; },
  };
  vm.runInNewContext(source, {
    document: { querySelector: () => container, createElement: () => ({}) },
    localStorage: { getItem: () => cached ? JSON.stringify(cached) : null, setItem: (...args) => saved.push(args) },
    fetch: () => rejected ? Promise.reject(new Error("offline")) : Promise.resolve({ ok: status === 200, json: () => Promise.resolve(response) }),
    AbortController, setTimeout, clearTimeout, Date, Intl,
  });
  await new Promise((resolve) => setImmediate(resolve));
  return { nodes, date, saved };
}

(async () => {
  const newer = { ...snapshot, updated_at: new Date(Date.now()).toISOString(), citations: 502 };
  let result = await test({ response: newer });
  assert.equal(result.nodes.citations.textContent, "502");
  assert.equal(result.saved.length, 1);

  for (const response of [null, { ...newer, author_id: "someone-else" }, { ...newer, citations: "Error" }, { ...newer, citations: 2 }, { ...newer, updated_at: "invalid" }]) {
    result = await test({ response });
    assert.equal(result.nodes.citations.textContent, String(snapshot.citations));
    assert.equal(result.saved.length, 0);
  }
  result = await test({ rejected: true });
  assert.equal(result.nodes.citations.textContent, String(snapshot.citations));
  result = await test({ response: newer, status: 503 });
  assert.equal(result.nodes.citations.textContent, String(snapshot.citations));
  result = await test({ cached: newer, rejected: true });
  assert.equal(result.nodes.citations.textContent, "502");
  result = await test({ cached: newer, response: { ...snapshot, updated_at: "2000-01-01T00:00:00Z" } });
  assert.equal(result.nodes.citations.textContent, "502");
  console.log("Scholar display: valid data, identity checks, invalid data, stale data, HTTP failure, offline fallback passed");
})().catch((error) => { console.error(error); process.exitCode = 1; });
