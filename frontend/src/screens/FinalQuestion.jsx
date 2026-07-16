import { useState } from "react";

export default function FinalQuestion({ product, onSubmit, busy }) {
  const [reason, setReason] = useState("");

  function submit(e) {
    e.preventDefault();
    onSubmit(reason.trim());
  }

  return (
    <div className="screen final">
      <form className="final-card" onSubmit={submit}>
        <h2>Almost done</h2>
        <p className="final-choice">
          You selected: <strong>{product.brand} — {product.name}</strong>
        </p>
        <label className="final-label" htmlFor="reason">
          Why did you pick this product?
        </label>
        <textarea
          id="reason"
          rows={4}
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="For example: liked the price, familiar brand, high rating…"
        />
        <button className="btn-primary" type="submit" disabled={busy}>
          {busy ? "Saving…" : "Finish"}
        </button>
      </form>
    </div>
  );
}
