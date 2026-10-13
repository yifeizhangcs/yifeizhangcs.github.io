(() => {
  const container = document.querySelector(".scholar-stats");
  if (!container) return;

  const keys = ["citations", "h_index", "i10_index"];
  const storageKey = `scholar-stats:${container.dataset.scholarId}`;
  let lastUpdated = Date.parse(container.dataset.updatedAt);

  function valid(data) {
    const timestamp = Date.parse(data?.updated_at);
    return data?.schema_version === 1 &&
      data.author_id === container.dataset.scholarId &&
      Number.isFinite(timestamp) && timestamp <= Date.now() + 300000 &&
      keys.every((key) => Number.isSafeInteger(data[key]) && data[key] >= 0) &&
      data.h_index ** 2 <= data.citations && data.i10_index * 10 <= data.citations;
  }

  function render(data) {
    if (!valid(data) || Date.parse(data.updated_at) < lastUpdated) return false;
    keys.forEach((key) => {
      container.querySelector(`[data-metric="${key}"]`).textContent = data[key].toLocaleString("en-US");
    });
    lastUpdated = Date.parse(data.updated_at);
    const time = document.createElement("time");
    time.dateTime = data.updated_at;
    time.textContent = new Intl.DateTimeFormat("en-US", {
      month: "short", day: "numeric", year: "numeric", timeZone: "UTC",
    }).format(lastUpdated);
    const label = Date.now() - lastUpdated > 3 * 86400000 ? "Last successful update " : "Last updated ";
    container.querySelector("[data-stats-date]").replaceChildren(label, time);
    return true;
  }

  // The built-in snapshot remains visible if storage, JavaScript, or the network fails.
  try {
    const cached = JSON.parse(localStorage.getItem(storageKey));
    if (cached) render(cached);
  } catch (_) {
    // Private browsing may disable persistent storage.
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 7000);
  fetch(container.dataset.statsUrl, { signal: controller.signal, cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error("Statistics unavailable");
      return response.json();
    })
    .then((data) => {
      if (render(data)) {
        try { localStorage.setItem(storageKey, JSON.stringify(data)); } catch (_) { /* Optional cache. */ }
      }
    })
    .catch(() => {})
    .finally(() => clearTimeout(timeout));
})();
