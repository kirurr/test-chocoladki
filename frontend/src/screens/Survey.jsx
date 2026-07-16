import { useState } from "react";
import { QUESTIONS } from "../data/questions.js";

export default function Survey({ onSubmit, busy }) {
  const [values, setValues] = useState({});
  const allAnswered = QUESTIONS.every((q) => values[q.id]);

  function submit(e) {
    e.preventDefault();
    if (!allAnswered) return;
    const answers = QUESTIONS.map((q) => ({
      question_id: q.id,
      answer: values[q.id],
    }));
    onSubmit(answers);
  }

  return (
    <div className="screen survey">
      <form className="survey-card" onSubmit={submit}>
        <h2>A few questions about you</h2>
        {QUESTIONS.map((q) => (
          <fieldset key={q.id} className="question">
            <legend>{q.label}</legend>
            <div className="options">
              {q.options.map((o) => (
                <label
                  key={o.value}
                  className={`option ${values[q.id] === o.value ? "selected" : ""}`}
                >
                  <input
                    type="radio"
                    name={q.id}
                    value={o.value}
                    checked={values[q.id] === o.value}
                    onChange={() =>
                      setValues((v) => ({ ...v, [q.id]: o.value }))
                    }
                  />
                  {o.label}
                </label>
              ))}
            </div>
          </fieldset>
        ))}
        <button className="btn-primary" type="submit" disabled={!allAnswered || busy}>
          {busy ? "One sec…" : "To the shelf"}
        </button>
      </form>
    </div>
  );
}
