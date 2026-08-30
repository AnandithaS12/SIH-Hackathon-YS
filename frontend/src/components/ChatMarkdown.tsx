import type { ReactNode } from "react";

/**
 * Minimal inline formatter for assistant replies. The model returns light
 * markdown (**bold**, `*` bullets, bare URLs); rendering it raw shows literal
 * asterisks to the citizen. This handles just those three cases — no markdown
 * dependency, no HTML injection (everything stays React nodes).
 */
function renderInline(text: string, keyPrefix: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  // Collapse markdown links [label](href) down to a single labelled link first,
  // otherwise the raw bracket/paren syntax leaks into the rendered reply.
  const normalised = text.replace(
    /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
    (_m, label: string, href: string) => (label.trim() === href.trim() ? href : `${label} ${href}`),
  );

  // Split on **bold** segments and bare http(s) URLs, keeping the delimiters.
  const pattern = /(\*\*[^*]+\*\*|https?:\/\/[^\s)]+)/g;
  const parts = normalised.split(pattern).filter((p) => p !== "");

  parts.forEach((part, i) => {
    const key = `${keyPrefix}-${i}`;
    if (part.startsWith("**") && part.endsWith("**") && part.length > 4) {
      nodes.push(
        <strong key={key} className="font-bold text-foreground">
          {part.slice(2, -2)}
        </strong>,
      );
    } else if (/^https?:\/\//.test(part)) {
      const href = part.replace(/[.,;]$/, "");
      nodes.push(
        <a
          key={key}
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="break-all font-semibold text-[#EA580C] underline decoration-[#EA580C]/40 hover:decoration-[#EA580C]"
        >
          {href}
        </a>,
      );
    } else {
      nodes.push(<span key={key}>{part.replace(/[`_]/g, "")}</span>);
    }
  });

  return nodes;
}

export default function ChatMarkdown({ text }: { text: string }) {
  const lines = text.split("\n");

  return (
    <div className="space-y-1.5 text-sm leading-relaxed text-foreground">
      {lines.map((raw, idx) => {
        const line = raw.trimEnd();
        if (!line.trim()) return <div key={`sp-${idx}`} className="h-1.5" />;

        // Bullet lines: "* item", "- item", "• item"
        const bullet = line.match(/^\s*[*\-•]\s+(.*)$/);
        if (bullet) {
          return (
            <div key={`li-${idx}`} className="flex gap-2 pl-0.5">
              <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-[#1E3A8A]" />
              <span className="min-w-0">{renderInline(bullet[1], `li-${idx}`)}</span>
            </div>
          );
        }

        // Numbered lines: "1. item"
        const numbered = line.match(/^\s*(\d+)[.)]\s+(.*)$/);
        if (numbered) {
          return (
            <div key={`no-${idx}`} className="flex gap-2">
              <span className="shrink-0 font-bold text-[#1E3A8A]">{numbered[1]}.</span>
              <span className="min-w-0">{renderInline(numbered[2], `no-${idx}`)}</span>
            </div>
          );
        }

        // Headings: "### Title" / "## Title"
        const heading = line.match(/^\s*#{1,6}\s+(.*)$/);
        if (heading) {
          return (
            <p key={`h-${idx}`} className="pt-1 font-heading text-sm font-bold tracking-tight">
              {renderInline(heading[1], `h-${idx}`)}
            </p>
          );
        }

        return <p key={`p-${idx}`}>{renderInline(line, `p-${idx}`)}</p>;
      })}
    </div>
  );
}
