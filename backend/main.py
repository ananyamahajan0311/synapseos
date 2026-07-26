from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
import os
from database import engine
from database import Base
from api.health_routes import router as health_router
from api.auth_routes import router as auth_router
from api.chat_routes import router as chat_router
from api.email_routes import router as email_router

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(email_router)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

