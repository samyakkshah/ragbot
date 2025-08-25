import { useEffect, useState } from "react";

type Mode = "light" | "dark" | "system";

const storageKey = "theme-mode";

export const useThemeMode = () => {
  const [theme, setTheme] = useState<Mode>(
    () => (localStorage.getItem(storageKey) as Mode) || "system"
  );

  useEffect(() => {
    const root = document.documentElement;
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const isDark = theme == "dark" || (theme === "system" && prefersDark);
    root.classList.toggle("dark", isDark);
    localStorage.setItem(storageKey, theme);
  }, [theme]);

  return { theme, setTheme };
};
