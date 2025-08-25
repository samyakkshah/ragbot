import { ButtonHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

type Variant = "primary" | "secondary" | "ghost";
type Size = "sm" | "md";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  loading?: boolean;
}

const base =
  "inline-flex items-center justify-center rounded-lg border transition-[background,box-shadow,transform] duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--ring-focus)] disabled:opacity-60 disabled:cursor-not-allowed";

const variants: Record<Variant, string> = {
  primary:
    "bg-[var(--primary-600)] hover:bg-[var(--primary-700)] text-[var(--text-inverted)] border-transparent shadow-[var(--shadow-md)] dark:bg-[var(--primary-400)] dark:text-[var(--text-primary)]",
  secondary:
    "bg-[var(--secondary-600)] hover:bg-[var(--secondary-700)] text-[var(--text-inverted)] border-transparent shadow-[var(--shadow-sm)]",
  ghost:
    "bg-transparent hover:bg-[var(--bg-muted)] text-[var(--text-primary)] border border-[var(--border-base)]",
};

export const Button = forwardRef<HTMLButtonElement, Props>(function Button(
  { className, variant = "primary", loading = false, children, ...rest },
  ref
) {
  return (
    <button
      ref={ref}
      className={clsx(base, variants[variant], className)}
      {...rest}
    >
      {loading ? "…" : children}
    </button>
  );
});
