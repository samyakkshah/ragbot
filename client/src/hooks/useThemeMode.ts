import { useEffect, useState } from "react";

type Mode = "light" | "dark" | "system";

const storageKey = "theme-mode";

export const useThemeMode = () => {
  const [mode, setMode] = useState<Mode>(
    () => (localStorage.getItem(storageKey) as Mode) || "system"
  );

  useEffect(() => {
    const root = document.documentElement;
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const isDark = mode == "dark" || (mode === "system" && prefersDark);
    root.classList.toggle("dark", isDark);
    localStorage.setItem(storageKey, mode);
  }, [mode]);

  return { mode, setMode };
};
