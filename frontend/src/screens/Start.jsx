export default function Start({ onStart, busy }) {
  return (
    <div className="screen start">
      <div className="start-card">
        <div className="start-emoji">🍫</div>
        <h1>Which chocolate would you pick?</h1>
        <p>
          A short choice study. Answer a few questions and pick a bar from the
          shelf — it takes about a minute.
        </p>
        <button className="btn-primary" onClick={onStart} disabled={busy}>
          {busy ? "Loading…" : "Start"}
        </button>
      </div>
    </div>
  );
}
