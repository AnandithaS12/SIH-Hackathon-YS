from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from lib.db import db
from models.citizen import CitizenProfile, QuestionnaireRequest, CitizenEvaluationResponse
from models.scheme import Scheme
from lib.eligibility_engine import determine_persona, evaluate_scheme_eligibility

router = APIRouter(prefix="/citizens", tags=["citizens"])

INDIAN_STATES_AND_UTS = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi (NCT)", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

OCCUPATIONS = [
    {"id": "farmer", "label": "Farmer / Agriculture (कृषक)", "icon": "Sprout"},
    {"id": "student", "label": "Student / Youth (विद्यार्थी / युवा)", "icon": "GraduationCap"},
    {"id": "artisan", "label": "Artisan / Craftsman (विश्वकर्मा / कारीगर)", "icon": "Hammer"},
    {"id": "vendor", "label": "Street Vendor / Hawker (स्ट्रीट वेंडर / रेहड़ी पटरी)", "icon": "Store"},
    {"id": "labor", "label": "Daily Wage Laborer / Shramik (दैनिक वेतनभोगी / श्रमिक)", "icon": "HardHat"},
    {"id": "business", "label": "Self-Employed / Micro Business (स्वरोजगार / सूक्ष्म उद्यम)", "icon": "Briefcase"},
    {"id": "homemaker", "label": "Homemaker / Woman Leader (गृहिणी / महिला)", "icon": "Heart"},
    {"id": "senior", "label": "Senior Citizen / Retired (वरिष्ठ नागरिक / सेवानिवृत्त)", "icon": "Users"},
    {"id": "dairy_fisher", "label": "Dairy / Animal Husbandry / Fisherfolk (पशुपालन / मत्स्य पालक)", "icon": "Fish"},
    {"id": "salaried", "label": "Salaried (Private / Public) (वेतनभोगी कर्मचारी)", "icon": "Building"},
    {"id": "unemployed", "label": "Unemployed / Jobseeker (बेरोजगार / रोजगार आकांक्षी)", "icon": "UserCheck"}
]

SOCIAL_CATEGORIES = ["General", "OBC", "SC", "ST", "EWS"]

@router.get("/metadata")
async def get_metadata():
    return {
        "states": INDIAN_STATES_AND_UTS,
        "occupations": OCCUPATIONS,
        "categories": SOCIAL_CATEGORIES,
        "education_levels": [
            "Pre-Matric (Class 1-10)",
            "Post-Matric (Class 11-12)",
            "Undergraduate Degree/Diploma",
            "Postgraduate",
            "Vocational / ITI",
            "Not Enrolled / None"
        ]
    }

@router.post("/evaluate", response_model=CitizenEvaluationResponse)
async def evaluate_citizen(input_data: QuestionnaireRequest):
    # 1. Build profile — drop None-valued optionals so CitizenProfile's own defaults apply
    #    (owned_documents is Optional on the request but a required list on the profile).
    profile_dict = {
        k: v for k, v in input_data.model_dump().items() if v is not None
    }
    profile = CitizenProfile(**profile_dict)
    
    # 2. Determine persona
    persona = determine_persona(profile)
    
    # 3. Fetch all schemes from DB
    schemes_cursor = db.schemes.find({})
    schemes_docs = await schemes_cursor.to_list(1000)
    
    eligibility_map: Dict[str, Any] = {}
    eligible_count = 0
    partially_eligible_count = 0
    estimated_benefit_sum = 0
    
    for s_doc in schemes_docs:
        s_doc.pop("_id", None)
        scheme_obj = Scheme(**s_doc)
        result = evaluate_scheme_eligibility(scheme_obj, profile)
        eligibility_map[scheme_obj.id] = result
        
        if result.status == "ELIGIBLE":
            eligible_count += 1
            if "6,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 6000
            elif "15,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 15000
            elif "24,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 24000
            elif "25,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 25000
            elif "50,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 50000
            elif "5,00,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 500000
            elif "78,000" in (scheme_obj.max_financial_benefit or ""):
                estimated_benefit_sum += 78000
        elif result.status == "PARTIALLY_ELIGIBLE":
            partially_eligible_count += 1

    persona.estimated_schemes_count = eligible_count
    if estimated_benefit_sum >= 100000:
        persona.estimated_total_benefit = f"₹{estimated_benefit_sum/100000:.1f} Lakhs+"
    elif estimated_benefit_sum > 0:
        persona.estimated_total_benefit = f"₹{estimated_benefit_sum:,}"
    else:
        persona.estimated_total_benefit = "₹10,000+"

    return CitizenEvaluationResponse(
        profile=profile,
        persona=persona,
        total_schemes_evaluated=len(schemes_docs),
        eligible_count=eligible_count,
        partially_eligible_count=partially_eligible_count,
        eligibility_map=eligibility_map
    )
