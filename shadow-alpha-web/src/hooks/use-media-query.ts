import { useState, useEffect } from "react";

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    
    // Defer initial state update to next tick to avoid React warning about cascading renders
    if (media.matches !== matches) {
      const timeoutId = setTimeout(() => setMatches(media.matches), 0);
      return () => clearTimeout(timeoutId);
    }
    
    const listener = () => setMatches(media.matches);
    window.addEventListener("resize", listener);
    return () => window.removeEventListener("resize", listener);
  }, [matches, query]);

  return matches;
}
