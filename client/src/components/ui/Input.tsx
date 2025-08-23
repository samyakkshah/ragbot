import { InputHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

interface Props extends InputHTMLAttributes<HTMLInputElement> {}

const base =
  "w-full h-10 px-3 rounded-lg border border-[var(--border-base)] bg-[var(--surface-base)] text-[var(--text-primary)] placeholder-[var(--text-muted)] outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring-focus)]";

export const Input = forwardRef<HTMLInputElement, Props>(function Input(
  { className, ...rest },
  ref
) {
  return <input ref={ref} className={clsx(base, className)} {...rest} />;
});
