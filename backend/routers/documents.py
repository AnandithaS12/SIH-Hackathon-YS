from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from lib.db import db
from models.document import MasterDocument

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/master", response_model=List[MasterDocument])
async def list_master_documents():
    docs = await db.master_documents.find({}).to_list(100)
    results: List[MasterDocument] = []
    for d in docs:
        d.pop("_id", None)
        results.append(MasterDocument(**d))
    return results

@router.post("/evaluate-readiness")
async def evaluate_document_readiness(payload: Dict[str, Any]):
    owned_docs = set(payload.get("owned_documents", []))
    
    master_docs = await db.master_documents.find({}).to_list(100)
    total_master_count = len(master_docs)
    owned_master_count = sum(1 for d in master_docs if d["id"] in owned_docs or d["name"] in owned_docs)
    
    # Evaluate across all schemes
    schemes = await db.schemes.find({}).to_list(1000)
    ready_schemes = []
    partially_ready_schemes = []
    
    for s in schemes:
        req_docs = s.get("required_documents", [])
        mandatory_docs = [d["name"] for d in req_docs if d.get("mandatory", True)]
        
        # Check how many mandatory docs the user has
        missing = []
        for m_name in mandatory_docs:
            m_low = m_name.lower()
            matched = any(
                o.lower() in m_low or m_low in o.lower() or
                ("aadhaar" in o.lower() and "aadhaar" in m_low) or
                ("bank" in o.lower() and "bank" in m_low) or
                ("ration" in o.lower() and "ration" in m_low) or
                ("income" in o.lower() and "income" in m_low) or
                ("caste" in o.lower() and "caste" in m_low) or
                ("land" in o.lower() and "land" in m_low)
                for o in owned_docs
            )
            if not matched:
                missing.append(m_name)
                
        if len(missing) == 0:
            ready_schemes.append(s["id"])
        elif len(missing) <= 2:
            partially_ready_schemes.append({"scheme_id": s["id"], "missing_docs": missing})
            
    return {
        "owned_documents_count": owned_master_count,
        "total_documents_count": total_master_count,
        "readiness_percentage": int((owned_master_count / max(total_master_count, 1)) * 100),
        "unlocked_schemes_count": len(ready_schemes),
        "partially_ready_schemes_count": len(partially_ready_schemes),
        "ready_schemes": ready_schemes,
        "partially_ready_schemes": partially_ready_schemes
    }
