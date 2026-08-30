from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SchemeDocument(BaseModel):
    name: str
    mandatory: bool = True
    description: str = ""
    how_to_get: Optional[str] = None

class ApplicationStep(BaseModel):
    step_number: int
    title: str
    description: str

class SchemeFAQ(BaseModel):
    question: str
    answer: str

class EligibilityRules(BaseModel):
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    genders: List[str] = Field(default_factory=lambda: ["any"]) # any, male, female, transgender
    categories: List[str] = Field(default_factory=lambda: ["All"]) # All, SC, ST, OBC, General, EWS
    occupations: List[str] = Field(default_factory=lambda: ["All"])
    max_annual_income: Optional[int] = None
    requires_land: Optional[bool] = None
    max_land_acres: Optional[float] = None
    requires_bpl: Optional[bool] = None
    requires_disability: Optional[bool] = None
    requires_minority: Optional[bool] = None
    area_type: Optional[str] = "any" # any, rural, urban
    marital_status: Optional[List[str]] = None
    requires_girl_child: Optional[bool] = None
    requires_pregnant_lactating: Optional[bool] = None
    student_levels: Optional[List[str]] = None
    state_restriction: Optional[List[str]] = None # None or ["All"] means national, otherwise specific states

class SchemeCutoffDate(BaseModel):
    """One recurring annual cut-off, e.g. Kharif crop insurance closing on 31 July."""
    label: str          # e.g. "Kharif season enrolment"
    month: int          # 1-12
    day: int            # 1-31

class SchemeDeadline(BaseModel):
    # ROLLING       -> genuinely open all year (no fake date shown)
    # ANNUAL        -> one recurring cut-off per year
    # SEASONAL      -> two or more recurring cut-offs per year
    # EVENT_BASED   -> clock starts from a personal event (birth, pregnancy, admission)
    window_type: str = "ROLLING"
    cutoff_dates: List[SchemeCutoffDate] = Field(default_factory=list)
    note: Optional[str] = None          # shown for ROLLING / EVENT_BASED
    source_note: Optional[str] = None   # where the date comes from

class DeadlineStatus(BaseModel):
    """Computed server-side against the IST clock — never derived in the browser."""
    window_type: str
    urgency: str                # ROLLING | EVENT_BASED | OPEN | CLOSING_SOON | CLOSING_CRITICAL
    headline: str               # short label for the badge
    detail: str                 # full sentence for cards / banner
    next_cutoff_date: Optional[str] = None   # YYYY-MM-DD
    next_cutoff_label: Optional[str] = None
    days_remaining: Optional[int] = None
    is_urgent: bool = False

class Scheme(BaseModel):
    id: str
    title: str
    title_hi: Optional[str] = None
    short_name: str
    ministry: str
    sector: str # Agriculture, Healthcare, Housing & Sanitation, Education & Skills, Financial Inclusion & Pension, Women & Child, Employment & MSME, Social Security
    is_central: bool = True
    applicable_states: List[str] = Field(default_factory=lambda: ["All"])
    description: str
    benefit_summary: str
    benefit_type: str # Direct Benefit Transfer (Cash), Health Coverage, Subsidized Loan, Scholarship / Educational Aid, Housing Grant, Asset / Equipment Subsidy, Pension, Free Training & Certification
    max_financial_benefit: Optional[str] = None
    eligibility_criteria: List[str]
    target_beneficiaries: List[str]
    eligibility_rules: EligibilityRules
    required_documents: List[SchemeDocument]
    application_steps: List[ApplicationStep]
    application_mode: str # Online Portal, Offline / CSC / Gram Panchayat, Hybrid
    official_portal_url: str
    india_gov_url: str
    helpline: Optional[str] = None
    faq: List[SchemeFAQ] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    featured: bool = False
    deadline: SchemeDeadline = Field(default_factory=SchemeDeadline)
    # Populated by the API layer on every read; not stored in Mongo.
    deadline_status: Optional[DeadlineStatus] = None

class SchemeFilterParams(BaseModel):
    search: Optional[str] = None
    sector: Optional[str] = None
    is_central: Optional[bool] = None
    state: Optional[str] = None
    benefit_type: Optional[str] = None
    category: Optional[str] = None
    occupation: Optional[str] = None
    application_mode: Optional[str] = None
    only_eligible: Optional[bool] = False

class SchemeComparisonRequest(BaseModel):
    scheme_ids: List[str]

class SchemeComparisonResponse(BaseModel):
    schemes: List[Scheme]
    comparison_attributes: List[Dict[str, Any]]
