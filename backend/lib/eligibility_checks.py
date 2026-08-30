"""Individual eligibility criterion checks.

Each `_check_*` function inspects exactly one rule and records its verdict on the
shared `CheckResult`. Splitting them this way keeps every rule independently
readable and testable, and makes the evaluation order in
`eligibility_engine.CRITERION_CHECKS` explicit.

A "hard blocker" is a mismatch that can never soften into PARTIALLY_ELIGIBLE — a
Karnataka-only scheme is simply unavailable to a Bihar resident.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from models.citizen import CitizenProfile
from models.scheme import EligibilityRules, Scheme

# A citizen up to this multiple over the income ceiling is treated as a
# conditional (documents-dependent) match rather than an outright rejection.
INCOME_GRACE_MULTIPLIER = 1.3
# Above this income we stop treating a missing BPL card as a soft condition.
BPL_SOFT_INCOME_CEILING = 180000


@dataclass
class CheckResult:
    passed: List[str] = field(default_factory=list)
    missing: List[str] = field(default_factory=list)
    hard_blockers: List[str] = field(default_factory=list)
    # Set when a mismatch is conditional (e.g. income slightly over ceiling).
    is_conditional: bool = False

    def ok(self, message: str) -> None:
        self.passed.append(message)

    def fail(self, message: str) -> None:
        self.missing.append(message)

    def block(self, message: str) -> None:
        """A decisive mismatch: recorded as missing AND as a hard blocker."""
        self.missing.append(message)
        self.hard_blockers.append(message)


def _check_state(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if rules.state_restriction and "All" not in rules.state_restriction:
        if p.state not in rules.state_restriction and "All" not in scheme.applicable_states:
            r.block(
                f"Scheme is specifically restricted to: {', '.join(rules.state_restriction)} (your selected state is {p.state})"
            )
        else:
            r.ok(f"Applicable in your state ({p.state})")
    else:
        r.ok("Pan-India / Central Scheme (Open to all States & UTs)")


def _check_age(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    has_min = rules.min_age is not None
    has_max = rules.max_age is not None

    if has_min and has_max:
        if p.age < rules.min_age:
            r.fail(f"Requires minimum age of {rules.min_age} years (current age: {p.age})")
        elif p.age > rules.max_age:
            r.fail(f"Requires maximum age of {rules.max_age} years (current age: {p.age})")
        else:
            r.ok(f"Age {p.age} is within eligible bracket ({rules.min_age} - {rules.max_age} years)")
    elif has_min:
        if p.age < rules.min_age:
            r.fail(f"Requires minimum age of {rules.min_age} years (current age: {p.age})")
        else:
            r.ok(f"Age {p.age} satisfies minimum requirement ({rules.min_age}+ years)")
    elif has_max:
        if p.age > rules.max_age:
            r.fail(f"Requires maximum age of {rules.max_age} years (current age: {p.age})")
        else:
            r.ok(f"Age {p.age} is within maximum limit (up to {rules.max_age} years)")


def _check_gender(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    scheme_genders = [g.lower() for g in rules.genders]
    if "any" in scheme_genders or "all" in scheme_genders:
        return
    if p.gender.lower() not in scheme_genders:
        r.block(f"Exclusively for {', '.join(rules.genders).title()} applicants")
    else:
        r.ok(f"Gender ({p.gender.title()}) matches target beneficiary criteria")


def _check_category(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    scheme_cats = rules.categories
    if "All" in scheme_cats or "any" in [c.lower() for c in scheme_cats]:
        r.ok("Open to all social categories (General, OBC, SC, ST, EWS)")
        return
    if p.category not in scheme_cats:
        r.fail(f"Targeted for {', '.join(scheme_cats)} categories (your category: {p.category})")
    else:
        r.ok(f"Category {p.category} is explicitly targeted")


# Semantic aliases so "Farmer / Agriculture" matches a scheme targeting "Farmer",
# "Unemployed / Jobseeker" (if young) matches "Student", and so on.
def _occupation_matches(target: str, p: CitizenProfile) -> bool:
    t = target.lower()
    occ = p.occupation.lower()

    if t in occ or occ in t:
        return True
    if "farmer" in t and ("farmer" in occ or "agriculture" in occ or p.has_land):
        return True
    if "artisan" in t and ("artisan" in occ or "craftsman" in occ or "vishwakarma" in occ):
        return True
    if "student" in t and (
        "student" in occ
        or "scholar" in occ
        or (p.age <= 25 and occ == "unemployed / jobseeker")
    ):
        return True
    if "vendor" in t and ("vendor" in occ or "hawker" in occ):
        return True
    if "labor" in t and ("labor" in occ or "wage" in occ or "construction" in occ):
        return True
    if "entrepreneur" in t and ("self-employed" in occ or "business" in occ or "vendor" in occ):
        return True
    if "women" in t and p.gender.lower() == "female":
        return True
    return False


def _check_occupation(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    scheme_occs = rules.occupations
    if "All" in scheme_occs or "any" in [o.lower() for o in scheme_occs]:
        return

    if any(_occupation_matches(target, p) for target in scheme_occs):
        r.ok(f"Occupation ({p.occupation}) qualifies for targeted benefits")
    else:
        r.fail(f"Targeted primarily for: {', '.join(scheme_occs)}")


def _check_income(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    ceiling = rules.max_annual_income
    if ceiling is None:
        return

    if p.annual_income > ceiling:
        if p.annual_income <= ceiling * INCOME_GRACE_MULTIPLIER:
            r.is_conditional = True
            r.fail(
                f"Annual income ceiling is ₹{ceiling:,} (declared income: ₹{p.annual_income:,}) - income certificate required"
            )
        else:
            r.fail(f"Income ₹{p.annual_income:,} exceeds maximum limit of ₹{ceiling:,}/year")
    else:
        r.ok(f"Annual income ₹{p.annual_income:,} satisfies the income ceiling (≤ ₹{ceiling:,})")


def _check_land(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.requires_land:
        return
    if not p.has_land and "farmer" not in p.occupation.lower():
        r.fail("Requires ownership/cultivation of agricultural land (RoR / 7-12 record)")
    else:
        r.ok("Landholder / agricultural practitioner requirement met")


def _check_bpl(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.requires_bpl:
        return
    if not p.has_bpl_card and p.annual_income > BPL_SOFT_INCOME_CEILING:
        r.is_conditional = True
        r.fail("Requires BPL / Antyodaya / Ration Card or SECC low-income inclusion")
    else:
        r.ok("Low-income / BPL economic requirement satisfied")


def _check_disability(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.requires_disability:
        return
    if not p.is_specially_abled:
        r.block("Exclusively for Persons with Disabilities (UDID card / 40%+ benchmark)")
    else:
        r.ok(
            f"Divyangjan / Specially-Abled status confirmed ({p.disability_percentage or 40}% benchmark)"
        )


def _check_minority(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.requires_minority:
        return
    if not p.is_minority:
        r.block(
            "Reserved for Notified National Minority Communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi)"
        )
    else:
        r.ok("National Minority Community eligibility met")


def _check_area(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.area_type or rules.area_type == "any":
        return
    if p.area_type.lower() != rules.area_type.lower():
        message = f"Restricted to {rules.area_type.title()} areas (your location is {p.area_type.title()})"
        # Semi-urban applicants sit on the rural/urban boundary — treat as soft.
        if p.area_type.lower() == "semi-urban":
            r.fail(message)
        else:
            r.block(message)
    else:
        r.ok(f"Location in {p.area_type.title()} area is eligible")


def _check_pregnancy(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.requires_pregnant_lactating:
        return
    if not p.is_pregnant_lactating and p.gender.lower() == "female":
        r.is_conditional = True
        r.fail("Requires current Pregnancy or Lactating Mother status with MCP Card")
    elif p.gender.lower() != "female":
        r.fail("Requires Female applicant with active Maternity / Pregnancy registration")
    else:
        r.ok("Maternal / Lactating registration confirmed")


def _check_girl_child(rules: EligibilityRules, p: CitizenProfile, r: CheckResult, scheme: Scheme) -> None:
    if not rules.requires_girl_child:
        return
    if not p.has_girl_child and p.gender.lower() != "female" and p.age > 10:
        r.fail("Requires girl child under 10 years of age in the family")
    else:
        r.ok("Girl child entitlement confirmed")


# Evaluation order is part of the contract — the first missing criterion is shown
# to the citizen as the headline reason, so this sequence must stay stable.
CRITERION_CHECKS = [
    _check_state,
    _check_age,
    _check_gender,
    _check_category,
    _check_occupation,
    _check_income,
    _check_land,
    _check_bpl,
    _check_disability,
    _check_minority,
    _check_area,
    _check_pregnancy,
    _check_girl_child,
]

# Keyword aliases used to decide whether a citizen's ticked document satisfies a
# scheme's required document (names differ across schemes for the same paper).
_DOCUMENT_ALIASES = (
    ("aadhaar", ("aadhaar",)),
    ("bank", ("bank", "passbook")),
    ("ration", ("ration", "bpl")),
    ("income", ("income",)),
    ("caste", ("caste",)),
    ("land", ("land", "7/12", "khatauni", "ror")),
    ("disability", ("disability", "udid")),
    ("marksheet", ("marksheet", "education", "college")),
    ("domicile", ("domicile", "residence")),
    ("photo", ("photo",)),
)


def build_document_status(scheme: Scheme, p: CitizenProfile) -> List[Dict[str, Any]]:
    """Mark each required document as owned or still to be collected."""
    owned = {d.lower().strip() for d in (p.owned_documents or [])}
    statuses: List[Dict[str, Any]] = []

    for doc in scheme.required_documents:
        name_low = doc.name.lower()
        keys = {name_low}
        for alias_key, needles in _DOCUMENT_ALIASES:
            if any(n in name_low for n in needles):
                keys.add(alias_key)

        statuses.append(
            {
                "name": doc.name,
                "mandatory": doc.mandatory,
                "description": doc.description,
                "is_owned": any(k in owned for k in keys),
                "how_to_get": doc.how_to_get,
            }
        )

    return statuses
