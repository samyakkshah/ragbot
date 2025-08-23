import { TextareaHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

interface Props extends TextareaHTMLAttributes<HTMLTextAreaElement> {}

const base =
  "w-full min-h-[56px] max-h-[40vh] px-3 py-2 rounded-lg border border-[var(--border-base)] bg-[var(--surface-base)] text-[var(--text-primary)] placeholder-[var(--text-muted)] resize-y outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring-focus)]";

export const TextArea = forwardRef<HTMLTextAreaElement, Props>(
  function TextArea({ className, ...rest }, ref) {
    return <textarea ref={ref} className={clsx(base, className)} {...rest} />;
  }
);
