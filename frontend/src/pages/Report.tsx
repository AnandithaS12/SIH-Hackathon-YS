import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Printer } from "lucide-react";
import { apiGet } from "@/lib/api";
import { Button, buttonVariants } from "@/components/ui/button";
import { useEvaluation, useOwnedDocuments } from "@/lib/citizenStore";
import type { Scheme } from "@/types";

const LOGO_URL =
  "https://customer-assets-eiarnc6j.emergentagent.net/job_e43c439c-0a56-49ac-ad23-99fa1ca30ab5/artifacts/2fvf23e5_image.png";

export default function Report() {
  const evaluation = useEvaluation();
  const { ownedDocuments } = useOwnedDocuments();

  const { data: schemes } = useQuery({
    queryKey: ["schemes"],
    queryFn: () => apiGet<Scheme[]>("/schemes"),
  });

  const eligibilityMap = evaluation?.eligibility_map ?? {};
  const matched = (schemes ?? []).filter((s) => {
    const st = eligibilityMap[s.id]?.status;
    return st === "ELIGIBLE" || st === "PARTIALLY_ELIGIBLE";
  });

  const pendingDocs = new Set<string>();
  matched.forEach((s) => {
    s.required_documents
      .filter((d) => d.mandatory)
      .forEach((d) => {
        const owned = ownedDocuments.some(
          (o) =>
            d.name.toLowerCase().includes(o.toLowerCase()) ||
            o.toLowerCase().includes(d.name.toLowerCase()),
        );
        if (!owned) pendingDocs.add(d.name);
      });
  });

  return (
    <div className="min-h-screen bg-background">
      <div className="no-print border-b border-border bg-white">
        <div className="mx-auto flex max-w-4xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
          <Link
            to="/results"
            className={buttonVariants({ variant: "ghost", size: "sm" })}
            data-testid="report-back-link"
          >
            <ArrowLeft className="size-4" />
            Back to my schemes
          </Link>
          <Button
            onClick={() => window.print()}
            className="rounded-full bg-[#EA580C] hover:bg-[#C2410C]"
            data-testid="report-print-button"
          >
            <Printer className="size-4" />
            Print / Save as PDF
          </Button>
        </div>
      </div>

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:py-12">
        {!evaluation ? (
          <div
            className="rounded-xl border border-border bg-card p-8"
            data-testid="report-empty-state"
          >
            <h1 className="font-heading text-2xl font-extrabold tracking-tight">
              No eligibility card yet
            </h1>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              Complete the questionnaire first and your personalised, printable eligibility card
              will be generated here.
            </p>
            <Link
              to="/questionnaire"
              className={`mt-5 ${buttonVariants()} rounded-full bg-[#1E3A8A] hover:bg-[#1E40AF]`}
              data-testid="report-start-link"
            >
              Start eligibility check
            </Link>
          </div>
        ) : (
          <article
            className="print-card rounded-xl border border-border bg-white p-6 sm:p-10"
            data-testid="eligibility-report-card"
          >
            <header className="flex items-start justify-between gap-4 border-b-2 border-[#1E3A8A] pb-5">
              <div className="flex items-center gap-3">
                <img src={LOGO_URL} alt="Yojana Setu" className="size-14 object-contain" />
                <div>
                  <p className="font-heading text-xl font-extrabold tracking-tight text-[#1E3A8A]">
                    Yojana Setu · Citizen Eligibility Card
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Bridging Schemes to Citizens · Generated{" "}
                    {new Date().toLocaleDateString("en-IN", {
                      day: "2-digit",
                      month: "short",
                      year: "numeric",
                    })}
                  </p>
                </div>
              </div>
            </header>

            <section className="mt-6">
              <h2 className="font-heading text-lg font-bold tracking-tight">Citizen details</h2>
              <dl className="mt-3 grid gap-x-8 gap-y-3 sm:grid-cols-3">
                {[
                  ["Name", evaluation.profile.name],
                  ["Age", `${evaluation.profile.age} years`],
                  ["Gender", evaluation.profile.gender],
                  ["State / UT", evaluation.profile.state],
                  ["Category", evaluation.profile.category],
                  ["Occupation", evaluation.profile.occupation],
                  ["Annual income", `₹${evaluation.profile.annual_income.toLocaleString("en-IN")}`],
                  ["Area", evaluation.profile.area_type],
                  ["Persona", evaluation.persona.title],
                ].map(([label, value]) => (
                  <div key={label}>
                    <dt className="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
                      {label}
                    </dt>
                    <dd className="text-sm font-semibold capitalize text-foreground">{value}</dd>
                  </div>
                ))}
              </dl>
            </section>

            <section className="mt-8">
              <h2 className="font-heading text-lg font-bold tracking-tight">
                Matched schemes ({matched.length})
              </h2>
              <div className="mt-3 space-y-3">
                {matched.map((s, i) => {
                  const r = eligibilityMap[s.id];
                  return (
                    <div
                      key={s.id}
                      className="print-card rounded-lg border border-border p-4"
                      data-testid={`report-scheme-${s.id}`}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <p className="text-sm font-bold text-foreground">
                          {i + 1}. {s.short_name}
                        </p>
                        <span
                          className={`shrink-0 rounded-full px-2.5 py-0.5 text-[10px] font-bold ${
                            r?.status === "ELIGIBLE"
                              ? "bg-[#059669]/12 text-[#047857]"
                              : "bg-[#D97706]/12 text-[#B45309]"
                          }`}
                        >
                          {r?.status === "ELIGIBLE" ? "ELIGIBLE" : "LIKELY ELIGIBLE"}
                        </span>
                      </div>
                      <p className="mt-1 text-xs text-muted-foreground">{s.title}</p>
                      <p className="mt-2 text-xs font-semibold text-foreground">
                        Benefit: {s.benefit_summary}
                      </p>
                      <p className="mt-1.5 text-xs text-muted-foreground">
                        Apply at: <span className="break-all">{s.official_portal_url}</span>
                        {s.helpline ? ` · Helpline: ${s.helpline}` : ""}
                      </p>
                      <p className="mt-1.5 text-xs text-muted-foreground">
                        Documents:{" "}
                        {s.required_documents
                          .filter((d) => d.mandatory)
                          .map((d) => d.name)
                          .join(", ")}
                      </p>
                    </div>
                  );
                })}
                {matched.length === 0 && (
                  <p className="text-sm text-muted-foreground">
                    No schemes matched — try adjusting your questionnaire answers.
                  </p>
                )}
              </div>
            </section>

            <section className="mt-8">
              <h2 className="font-heading text-lg font-bold tracking-tight">
                Documents still to collect ({pendingDocs.size})
              </h2>
              <ul className="mt-3 grid gap-2 sm:grid-cols-2" data-testid="report-pending-documents">
                {[...pendingDocs].map((d) => (
                  <li key={d} className="flex gap-2 text-xs text-foreground">
                    <span className="mt-0.5 inline-block size-3 shrink-0 rounded-sm border border-foreground/40" />
                    {d}
                  </li>
                ))}
                {pendingDocs.size === 0 && (
                  <li className="text-xs text-muted-foreground">
                    All mandatory documents for your matched schemes are already ticked as ready.
                  </li>
                )}
              </ul>
            </section>

            <footer className="mt-8 border-t border-border pt-4 text-[10px] leading-relaxed text-muted-foreground">
              This card is an informational aid generated by Yojana Setu from criteria published on
              india.gov.in and ministry portals. It is not a government-issued certificate. Final
              eligibility is decided by the concerned department. Verify each scheme on its official
              portal before applying.
            </footer>
          </article>
        )}
      </main>
    </div>
  );
}
