import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowLeft, ArrowRight, Loader2, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { apiGet, apiPost } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import AppHeader from "@/components/AppHeader";
import YojanaSahayakChat from "@/components/YojanaSahayakChat";
import { saveEvaluation } from "@/lib/citizenStore";
import type { CitizenEvaluationResponse, CitizenMetadata, QuestionnaireRequest } from "@/types";

const FALLBACK_STATES = [
  "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi (NCT)", "Gujarat",
  "Haryana", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
  "Odisha", "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh",
  "Uttarakhand", "West Bengal",
];

const OCCUPATION_OPTIONS = [
  "Farmer / Agriculture",
  "Student",
  "Unemployed / Jobseeker",
  "Daily Wage Laborer / Construction Worker",
  "Street Vendor / Hawkers",
  "Artisan / Craftsman (Vishwakarma)",
  "Self-Employed / Micro Business",
  "Homemaker",
  "Salaried (Private/Public)",
  "Senior Citizen / Retired",
  "Fisherfolk / Dairy Farmer",
];

const GENDER_OPTIONS = [
  { value: "female", label: "Female / महिला" },
  { value: "male", label: "Male / पुरुष" },
  { value: "transgender", label: "Transgender / ट्रांसजेंडर" },
];

const CATEGORY_OPTIONS = ["General", "OBC", "SC", "ST", "EWS"];

const AREA_OPTIONS = [
  { value: "rural", label: "Rural / ग्रामीण" },
  { value: "urban", label: "Urban / शहरी" },
  { value: "semi-urban", label: "Semi-urban / अर्ध-शहरी" },
];

const MARITAL_OPTIONS = [
  { value: "single", label: "Unmarried / अविवाहित" },
  { value: "married", label: "Married / विवाहित" },
  { value: "widowed", label: "Widowed / विधवा" },
  { value: "divorced_separated", label: "Divorced / Separated" },
];

const EDUCATION_OPTIONS = [
  "Pre-Matric",
  "Post-Matric",
  "Undergraduate",
  "Postgraduate",
  "Vocational/ITI",
  "None",
];

const TOTAL_STEPS = 4;

// Validation / default bounds — kept as named constants so they can be tuned in one place.
const MIN_AGE = 1;
const MAX_AGE = 110;
const DEFAULT_AGE = 30;
const DEFAULT_ANNUAL_INCOME = 150000;
const INCOME_STEP = 10000;
const LAND_SIZE_STEP = 0.5;

