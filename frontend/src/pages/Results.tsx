import { useCallback, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ExternalLink,
  GitCompareArrows,
  Landmark,
  Printer,
  Sparkles,
  X,
} from "lucide-react";
import { toast } from "sonner";
import { apiGet, apiPost } from "@/lib/api";
import { Button, buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import AppHeader from "@/components/AppHeader";
import YojanaSahayakChat from "@/components/YojanaSahayakChat";
import SchemeCard from "@/components/SchemeCard";
import SchemeDetailDialog from "@/components/SchemeDetailDialog";
import DeadlineAlertBanner from "@/components/DeadlineAlertBanner";
import SchemeFilters from "@/components/SchemeFilters";
import type { SchemeFilterState } from "@/components/SchemeFilters";
import DocumentLockerPanel from "@/components/DocumentLockerPanel";
import { useEvaluation, useOwnedDocuments } from "@/lib/citizenStore";
import type {
  Scheme,
  SchemeComparisonResponse,
} from "@/types";

const STATUS_FILTER_DEFAULT = "likely";

export default function Results() {
  const evaluation = useEvaluation();
  const { ownedDocuments, toggleDocument } = useOwnedDocuments();

  const [filters, setFilters] = useState<SchemeFilterState>({
    search: "",
    sector: "All",
    govLevel: "all",
    statusFilter: STATUS_FILTER_DEFAULT,
    onlyClosingSoon: false,
  });
  const { search, sector, govLevel, statusFilter, onlyClosingSoon } = filters;

  const updateFilter = useCallback(
    <K extends keyof SchemeFilterState>(key: K, value: SchemeFilterState[K]) => {
      setFilters((prev) => ({ ...prev, [key]: value }));
    },
    [],
  );

  const [activeScheme, setActiveScheme] = useState<Scheme | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [compareIds, setCompareIds] = useState<string[]>([]);
  const [comparison, setComparison] = useState<SchemeComparisonResponse | null>(null);

  const { data: schemes, isError: schemesError } = useQuery({
    queryKey: ["schemes"],
    queryFn: () => apiGet<Scheme[]>("/schemes"),
  });

  const compareMutation = useMutation({
    mutationFn: (ids: string[]) =>
      apiPost<SchemeComparisonResponse>("/schemes/compare", { scheme_ids: ids }),
    onSuccess: (data) => setComparison(data),
    onError: () => toast.error("Select between 2 and 4 schemes to compare"),
  });

  const eligibilityMap = evaluation?.eligibility_map ?? {};

  const visibleSchemes = useMemo(() => {
    const list = schemes ?? [];
    const filtered = list.filter((s) => {
      const result = eligibilityMap[s.id];

      if (evaluation && statusFilter !== "all") {
        const status = result?.status ?? "INELIGIBLE";
        if (statusFilter === "eligible" && status !== "ELIGIBLE") return false;
        if (
          statusFilter === "likely" &&
          status !== "ELIGIBLE" &&
          status !== "PARTIALLY_ELIGIBLE"
        )
          return false;
      }

      if (sector !== "All" && s.sector !== sector) return false;
      if (govLevel === "central" && !s.is_central) return false;
      if (govLevel === "state" && s.is_central) return false;
      if (onlyClosingSoon && !s.deadline_status?.is_urgent) return false;

      if (search.trim()) {
        const q = search.toLowerCase();
        const corpus = `${s.title} ${s.short_name} ${s.description} ${s.ministry} ${s.tags.join(" ")}`.toLowerCase();
        if (!corpus.includes(q)) return false;
      }
      return true;
    });

    return filtered.sort((a, b) => {
      const sa = eligibilityMap[a.id]?.match_score ?? 0;
      const sb = eligibilityMap[b.id]?.match_score ?? 0;
      if (sb !== sa) return sb - sa;
      return Number(b.featured) - Number(a.featured);
    });
  }, [schemes, eligibilityMap, evaluation, statusFilter, sector, govLevel, search, onlyClosingSoon]);

  function toggleCompare(id: string) {
    setCompareIds((prev) => {
      if (prev.includes(id)) return prev.filter((p) => p !== id);
      if (prev.length >= 4) {
        toast.error("You can compare up to 4 schemes at a time");
        return prev;
      }
      return [...prev, id];
    });
  }

  // Documents required across the citizen's eligible schemes
  const requiredDocsAcrossEligible = useMemo(() => {
    if (!schemes || !evaluation) return [];
    const counts = new Map<string, number>();
    schemes.forEach((s) => {
      const r = eligibilityMap[s.id];
      if (r && (r.status === "ELIGIBLE" || r.status === "PARTIALLY_ELIGIBLE")) {
        s.required_documents.forEach((d) => {
          counts.set(d.name, (counts.get(d.name) ?? 0) + 1);
        });
      }
    });
    return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
  }, [schemes, evaluation, eligibilityMap]);

  const persona = evaluation?.persona;

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
        {/* Persona summary */}
        {persona && evaluation ? (
          <section
            className="overflow-hidden rounded-2xl border border-border bg-[#1E3A8A] p-6 text-white sm:p-8"
            data-testid="persona-summary-card"
          >
            <div className="flex flex-wrap items-start justify-between gap-6">
              <div className="max-w-2xl">
                <Badge
                  variant="outline"
                  className="border-white/25 bg-white/10 text-white"
                  data-testid="persona-demographic-badge"
                >
                  {persona.demographic_badge}
                </Badge>
                <h1
                  className="mt-4 font-heading text-2xl font-extrabold leading-tight tracking-tight sm:text-3xl"
                  data-testid="persona-title"
                >
                  {evaluation.profile.name}, you are a {persona.title}
                </h1>
                <p className="mt-2 text-sm font-semibold text-[#FDBA74]">{persona.tagline}</p>
                <p className="mt-3 text-sm leading-relaxed text-white/80">
                  {persona.description}
                </p>
              </div>

              <div className="grid shrink-0 grid-cols-3 gap-5 sm:gap-8">
                <div>
                  <p className="text-[11px] font-medium uppercase tracking-wide text-white/60">
                    Eligible
                  </p>
                  <p
                    className="font-heading text-4xl font-black leading-none text-[#FDBA74]"
                    data-testid="stat-eligible-count"
                  >
                    {evaluation.eligible_count}
                  </p>
                </div>
                <div>
                  <p className="text-[11px] font-medium uppercase tracking-wide text-white/60">
                    Likely
                  </p>
                  <p
                    className="font-heading text-4xl font-black leading-none"
                    data-testid="stat-partial-count"
                  >
                    {evaluation.partially_eligible_count}
                  </p>
                </div>
                <div>
                  <p className="text-[11px] font-medium uppercase tracking-wide text-white/60">
                    Screened
                  </p>
                  <p
                    className="font-heading text-4xl font-black leading-none"
                    data-testid="stat-total-evaluated"
                  >
                    {evaluation.total_schemes_evaluated}
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 flex flex-wrap items-center gap-2.5 border-t border-white/15 pt-5">
              {persona.key_sectors.map((s) => (
                <Badge key={s} variant="outline" className="border-white/25 bg-white/10 text-white">
                  {s}
                </Badge>
              ))}
              <Link
                to="/report"
                className="ml-auto inline-flex h-10 items-center gap-2 rounded-full bg-[#EA580C] px-5 text-sm font-bold text-white transition-colors duration-200 hover:bg-[#C2410C]"
                data-testid="open-print-report-link"
              >
                <Printer className="size-4" />
                Printable eligibility card
              </Link>
            </div>
          </section>
        ) : (
          <section
            className="rounded-2xl border border-border bg-card p-6 sm:p-8"
            data-testid="no-profile-banner"
          >
            <h1 className="font-heading text-2xl font-extrabold tracking-tight">
              Browsing all government schemes
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              You have not completed the questionnaire yet, so nothing is personalised. Answer nine
              quick questions to see which of these schemes you actually qualify for.
            </p>
            <Link
              to="/questionnaire"
              className={`mt-5 ${buttonVariants({ size: "lg" })} rounded-full bg-[#1E3A8A] px-6 hover:bg-[#1E40AF]`}
              data-testid="no-profile-start-link"
            >
              <Sparkles className="size-4" />
              Start eligibility check
            </Link>
          </section>
        )}

        {/* Closing-soon warning for the citizen's matched schemes */}
        <DeadlineAlertBanner
          schemeIds={
            evaluation
              ? Object.values(eligibilityMap)
                  .filter((r) => r.status === "ELIGIBLE" || r.status === "PARTIALLY_ELIGIBLE")
                  .map((r) => r.scheme_id)
              : undefined
          }
          onOpenScheme={(schemeId) => {
            const found = (schemes ?? []).find((s) => s.id === schemeId);
            if (found) {
              setActiveScheme(found);
              setDialogOpen(true);
            }
          }}
        />

        <Tabs defaultValue="schemes" className="mt-10">          <TabsList variant="line" className="w-full justify-start overflow-x-auto">
            <TabsTrigger value="schemes" data-testid="tab-schemes">
              Schemes for me
            </TabsTrigger>
            <TabsTrigger value="documents" data-testid="tab-documents">
              Document locker
            </TabsTrigger>
            <TabsTrigger value="compare" data-testid="tab-compare">
              Compare ({compareIds.length})
            </TabsTrigger>
          </TabsList>

          {/* ---------- SCHEMES ---------- */}
          <TabsContent value="schemes" className="pt-6">
            <SchemeFilters
              {...filters}
              showEligibilityFilter={Boolean(evaluation)}
              resultCount={visibleSchemes.length}
              hasProfile={Boolean(evaluation)}
              onChange={updateFilter}
            />

            {schemesError && (
              <div
                className="mt-6 rounded-xl border border-border bg-secondary/50 p-6 text-sm text-muted-foreground"
                data-testid="schemes-error-state"
              >
                Scheme data could not be loaded right now. Please refresh in a moment — the rest of
                the page still works.
              </div>
            )}

            {!schemesError && visibleSchemes.length === 0 && (
              <div
                className="mt-6 rounded-xl border border-border bg-secondary/40 p-8 text-center"
                data-testid="schemes-empty-state"
              >
                <p className="font-heading text-lg font-bold">No schemes match these filters</p>
                <p className="mt-1.5 text-sm text-muted-foreground">
                  Try widening the eligibility filter to "All schemes" or clearing the sector.
                </p>
              </div>
            )}

            <div className="mt-6 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
              {visibleSchemes.map((s, i) => (
                <SchemeCard
                  key={s.id}
                  scheme={s}
                  result={eligibilityMap[s.id]}
                  index={i}
                  onOpen={(scheme) => {
                    setActiveScheme(scheme);
                    setDialogOpen(true);
                  }}
                  selectedForCompare={compareIds.includes(s.id)}
                  onToggleCompare={toggleCompare}
                />
              ))}
            </div>
          </TabsContent>

          {/* ---------- DOCUMENT LOCKER ---------- */}
          <TabsContent value="documents" className="pt-6">
            <DocumentLockerPanel
              ownedDocuments={ownedDocuments}
              onToggleDocument={toggleDocument}
              neededDocuments={requiredDocsAcrossEligible}
            />
          </TabsContent>

          {/* ---------- COMPARE ---------- */}
          <TabsContent value="compare" className="pt-6">
            <div className="rounded-xl border border-border bg-card p-6">
              <h2 className="flex items-center gap-2 font-heading text-xl font-bold tracking-tight">
                <GitCompareArrows className="size-5 text-[#1E3A8A]" />
                Side-by-side scheme comparison
              </h2>
              <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                Tick "Compare" on 2 to 4 scheme cards in the "Schemes for me" tab, then generate a
                comparison here.
              </p>

              <div className="mt-4 flex flex-wrap items-center gap-2">
                {compareIds.length === 0 && (
                  <span className="text-xs text-muted-foreground">No schemes selected yet.</span>
                )}
                {compareIds.map((id) => {
                  const s = (schemes ?? []).find((x) => x.id === id);
                  return (
                    <Badge
                      key={id}
                      variant="secondary"
                      className="gap-1.5 py-1.5 pl-3 pr-2"
                      data-testid={`compare-chip-${id}`}
                    >
                      {s?.short_name ?? id}
                      <button
                        type="button"
                        onClick={() => toggleCompare(id)}
                        aria-label={`Remove ${s?.short_name ?? id}`}
                        className="rounded-full p-0.5 transition-colors duration-200 hover:bg-foreground/10"
                      >
                        <X className="size-3" />
                      </button>
                    </Badge>
                  );
                })}
              </div>

              <div className="mt-5 flex flex-wrap gap-3">
                <Button
                  onClick={() => compareMutation.mutate(compareIds)}
                  disabled={compareIds.length < 2 || compareMutation.isPending}
                  className="rounded-full bg-[#1E3A8A] hover:bg-[#1E40AF]"
                  data-testid="generate-comparison-button"
                >
                  Generate comparison
                </Button>
                {compareIds.length > 0 && (
                  <Button
                    variant="ghost"
                    onClick={() => {
                      setCompareIds([]);
                      setComparison(null);
                    }}
                    data-testid="clear-comparison-button"
                  >
                    Clear selection
                  </Button>
                )}
              </div>
            </div>

            {comparison && (
              <div
                className="mt-6 overflow-hidden rounded-xl border border-border bg-card"
                data-testid="comparison-table-wrapper"
              >
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="min-w-[180px]">Attribute</TableHead>
                      {comparison.schemes.map((s) => (
                        <TableHead key={s.id} className="min-w-[220px]">
                          <span className="font-heading font-bold text-foreground">
                            {s.short_name}
                          </span>
                        </TableHead>
                      ))}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {comparison.comparison_attributes.map((attr) => (
                      <TableRow key={attr.key} data-testid={`comparison-row-${attr.key}`}>
                        <TableCell className="align-top text-xs font-semibold text-muted-foreground">
                          {attr.label}
                        </TableCell>
                        {comparison.schemes.map((s) => (
                          <TableCell
                            key={s.id}
                            className="align-top text-xs leading-relaxed text-foreground"
                          >
                            {attr.key === "official_portal_url" ? (
                              <a
                                href={attr.values[s.id]}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 font-semibold text-[#EA580C] hover:underline"
                              >
                                Open portal
                                <ExternalLink className="size-3" />
                              </a>
                            ) : (
                              attr.values[s.id]
                            )}
                          </TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </TabsContent>
        </Tabs>

        <p className="mt-12 flex items-start gap-2 border-t border-border pt-6 text-xs leading-relaxed text-muted-foreground">
          <Landmark className="mt-0.5 size-4 shrink-0" />
          Eligibility shown here is indicative, computed from published criteria on india.gov.in and
          ministry portals. Final approval always rests with the concerned government department.
        </p>
      </main>

      <SchemeDetailDialog
        scheme={activeScheme}
        result={activeScheme ? eligibilityMap[activeScheme.id] : undefined}
        open={dialogOpen}
        onOpenChange={setDialogOpen}
      />

      <YojanaSahayakChat activeSchemeId={dialogOpen ? activeScheme?.id ?? null : null} />
    </div>
  );
}
