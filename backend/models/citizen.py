from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

class CitizenProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Citizen"
    age: int = 25
    gender: str = "female"  # male, female, transgender, other
    state: str = "All"      # Indian State / UT
    category: str = "General"  # General, OBC, SC, ST, EWS
    occupation: str = "Student" # Farmer / Agriculture, Student, Unemployed / Jobseeker, Daily Wage Laborer / Construction Worker, Street Vendor / Hawkers, Artisan / Craftsman (Vishwakarma), Self-Employed / Micro Business, Homemaker, Salaried (Private/Public), Senior Citizen / Retired, Fisherfolk / Dairy Farmer
    annual_income: int = 150000 # in INR
    is_specially_abled: bool = False # PwD
    disability_percentage: Optional[int] = None
    is_minority: bool = False
    area_type: str = "rural" # rural, urban, semi-urban
    marital_status: str = "single" # single, married, widowed, divorced_separated
    has_land: bool = False
    land_size_acres: Optional[float] = 0.0
    has_bpl_card: bool = False
    has_girl_child: bool = False
    is_pregnant_lactating: bool = False
    has_senior_dependent: bool = False
    student_education_level: Optional[str] = "Post-Matric" # Pre-Matric, Post-Matric, Undergraduate, Postgraduate, Vocational/ITI, None
    owned_documents: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuestionnaireRequest(BaseModel):
    name: str
    age: int
    gender: str
    state: str
    category: str
    occupation: str
    annual_income: int
    is_specially_abled: bool = False
    disability_percentage: Optional[int] = None
    is_minority: bool = False
    area_type: str = "rural"
    marital_status: str = "single"
    has_land: bool = False
    land_size_acres: Optional[float] = 0.0
    has_bpl_card: bool = False
    has_girl_child: bool = False
    is_pregnant_lactating: bool = False
    has_senior_dependent: bool = False
    student_education_level: Optional[str] = None
    owned_documents: Optional[List[str]] = None

class PersonaInfo(BaseModel):
    persona_code: str
    title: str
    tagline: str
    description: str
    key_sectors: List[str]
    demographic_badge: str
    estimated_schemes_count: int = 0
    estimated_total_benefit: str = "₹0"

class EligibilityResult(BaseModel):
    scheme_id: str
    status: str  # ELIGIBLE, PARTIALLY_ELIGIBLE, INELIGIBLE
    match_score: int  # 0 - 100
    is_fully_eligible: bool
    passed_criteria: List[str]
    missing_criteria: List[str]
    next_action_tip: str
    required_documents_status: List[Dict[str, Any]] # document name, mandatory, is_owned

class CitizenEvaluationResponse(BaseModel):
    profile: CitizenProfile
    persona: PersonaInfo
    total_schemes_evaluated: int
    eligible_count: int
    partially_eligible_count: int
    eligibility_map: Dict[str, EligibilityResult] # scheme_id -> EligibilityResult
