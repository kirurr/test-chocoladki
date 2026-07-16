async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return res.json();
}

export function createSession() {
  return post("/api/session");
}

export function saveSurvey(sessionId, answers) {
  return post(`/api/session/${sessionId}/survey`, { answers });
}

export function logClick(sessionId, productId, sinceShown, clickOrder) {
  return post(`/api/session/${sessionId}/click`, {
    product_id: productId,
    since_shown: sinceShown,
    click_order: clickOrder,
  });
}

export function saveChoice(sessionId, productId, sinceShown, reason) {
  return post(`/api/session/${sessionId}/choice`, {
    product_id: productId,
    since_shown: sinceShown,
    reason,
  });
}
