# Yojana Setu — Living Spec

## What the app does
Yojana Setu ("Bridging Schemes to Citizens") helps Indian citizens discover which Central and State
government welfare schemes they are eligible for. A short questionnaire (name, age, gender, state,
category, occupation, income, area, plus special-condition flags) is run against the published
eligibility rules of every scheme in the database. Citizens get a persona classification, a filtered
list of matched schemes with official gov links, a document-readiness locker, a side-by-side scheme
comparison tool, a printable eligibility card, and a multilingual AI assistant (22 scheduled Indian
languages).

## Stack
- Backend: FastAPI + motor/MongoDB, all routes on `api_router` under `/api`.
- Frontend: Vite + React 19 + TS strict + Tailwind v4 + shadcn (base-ui), TanStack Query.
- AI: Gemini 2.5 Flash via `emergentintegrations` LlmChat, streamed as SSE. Key: `EMERGENT_LLM_KEY` in backend/.env.
- Fonts: Manrope (headings) + IBM Plex Sans (body) via @fontsource.

## Data model (Mongo collections)
- `schemes` — 40 seeded schemes (`backend/seed.py`). Fields: id (slug), title, short_name, ministry,
  sector, is_central, applicable_states, description, benefit_summary, benefit_type,
  max_financial_benefit, eligibility_criteria[], target_beneficiaries[], eligibility_rules{},
  required_documents[], application_steps[], application_mode, official_portal_url, india_gov_url,
  helpline, faq[], tags[], featured.
- `master_documents` — 12 core citizen documents (Aadhaar, bank passbook, ration card, income cert,
  caste cert, domicile, land record, UDID, MGNREGA job card, MCP card, Udyam, marksheets).
- `chat_sessions` — persisted Yojana Sahayak conversations (`id`, `messages[]`, `citizen_context`).
- `status_checks` — template health collection (unused by features).

## Eligibility engine (`backend/lib/eligibility_engine.py`)
- `determine_persona(profile)` → one of 10 personas: DIVYANGJAN_HERO, SENIOR_CITIZEN,
  ANNADATA_FARMER, VISHWAKARMA_ARTISAN, SVANIDHI_VENDOR, YOUTH_SCHOLAR, MATRU_SHAKTI, NARI_SHAKTI,
  SHRAMIK_CITIZEN, MSME_ENTREPRENEUR, CITIZEN_GENERAL.
- `evaluate_scheme_eligibility(scheme, profile)` → status `ELIGIBLE` / `PARTIALLY_ELIGIBLE` /
  `INELIGIBLE`, match_score 0-100, passed_criteria[], missing_criteria[], next_action_tip,
  required_documents_status[]. Checks state, age, gender, category, occupation (with semantic
  matching), income ceiling, land, BPL, disability, minority, area type, pregnancy, girl child.

## API endpoints (all under /api)
- `GET  /` — health/banner.
- `GET  /citizens/metadata` — states (36), occupations, categories, education levels.
- `POST /citizens/evaluate` — body QuestionnaireRequest → CitizenEvaluationResponse
  (profile, persona, total_schemes_evaluated, eligible_count, partially_eligible_count, eligibility_map).
- `GET  /schemes` — list + optional filters (search, sector, is_central, state, benefit_type).
- `GET  /schemes/sectors` — 8 sector names.
- `GET  /schemes/stats/overview` — total/central/state counts + sector breakdown.
- `GET  /schemes/{id}` — single scheme (404 if unknown).
- `POST /schemes/compare` — body {scheme_ids: [2..4]} → schemes + comparison_attributes (400 otherwise).
- `GET  /documents/master` — 12 master documents.
- `POST /documents/evaluate-readiness` — body {owned_documents: []} → readiness %, unlocked counts.
- `GET  /chat/languages` — 23 language entries (22 scheduled + English).
- `GET  /chat/sessions/{session_id}` — persisted history.
- `POST /chat/stream` — SSE stream of Gemini 2.5 Flash reply in the requested language.

## Key flows
1. `/` landing → "Check my eligibility".
2. `/questionnaire` — 4 steps (identity → social/economic → livelihood → confirm) → POST evaluate →
   result saved to localStorage (`yojana-setu:evaluation`) → navigate to `/results`.
3. `/results` — persona banner + 3 tabs: "Schemes for me" (search/sector/gov-level/eligibility
   filters, cards with status badge + match %, detail dialog with 4 tabs, Apply link to gov portal),
   "Document locker" (checklist + readiness %), "Compare" (2-4 schemes → table).
4. `/report` — printable citizen eligibility card (window.print()).
5. Yojana Sahayak floating chat on every page; language chosen in the header switcher
   (`yojana-setu:language`, default `hi`).

