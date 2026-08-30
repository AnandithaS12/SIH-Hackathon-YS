from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from lib.db import db
from models.scheme import Scheme, SchemeComparisonRequest, SchemeComparisonResponse

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
        scheme_obj = Scheme(**doc)
        
        # In-memory search filtering if query provided
        if search:
            s_low = search.lower().strip()
            text_corpus = f"{scheme_obj.title} {scheme_obj.short_name} {scheme_obj.description} {scheme_obj.ministry} {' '.join(scheme_obj.tags)}".lower()
            if s_low not in text_corpus:
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

@router.get("/{id}", response_model=Scheme)
async def get_scheme_by_id(id: str):
    doc = await db.schemes.find_one({"id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scheme not found")
    doc.pop("_id", None)
    return Scheme(**doc)

@router.post("/compare", response_model=SchemeComparisonResponse)
async def compare_schemes(payload: SchemeComparisonRequest):
    if len(payload.scheme_ids) < 2 or len(payload.scheme_ids) > 4:
        raise HTTPException(status_code=400, detail="Please select between 2 and 4 schemes for comparison")
        
    docs = await db.schemes.find({"id": {"$in": payload.scheme_ids}}).to_list(10)
    schemes: List[Scheme] = []
    for d in docs:
        d.pop("_id", None)
        schemes.append(Scheme(**d))
        
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
            "key": "official_portal_url",
            "label": "Direct Portal Link",
            "values": {s.id: s.official_portal_url for s in schemes}
        }
    ]
    
    return SchemeComparisonResponse(
        schemes=schemes,
        comparison_attributes=attributes
    )
