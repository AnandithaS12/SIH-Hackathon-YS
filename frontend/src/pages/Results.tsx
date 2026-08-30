import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ExternalLink,
  FileCheck2,
  Filter,
  GitCompareArrows,
  Landmark,
  Printer,
  Search,
  Sparkles,
  X,
} from "lucide-react";
import { toast } from "sonner";
import { apiGet, apiPost } from "@/lib/api";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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
import { useEvaluation, useOwnedDocuments } from "@/lib/citizenStore";
import type {
  DocumentReadinessResponse,
  MasterDocument,
  Scheme,
  SchemeComparisonResponse,
} from "@/types";

const SECTORS = [
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

const STATUS_FILTERS = [
  { value: "eligible", label: "Eligible only" },
  { value: "likely", label: "Eligible + Likely" },
  { value: "all", label: "All schemes" },
];

export default function Results() {
  const evaluation = useEvaluation();
  const { ownedDocuments, toggleDocument } = useOwnedDocuments();

  const [search, setSearch] = useState("");
  const [sector, setSector] = useState("All");
  const [statusFilter, setStatusFilter] = useState("likely");
  const [govLevel, setGovLevel] = useState("all");
  const [activeScheme, setActiveScheme] = useState<Scheme | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [compareIds, setCompareIds] = useState<string[]>([]);
  const [comparison, setComparison] = useState<SchemeComparisonResponse | null>(null);

  const { data: schemes, isError: schemesError } = useQuery({
    queryKey: ["schemes"],
    queryFn: () => apiGet<Scheme[]>("/schemes"),
  });

  const { data: masterDocs } = useQuery({
    queryKey: ["master-documents"],
    queryFn: () => apiGet<MasterDocument[]>("/documents/master"),
  });

  const { data: readiness } = useQuery({
    queryKey: ["document-readiness", ownedDocuments],
    queryFn: () =>
      apiPost<DocumentReadinessResponse>("/documents/evaluate-readiness", {
        owned_documents: ownedDocuments,
      }),
    enabled: ownedDocuments.length >= 0,
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
  }, [schemes, eligibilityMap, evaluation, statusFilter, sector, govLevel, search]);

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

        <Tabs defaultValue="schemes" className="mt-10">
          <TabsList variant="line" className="w-full justify-start overflow-x-auto">
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
            <div className="rounded-xl border border-border bg-card p-4 sm:p-5">
              <div className="flex flex-wrap items-end gap-3">
                <div className="relative min-w-[220px] flex-1">
                  <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search scheme, ministry or benefit…"
                    className="h-11 pl-9"
                    data-testid="scheme-search-input"
                  />
                </div>

                <Select value={sector} onValueChange={(v: string) => setSector(v)}>
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

                <Select value={govLevel} onValueChange={(v: string) => setGovLevel(v)}>
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

                {evaluation && (
                  <Select value={statusFilter} onValueChange={(v: string) => setStatusFilter(v)}>
                    <SelectTrigger className="h-11 w-[180px]" data-testid="status-filter-select">
                      <SelectValue>
                        {(v) =>
                          STATUS_FILTERS.find((f) => f.value === v)?.label ?? "Eligibility"
                        }
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
                className="mt-3 flex items-center gap-2 text-xs text-muted-foreground"
                data-testid="scheme-result-count"
              >
                <Filter className="size-3.5" />
                Showing {visibleSchemes.length} scheme
                {visibleSchemes.length === 1 ? "" : "s"}
                {evaluation ? " matched against your profile" : " from the national database"}
              </p>
            </div>

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
            <div className="grid gap-6 lg:grid-cols-[1.35fr_1fr]">
              <div>
                <h2 className="font-heading text-xl font-bold tracking-tight">
                  Tick the documents you already have
                </h2>
                <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                  Nothing is uploaded — this is a private checklist stored on your device so you
                  know exactly what to collect before visiting a CSC or Gram Panchayat.
                </p>

                <div className="mt-5 space-y-3">
                  {(masterDocs ?? []).map((d) => {
                    const owned = ownedDocuments.includes(d.name);
                    return (
                      <label
                        key={d.id}
                        className={`flex cursor-pointer gap-3.5 rounded-xl border p-4 transition-colors duration-200 ${
                          owned
                            ? "border-[#059669]/40 bg-[#059669]/6"
                            : "border-border bg-card hover:bg-secondary/40"
                        }`}
                        data-testid={`document-locker-item-${d.id}`}
                      >
                        <Checkbox
                          checked={owned}
                          onCheckedChange={() => toggleDocument(d.name)}
                          className="mt-0.5"
                          data-testid={`document-checkbox-${d.id}`}
                        />
                        <div className="min-w-0">
                          <p className="text-sm font-bold text-foreground">
                            {d.name}
                            <span className="ml-2 font-normal text-muted-foreground">
                              {d.name_hi}
                            </span>
                          </p>
                          <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                            {d.description}
                          </p>
                          <p className="mt-1.5 text-xs leading-relaxed text-[#1E3A8A]">
                            How to get: {d.how_to_obtain}
                          </p>
                          <div className="mt-2 flex flex-wrap items-center gap-2">
                            <Badge variant="secondary" className="text-[10px]">
                              {d.category}
                            </Badge>
                            <Badge variant="outline" className="text-[10px]">
                              Used by ~{d.common_schemes_count} schemes
                            </Badge>
                            {d.digital_portal_url && (
                              <a
                                href={d.digital_portal_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                onClick={(e) => e.stopPropagation()}
                                className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#EA580C] hover:underline"
                                data-testid={`document-portal-link-${d.id}`}
                              >
                                Official portal
                                <ExternalLink className="size-3" />
                              </a>
                            )}
                          </div>
                        </div>
                      </label>
                    );
                  })}
                </div>
              </div>

              <aside className="lg:sticky lg:top-24 lg:self-start">
                <div
                  className="rounded-xl border border-border bg-card p-6"
                  data-testid="document-readiness-panel"
                >
                  <h3 className="flex items-center gap-2 font-heading text-lg font-bold tracking-tight">
                    <FileCheck2 className="size-5 text-[#059669]" />
                    Document readiness
                  </h3>

                  <p
                    className="mt-4 font-heading text-5xl font-black leading-none text-[#1E3A8A]"
                    data-testid="readiness-percentage"
                  >
                    {readiness?.readiness_percentage ?? 0}%
                  </p>
                  <p className="mt-1.5 text-xs text-muted-foreground">
                    {readiness?.owned_documents_count ?? 0} of{" "}
                    {readiness?.total_documents_count ?? 12} core documents ready
                  </p>

                  <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-secondary">
                    <div
                      className="h-full rounded-full bg-[#059669] transition-[width] duration-500"
                      style={{ width: `${readiness?.readiness_percentage ?? 0}%` }}
                    />
                  </div>

                  <dl className="mt-6 space-y-3 border-t border-border pt-4">
                    <div className="flex items-center justify-between gap-3">
                      <dt className="text-xs text-muted-foreground">
                        Schemes you can apply to today
                      </dt>
                      <dd
                        className="font-heading text-xl font-extrabold text-[#059669]"
                        data-testid="readiness-unlocked-count"
                      >
                        {readiness?.unlocked_schemes_count ?? 0}
                      </dd>
                    </div>
                    <div className="flex items-center justify-between gap-3">
                      <dt className="text-xs text-muted-foreground">
                        Almost ready (1-2 docs pending)
                      </dt>
                      <dd className="font-heading text-xl font-extrabold text-[#D97706]">
                        {readiness?.partially_ready_schemes_count ?? 0}
                      </dd>
                    </div>
                  </dl>
                </div>

                {requiredDocsAcrossEligible.length > 0 && (
                  <div className="mt-5 rounded-xl border border-border bg-card p-6">
                    <h3 className="font-heading text-base font-bold tracking-tight">
                      Most-needed for your matched schemes
                    </h3>
                    <ul className="mt-3 space-y-2">
                      {requiredDocsAcrossEligible.map(([name, count]) => {
                        const owned = ownedDocuments.some(
                          (o) =>
                            name.toLowerCase().includes(o.toLowerCase()) ||
                            o.toLowerCase().includes(name.toLowerCase()),
                        );
                        return (
                          <li
                            key={name}
                            className="flex items-start justify-between gap-3 text-xs"
                            data-testid={`needed-document-${name}`}
                          >
                            <span
                              className={owned ? "text-muted-foreground line-through" : "text-foreground"}
                            >
                              {name}
                            </span>
                            <span className="shrink-0 font-semibold text-muted-foreground">
                              {count}×
                            </span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                )}
              </aside>
            </div>
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
