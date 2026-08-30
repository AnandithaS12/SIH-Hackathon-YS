from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
from lib.db import client, db

# Import modular routers
from routers.citizens import router as citizens_router
from routers.schemes import router as schemes_router
from routers.documents import router as documents_router
from routers.chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.close()

# Create the main app without a prefix
app = FastAPI(lifespan=lifespan, title="Yojana Setu API", description="API for Government Schemes Discovery & Multilingual AI Consultation")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Health routes
@api_router.get("/")
async def root():
    return {
        "message": "Welcome to Yojana Setu API",
        "status": "online",
        "tagline": "Bridging Schemes to Citizens",
        "official_sources": ["india.gov.in", "myscheme.gov.in"]
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.model_dump())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Mount all feature routers onto api_router
api_router.include_router(citizens_router)
api_router.include_router(schemes_router)
api_router.include_router(documents_router)
api_router.include_router(chat_router)

# Include the router in the main app (MUST be after all routes are registered on api_router)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
