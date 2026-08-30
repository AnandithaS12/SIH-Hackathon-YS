import { useQuery } from "@tanstack/react-query";
import { ArrowUpRight, CalendarClock, ChevronDown } from "lucide-react";
import { useState } from "react";
import { apiGet } from "@/lib/api";
import type { UpcomingDeadlinesResponse } from "@/types";

interface Props {
  /** Restrict the warning to the citizen's matched schemes; omit to cover all. */
  schemeIds?: string[];
  onOpenScheme?: (schemeId: string) => void;
}

/**
 * Warns about matched schemes closing within 30 days. Dates come pre-computed
 * from the backend against the IST clock — never recalculated here.
 */
export default function DeadlineAlertBanner({ schemeIds, onOpenScheme }: Props) {
  const [expanded, setExpanded] = useState(false);

  const idsParam = schemeIds && schemeIds.length > 0 ? schemeIds.join(",") : null;

  const { data } = useQuery({
    queryKey: ["upcoming-deadlines", idsParam],
    queryFn: () =>
      apiGet<UpcomingDeadlinesResponse>(
        `/schemes/deadlines/upcoming?within_days=30${idsParam ? `&scheme_ids=${encodeURIComponent(idsParam)}` : ""}`,
      ),
  });

  if (!data || data.count === 0) return null;

  const critical = data.deadlines.filter((d) => d.urgency === "CLOSING_CRITICAL");
  const isCritical = critical.length > 0;
  const visible = expanded ? data.deadlines : data.deadlines.slice(0, 3);

  return (
    <section
      className={`mt-6 overflow-hidden rounded-xl border-2 ${
        isCritical
          ? "border-destructive/45 bg-destructive/6"
          : "border-[#D97706]/45 bg-[#D97706]/6"
      }`}
      data-testid="deadline-alert-banner"
    >
      <div className="flex flex-wrap items-start gap-3 px-5 pt-4">
        <span
          className={`mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-lg ${
            isCritical ? "bg-destructive/12 text-destructive" : "bg-[#D97706]/14 text-[#B45309]"
          }`}
        >
          <CalendarClock className="size-5" />
        </span>
        <div className="min-w-0 flex-1">
          <h2
            className={`font-heading text-base font-extrabold tracking-tight ${
              isCritical ? "text-destructive" : "text-[#B45309]"
            }`}
            data-testid="deadline-banner-title"
          >
            {data.count} scheme{data.count === 1 ? "" : "s"} closing soon
            {isCritical ? ` — ${critical.length} within a week` : ""}
          </h2>
          <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
            Cut-off dates below are as on{" "}
            {new Date(`${data.today}T00:00:00`).toLocaleDateString("en-IN", {
              day: "2-digit",
              month: "short",
              year: "numeric",
            })}{" "}
            (IST). Apply before the portal closes for this cycle.
          </p>
        </div>
      </div>

      <ul className="mt-3 divide-y divide-border/70 px-5 pb-2">
        {visible.map((d) => (
          <li
            key={d.scheme_id}
            className="flex flex-wrap items-center gap-x-4 gap-y-2 py-3"
            data-testid={`deadline-item-${d.scheme_id}`}
          >
            <span
              className={`inline-flex shrink-0 items-center rounded-full px-2.5 py-1 text-[11px] font-black uppercase tracking-wide ${
                d.urgency === "CLOSING_CRITICAL"
                  ? "bg-destructive text-white"
                  : "bg-[#D97706] text-white"
              }`}
              data-testid={`deadline-item-days-${d.scheme_id}`}
            >
              {d.days_remaining === 0
                ? "Today"
                : `${d.days_remaining} day${d.days_remaining === 1 ? "" : "s"}`}
            </span>

            <div className="min-w-0 flex-1">
              <p className="text-sm font-bold text-foreground">{d.short_name}</p>
              <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                {d.next_cutoff_label} ·{" "}
                {new Date(`${d.next_cutoff_date}T00:00:00`).toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </p>
            </div>

            <div className="flex shrink-0 items-center gap-2">
              {onOpenScheme && (
                <button
                  type="button"
                  onClick={() => onOpenScheme(d.scheme_id)}
                  className="rounded-full border border-border bg-white px-3 py-1.5 text-xs font-semibold text-foreground transition-colors duration-200 hover:bg-secondary"
                  data-testid={`deadline-item-details-${d.scheme_id}`}
                >
                  Details
                </button>
              )}
              <a
                href={d.official_portal_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 rounded-full bg-[#EA580C] px-3 py-1.5 text-xs font-semibold text-white transition-colors duration-200 hover:bg-[#C2410C]"
                data-testid={`deadline-item-apply-${d.scheme_id}`}
              >
                Apply now
                <ArrowUpRight className="size-3" />
              </a>
            </div>
          </li>
        ))}
      </ul>

      {data.deadlines.length > 3 && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="w-full border-t border-border/70 px-5 py-2.5 text-xs font-semibold text-muted-foreground transition-colors duration-200 hover:bg-white/50"
          data-testid="deadline-banner-toggle"
        >
          <span className="inline-flex items-center gap-1.5">
            {expanded ? "Show fewer" : `Show all ${data.deadlines.length} closing schemes`}
            <ChevronDown
              className={`size-3.5 transition-transform duration-300 ${expanded ? "rotate-180" : ""}`}
            />
          </span>
        </button>
      )}
    </section>
  );
}