## Voice (frontend-only, no backend/API cost)
`frontend/src/lib/speech.ts` — browser Web Speech API, no keys, no uploads.
- `useSpeechRecognition(lang)` — mic button in the chat composer. Continuous + interim results, so a
  live transcript strip shows words as the citizen speaks and fills the textarea, which stays
  editable before sending. Mic auto-stops on send/panel close. Permission-denied, no-speech and
  unsupported-browser cases each render an inline dismissible message (never a crash).
- `useSpeechSynthesis(lang)` — "Listen · <native>" button under every completed assistant reply.
  Playback is explicit (tap to start, tap again to stop); nothing ever auto-speaks. Markdown is
  stripped before speaking, and the closest matching voice is picked (exact locale → same language →
  any `-IN` voice).
- `SPEECH_LOCALES` maps all 23 app language codes to BCP-47 locales (hi-IN, bn-IN, ta-IN, te-IN,
  ml-IN, kn-IN, gu-IN, pa-IN, or-IN, ur-IN, as-IN, mr-IN, ne-NP…). Languages without a dedicated
  browser voice fall back to the closest Indian locale (e.g. Maithili/Dogri/Bodo/Sanskrit → hi-IN,
  Konkani → mr-IN, Manipuri → bn-IN, Kashmiri → ur-IN).
- Feature-detected: if the browser lacks SpeechRecognition (e.g. Firefox) the mic button is simply
  not rendered and typing works unchanged.

## Chat reply formatting
`frontend/src/components/ChatMarkdown.tsx` — dependency-free renderer for the model's light
markdown: `**bold**`, `*`/`-`/`•` bullets, numbered lists, `#` headings, bare URLs and
`[label](href)` links (rendered as tappable orange links). Prevents raw asterisks/brackets from
leaking into replies. Everything stays React nodes — no HTML injection.

## Application cut-off dates / deadline warnings
Server-anchored to the **IST** clock (`APP_TZ=Asia/Kolkata` in backend/.env) via `lib/dates.today_iso()`
— never computed in the browser, so a wrong device clock can't tell a citizen a closed scheme is open.

- `backend/lib/deadlines.py` — `compute_deadline_status()` resolves the next occurrence of each
  recurring `(month, day)` cut-off and classifies urgency:
  `CLOSING_CRITICAL` (≤7 days) · `CLOSING_SOON` (≤30 days) · `OPEN` (>30 days) ·
  `ROLLING` (genuinely open all year) · `EVENT_BASED` (window starts from a personal event).
  Handles year rollover and 29 Feb in non-leap years. `attach_deadline_status()` is applied on every
  scheme read; `deadline_status` is computed per request and never stored in Mongo.
- `SchemeDeadline` (stored) = `window_type` + `cutoff_dates[]` + `note` + `source_note`.
  `DeadlineStatus` (computed) = urgency, headline, detail, next_cutoff_date, days_remaining, is_urgent.
- Seed data: `SCHEME_DEADLINES` (20 schemes with real dates) and `ROLLING_DEADLINE_NOTES` (20 honestly
  open all year) in `backend/seed.py`, keyed by scheme id. Real dates include PM Fasal Bima Kharif
  31 Jul / Rabi 31 Dec, NSP scholarships 31 Oct, Kanyashree 15 Oct, PM-KISAN per-instalment eKYC
  cycles, FY-budget schemes 31 Mar, PMJJBY/PMSBY renewal 31 May, Rythu Bandhu seasonal cycles.
  Event-based: PMMVY (270 days from LMP), Sukanya Samriddhi (before girl turns 10), Kanya Sumangala
  (6 stages), Yuva Nidhi (after 180 days unemployed), ADIP/Vayoshri (district camps), NAPS.
- New endpoint: `GET /api/schemes/deadlines/upcoming?within_days=30&scheme_ids=a,b` → `{today,
  within_days, count, deadlines[]}` sorted soonest-first. `within_days` is validated 1-365 (422 otherwise).
- `GET /api/schemes?closing_soon=true` returns only urgent schemes.
- Comparison table gained an "Application Cut-off" row.

### Frontend surfaces
- `components/DeadlineAlertBanner.tsx` — banner above the tabs on `/results`, scoped to the citizen's
  matched schemes, listing schemes closing within 30 days (soonest first, top 3 then expandable).
  Red styling when anything is inside 7 days, amber otherwise. Each row has Details + "Apply now".
  Renders nothing when no scheme is closing — that is correct, not a failure.
- `SchemeCard` — per-card cut-off chip ("Closes in N days" / "Next cut-off 31 Oct 2026" /
  "Open all year" / "Time-limited after event"), with an "Urgent" pill inside 7 days.
- `SchemeDetailDialog` — "Application window" panel with the full sentence and later windows.
- `/results` — "Closing within 30 days only" checkbox filter.
- `/report` — each matched scheme prints its cut-off line.
## Auth
None. No login, no accounts, no credentials. All citizen data is held in browser localStorage only.

## Seeding
`cd /app/backend && python seed.py` — idempotent (deletes then re-inserts schemes + master docs).
