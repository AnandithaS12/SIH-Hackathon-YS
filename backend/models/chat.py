from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str # "user" | "assistant" | "system"
    content: str
    language: str = "en"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Government Scheme Consultation"
    language: str = "en"
    messages: List[ChatMessage] = Field(default_factory=list)
    citizen_context: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChatStreamRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    language: str = "en" # "hi", "bn", "te", "mr", "ta", "ur", "gu", "kn", "or", "ml", "pa", "as", "mai", "sat", "ks", "ne", "kok", "doi", "sd", "brx", "sa", "mni", "en"
    citizen_profile: Optional[Dict[str, Any]] = None
    active_scheme_id: Optional[str] = None
