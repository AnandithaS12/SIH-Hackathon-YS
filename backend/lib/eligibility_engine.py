from typing import Dict, Any, List, Tuple
from models.citizen import CitizenProfile, PersonaInfo, EligibilityResult
from models.scheme import Scheme

def determine_persona(profile: CitizenProfile) -> PersonaInfo:
    age = profile.age
    gender = profile.gender.lower()
    occ = profile.occupation.lower()
    income = profile.annual_income
    state = profile.state
    area = profile.area_type.lower()
    cat = profile.category
    
    # 1. Specially Abled Divyangjan
    if profile.is_specially_abled:
        return PersonaInfo(
            persona_code="DIVYANGJAN_HERO",
            title="Divyangjan Citizen Welfare Beneficiary",
            tagline="Empowerment through Accessible Assistive & Financial Schemes",
            description=f"Tailored support for specially-abled citizens across {state}, prioritizing disability pensions, assistive aid grants (ADIP), accessible education, and affirmative employment.",
            key_sectors=["Social Security", "Healthcare", "Education & Skills", "Financial Inclusion & Pension"],
            demographic_badge=f"Divyangjan • {cat} • {state}"
        )
    
    # 2. Senior Citizen
    if age >= 60 or "senior" in occ or "retired" in occ:
        return PersonaInfo(
            persona_code="SENIOR_CITIZEN",
            title="Senior Citizen & Elder Care Beneficiary",
            tagline="Dignified Social Security, Healthcare & Guaranteed Pension",
            description=f"Focused on monthly national pensions (IGNOAPS, Atal Pension), Ayushman Bharat universal elderly cover, Rashtriya Vayoshri assistive equipment, and special railway/banking benefits.",
            key_sectors=["Financial Inclusion & Pension", "Healthcare", "Social Security"],
            demographic_badge=f"Senior (Age {age}) • {gender.title()} • {state}"
        )
    
    # 3. Farmer / Agricultural Worker
    if "farmer" in occ or "agriculture" in occ or "dairy" in occ or "fisher" in occ or profile.has_land:
        return PersonaInfo(
            persona_code="ANNADATA_FARMER",
            title="Krishi & Annadata Agricultural Producer",
            tagline="Direct Income Support, Crop Insurance & Modern Farm Credit",
            description=f"Unlocking ₹6,000/yr PM-KISAN direct cash transfer, Kisan Credit Card (KCC) low-interest loans, PM Fasal Bima crop cover, solar pump subsidies (KUSUM), and Soil Health initiatives in {state}.",
            key_sectors=["Agriculture", "Financial Inclusion & Pension", "Social Security"],
            demographic_badge=f"Farmer • {area.title()} • {state}"
        )
        
    # 4. Traditional Artisan / Craftsman (Vishwakarma)
    if "artisan" in occ or "craftsman" in occ or "vishwakarma" in occ:
        return PersonaInfo(
            persona_code="VISHWAKARMA_ARTISAN",
            title="Traditional Artisan & Skilled Craftsman (Vishwakarma)",
            tagline="₹3 Lakh Collateral-Free Loans @ 5%, ₹15,000 Toolkit Grant & Skill Upgrades",
            description=f"Special recognition for 18 traditional trade masters (carpenters, blacksmiths, goldsmiths, potters, cobblers, weavers) with PM Vishwakarma ID, modern tool vouchers, and credit support.",
            key_sectors=["Employment & MSME", "Financial Inclusion & Pension", "Education & Skills"],
            demographic_badge=f"Artisan • {cat} • {state}"
        )
        
    # 5. Street Vendor / Micro Enterprise
    if "vendor" in occ or "hawker" in occ:
        return PersonaInfo(
            persona_code="SVANIDHI_VENDOR",
            title="Urban/Semi-Urban Street Vendor & Micro-Merchant",
            tagline="Working Capital Loans up to ₹50,000 with Cashback & Digital Incentives",
            description=f"Directly eligible for PM SVANidhi working capital micro-credit with 7% interest subsidy, PM Mudra Shishu loans, and Jan Dhan overdraft facilities in {state}.",
            key_sectors=["Financial Inclusion & Pension", "Employment & MSME", "Social Security"],
            demographic_badge=f"Micro Vendor • {area.title()} • {state}"
        )
        
    # 6. Student / Youth Jobseeker
    if "student" in occ or "unemployed" in occ or "jobseeker" in occ or (age <= 25 and occ not in ["salaried", "business"]):
        education = profile.student_education_level or "College/Higher Ed"
        return PersonaInfo(
            persona_code="YOUTH_SCHOLAR",
            title="Youth Aspirant & Future Builder",
            tagline="Higher-Education Scholarships, Free Skill Certifications & Career Grants",
            description=f"Comprehensive coverage for National Scholarships (Post-Matric, Merit-cum-Means), free PMKVY 4.0 technical certifications, Yuva internship stipend programs, and Mudra/Stand-Up India start-up capital.",
            key_sectors=["Education & Skills", "Employment & MSME", "Social Security"],
            demographic_badge=f"Student/Youth (Age {age}) • {education} • {state}"
        )

    # 7. Women Homemaker / Aspiring Female Entrepreneur
    if gender == "female":
        if profile.is_pregnant_lactating:
            return PersonaInfo(
                persona_code="MATRU_SHAKTI",
                title="Maternal Health & Nutrition Beneficiary",
                tagline="Direct Maternity Cash Transfer & High-Nutrition Child Care Support",
                description=f"Full entitlement for PM Matru Vandana Yojana (₹5,000 - ₹6,000 cash for nutrition), Poshan Abhiyaan ration kits, and free Institutional Delivery under Janani Suraksha Yojana in {state}.",
                key_sectors=["Women & Child", "Healthcare", "Social Security"],
                demographic_badge=f"Maternal Care • {state}"
            )
        return PersonaInfo(
            persona_code="NARI_SHAKTI",
            title="Nari Shakti & Women Empowerment Beneficiary",
            tagline="Interest-Free SHG Credit, Free LPG Connection & Enterprise Subsidies",
            description=f"Unlocking Lakhpati Didi micro-business credit up to ₹5 Lakhs, PM Ujjwala free LPG connection, Stand-Up India women entrepreneurship collateral-free loans, and state-level cash schemes.",
            key_sectors=["Women & Child", "Employment & MSME", "Healthcare", "Housing & Sanitation"],
            demographic_badge=f"Women Leader • {cat} • {area.title()}"
        )

    # 8. Unorganized / Daily Wage Laborer
    if "labor" in occ or "construction" in occ or "wage" in occ or profile.has_bpl_card or income <= 120000:
        return PersonaInfo(
            persona_code="SHRAMIK_CITIZEN",
            title="Shramik & Unorganized Worker Family",
            tagline="MGNREGA 100-Day Wage Guarantee, ₹5 Lakh Free Health Cover & Housing Grant",
            description=f"Prioritized for PM Awas Yojana house building grant (₹1.2 - 2.5 Lakhs), e-Shram accident insurance, Ayushman Bharat health card, and PM Suraksha Bima insurance.",
            key_sectors=["Housing & Sanitation", "Healthcare", "Social Security", "Employment & MSME"],
            demographic_badge=f"Shramik • {cat} • {area.title()}"
        )

    # 9. Micro-Enterprise / Self-Employed
    if "self" in occ or "business" in occ:
        return PersonaInfo(
            persona_code="MSME_ENTREPRENEUR",
            title="Self-Employed & MSME Business Innovator",
            tagline="Mudra Loans up to ₹20 Lakhs, PMEGP 35% Capital Subsidy & CGTMSE Guarantee",
            description=f"Priority access to PM Mudra Yojana (Shishu, Kishore, Tarun), Prime Minister Employment Generation Programme (PMEGP) manufacturing/service setup subsidies, and MSME Samadhaan.",
            key_sectors=["Employment & MSME", "Financial Inclusion & Pension"],
            demographic_badge=f"Entrepreneur • {area.title()} • {state}"
        )

    # 10. General Citizen & Family
    return PersonaInfo(
        persona_code="CITIZEN_GENERAL",
        title="Active Citizen & Family Welfare Beneficiary",
        tagline="Universal Healthcare, Subsidized Housing & Social Insurance Protection",
        description=f"Accessing PM-JAY Ayushman Card (₹5 Lakhs/family hospital coverage), PM Jeevan Jyoti life cover (₹2 Lakhs for ₹436/yr), Atal Pension Yojana, and digital governance schemes in {state}.",
        key_sectors=["Healthcare", "Financial Inclusion & Pension", "Housing & Sanitation", "Social Security"],
        demographic_badge=f"Citizen • Age {age} • {state}"
    )


