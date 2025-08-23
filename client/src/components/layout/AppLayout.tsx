import { ReactNode } from "react";
import { useThemeMode } from "../../hooks/useThemeMode";
import { ToggleSwitch } from "../ui/ToggleSwitch";

export default function AppLayout({ children }: { children: ReactNode }) {
  const { mode, setMode } = useThemeMode();

  return (
    <div className="min-h-screen bg-bg-base text-text-primary">
      <header className="sticky top-0 z-30 border-b border-border-subtle backdrop-blur bg-surface-base/80">
        <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-accent-400 to-primary-600 shadow-md" />
            <span className="text-lg font-semibold tracking-tight">
              Eloquent
            </span>
          </div>
          <div className="flex items-center gap-2">
            <ToggleSwitch
              onChange={(val) => setMode(val ? "dark" : "light")}
              checked={mode === "dark"}
              aria-label="Toggle theme"
            />
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
    </div>
  );
}
