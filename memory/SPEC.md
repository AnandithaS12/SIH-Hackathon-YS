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

## Auth
None. No login, no accounts, no credentials. All citizen data is held in browser localStorage only.

## Seeding
`cd /app/backend && python seed.py` — idempotent (deletes then re-inserts schemes + master docs).
