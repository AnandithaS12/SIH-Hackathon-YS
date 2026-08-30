from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from lib.db import db
from models.scheme import Scheme, SchemeComparisonRequest, SchemeComparisonResponse
from lib.deadlines import attach_deadline_status
from lib.dates import today_iso

router = APIRouter(prefix="/schemes", tags=["schemes"])

@router.get("", response_model=List[Scheme])
async def list_schemes(
    search: Optional[str] = None,
    sector: Optional[str] = None,
    is_central: Optional[bool] = None,
    state: Optional[str] = None,
    benefit_type: Optional[str] = None,
    category: Optional[str] = None,
    occupation: Optional[str] = None,
    closing_soon: Optional[bool] = None,
    limit: int = Query(default=100, ge=1, le=200)
):
    query: Dict[str, Any] = {}
    
    if sector and sector != "All":
        query["sector"] = sector
        
    if is_central is not None:
        query["is_central"] = is_central
        
    if state and state != "All":
        # Either applicable to "All" or includes this specific state
        query["$or"] = [
            {"applicable_states": "All"},
            {"applicable_states": state}
        ]
        
    if benefit_type and benefit_type != "All":
        query["benefit_type"] = benefit_type
        
    schemes_docs = await db.schemes.find(query).to_list(limit)
    
    results: List[Scheme] = []
    for doc in schemes_docs:
        doc.pop("_id", None)
        scheme_obj = attach_deadline_status(Scheme(**doc))
        
        # In-memory search filtering if query provided
        if search:
            s_low = search.lower().strip()
            text_corpus = f"{scheme_obj.title} {scheme_obj.short_name} {scheme_obj.description} {scheme_obj.ministry} {' '.join(scheme_obj.tags)}".lower()
            if s_low not in text_corpus:
                continue

        if closing_soon and not (scheme_obj.deadline_status and scheme_obj.deadline_status.is_urgent):
            continue
                
        results.append(scheme_obj)
        
    return results

@router.get("/sectors")
async def get_sectors():
    sectors = [
        "Agriculture",
        "Healthcare",
        "Housing & Sanitation",
        "Education & Skills",
        "Financial Inclusion & Pension",
        "Women & Child",
        "Employment & MSME",
        "Social Security"
    ]
    return sectors

@router.get("/stats/overview")
async def get_stats_overview():
    total_schemes = await db.schemes.count_documents({})
    central_schemes = await db.schemes.count_documents({"is_central": True})
    state_schemes = await db.schemes.count_documents({"is_central": False})
    
    pipeline = [
        {"$group": {"_id": "$sector", "count": {"$sum": 1}}}
    ]
    sector_counts = await db.schemes.aggregate(pipeline).to_list(100)
    
    return {
        "total_schemes": total_schemes,
        "central_schemes": central_schemes,
        "state_schemes": state_schemes,
        "sectors_breakdown": {item["_id"]: item["count"] for item in sector_counts if item["_id"]}
    }

@router.get("/deadlines/upcoming")
async def get_upcoming_deadlines(
    scheme_ids: Optional[str] = Query(default=None, description="Comma-separated scheme ids to restrict to"),
    within_days: int = Query(default=30, ge=1, le=365)
):
    """Schemes with a cut-off inside `within_days`, soonest first.

    Dates are resolved against the IST server clock, so the warning is identical
    for every citizen regardless of their device clock.
    """
    query: Dict[str, Any] = {}
    if scheme_ids:
        wanted = [s.strip() for s in scheme_ids.split(",") if s.strip()]
        if wanted:
            query["id"] = {"$in": wanted}

    docs = await db.schemes.find(query).to_list(500)
    urgent = []
    for d in docs:
        d.pop("_id", None)
        s = attach_deadline_status(Scheme(**d))
        st = s.deadline_status
        if st and st.days_remaining is not None and st.days_remaining <= within_days:
            urgent.append({
                "scheme_id": s.id,
                "short_name": s.short_name,
                "title": s.title,
                "sector": s.sector,
                "official_portal_url": s.official_portal_url,
                "urgency": st.urgency,
                "headline": st.headline,
                "detail": st.detail,
                "next_cutoff_date": st.next_cutoff_date,
                "next_cutoff_label": st.next_cutoff_label,
                "days_remaining": st.days_remaining,
            })

    urgent.sort(key=lambda item: item["days_remaining"])
    return {
        "today": today_iso("Asia/Kolkata"),
        "within_days": within_days,
        "count": len(urgent),
        "deadlines": urgent,
    }

@router.get("/{id}", response_model=Scheme)
async def get_scheme_by_id(id: str):
    doc = await db.schemes.find_one({"id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scheme not found")
    doc.pop("_id", None)
    return attach_deadline_status(Scheme(**doc))

@router.post("/compare", response_model=SchemeComparisonResponse)
async def compare_schemes(payload: SchemeComparisonRequest):
    if len(payload.scheme_ids) < 2 or len(payload.scheme_ids) > 4:
        raise HTTPException(status_code=400, detail="Please select between 2 and 4 schemes for comparison")
        
    docs = await db.schemes.find({"id": {"$in": payload.scheme_ids}}).to_list(10)
    schemes: List[Scheme] = []
    for d in docs:
        d.pop("_id", None)
        schemes.append(attach_deadline_status(Scheme(**d)))
        
    attributes = [
        {
            "key": "ministry",
            "label": "Nodal Ministry / Department",
            "values": {s.id: s.ministry for s in schemes}
        },
        {
            "key": "sector",
            "label": "Sector / Domain",
            "values": {s.id: s.sector for s in schemes}
        },
        {
            "key": "benefit_type",
            "label": "Primary Benefit Type",
            "values": {s.id: s.benefit_type for s in schemes}
        },
        {
            "key": "max_financial_benefit",
            "label": "Maximum Financial Benefit",
            "values": {s.id: s.max_financial_benefit or "Non-financial / Training" for s in schemes}
        },
        {
            "key": "age_limit",
            "label": "Age Eligibility",
            "values": {
                s.id: f"{s.eligibility_rules.min_age or 0} - {s.eligibility_rules.max_age or 'No upper limit'} Years"
                for s in schemes
            }
        },
        {
            "key": "target_beneficiaries",
            "label": "Target Groups",
            "values": {s.id: ", ".join(s.target_beneficiaries) for s in schemes}
        },
        {
            "key": "application_mode",
            "label": "Application Channel",
            "values": {s.id: s.application_mode for s in schemes}
        },
        {
            "key": "deadline",
            "label": "Application Cut-off",
            "values": {
                s.id: (s.deadline_status.headline if s.deadline_status else "Open all year")
                for s in schemes
            }
        },
        {
            "key": "official_portal_url",
            "label": "Direct Portal Link",
            "values": {s.id: s.official_portal_url for s in schemes}
        }
    ]
    
    return SchemeComparisonResponse(
        schemes=schemes,
        comparison_attributes=attributes
    )