export default function Questionnaire() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [form, setForm] = useState<QuestionnaireRequest>({
    name: "",
    age: DEFAULT_AGE,
    gender: "female",
    state: "Madhya Pradesh",
    category: "General",
    occupation: "Farmer / Agriculture",
    annual_income: DEFAULT_ANNUAL_INCOME,
    is_specially_abled: false,
    disability_percentage: null,
    is_minority: false,
    area_type: "rural",
    marital_status: "married",
    has_land: false,
    land_size_acres: 0,
    has_bpl_card: false,
    has_girl_child: false,
    is_pregnant_lactating: false,
    has_senior_dependent: false,
    student_education_level: "None",
  });

  const { data: metadata } = useQuery({
    queryKey: ["citizen-metadata"],
    queryFn: () => apiGet<CitizenMetadata>("/citizens/metadata"),
  });

  const states = metadata?.states ?? FALLBACK_STATES;
  const categories = metadata?.categories ?? CATEGORY_OPTIONS;

  const evaluateMutation = useMutation({
    mutationFn: (payload: QuestionnaireRequest) =>
      apiPost<CitizenEvaluationResponse>("/citizens/evaluate", payload),
    onSuccess: (data) => {
      saveEvaluation(data);
      toast.success(
        `${data.eligible_count} schemes matched for ${data.profile.name || "you"}`,
      );
      navigate("/results");
    },
    onError: () => {
      toast.error("Could not evaluate right now. Please try again in a moment.");
    },
  });

  function update<K extends keyof QuestionnaireRequest>(
    key: K,
    value: QuestionnaireRequest[K],
  ) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function handleNext() {
    if (step === 1 && !form.name.trim()) {
      toast.error("Please enter your name to continue");
      return;
    }
    if (step === 1 && (form.age < MIN_AGE || form.age > MAX_AGE)) {
      toast.error(`Please enter a valid age between ${MIN_AGE} and ${MAX_AGE}`);
      return;
    }
    if (step < TOTAL_STEPS) {
      setStep((s) => s + 1);
    } else {
      evaluateMutation.mutate(form);
    }
  }

  const progressPercent = Math.round((step / TOTAL_STEPS) * 100);

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />

      <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:py-14">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-[#EA580C]">
          <Sparkles className="size-3.5" />
          Citizen eligibility questionnaire
        </div>
        <h1 className="mt-3 font-heading text-3xl font-extrabold leading-none tracking-tight text-foreground sm:text-4xl">
          Step {step} of {TOTAL_STEPS}
        </h1>

        {/* Progress */}
        <div className="mt-6" data-testid="questionnaire-progress">
          <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
            <div
              className="h-full rounded-full bg-[#EA580C] transition-[width] duration-500 ease-out"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <p className="mt-2 text-xs text-muted-foreground">
            {progressPercent}% complete · your answers stay on this device
          </p>
        </div>

        <div className="mt-8 rounded-2xl border border-border bg-card p-6 sm:p-8">
          {step === 1 && (
            <div className="space-y-6" data-testid="questionnaire-step-1">
              <div>
                <h2 className="font-heading text-xl font-bold tracking-tight">
                  Who are you? / आप कौन हैं?
                </h2>
                <p className="mt-1 text-sm text-muted-foreground">
                  We use these to group you by age, gender and state.
                </p>
              </div>

              <div className="grid gap-5 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="name">Full name / पूरा नाम</Label>
                  <Input
                    id="name"
                    value={form.name}
                    onChange={(e) => update("name", e.target.value)}
                    placeholder="e.g. Sunita Devi"
                    className="h-11"
                    data-testid="questionnaire-name-input"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="age">Age / आयु (years)</Label>
                  <Input
                    id="age"
                    type="number"
                    min={MIN_AGE}
                    max={MAX_AGE}
                    value={form.age}
                    onChange={(e) => update("age", Number(e.target.value))}
                    className="h-11"
                    data-testid="questionnaire-age-input"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Gender / लिंग</Label>
                  <Select
                    value={form.gender}
                    onValueChange={(value: string) => update("gender", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-gender-select">
                      <SelectValue>
                        {(v) =>
                          GENDER_OPTIONS.find((g) => g.value === v)?.label ?? "Select gender"
                        }
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {GENDER_OPTIONS.map((g) => (
                        <SelectItem key={g.value} value={g.value}>
                          {g.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>State / UT · राज्य</Label>
                  <Select
                    value={form.state}
                    onValueChange={(value: string) => update("state", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-state-select">
                      <SelectValue>{(v) => (v as string) || "Select state"}</SelectValue>
                    </SelectTrigger>
                    <SelectContent className="max-h-[300px]">
                      {states.map((s) => (
                        <SelectItem key={s} value={s}>
                          {s}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6" data-testid="questionnaire-step-2">
              <div>
                <h2 className="font-heading text-xl font-bold tracking-tight">
                  Social & economic profile
                </h2>
                <p className="mt-1 text-sm text-muted-foreground">
                  Most schemes have a category and income ceiling.
                </p>
              </div>

              <div className="grid gap-5 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Social category / श्रेणी</Label>
                  <Select
                    value={form.category}
                    onValueChange={(value: string) => update("category", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-category-select">
                      <SelectValue>{(v) => (v as string) || "Select category"}</SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((c) => (
                        <SelectItem key={c} value={c}>
                          {c}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="income">Annual family income (₹)</Label>
                  <Input
                    id="income"
                    type="number"
                    min={0}
                    step={INCOME_STEP}
                    value={form.annual_income}
                    onChange={(e) => update("annual_income", Number(e.target.value))}
                    className="h-11"
                    data-testid="questionnaire-income-input"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Where do you live?</Label>
                  <Select
                    value={form.area_type}
                    onValueChange={(value: string) => update("area_type", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-area-select">
                      <SelectValue>
                        {(v) => AREA_OPTIONS.find((a) => a.value === v)?.label ?? "Select area"}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {AREA_OPTIONS.map((a) => (
                        <SelectItem key={a.value} value={a.value}>
                          {a.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Marital status</Label>
                  <Select
                    value={form.marital_status}
                    onValueChange={(value: string) => update("marital_status", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-marital-select">
                      <SelectValue>
                        {(v) =>
                          MARITAL_OPTIONS.find((m) => m.value === v)?.label ?? "Select status"
                        }
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {MARITAL_OPTIONS.map((m) => (
                        <SelectItem key={m.value} value={m.value}>
                          {m.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-3 rounded-xl border border-border bg-secondary/40 p-4">
                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.has_bpl_card}
                    onCheckedChange={(c) => update("has_bpl_card", Boolean(c))}
                    data-testid="questionnaire-bpl-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">I hold a BPL / Antyodaya / NFSA ration card</span>
                    <span className="block text-xs text-muted-foreground">
                      Unlocks housing, health and pension schemes
                    </span>
                  </span>
                </label>

                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.is_minority}
                    onCheckedChange={(c) => update("is_minority", Boolean(c))}
                    data-testid="questionnaire-minority-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">
                      I belong to a notified minority community
                    </span>
                    <span className="block text-xs text-muted-foreground">
                      Muslim, Christian, Sikh, Buddhist, Jain or Parsi
                    </span>
                  </span>
                </label>

                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.is_specially_abled}
                    onCheckedChange={(c) => update("is_specially_abled", Boolean(c))}
                    data-testid="questionnaire-disability-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">
                      I am a person with disability (Divyangjan, 40%+)
                    </span>
                    <span className="block text-xs text-muted-foreground">
                      Unlocks ADIP assistive aids and disability pensions
                    </span>
                  </span>
                </label>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6" data-testid="questionnaire-step-3">
              <div>
                <h2 className="font-heading text-xl font-bold tracking-tight">
                  Livelihood / आपका कार्य
                </h2>
                <p className="mt-1 text-sm text-muted-foreground">
                  This decides your citizen persona and the schemes written for it.
                </p>
              </div>

              <div className="grid gap-5 sm:grid-cols-2">
                <div className="space-y-2 sm:col-span-2">
                  <Label>Primary occupation</Label>
                  <Select
                    value={form.occupation}
                    onValueChange={(value: string) => update("occupation", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-occupation-select">
                      <SelectValue>{(v) => (v as string) || "Select occupation"}</SelectValue>
                    </SelectTrigger>
                    <SelectContent className="max-h-[300px]">
                      {OCCUPATION_OPTIONS.map((o) => (
                        <SelectItem key={o} value={o}>
                          {o}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Current education level (if studying)</Label>
                  <Select
                    value={form.student_education_level ?? "None"}
                    onValueChange={(value: string) => update("student_education_level", value)}
                  >
                    <SelectTrigger className="h-11" data-testid="questionnaire-education-select">
                      <SelectValue>{(v) => (v as string) || "None"}</SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {EDUCATION_OPTIONS.map((e) => (
                        <SelectItem key={e} value={e}>
                          {e}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {form.has_land && (
                  <div className="space-y-2">
                    <Label htmlFor="land">Land size (acres)</Label>
                    <Input
                      id="land"
                      type="number"
                      min={0}
                      step={LAND_SIZE_STEP}
                      value={form.land_size_acres ?? 0}
                      onChange={(e) => update("land_size_acres", Number(e.target.value))}
                      className="h-11"
                      data-testid="questionnaire-land-size-input"
                    />
                  </div>
                )}
              </div>

              <div className="space-y-3 rounded-xl border border-border bg-secondary/40 p-4">
                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.has_land}
                    onCheckedChange={(c) => update("has_land", Boolean(c))}
                    data-testid="questionnaire-land-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">
                      My family owns or cultivates agricultural land
                    </span>
                    <span className="block text-xs text-muted-foreground">
                      Required for PM-KISAN, Fasal Bima, KCC, PM-KUSUM
                    </span>
                  </span>
                </label>

                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.has_girl_child}
                    onCheckedChange={(c) => update("has_girl_child", Boolean(c))}
                    data-testid="questionnaire-girl-child-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">There is a girl child in my family</span>
                    <span className="block text-xs text-muted-foreground">
                      Unlocks Sukanya Samriddhi, Kanyashree, Kanya Sumangala
                    </span>
                  </span>
                </label>

                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.is_pregnant_lactating}
                    onCheckedChange={(c) => update("is_pregnant_lactating", Boolean(c))}
                    data-testid="questionnaire-pregnant-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">
                      I am currently pregnant or a lactating mother
                    </span>
                    <span className="block text-xs text-muted-foreground">
                      Unlocks PMMVY maternity benefit and Poshan Abhiyaan
                    </span>
                  </span>
                </label>

                <label className="flex cursor-pointer items-start gap-3">
                  <Checkbox
                    checked={form.has_senior_dependent}
                    onCheckedChange={(c) => update("has_senior_dependent", Boolean(c))}
                    data-testid="questionnaire-senior-checkbox"
                  />
                  <span className="text-sm leading-snug">
                    <span className="font-semibold">
                      A senior citizen (60+) lives in my household
                    </span>
                    <span className="block text-xs text-muted-foreground">
                      Unlocks Vayoshri aids and old-age pension guidance
                    </span>
                  </span>
                </label>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-6" data-testid="questionnaire-step-4">
              <div>
                <h2 className="font-heading text-xl font-bold tracking-tight">
                  Confirm your details
                </h2>
                <p className="mt-1 text-sm text-muted-foreground">
                  We will now run all official criteria against this profile.
                </p>
              </div>

              <dl className="grid gap-x-6 gap-y-4 rounded-xl border border-border bg-secondary/40 p-5 sm:grid-cols-2">
                {[
                  ["Name", form.name || "—"],
                  ["Age", `${form.age} years`],
                  ["Gender", form.gender],
                  ["State / UT", form.state],
                  ["Category", form.category],
                  ["Occupation", form.occupation],
                  ["Annual income", `₹${form.annual_income.toLocaleString("en-IN")}`],
                  ["Area", form.area_type],
                ].map(([label, value]) => (
                  <div key={label}>
                    <dt className="text-xs font-medium text-muted-foreground">{label}</dt>
                    <dd
                      className="mt-0.5 text-sm font-semibold capitalize text-foreground"
                      data-testid={`questionnaire-summary-${label}`}
                    >
                      {value}
                    </dd>
                  </div>
                ))}
              </dl>

              <p className="text-xs leading-relaxed text-muted-foreground">
                Yojana Setu never asks for your Aadhaar number, bank details or OTP. We only use
                these answers locally to filter schemes.
              </p>
            </div>
          )}

          {/* Nav */}
          <div className="mt-8 flex items-center justify-between gap-3 border-t border-border pt-6">
            <Button
              variant="ghost"
              onClick={() => (step === 1 ? navigate("/") : setStep((s) => s - 1))}
              data-testid="questionnaire-back-button"
            >
              <ArrowLeft className="size-4" />
              {step === 1 ? "Home" : "Back"}
            </Button>

            <Button
              onClick={handleNext}
              disabled={evaluateMutation.isPending}
              size="lg"
              className="rounded-full bg-[#1E3A8A] px-7 hover:bg-[#1E40AF]"
              data-testid="questionnaire-next-button"
            >
              {evaluateMutation.isPending ? (
                <>
                  <Loader2 className="size-4 animate-spin" />
                  Matching schemes…
                </>
              ) : (
                <>
                  {step === TOTAL_STEPS ? "Show my schemes" : "Continue"}
                  <ArrowRight className="size-4" />
                </>
              )}
            </Button>
          </div>
        </div>
      </main>

      <YojanaSahayakChat />
    </div>
  );
}
