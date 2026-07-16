import { useRef } from "react";

export function useTiming() {
  const start = useRef(null);
  const clicks = useRef(0);

  return {
    begin() {
      start.current = performance.now();
      clicks.current = 0;
    },
    sinceShown() {
      if (start.current === null) return 0;
      return Math.round(performance.now() - start.current);
    },
    nextClickOrder() {
      clicks.current += 1;
      return clicks.current;
    },
  };
}
