import { ArrowUpRight, CheckCircle2, AlertTriangle, XCircle, Landmark, MapPin } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import type { EligibilityResult, Scheme } from "@/types";

interface Props {
  scheme: Scheme;
  result?: EligibilityResult;
  index: number;
  onOpen: (scheme: Scheme) => void;
  selectedForCompare: boolean;
  onToggleCompare: (schemeId: string) => void;
}

const STATUS_META: Record<
  string,
  { label: string; className: string; Icon: typeof CheckCircle2 }
> = {
  ELIGIBLE: {
    label: "Eligible",
    className: "border-[#059669]/30 bg-[#059669]/10 text-[#047857]",
    Icon: CheckCircle2,
  },
  PARTIALLY_ELIGIBLE: {
    label: "Likely Eligible",
    className: "border-[#D97706]/30 bg-[#D97706]/10 text-[#B45309]",
    Icon: AlertTriangle,
  },
  INELIGIBLE: {
    label: "Not Eligible",
    className: "border-border bg-secondary text-muted-foreground",
    Icon: XCircle,
  },
};

export default function SchemeCard({
  scheme,
  result,
  index,
  onOpen,
  selectedForCompare,
  onToggleCompare,
}: Props) {
  const status = result?.status ?? "ELIGIBLE";
  const meta = STATUS_META[status] ?? STATUS_META.ELIGIBLE;
  const StatusIcon = meta.Icon;

  return (
    <article
      className="group relative flex flex-col overflow-hidden rounded-xl border border-border bg-card p-6 transition-transform duration-300 hover:-translate-y-1 hover:shadow-md"
      style={{ animation: `fade-in 420ms ease-out ${Math.min(index * 45, 400)}ms both` }}
      data-testid={`scheme-card-${scheme.id}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <Badge
            variant="outline"
            className={`gap-1.5 font-semibold ${meta.className}`}
            data-testid={`scheme-status-badge-${scheme.id}`}
          >
            <StatusIcon className="size-3.5" />
            {meta.label}
          </Badge>
          {result && (
            <span
              className="text-xs font-semibold text-muted-foreground"
              data-testid={`scheme-match-score-${scheme.id}`}
            >
              {result.match_score}% match
            </span>
          )}
        </div>

        <label
          className="flex cursor-pointer items-center gap-1.5 text-[11px] font-medium text-muted-foreground"
          title="Add to comparison"
        >
          <Checkbox
            checked={selectedForCompare}
            onCheckedChange={() => onToggleCompare(scheme.id)}
            data-testid={`scheme-compare-checkbox-${scheme.id}`}
          />
          Compare
        </label>
      </div>

      <h3
        className="mt-4 font-heading text-lg font-bold leading-tight tracking-tight text-foreground"
        data-testid={`scheme-title-${scheme.id}`}
      >
        {scheme.short_name}
      </h3>
      <p className="mt-1 text-xs font-medium text-muted-foreground">{scheme.title}</p>

      <div className="mt-4 rounded-lg border border-[#059669]/20 bg-[#059669]/6 px-3.5 py-3">
        <p className="text-[11px] font-bold uppercase tracking-wide text-[#047857]">
          Benefit
        </p>
        <p
          className="mt-1 text-sm font-semibold leading-relaxed text-foreground"
          data-testid={`scheme-benefit-${scheme.id}`}
        >
          {scheme.benefit_summary}
        </p>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted-foreground">
        <span className="inline-flex items-center gap-1.5">
          <Landmark className="size-3.5 shrink-0" />
          {scheme.is_central ? "Central Scheme" : "State Scheme"}
        </span>
        <span className="inline-flex items-center gap-1.5">
          <MapPin className="size-3.5 shrink-0" />
          {scheme.applicable_states.includes("All")
            ? "All India"
            : scheme.applicable_states.join(", ")}
        </span>
        <Badge variant="secondary" className="text-[10px]">
          {scheme.sector}
        </Badge>
      </div>

      {result && result.missing_criteria.length > 0 && (
        <p
          className="mt-4 border-l-2 border-[#D97706]/50 pl-3 text-xs leading-relaxed text-muted-foreground"
          data-testid={`scheme-missing-note-${scheme.id}`}
        >
          {result.missing_criteria[0]}
        </p>
      )}

      <div className="mt-5 flex items-center gap-2 pt-1">
        <Button
          variant="outline"
          size="sm"
          className="flex-1"
          onClick={() => onOpen(scheme)}
          data-testid={`scheme-details-button-${scheme.id}`}
        >
          View Details
        </Button>
        <a
          href={scheme.official_portal_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex h-9 items-center gap-1.5 rounded-full bg-[#EA580C] px-4 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#C2410C]"
          data-testid={`scheme-apply-link-${scheme.id}`}
        >
          Apply
          <ArrowUpRight className="size-3.5" />
        </a>
      </div>
    </article>
  );
}
