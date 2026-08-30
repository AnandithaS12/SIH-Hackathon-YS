// Hand-written TS mirrors of the backend Pydantic v2 models (backend/models/*.py).
// Keep these in sync with the Python models in the same edit.

export interface SchemeDocument {
  name: string;
  mandatory: boolean;
  description: string;
  how_to_get?: string | null;
}

export interface ApplicationStep {
  step_number: number;
  title: string;
  description: string;
}

export interface SchemeFAQ {
  question: string;
  answer: string;
}

export interface EligibilityRules {
  min_age?: number | null;
  max_age?: number | null;
  genders: string[];
  categories: string[];
  occupations: string[];
  max_annual_income?: number | null;
  requires_land?: boolean | null;
  max_land_acres?: number | null;
  requires_bpl?: boolean | null;
  requires_disability?: boolean | null;
  requires_minority?: boolean | null;
  area_type?: string | null;
  marital_status?: string[] | null;
  requires_girl_child?: boolean | null;
  requires_pregnant_lactating?: boolean | null;
  student_levels?: string[] | null;
  state_restriction?: string[] | null;
}

export interface Scheme {
  id: string;
  title: string;
  title_hi?: string | null;
  short_name: string;
  ministry: string;
  sector: string;
  is_central: boolean;
  applicable_states: string[];
  description: string;
  benefit_summary: string;
  benefit_type: string;
  max_financial_benefit?: string | null;
  eligibility_criteria: string[];
  target_beneficiaries: string[];
  eligibility_rules: EligibilityRules;
  required_documents: SchemeDocument[];
  application_steps: ApplicationStep[];
  application_mode: string;
  official_portal_url: string;
  india_gov_url: string;
  helpline?: string | null;
  faq: SchemeFAQ[];
  tags: string[];
  featured: boolean;
}

export interface CitizenProfile {
  id: string;
  name: string;
  age: number;
  gender: string;
  state: string;
  category: string;
  occupation: string;
  annual_income: number;
  is_specially_abled: boolean;
  disability_percentage?: number | null;
  is_minority: boolean;
  area_type: string;
  marital_status: string;
  has_land: boolean;
  land_size_acres?: number | null;
  has_bpl_card: boolean;
  has_girl_child: boolean;
  is_pregnant_lactating: boolean;
  has_senior_dependent: boolean;
  student_education_level?: string | null;
  owned_documents: string[];
  created_at: string;
}

export interface QuestionnaireRequest {
  name: string;
  age: number;
  gender: string;
  state: string;
  category: string;
  occupation: string;
  annual_income: number;
  is_specially_abled: boolean;
  disability_percentage?: number | null;
  is_minority: boolean;
  area_type: string;
  marital_status: string;
  has_land: boolean;
  land_size_acres?: number | null;
  has_bpl_card: boolean;
  has_girl_child: boolean;
  is_pregnant_lactating: boolean;
  has_senior_dependent: boolean;
  student_education_level?: string | null;
  owned_documents?: string[] | null;
}

export interface PersonaInfo {
  persona_code: string;
  title: string;
  tagline: string;
  description: string;
  key_sectors: string[];
  demographic_badge: string;
  estimated_schemes_count: number;
  estimated_total_benefit: string;
}

export interface RequiredDocumentStatus {
  name: string;
  mandatory: boolean;
  description: string;
  is_owned: boolean;
  how_to_get?: string | null;
}

export interface EligibilityResult {
  scheme_id: string;
  status: "ELIGIBLE" | "PARTIALLY_ELIGIBLE" | "INELIGIBLE";
  match_score: number;
  is_fully_eligible: boolean;
  passed_criteria: string[];
  missing_criteria: string[];
  next_action_tip: string;
  required_documents_status: RequiredDocumentStatus[];
}

export interface CitizenEvaluationResponse {
  profile: CitizenProfile;
  persona: PersonaInfo;
  total_schemes_evaluated: number;
  eligible_count: number;
  partially_eligible_count: number;
  eligibility_map: Record<string, EligibilityResult>;
}

export interface CitizenMetadata {
  states: string[];
  occupations: { id: string; label: string; icon: string }[];
  categories: string[];
  education_levels: string[];
}

export interface MasterDocument {
  id: string;
  name: string;
  name_hi: string;
  category: string;
  description: string;
  issuing_authority: string;
  how_to_obtain: string;
  digital_portal_url?: string | null;
  common_schemes_count: number;
  common_schemes: string[];
}

export interface DocumentReadinessResponse {
  owned_documents_count: number;
  total_documents_count: number;
  readiness_percentage: number;
  unlocked_schemes_count: number;
  partially_ready_schemes_count: number;
  ready_schemes: string[];
  partially_ready_schemes: { scheme_id: string; missing_docs: string[] }[];
}

export interface SchemeComparisonResponse {
  schemes: Scheme[];
  comparison_attributes: { key: string; label: string; values: Record<string, string> }[];
}

export interface SchemeStats {
  total_schemes: number;
  central_schemes: number;
  state_schemes: number;
  sectors_breakdown: Record<string, number>;
}

export interface VernacularLanguage {
  code: string;
  name: string;
  native: string;
}

export interface ChatMessageUi {
  id: string;
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
}
