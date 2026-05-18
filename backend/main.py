from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "SynapseOS Backend Running"}

@app.post("/generate-email")
def generate_email(data: PromptRequest):

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Write a professional email:\n{data.prompt}"
    )

    return {
        "email": response.text
    }