def evaluate_scheme_eligibility(scheme: Scheme, profile: CitizenProfile) -> EligibilityResult:
    rules = scheme.eligibility_rules
    passed_criteria: List[str] = []
    missing_criteria: List[str] = []
    is_partially_eligible = False
    # Hard blockers can never soften to PARTIALLY_ELIGIBLE — a Karnataka-only scheme is simply
    # not available to a Bihar resident, and a Divyangjan-only scheme not to a non-PwD applicant.
    hard_blockers: List[str] = []
    
    # 1. State check
    if rules.state_restriction and "All" not in rules.state_restriction:
        if profile.state not in rules.state_restriction and "All" not in scheme.applicable_states:
            blocker = f"Scheme is specifically restricted to: {', '.join(rules.state_restriction)} (your selected state is {profile.state})"
            missing_criteria.append(blocker)
            hard_blockers.append(blocker)
        else:
            passed_criteria.append(f"Applicable in your state ({profile.state})")
    else:
        passed_criteria.append("Pan-India / Central Scheme (Open to all States & UTs)")

    # 2. Age check
    if rules.min_age is not None and rules.max_age is not None:
        if profile.age < rules.min_age:
            missing_criteria.append(f"Requires minimum age of {rules.min_age} years (current age: {profile.age})")
        elif profile.age > rules.max_age:
            missing_criteria.append(f"Requires maximum age of {rules.max_age} years (current age: {profile.age})")
        else:
            passed_criteria.append(f"Age {profile.age} is within eligible bracket ({rules.min_age} - {rules.max_age} years)")
    elif rules.min_age is not None:
        if profile.age < rules.min_age:
            missing_criteria.append(f"Requires minimum age of {rules.min_age} years (current age: {profile.age})")
        else:
            passed_criteria.append(f"Age {profile.age} satisfies minimum requirement ({rules.min_age}+ years)")
    elif rules.max_age is not None:
        if profile.age > rules.max_age:
            missing_criteria.append(f"Requires maximum age of {rules.max_age} years (current age: {profile.age})")
        else:
            passed_criteria.append(f"Age {profile.age} is within maximum limit (up to {rules.max_age} years)")

    # 3. Gender check
    scheme_genders = [g.lower() for g in rules.genders]
    if "any" not in scheme_genders and "all" not in scheme_genders:
        user_gender = profile.gender.lower()
        if user_gender not in scheme_genders:
            blocker = f"Exclusively for {', '.join(rules.genders).title()} applicants"
            missing_criteria.append(blocker)
            hard_blockers.append(blocker)
        else:
            passed_criteria.append(f"Gender ({profile.gender.title()}) matches target beneficiary criteria")

    # 4. Social Category (SC/ST/OBC/EWS/General)
    scheme_cats = rules.categories
    if "All" not in scheme_cats and "any" not in [c.lower() for c in scheme_cats]:
        if profile.category not in scheme_cats:
            missing_criteria.append(f"Targeted for {', '.join(scheme_cats)} categories (your category: {profile.category})")
        else:
            passed_criteria.append(f"Category {profile.category} is explicitly targeted")
    else:
        passed_criteria.append("Open to all social categories (General, OBC, SC, ST, EWS)")

    # 5. Occupation check
    scheme_occs = rules.occupations
    if "All" not in scheme_occs and "any" not in [o.lower() for o in scheme_occs]:
        occ_lower = profile.occupation.lower()
        # check semantic matches
        matches_occ = False
        for target_occ in scheme_occs:
            t_low = target_occ.lower()
            if t_low in occ_lower or occ_lower in t_low:
                matches_occ = True
                break
            if "farmer" in t_low and ("farmer" in occ_lower or "agriculture" in occ_lower or profile.has_land):
                matches_occ = True
                break
            if "artisan" in t_low and ("artisan" in occ_lower or "craftsman" in occ_lower or "vishwakarma" in occ_lower):
                matches_occ = True
                break
            if "student" in t_low and ("student" in occ_lower or "scholar" in occ_lower or (profile.age <= 25 and occ_lower == "unemployed / jobseeker")):
                matches_occ = True
                break
            if "vendor" in t_low and ("vendor" in occ_lower or "hawker" in occ_lower):
                matches_occ = True
                break
            if "labor" in t_low and ("labor" in occ_lower or "wage" in occ_lower or "construction" in occ_lower):
                matches_occ = True
                break
            if "entrepreneur" in t_low and ("self-employed" in occ_lower or "business" in occ_lower or "vendor" in occ_lower):
                matches_occ = True
                break
            if "women" in t_low and profile.gender.lower() == "female":
                matches_occ = True
                break
                
        if matches_occ:
            passed_criteria.append(f"Occupation ({profile.occupation}) qualifies for targeted benefits")
        else:
            # Check if this is a primary mismatch or secondary
            missing_criteria.append(f"Targeted primarily for: {', '.join(scheme_occs)}")

    # 6. Income check
    if rules.max_annual_income is not None:
        if profile.annual_income > rules.max_annual_income:
            # If slightly over, might be partially eligible
            if profile.annual_income <= rules.max_annual_income * 1.3:
                is_partially_eligible = True
                missing_criteria.append(f"Annual income ceiling is ₹{rules.max_annual_income:,} (declared income: ₹{profile.annual_income:,}) - income certificate required")
            else:
                missing_criteria.append(f"Income ₹{profile.annual_income:,} exceeds maximum limit of ₹{rules.max_annual_income:,}/year")
        else:
            passed_criteria.append(f"Annual income ₹{profile.annual_income:,} satisfies the income ceiling (≤ ₹{rules.max_annual_income:,})")

    # 7. Land requirement (for farm schemes)
    if rules.requires_land is True:
        if not profile.has_land and "farmer" not in profile.occupation.lower():
            missing_criteria.append("Requires ownership/cultivation of agricultural land (RoR / 7-12 record)")
        else:
            passed_criteria.append("Landholder / agricultural practitioner requirement met")

    # 8. BPL requirement
    if rules.requires_bpl is True:
        if not profile.has_bpl_card and profile.annual_income > 180000:
            is_partially_eligible = True
            missing_criteria.append("Requires BPL / Antyodaya / Ration Card or SECC low-income inclusion")
        else:
            passed_criteria.append("Low-income / BPL economic requirement satisfied")

    # 9. Disability requirement
    if rules.requires_disability is True:
        if not profile.is_specially_abled:
            blocker = "Exclusively for Persons with Disabilities (UDID card / 40%+ benchmark)"
            missing_criteria.append(blocker)
            hard_blockers.append(blocker)
        else:
            passed_criteria.append(f"Divyangjan / Specially-Abled status confirmed ({profile.disability_percentage or 40}% benchmark)")

    # 10. Minority requirement
    if rules.requires_minority is True:
        if not profile.is_minority:
            blocker = "Reserved for Notified National Minority Communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi)"
            missing_criteria.append(blocker)
            hard_blockers.append(blocker)
        else:
            passed_criteria.append("National Minority Community eligibility met")

    # 11. Area type requirement
    if rules.area_type and rules.area_type != "any":
        if profile.area_type.lower() != rules.area_type.lower():
            blocker = f"Restricted to {rules.area_type.title()} areas (your location is {profile.area_type.title()})"
            missing_criteria.append(blocker)
            # Semi-urban applicants sit on the boundary, so treat that as soft, not decisive.
            if profile.area_type.lower() != "semi-urban":
                hard_blockers.append(blocker)
        else:
            passed_criteria.append(f"Location in {profile.area_type.title()} area is eligible")

    # 12. Pregnant / Lactating requirement
    if rules.requires_pregnant_lactating is True:
        if not profile.is_pregnant_lactating and profile.gender.lower() == "female":
            is_partially_eligible = True
            missing_criteria.append("Requires current Pregnancy or Lactating Mother status with MCP Card")
        elif profile.gender.lower() != "female":
            missing_criteria.append("Requires Female applicant with active Maternity / Pregnancy registration")
        else:
            passed_criteria.append("Maternal / Lactating registration confirmed")

    # 13. Girl Child requirement
    if rules.requires_girl_child is True:
        if not profile.has_girl_child and profile.gender.lower() != "female" and profile.age > 10:
            missing_criteria.append("Requires girl child under 10 years of age in the family")
        else:
            passed_criteria.append("Girl child entitlement confirmed")

    # Map Document readiness
    user_docs = set(d.lower().strip() for d in (profile.owned_documents or []))
    doc_statuses: List[Dict[str, Any]] = []
    
    for doc in scheme.required_documents:
        d_name_low = doc.name.lower()
        is_owned = any(k in user_docs for k in [
            d_name_low,
            doc.name.lower(),
            "aadhaar" if "aadhaar" in d_name_low else "---",
            "bank" if "bank" in d_name_low or "passbook" in d_name_low else "---",
            "ration" if "ration" in d_name_low or "bpl" in d_name_low else "---",
            "income" if "income" in d_name_low else "---",
            "caste" if "caste" in d_name_low else "---",
            "land" if "land" in d_name_low or "7/12" in d_name_low or "khatauni" in d_name_low or "ror" in d_name_low else "---",
            "disability" if "disability" in d_name_low or "udid" in d_name_low else "---",
            "marksheet" if "marksheet" in d_name_low or "education" in d_name_low or "college" in d_name_low else "---",
            "domicile" if "domicile" in d_name_low or "residence" in d_name_low else "---",
            "photo" if "photo" in d_name_low else "---"
        ])
        doc_statuses.append({
            "name": doc.name,
            "mandatory": doc.mandatory,
            "description": doc.description,
            "is_owned": is_owned,
            "how_to_get": doc.how_to_get
        })

    # Final scoring and status calculation
    total_checks = len(passed_criteria) + len(missing_criteria)
    if total_checks == 0:
        match_score = 100
    else:
        match_score = int((len(passed_criteria) / total_checks) * 100)

    # Determine status. A hard blocker (wrong state, wrong gender, non-PwD on a PwD-only scheme,
    # wrong area) is decisive and can never be reported as a partial/likely match.
    if len(missing_criteria) == 0:
        status = "ELIGIBLE"
        is_fully_eligible = True
        next_action_tip = f"You satisfy all criteria! Have your {scheme.required_documents[0].name if scheme.required_documents else 'Aadhaar'} ready and apply directly on the official portal."
    elif hard_blockers:
        status = "INELIGIBLE"
        is_fully_eligible = False
        next_action_tip = f"Not eligible: {hard_blockers[0]}"
    elif len(missing_criteria) == 1 and is_partially_eligible:
        status = "PARTIALLY_ELIGIBLE"
        is_fully_eligible = False
        next_action_tip = f"Conditional match: review the requirement for '{missing_criteria[0]}' to unlock full benefits."
    elif len(missing_criteria) <= 2 and match_score >= 60:
        status = "PARTIALLY_ELIGIBLE"
        is_fully_eligible = False
        next_action_tip = "Check supporting document verification to confirm your application status."
    else:
        status = "INELIGIBLE"
        is_fully_eligible = False
        next_action_tip = f"Not directly eligible due to: {missing_criteria[0] if missing_criteria else 'eligibility criteria'}"

    return EligibilityResult(
        scheme_id=scheme.id,
        status=status,
        match_score=match_score,
        is_fully_eligible=is_fully_eligible,
        passed_criteria=passed_criteria,
        missing_criteria=missing_criteria,
        next_action_tip=next_action_tip,
        required_documents_status=doc_statuses
    )
