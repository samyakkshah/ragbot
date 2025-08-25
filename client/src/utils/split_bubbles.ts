export const BUBBLE_DELIM = "[[NEW_BUBBLE]]";

export function splitIntoBubbles(content: string): string[] {
  return content
    .split(/\s*\[\[NEW_BUBBLE\]\]\s*/g)
    .map((s) => s.trim())
    .filter(Boolean);
}
