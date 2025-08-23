import { ReactNode } from "react";
import clsx from "clsx";
import { Card } from "../../ui/Card";

export type Role = "user" | "assistant" | "system";

export function MessageBubble({
  role,
  children,
  className,
}: {
  role: Role;
  children: ReactNode;
  className?: string;
}) {
  const align = role === "user" ? "justify-end" : "justify-start";
  const bubble =
    role === "user"
      ? "bg-[var(--primary-600)] text-[var(--text-primary)]"
      : "bg-[var(--surface-base)] text-[var(--text-primary)] border border-[var(--border-subtle)]";

  return (
    <div className={clsx("w-full flex", align, className)}>
      <div className="max-w-[78%]">
        <Card className={clsx("shadow-none", bubble)}>
          <div className="p-3 leading-relaxed text-sm">{children}</div>
        </Card>
      </div>
    </div>
  );
}
