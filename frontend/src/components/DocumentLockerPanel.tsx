import { useQuery } from "@tanstack/react-query";
import { ExternalLink, FileCheck2 } from "lucide-react";
import { apiGet, apiPost } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import type { DocumentReadinessResponse, MasterDocument } from "@/types";

const TOTAL_CORE_DOCUMENTS_FALLBACK = 12;

interface Props {
  ownedDocuments: string[];
  onToggleDocument: (docName: string) => void;
  /** [documentName, howManyMatchedSchemesNeedIt] pairs, most-needed first. */
  neededDocuments: [string, number][];
}

/**
 * Private, device-local checklist of the certificates a citizen already holds,
 * plus a readiness score computed by the backend.
 */
export default function DocumentLockerPanel({
  ownedDocuments,
  onToggleDocument,
  neededDocuments,
}: Props) {
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
  });

  return (
    <div className="grid gap-6 lg:grid-cols-[1.35fr_1fr]">
      <div>
        <h2 className="font-heading text-xl font-bold tracking-tight">
          Tick the documents you already have
        </h2>
        <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
          Nothing is uploaded — this is a private checklist stored on your device so you know
          exactly what to collect before visiting a CSC or Gram Panchayat.
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
                  onCheckedChange={() => onToggleDocument(d.name)}
                  className="mt-0.5"
                  data-testid={`document-checkbox-${d.id}`}
                />
                <div className="min-w-0">
                  <p className="text-sm font-bold text-foreground">
                    {d.name}
                    <span className="ml-2 font-normal text-muted-foreground">{d.name_hi}</span>
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
            {readiness?.total_documents_count ?? TOTAL_CORE_DOCUMENTS_FALLBACK} core documents
            ready
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

        {neededDocuments.length > 0 && (
          <div className="mt-5 rounded-xl border border-border bg-card p-6">
            <h3 className="font-heading text-base font-bold tracking-tight">
              Most-needed for your matched schemes
            </h3>
            <ul className="mt-3 space-y-2">
              {neededDocuments.map(([name, count]) => {
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
                      className={
                        owned ? "text-muted-foreground line-through" : "text-foreground"
                      }
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
  );
}
