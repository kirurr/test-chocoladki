import { useState } from "react";
import { createSession, saveSurvey, saveChoice } from "./api.js";
import Start from "./screens/Start.jsx";
import Survey from "./screens/Survey.jsx";
import Catalog from "./screens/Catalog.jsx";
import FinalQuestion from "./screens/FinalQuestion.jsx";
import Done from "./screens/Done.jsx";

export default function App() {
  const [stage, setStage] = useState("start");
  const [session, setSession] = useState(null);
  const [choice, setChoice] = useState(null);
  const [busy, setBusy] = useState(false);

  async function handleStart() {
    setBusy(true);
    try {
      const data = await createSession();
      setSession(data);
      setStage("survey");
    } finally {
      setBusy(false);
    }
  }

  async function handleSurvey(answers) {
    setBusy(true);
    try {
      await saveSurvey(session.session_id, answers);
      setStage("catalog");
    } finally {
      setBusy(false);
    }
  }

  function handleSelect(productId, sinceShown) {
    setChoice({ productId, sinceShown });
    setStage("final");
  }

  async function handleReason(reason) {
    setBusy(true);
    try {
      await saveChoice(
        session.session_id,
        choice.productId,
        choice.sinceShown,
        reason
      );
      setStage("done");
    } finally {
      setBusy(false);
    }
  }

  const variant = session?.variant;

  return (
    <div className={`app variant-${variant || "none"}`}>
      {stage === "start" && <Start onStart={handleStart} busy={busy} />}
      {stage === "survey" && <Survey onSubmit={handleSurvey} busy={busy} />}
      {stage === "catalog" && (
        <Catalog session={session} onSelect={handleSelect} />
      )}
      {stage === "final" && (
        <FinalQuestion
          product={session.catalog.find((p) => p.id === choice.productId)}
          onSubmit={handleReason}
          busy={busy}
        />
      )}
      {stage === "done" && <Done />}
    </div>
  );
}
