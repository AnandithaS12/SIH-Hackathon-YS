import { Filter, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const SECTORS = [
  "All",
  "Agriculture",
  "Healthcare",
  "Housing & Sanitation",
  "Education & Skills",
  "Financial Inclusion & Pension",
  "Women & Child",
  "Employment & MSME",
  "Social Security",
];

export const STATUS_FILTERS = [
  { value: "eligible", label: "Eligible only" },
  { value: "likely", label: "Eligible + Likely" },
  { value: "all", label: "All schemes" },
];

export interface SchemeFilterState {
  search: string;
  sector: string;
  govLevel: string;
  statusFilter: string;
  onlyClosingSoon: boolean;
}

interface Props extends SchemeFilterState {
  /** Eligibility filter is only meaningful once a profile exists. */
  showEligibilityFilter: boolean;
  resultCount: number;
  hasProfile: boolean;
  onChange: <K extends keyof SchemeFilterState>(
    key: K,
    value: SchemeFilterState[K],
  ) => void;
}

/** Search + sector + government level + eligibility + deadline filters. */
export default function SchemeFilters({
  search,
  sector,
  govLevel,
  statusFilter,
  onlyClosingSoon,
  showEligibilityFilter,
  resultCount,
  hasProfile,
  onChange,
}: Props) {
  return (
    <div className="rounded-xl border border-border bg-card p-4 sm:p-5">
      <div className="flex flex-wrap items-end gap-3">
        <div className="relative min-w-[220px] flex-1">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={search}
            onChange={(e) => onChange("search", e.target.value)}
            placeholder="Search scheme, ministry or benefit…"
            className="h-11 pl-9"
            data-testid="scheme-search-input"
          />
        </div>

        <Select value={sector} onValueChange={(v: string) => onChange("sector", v)}>
          <SelectTrigger className="h-11 w-[190px]" data-testid="sector-filter-select">
            <SelectValue>{(v) => (v as string) || "All sectors"}</SelectValue>
          </SelectTrigger>
          <SelectContent className="max-h-[300px]">
            {SECTORS.map((s) => (
              <SelectItem key={s} value={s}>
                {s}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={govLevel} onValueChange={(v: string) => onChange("govLevel", v)}>
          <SelectTrigger className="h-11 w-[160px]" data-testid="gov-level-filter-select">
            <SelectValue>
              {(v) =>
                v === "central"
                  ? "Central only"
                  : v === "state"
                    ? "State only"
                    : "Central + State"
              }
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Central + State</SelectItem>
            <SelectItem value="central">Central only</SelectItem>
            <SelectItem value="state">State only</SelectItem>
          </SelectContent>
        </Select>

        {showEligibilityFilter && (
          <Select
            value={statusFilter}
            onValueChange={(v: string) => onChange("statusFilter", v)}
          >
            <SelectTrigger className="h-11 w-[180px]" data-testid="status-filter-select">
              <SelectValue>
                {(v) => STATUS_FILTERS.find((f) => f.value === v)?.label ?? "Eligibility"}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              {STATUS_FILTERS.map((f) => (
                <SelectItem key={f.value} value={f.value}>
                  {f.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
      </div>

      <p
        className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted-foreground"
        data-testid="scheme-result-count"
      >
        <span className="inline-flex items-center gap-2">
          <Filter className="size-3.5" />
          Showing {resultCount} scheme{resultCount === 1 ? "" : "s"}
          {hasProfile ? " matched against your profile" : " from the national database"}
        </span>

        <label className="inline-flex cursor-pointer items-center gap-2 font-semibold text-foreground">
          <Checkbox
            checked={onlyClosingSoon}
            onCheckedChange={(c) => onChange("onlyClosingSoon", Boolean(c))}
            data-testid="closing-soon-filter-checkbox"
          />
          Closing within 30 days only
        </label>
      </p>
    </div>
  );
}
