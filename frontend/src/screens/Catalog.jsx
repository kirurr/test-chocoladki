import { useEffect, useMemo, useRef } from "react";
import { logClick } from "../api.js";
import { useTiming } from "../hooks/useTiming.js";
import ProductCard from "../components/ProductCard.jsx";

export default function Catalog({ session, onSelect }) {
  const timing = useTiming();
  const started = useRef(false);
  const { variant, catalog, session_id } = session;

  useEffect(() => {
    timing.begin();
    started.current = true;
  }, []);

  const products = useMemo(() => {
    if (variant === "A") {
      return [...catalog].sort((a, b) => a.price - b.price);
    }
    return catalog;
  }, [catalog, variant]);

  function handleClick(productId) {
    logClick(session_id, productId, timing.sinceShown(), timing.nextClickOrder());
  }

  function handleSelect(productId) {
    const delta = timing.sinceShown();
    logClick(session_id, productId, delta, timing.nextClickOrder());
    onSelect(productId, delta);
  }

  return (
    <div className="screen catalog">
      <header className="catalog-head">
        <h2>Chocolate shelf</h2>
        <p>Pick the bar you would buy.</p>
      </header>
      <div className="grid">
        {products.map((p) => (
          <ProductCard
            key={p.id}
            product={p}
            variant={variant}
            onClick={handleClick}
            onSelect={handleSelect}
          />
        ))}
      </div>
    </div>
  );
}
