import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from lib.db import db
from models.chat import ChatMessage, ChatSession, ChatStreamRequest
from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

router = APIRouter(prefix="/chat", tags=["chat"])

VERNACULAR_LANGUAGES = [
    {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
    {"code": "en", "name": "English", "native": "English"},
    {"code": "bn", "name": "Bengali", "native": "বাংলা"},
    {"code": "te", "name": "Telugu", "native": "తెలుగు"},
    {"code": "mr", "name": "Marathi", "native": "मराठी"},
    {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
    {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
    {"code": "ur", "name": "Urdu", "native": "اردو"},
    {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
    {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
    {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
    {"code": "pa", "name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    {"code": "as", "name": "Assamese", "native": "অসমীয়া"},
    {"code": "mai", "name": "Maithili", "native": "मैथिली"},
    {"code": "sat", "name": "Santali", "native": "ᱥᱟᱱᱛᱟᱲᱤ"},
    {"code": "ks", "name": "Kashmiri", "native": "कॉशुर / کٲشُر"},
    {"code": "ne", "name": "Nepali", "native": "नेपाली"},
    {"code": "kok", "name": "Konkani", "native": "कोंकणी"},
    {"code": "doi", "name": "Dogri", "native": "डोगरी"},
    {"code": "sd", "name": "Sindhi", "native": "سنڌي / सिन्धी"},
    {"code": "brx", "name": "Bodo", "native": "बर'"},
    {"code": "sa", "name": "Sanskrit", "native": "संस्कृतम्"},
    {"code": "mni", "name": "Manipuri", "native": "মণিপুরী / ꯃꯤꯇꯩꯂꯣꯟ"}
]

LANGUAGE_NAMES = {l["code"]: f"{l['name']} ({l['native']})" for l in VERNACULAR_LANGUAGES}

@router.get("/languages")
async def get_supported_languages():
    return VERNACULAR_LANGUAGES

@router.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    doc = await db.chat_sessions.find_one({"id": session_id})
    if not doc:
        return {"session_id": session_id, "messages": []}
    doc.pop("_id", None)
    return doc

@router.post("/stream")
async def stream_chat_response(req: ChatStreamRequest):
    session_id = req.session_id or str(uuid.uuid4())
    lang_code = req.language or "hi"
    lang_label = LANGUAGE_NAMES.get(lang_code, "Hindi (हिन्दी)")
    
    # 1. Fetch relevant scheme information if user asked about a specific scheme or general context
    schemes_summary_text = ""
    if req.active_scheme_id:
        active_doc = await db.schemes.find_one({"id": req.active_scheme_id})
        if active_doc:
            schemes_summary_text = (
                f"\nACTIVE FOCUSED SCHEME:\n"
                f"Title: {active_doc.get('title')}\n"
                f"Ministry: {active_doc.get('ministry')}\n"
                f"Sector: {active_doc.get('sector')}\n"
                f"Benefits: {active_doc.get('benefit_summary')}\n"
                f"Criteria: {'; '.join(active_doc.get('eligibility_criteria', []))}\n"
                f"Required Documents: {', '.join([d['name'] for d in active_doc.get('required_documents', [])])}\n"
                f"Official Link: {active_doc.get('official_portal_url')}\n"
                f"Helpline: {active_doc.get('helpline', 'N/A')}\n"
            )
    else:
        # Load top schemes summary for context
        sample_schemes = await db.schemes.find({}, {"title": 1, "short_name": 1, "sector": 1, "benefit_summary": 1, "official_portal_url": 1}).to_list(20)
        schemes_summary_text = "\nPOPULAR GOVERNMENT SCHEMES IN DATABASE:\n" + "\n".join([
            f"- {s.get('short_name')}: {s.get('title')} ({s.get('sector')}) -> {s.get('benefit_summary')} [Link: {s.get('official_portal_url')}]"
            for s in sample_schemes
        ])

    # 2. Citizen profile context
    profile_text = "No profile details provided yet."
    if req.citizen_profile:
        p = req.citizen_profile
        profile_text = (
            f"Citizen Name: {p.get('name', 'Citizen')}, Age: {p.get('age', 25)}, Gender: {p.get('gender', 'N/A')}, "
            f"State: {p.get('state', 'All India')}, Category: {p.get('category', 'General')}, "
            f"Occupation: {p.get('occupation', 'N/A')}, Annual Income: ₹{p.get('annual_income', 0):,}, "
            f"Area: {p.get('area_type', 'rural')}, Specially Abled: {p.get('is_specially_abled', False)}, "
            f"BPL Card: {p.get('has_bpl_card', False)}, Land: {p.get('has_land', False)}"
        )

    # 3. System prompt enforcing the requested Indian vernacular language and structured helpful guidance
    system_prompt = f"""You are **Yojana Sahayak (योजना सहायक)**, an empathetic, highly knowledgeable AI Assistant for the **Yojana Setu (योजना सेतु)** citizen welfare platform.
Your mission is to help Indian citizens discover eligible government schemes, understand required documents, check eligibility rules, and guide them on step-by-step application procedures with official government links (india.gov.in, myscheme.gov.in, and official ministry portals).

CRITICAL LANGUAGE INSTRUCTION:
- The user has requested communication in: **{lang_label} (Language code: {lang_code})**.
- You MUST respond primarily and fluently in **{lang_label}** using its native script (e.g., Devanagari for Hindi/Marathi/Sanskrit/Dogri/Maithili, Bengali for Bangla/Assamese, Telugu, Tamil, Kannada, Malayalam, Gujarati, Gurmukhi for Punjabi, Odia, Urdu, etc.).
- If technical terms like scheme names (e.g. 'PM-KISAN', 'Ayushman Bharat', 'Aadhaar', 'DBT') or website URLs are used, you can write them clearly with their official English/Latin spelling alongside vernacular explanations.

CITIZEN CONTEXT:
{profile_text}

DATABASE CONTEXT:
{schemes_summary_text}

GUIDELINES FOR YOUR RESPONSE:
1. Be warm, respectful, concise, and empowering. Speak like a helpful government seva kendra officer.
2. If the user asks about eligibility, cite specific criteria (age, income ceiling, occupation, documents).
3. If the user asks about documents, list the exact documents needed (e.g., Aadhaar, Ration Card, Income Certificate) and where to obtain them (DigiLocker, CSC, Tehsildar).
4. Always provide official government portal links (e.g. pmkisan.gov.in, beneficiary.nha.gov.in) whenever mentioning a scheme.
5. Provide actionable next steps. Use bullet points for readability.
"""

    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="EMERGENT_LLM_KEY is not configured in backend/.env")

    # Record user message in DB
    user_msg_obj = ChatMessage(role="user", content=req.message, language=lang_code)
    await db.chat_sessions.update_one(
        {"id": session_id},
        {
            "$setOnInsert": {"id": session_id, "created_at": datetime.utcnow(), "language": lang_code},
            "$set": {"updated_at": datetime.utcnow(), "citizen_context": req.citizen_profile},
            "$push": {"messages": user_msg_obj.model_dump()}
        },
        upsert=True
    )

    # Initialize Gemini 2.5 Flash LlmChat
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=system_prompt
    ).with_model("gemini", "gemini-2.5-flash")

    async def event_generator():
        accumulated_response = []
        try:
            # Yield initial metadata
            yield f"data: {json.dumps({'session_id': session_id, 'type': 'start', 'language': lang_code})}\n\n"
            
            user_msg = UserMessage(text=req.message)
            async for event in chat.stream_message(user_msg):
                if isinstance(event, TextDelta):
                    accumulated_response.append(event.content)
                    yield f"data: {json.dumps({'content': event.content, 'type': 'chunk'})}\n\n"
                elif isinstance(event, StreamDone):
                    break
                    
            full_reply = "".join(accumulated_response)
            # Save assistant reply to MongoDB
            assistant_msg_obj = ChatMessage(role="assistant", content=full_reply, language=lang_code)
            await db.chat_sessions.update_one(
                {"id": session_id},
                {"$push": {"messages": assistant_msg_obj.model_dump()}}
            )
            yield f"data: {json.dumps({'done': True, 'type': 'done'})}\n\n"
        except Exception as e:
            err_msg = str(e)
            yield f"data: {json.dumps({'error': err_msg, 'type': 'error'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
