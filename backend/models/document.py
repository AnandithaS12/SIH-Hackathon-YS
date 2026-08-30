from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MasterDocument(BaseModel):
    id: str
    name: str
    name_hi: str
    category: str # "Identity", "Income & Financial", "Social & Caste", "Residence & Land", "Education & Employment", "Special Category"
    description: str
    issuing_authority: str
    how_to_obtain: str
    digital_portal_url: Optional[str] = None
    common_schemes_count: int = 0
    common_schemes: List[str] = Field(default_factory=list)

class DocumentLockerState(BaseModel):
    owned_documents: List[str] # Document IDs or names
    missing_critical: List[str]
    unlocked_schemes_count: int
    partially_ready_schemes_count: int
