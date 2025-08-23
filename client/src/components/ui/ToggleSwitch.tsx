import { useId } from "react";
import clsx from "clsx";

type Size = "sm" | "md";

export function ToggleSwitch({
  checked,
  onChange,
  disabled,
  size = "md",
  label,
}: {
  checked: boolean;
  onChange: (val: boolean) => void;
  disabled?: boolean;
  size?: Size;
  label?: string;
}) {
  const id = useId();
  const dims =
    size === "sm"
      ? { track: "w-10 h-6", knob: "h-5 w-5", translate: "translate-x-4" }
      : { track: "w-12 h-7", knob: "h-6 w-6", translate: "translate-x-5" };

  return (
    <label
      htmlFor={id}
      className="inline-flex items-center gap-2 cursor-pointer select-none"
    >
      {label ? (
        <span className="text-sm text-[var(--text-secondary)]">{label}</span>
      ) : null}
      <span
        role="switch"
        aria-checked={checked}
        aria-disabled={disabled}
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            !disabled && onChange(!checked);
          }
        }}
        onClick={() => !disabled && onChange(!checked)}
        className={clsx(
          "relative rounded-full transition-[background] duration-200",
          dims.track,
          checked ? "bg-[var(--primary-600)]" : "bg-[var(--muted-300)]",
          disabled && "opacity-60 cursor-not-allowed"
        )}
      >
        <span
          className={clsx(
            "absolute top-1 left-1 rounded-full bg-[var(--surface-base)] shadow",
            "transition-transform duration-200",
            dims.knob,
            checked && dims.translate
          )}
        />
      </span>
      <input
        id={id}
        type="checkbox"
        className="sr-only"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        disabled={disabled}
      />
    </label>
  );
}
