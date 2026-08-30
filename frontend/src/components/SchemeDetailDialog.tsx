import {
  ArrowUpRight,
  CalendarClock,
  CheckCircle2,
  CircleDashed,
  ExternalLink,
  FileText,
  Phone,
  XCircle,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { EligibilityResult, Scheme } from "@/types";

interface Props {
  scheme: Scheme | null;
  result?: EligibilityResult;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function SchemeDetailDialog({ scheme, result, open, onOpenChange }: Props) {
  if (!scheme) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        className="max-h-[88vh] overflow-y-auto sm:max-w-3xl"
        data-testid="scheme-detail-dialog"
      >
        <DialogHeader>
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="secondary" data-testid="detail-sector-badge">
              {scheme.sector}
            </Badge>
            <Badge variant="outline">
              {scheme.is_central ? "Central Government" : "State Government"}
            </Badge>
            <Badge variant="outline">{scheme.application_mode}</Badge>
          </div>
          <DialogTitle
            className="mt-2 font-heading text-2xl font-extrabold leading-tight tracking-tight"
            data-testid="detail-scheme-title"
          >
            {scheme.title}
          </DialogTitle>
          <DialogDescription className="leading-relaxed">
            {scheme.ministry}
          </DialogDescription>
        </DialogHeader>

        <div className="rounded-xl border border-[#059669]/25 bg-[#059669]/8 p-4">
          <p className="text-[11px] font-bold uppercase tracking-wide text-[#047857]">
            What you get
          </p>
          <p
            className="mt-1.5 font-heading text-lg font-bold leading-snug text-foreground"
            data-testid="detail-benefit-summary"
          >
            {scheme.benefit_summary}
          </p>
        </div>

        <p className="text-sm leading-relaxed text-muted-foreground">{scheme.description}</p>

        {/* Application window / cut-off */}
        {scheme.deadline_status && (
          <div
            className={`rounded-xl border p-4 ${
              scheme.deadline_status.urgency === "CLOSING_CRITICAL"
                ? "border-destructive/40 bg-destructive/6"
                : scheme.deadline_status.urgency === "CLOSING_SOON"
                  ? "border-[#D97706]/40 bg-[#D97706]/6"
                  : "border-border bg-secondary/50"
            }`}
            data-testid="detail-deadline-panel"
          >
            <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-wide text-muted-foreground">
              <CalendarClock className="size-3.5" />
              Application window
            </p>
            <p
              className="mt-1.5 font-heading text-base font-bold leading-snug text-foreground"
              data-testid="detail-deadline-headline"
            >
              {scheme.deadline_status.headline}
            </p>
            <p
              className="mt-1 text-xs leading-relaxed text-muted-foreground"
              data-testid="detail-deadline-detail"
            >
              {scheme.deadline_status.detail}
            </p>
          </div>
        )}

        <Tabs defaultValue="eligibility" className="mt-2">
          <TabsList variant="line" className="w-full justify-start overflow-x-auto">
            <TabsTrigger value="eligibility" data-testid="detail-tab-eligibility">
              Eligibility
            </TabsTrigger>
            <TabsTrigger value="documents" data-testid="detail-tab-documents">
              Documents
            </TabsTrigger>
            <TabsTrigger value="apply" data-testid="detail-tab-apply">
              How to Apply
            </TabsTrigger>
            <TabsTrigger value="faq" data-testid="detail-tab-faq">
              FAQ & Helpline
            </TabsTrigger>
          </TabsList>

          <TabsContent value="eligibility" className="space-y-4 pt-4">
            <div>
              <p className="text-sm font-bold text-foreground">Official criteria</p>
              <ul className="mt-2 space-y-2">
                {scheme.eligibility_criteria.map((c) => (
                  <li key={c} className="flex gap-2 text-sm leading-relaxed text-muted-foreground">
                    <CircleDashed className="mt-0.5 size-4 shrink-0 text-[#1E3A8A]" />
                    {c}
                  </li>
                ))}
              </ul>
            </div>

            {result && (
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-lg border border-[#059669]/25 bg-[#059669]/6 p-3.5">
                  <p className="text-xs font-bold uppercase text-[#047857]">
                    You match ({result.passed_criteria.length})
                  </p>
                  <ul className="mt-2 space-y-1.5" data-testid="detail-passed-criteria">
                    {result.passed_criteria.map((c) => (
                      <li key={c} className="flex gap-2 text-xs leading-relaxed text-foreground">
                        <CheckCircle2 className="mt-0.5 size-3.5 shrink-0 text-[#059669]" />
                        {c}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-lg border border-border bg-secondary/50 p-3.5">
                  <p className="text-xs font-bold uppercase text-muted-foreground">
                    Needs attention ({result.missing_criteria.length})
                  </p>
                  {result.missing_criteria.length === 0 ? (
                    <p className="mt-2 text-xs text-muted-foreground">
                      Nothing pending — you satisfy every published criterion.
                    </p>
                  ) : (
                    <ul className="mt-2 space-y-1.5" data-testid="detail-missing-criteria">
                      {result.missing_criteria.map((c) => (
                        <li key={c} className="flex gap-2 text-xs leading-relaxed text-foreground">
                          <XCircle className="mt-0.5 size-3.5 shrink-0 text-[#D97706]" />
                          {c}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            )}
          </TabsContent>

          <TabsContent value="documents" className="space-y-3 pt-4">
            {scheme.required_documents.map((d) => (
              <div
                key={d.name}
                className="rounded-lg border border-border bg-card p-3.5"
                data-testid={`detail-document-${d.name}`}
              >
                <div className="flex items-start justify-between gap-3">
                  <p className="flex items-start gap-2 text-sm font-semibold text-foreground">
                    <FileText className="mt-0.5 size-4 shrink-0 text-[#1E3A8A]" />
                    {d.name}
                  </p>
                  <Badge variant={d.mandatory ? "default" : "secondary"} className="shrink-0 text-[10px]">
                    {d.mandatory ? "Mandatory" : "Optional"}
                  </Badge>
                </div>
                <p className="mt-1.5 pl-6 text-xs leading-relaxed text-muted-foreground">
                  {d.description}
                </p>
                {d.how_to_get && (
                  <p className="mt-1 pl-6 text-xs leading-relaxed text-[#1E3A8A]">
                    How to obtain: {d.how_to_get}
                  </p>
                )}
              </div>
            ))}
          </TabsContent>

          <TabsContent value="apply" className="space-y-3 pt-4">
            {scheme.application_steps.map((s) => (
              <div key={s.step_number} className="flex gap-3.5">
                <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-[#1E3A8A] text-sm font-bold text-white">
                  {s.step_number}
                </span>
                <div className="pb-1">
                  <p className="text-sm font-semibold text-foreground">{s.title}</p>
                  <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                    {s.description}
                  </p>
                </div>
              </div>
            ))}

            <div className="mt-4 flex flex-wrap gap-2.5 border-t border-border pt-4">
              <a
                href={scheme.official_portal_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex h-10 items-center gap-2 rounded-full bg-[#EA580C] px-5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#C2410C]"
                data-testid="detail-official-portal-link"
              >
                Official Portal
                <ArrowUpRight className="size-4" />
              </a>
              <a
                href={scheme.india_gov_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex h-10 items-center gap-2 rounded-full border border-border px-5 text-sm font-semibold text-foreground transition-colors duration-200 hover:bg-secondary"
                data-testid="detail-india-gov-link"
              >
                india.gov.in listing
                <ExternalLink className="size-4" />
              </a>
            </div>
          </TabsContent>

          <TabsContent value="faq" className="space-y-3 pt-4">
            {scheme.faq.map((f) => (
              <div key={f.question} className="rounded-lg border border-border bg-card p-3.5">
                <p className="text-sm font-semibold text-foreground">{f.question}</p>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{f.answer}</p>
              </div>
            ))}
            {scheme.helpline && (
              <div className="flex items-center gap-2.5 rounded-lg border border-[#1E3A8A]/20 bg-[#1E3A8A]/6 p-3.5">
                <Phone className="size-4 shrink-0 text-[#1E3A8A]" />
                <p className="text-sm font-semibold text-foreground" data-testid="detail-helpline">
                  Toll-free helpline: {scheme.helpline}
                </p>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
