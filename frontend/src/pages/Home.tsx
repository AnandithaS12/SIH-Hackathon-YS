import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  BadgeCheck,
  FileCheck2,
  Languages,
  Landmark,
  Printer,
  ScanSearch,
  Sparkles,
} from "lucide-react";
import { apiGet } from "@/lib/api";
import { buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import AppHeader from "@/components/AppHeader";
import YojanaSahayakChat from "@/components/YojanaSahayakChat";
import { useEvaluation } from "@/lib/citizenStore";
import type { SchemeStats } from "@/types";

const HERO_IMAGE =
  "https://images.unsplash.com/photo-1632414237690-7713a79fe9d3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwyfHxpbmRpYW4lMjBydXJhbCUyMHBlb3BsZSUyMHNtaWxpbmd8ZW58MHx8fHwxNzg4MDY0Mjc3fDA&ixlib=rb-4.1.0&q=85";

const STEPS = [
  {
    Icon: ScanSearch,
    title: "Answer a short questionnaire",
    body: "Name, age, gender, state, category and work — nine simple questions, no login, no Aadhaar number needed.",
  },
  {
    Icon: BadgeCheck,
    title: "Get grouped into your citizen persona",
    body: "We classify you by age, gender, state and livelihood, then run every scheme's official rules against your profile.",
  },
  {
    Icon: FileCheck2,
    title: "See eligible schemes with gov links",
    body: "Each result shows benefits, criteria you match, required documents, application steps and the official portal link.",
  },
];

const FEATURES = [
  {
    Icon: Languages,
    title: "22 vernacular languages",
    body: "Yojana Sahayak, the built-in AI assistant, explains any scheme in Hindi, Bengali, Tamil, Telugu, Marathi, Odia, Punjabi and 15 more.",
  },
  {
    Icon: FileCheck2,
    title: "Document readiness locker",
    body: "Tick the certificates you already hold — Aadhaar, ration card, income, caste, land record — and see which schemes unlock.",
  },
  {
    Icon: Printer,
    title: "Printable eligibility card",
    body: "Carry a clean printed summary of your eligible schemes and pending documents to the CSC or Gram Panchayat.",
  },
];

export default function Home() {
  const evaluation = useEvaluation();

  const { data: stats } = useQuery({
    queryKey: ["scheme-stats"],
    queryFn: () => apiGet<SchemeStats>("/schemes/stats/overview"),
  });

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border bg-white">
        <div className="mx-auto grid max-w-7xl items-center gap-12 px-4 py-16 sm:px-6 lg:grid-cols-[1.15fr_1fr] lg:gap-16 lg:px-8 lg:py-24">
          <div>
            <Badge
              variant="outline"
              className="gap-1.5 border-[#EA580C]/30 bg-[#EA580C]/8 text-[#C2410C]"
              data-testid="hero-source-badge"
            >
              <Landmark className="size-3.5" />
              Scheme data sourced from india.gov.in & myscheme.gov.in
            </Badge>

            <h1 className="mt-5 font-heading text-4xl font-extrabold leading-none tracking-tight text-foreground sm:text-5xl lg:text-6xl">
              Find every government
              <br />
              scheme you are
              <span className="text-[#EA580C]"> actually eligible</span> for
            </h1>

            <p className="mt-6 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
              Yojana Setu bridges the gap between India's welfare schemes and the citizens they
              were written for. Answer a few questions, and we filter{" "}
              <strong className="font-semibold text-foreground">
                {stats?.total_schemes ?? 40}+ Central and State schemes
              </strong>{" "}
              down to the ones meant for you — with criteria, documents and official links.
            </p>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link
                to="/questionnaire"
                className="inline-flex h-12 items-center gap-2 rounded-full bg-[#1E3A8A] px-7 text-base font-bold text-white shadow-lg shadow-[#1E3A8A]/20 transition-transform duration-300 hover:-translate-y-0.5 hover:bg-[#1E40AF]"
                data-testid="hero-start-questionnaire-button"
              >
                Check my eligibility
                <ArrowRight className="size-5" />
              </Link>

              {evaluation && (
                <Link
                  to="/results"
                  className={buttonVariants({ variant: "outline", size: "lg" })}
                  data-testid="hero-view-results-button"
                >
                  View my {evaluation.eligible_count} eligible schemes
                </Link>
              )}
            </div>

            <dl className="mt-12 grid max-w-lg grid-cols-3 gap-6 border-t border-border pt-8">
              <div>
                <dt className="text-xs font-medium text-muted-foreground">Schemes indexed</dt>
                <dd
                  className="font-heading text-3xl font-extrabold tracking-tight text-[#1E3A8A]"
                  data-testid="stat-total-schemes"
                >
                  {stats?.total_schemes ?? "40"}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-muted-foreground">Central schemes</dt>
                <dd
                  className="font-heading text-3xl font-extrabold tracking-tight text-[#1E3A8A]"
                  data-testid="stat-central-schemes"
                >
                  {stats?.central_schemes ?? "31"}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-muted-foreground">Languages</dt>
                <dd className="font-heading text-3xl font-extrabold tracking-tight text-[#EA580C]">
                  22
                </dd>
              </div>
            </dl>
          </div>

          <div className="relative">
            <div className="absolute -left-6 -top-6 hidden size-28 rounded-full bg-[#EA580C]/10 lg:block" />
            <img
              src={HERO_IMAGE}
              alt="Indian citizens accessing welfare schemes"
              className="relative z-10 aspect-[4/5] w-full rounded-2xl border border-border object-cover shadow-xl"
              data-testid="hero-image"
            />
            <div className="relative z-20 -mt-12 ml-4 mr-8 rounded-xl border border-border bg-white p-4 shadow-lg lg:-mt-16">
              <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-[#1E3A8A]">
                <Sparkles className="size-3.5" />
                Yojana Sahayak
              </p>
              <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                "मैं आपकी भाषा में हर योजना समझाऊँगा — पात्रता, दस्तावेज़ और आवेदन प्रक्रिया।"
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
        <h2 className="max-w-2xl font-heading text-3xl font-extrabold leading-none tracking-tight text-foreground">
          Three steps from confusion to a filled application
        </h2>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {STEPS.map((s, i) => (
            <div
              key={s.title}
              className="rounded-xl border border-border bg-card p-6 transition-transform duration-300 hover:-translate-y-1 hover:shadow-md"
              data-testid={`how-it-works-step-${i + 1}`}
            >
              <div className="flex items-center gap-3">
                <span className="flex size-10 items-center justify-center rounded-lg bg-[#1E3A8A]/8 text-[#1E3A8A]">
                  <s.Icon className="size-5" />
                </span>
                <span className="font-heading text-4xl font-black leading-none text-border">
                  0{i + 1}
                </span>
              </div>
              <h3 className="mt-4 font-heading text-lg font-bold tracking-tight text-foreground">
                {s.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="border-y border-border bg-white">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
          <div className="grid gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:gap-16">
            <div>
              <h2 className="font-heading text-3xl font-extrabold leading-none tracking-tight text-foreground">
                Built for every Indian citizen — not just the digitally fluent
              </h2>
              <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
                Large touch targets, plain-language explanations, native scripts, and an assistant
                that answers in the language you actually speak at home.
              </p>
            </div>
            <div className="grid gap-5 sm:grid-cols-3">
              {FEATURES.map((f) => (
                <div
                  key={f.title}
                  className="rounded-xl border border-border bg-background p-5"
                  data-testid={`feature-card-${f.title}`}
                >
                  <span className="flex size-9 items-center justify-center rounded-lg bg-[#EA580C]/10 text-[#EA580C]">
                    <f.Icon className="size-4.5" />
                  </span>
                  <h3 className="mt-3.5 font-heading text-base font-bold tracking-tight text-foreground">
                    {f.title}
                  </h3>
                  <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">{f.body}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="flex flex-col items-start justify-between gap-6 rounded-2xl border border-border bg-[#1E3A8A] p-8 sm:p-12 lg:flex-row lg:items-center">
          <div>
            <h2 className="font-heading text-2xl font-extrabold leading-tight tracking-tight text-white sm:text-3xl">
              Your entitlements are waiting. Takes under two minutes.
            </h2>
            <p className="mt-2 max-w-xl text-sm leading-relaxed text-white/75">
              No sign-up, no personal ID numbers. Everything stays on your device.
            </p>
          </div>
          <Link
            to="/questionnaire"
            className="inline-flex h-12 shrink-0 items-center gap-2 rounded-full bg-[#EA580C] px-7 text-base font-bold text-white transition-transform duration-300 hover:-translate-y-0.5 hover:bg-[#C2410C]"
            data-testid="cta-start-questionnaire-button"
          >
            Start eligibility check
            <ArrowRight className="size-5" />
          </Link>
        </div>
      </section>

      <footer className="border-t border-border bg-white py-8">
        <div className="mx-auto max-w-7xl px-4 text-xs leading-relaxed text-muted-foreground sm:px-6 lg:px-8">
          <p className="font-semibold text-foreground">Yojana Setu · Bridging Schemes to Citizens</p>
          <p className="mt-1.5 max-w-3xl">
            Scheme details are compiled from public sources including india.gov.in,
            myscheme.gov.in and individual ministry portals. Yojana Setu is an informational aid —
            final eligibility is always determined by the concerned government department. Always
            verify on the official portal linked with each scheme.
          </p>
        </div>
      </footer>

      <YojanaSahayakChat />
    </div>
  );
}
