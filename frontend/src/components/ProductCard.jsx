function Stars({ rating }) {
  const full = Math.round(rating);
  return (
    <span className="stars" aria-label={`Rating ${rating}`}>
      {"★".repeat(full)}
      {"☆".repeat(5 - full)}
    </span>
  );
}

export default function ProductCard({ product, variant, onClick, onSelect }) {
  const hasDiscount = product.discount_percent > 0;

  return (
    <article className="card" onClick={() => onClick(product.id)}>
      <div className="card-media">
        <img src={product.image} alt={product.name} loading="lazy" />
        {variant === "A" && hasDiscount && (
          <span className="badge-discount">−{product.discount_percent}%</span>
        )}
        {variant === "B" && product.trusted && (
          <span className="badge-trusted" title="Trusted brand">
            ✓ Trusted brand
          </span>
        )}
      </div>

      <div className="card-body">
        <div className="card-brand">{product.brand}</div>
        <div className="card-name">{product.name}</div>

        <div className="card-rating">
          <Stars rating={product.rating} />
          <span className="reviews">{product.reviews_count}</span>
        </div>

        <div className="card-price">
          {hasDiscount && product.old_price != null && (
            <span className="old-price">€{product.old_price.toFixed(2)}</span>
          )}
          <span className="price">€{product.price.toFixed(2)}</span>
        </div>

        <button
          className="btn-select"
          onClick={(e) => {
            e.stopPropagation();
            onSelect(product.id);
          }}
        >
          Select
        </button>
      </div>
    </article>
  );
}
