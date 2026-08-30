"""Persona classification for a citizen profile.

Rules are evaluated in priority order — the first match wins — so that the most
specific, benefit-dense identity (e.g. Divyangjan, senior citizen) is chosen over
a broader one. Keeping them as an ordered list of (predicate, builder) pairs makes
the precedence explicit and each rule independently testable.
"""

from typing import Callable, List, Tuple

from models.citizen import CitizenProfile, PersonaInfo

PersonaPredicate = Callable[[CitizenProfile], bool]
PersonaBuilder = Callable[[CitizenProfile], PersonaInfo]


def _is_divyangjan(p: CitizenProfile) -> bool:
    return p.is_specially_abled


def _is_senior(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return p.age >= 60 or "senior" in occ or "retired" in occ


def _is_farmer(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return (
        "farmer" in occ
        or "agriculture" in occ
        or "dairy" in occ
        or "fisher" in occ
        or p.has_land
    )


def _is_artisan(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return "artisan" in occ or "craftsman" in occ or "vishwakarma" in occ


def _is_vendor(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return "vendor" in occ or "hawker" in occ


def _is_youth(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return (
        "student" in occ
        or "unemployed" in occ
        or "jobseeker" in occ
        or (p.age <= 25 and occ not in ["salaried", "business"])
    )


def _is_maternal(p: CitizenProfile) -> bool:
    return p.gender.lower() == "female" and p.is_pregnant_lactating


def _is_woman(p: CitizenProfile) -> bool:
    return p.gender.lower() == "female"


def _is_shramik(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return (
        "labor" in occ
        or "construction" in occ
        or "wage" in occ
        or p.has_bpl_card
        or p.annual_income <= 120000
    )


def _is_msme(p: CitizenProfile) -> bool:
    occ = p.occupation.lower()
    return "self" in occ or "business" in occ


# --- Builders -------------------------------------------------------------


def _divyangjan(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="DIVYANGJAN_HERO",
        title="Divyangjan Citizen Welfare Beneficiary",
        tagline="Empowerment through Accessible Assistive & Financial Schemes",
        description=f"Tailored support for specially-abled citizens across {p.state}, prioritizing disability pensions, assistive aid grants (ADIP), accessible education, and affirmative employment.",
        key_sectors=["Social Security", "Healthcare", "Education & Skills", "Financial Inclusion & Pension"],
        demographic_badge=f"Divyangjan • {p.category} • {p.state}",
    )


def _senior(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="SENIOR_CITIZEN",
        title="Senior Citizen & Elder Care Beneficiary",
        tagline="Dignified Social Security, Healthcare & Guaranteed Pension",
        description="Focused on monthly national pensions (IGNOAPS, Atal Pension), Ayushman Bharat universal elderly cover, Rashtriya Vayoshri assistive equipment, and special railway/banking benefits.",
        key_sectors=["Financial Inclusion & Pension", "Healthcare", "Social Security"],
        demographic_badge=f"Senior (Age {p.age}) • {p.gender.lower().title()} • {p.state}",
    )


def _farmer(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="ANNADATA_FARMER",
        title="Krishi & Annadata Agricultural Producer",
        tagline="Direct Income Support, Crop Insurance & Modern Farm Credit",
        description=f"Unlocking ₹6,000/yr PM-KISAN direct cash transfer, Kisan Credit Card (KCC) low-interest loans, PM Fasal Bima crop cover, solar pump subsidies (KUSUM), and Soil Health initiatives in {p.state}.",
        key_sectors=["Agriculture", "Financial Inclusion & Pension", "Social Security"],
        demographic_badge=f"Farmer • {p.area_type.lower().title()} • {p.state}",
    )


def _artisan(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="VISHWAKARMA_ARTISAN",
        title="Traditional Artisan & Skilled Craftsman (Vishwakarma)",
        tagline="₹3 Lakh Collateral-Free Loans @ 5%, ₹15,000 Toolkit Grant & Skill Upgrades",
        description="Special recognition for 18 traditional trade masters (carpenters, blacksmiths, goldsmiths, potters, cobblers, weavers) with PM Vishwakarma ID, modern tool vouchers, and credit support.",
        key_sectors=["Employment & MSME", "Financial Inclusion & Pension", "Education & Skills"],
        demographic_badge=f"Artisan • {p.category} • {p.state}",
    )


def _vendor(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="SVANIDHI_VENDOR",
        title="Urban/Semi-Urban Street Vendor & Micro-Merchant",
        tagline="Working Capital Loans up to ₹50,000 with Cashback & Digital Incentives",
        description=f"Directly eligible for PM SVANidhi working capital micro-credit with 7% interest subsidy, PM Mudra Shishu loans, and Jan Dhan overdraft facilities in {p.state}.",
        key_sectors=["Financial Inclusion & Pension", "Employment & MSME", "Social Security"],
        demographic_badge=f"Micro Vendor • {p.area_type.lower().title()} • {p.state}",
    )


def _youth(p: CitizenProfile) -> PersonaInfo:
    education = p.student_education_level or "College/Higher Ed"
    return PersonaInfo(
        persona_code="YOUTH_SCHOLAR",
        title="Youth Aspirant & Future Builder",
        tagline="Higher-Education Scholarships, Free Skill Certifications & Career Grants",
        description="Comprehensive coverage for National Scholarships (Post-Matric, Merit-cum-Means), free PMKVY 4.0 technical certifications, Yuva internship stipend programs, and Mudra/Stand-Up India start-up capital.",
        key_sectors=["Education & Skills", "Employment & MSME", "Social Security"],
        demographic_badge=f"Student/Youth (Age {p.age}) • {education} • {p.state}",
    )


def _maternal(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="MATRU_SHAKTI",
        title="Maternal Health & Nutrition Beneficiary",
        tagline="Direct Maternity Cash Transfer & High-Nutrition Child Care Support",
        description=f"Full entitlement for PM Matru Vandana Yojana (₹5,000 - ₹6,000 cash for nutrition), Poshan Abhiyaan ration kits, and free Institutional Delivery under Janani Suraksha Yojana in {p.state}.",
        key_sectors=["Women & Child", "Healthcare", "Social Security"],
        demographic_badge=f"Maternal Care • {p.state}",
    )


def _woman(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="NARI_SHAKTI",
        title="Nari Shakti & Women Empowerment Beneficiary",
        tagline="Interest-Free SHG Credit, Free LPG Connection & Enterprise Subsidies",
        description="Unlocking Lakhpati Didi micro-business credit up to ₹5 Lakhs, PM Ujjwala free LPG connection, Stand-Up India women entrepreneurship collateral-free loans, and state-level cash schemes.",
        key_sectors=["Women & Child", "Employment & MSME", "Healthcare", "Housing & Sanitation"],
        demographic_badge=f"Women Leader • {p.category} • {p.area_type.lower().title()}",
    )


def _shramik(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="SHRAMIK_CITIZEN",
        title="Shramik & Unorganized Worker Family",
        tagline="MGNREGA 100-Day Wage Guarantee, ₹5 Lakh Free Health Cover & Housing Grant",
        description="Prioritized for PM Awas Yojana house building grant (₹1.2 - 2.5 Lakhs), e-Shram accident insurance, Ayushman Bharat health card, and PM Suraksha Bima insurance.",
        key_sectors=["Housing & Sanitation", "Healthcare", "Social Security", "Employment & MSME"],
        demographic_badge=f"Shramik • {p.category} • {p.area_type.lower().title()}",
    )


def _msme(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="MSME_ENTREPRENEUR",
        title="Self-Employed & MSME Business Innovator",
        tagline="Mudra Loans up to ₹20 Lakhs, PMEGP 35% Capital Subsidy & CGTMSE Guarantee",
        description="Priority access to PM Mudra Yojana (Shishu, Kishore, Tarun), Prime Minister Employment Generation Programme (PMEGP) manufacturing/service setup subsidies, and MSME Samadhaan.",
        key_sectors=["Employment & MSME", "Financial Inclusion & Pension"],
        demographic_badge=f"Entrepreneur • {p.area_type.lower().title()} • {p.state}",
    )


def _general(p: CitizenProfile) -> PersonaInfo:
    return PersonaInfo(
        persona_code="CITIZEN_GENERAL",
        title="Active Citizen & Family Welfare Beneficiary",
        tagline="Universal Healthcare, Subsidized Housing & Social Insurance Protection",
        description=f"Accessing PM-JAY Ayushman Card (₹5 Lakhs/family hospital coverage), PM Jeevan Jyoti life cover (₹2 Lakhs for ₹436/yr), Atal Pension Yojana, and digital governance schemes in {p.state}.",
        key_sectors=["Healthcare", "Financial Inclusion & Pension", "Housing & Sanitation", "Social Security"],
        demographic_badge=f"Citizen • Age {p.age} • {p.state}",
    )


# Highest priority first.
PERSONA_RULES: List[Tuple[PersonaPredicate, PersonaBuilder]] = [
    (_is_divyangjan, _divyangjan),
    (_is_senior, _senior),
    (_is_farmer, _farmer),
    (_is_artisan, _artisan),
    (_is_vendor, _vendor),
    (_is_youth, _youth),
    (_is_maternal, _maternal),
    (_is_woman, _woman),
    (_is_shramik, _shramik),
    (_is_msme, _msme),
]


def determine_persona(profile: CitizenProfile) -> PersonaInfo:
    for matches, build in PERSONA_RULES:
        if matches(profile):
            return build(profile)
    return _general(profile)
