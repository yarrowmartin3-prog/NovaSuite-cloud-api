from fastapi import FastAPI
from pydantic import BaseModel
import os
from providers import get_provider

app = FastAPI(title="NovaSuite Cloud API", version="1.0.0")
PROVIDER = os.getenv("NOVA_PROVIDER", "dummy")
MODEL = os.getenv("NOVA_MODEL", "gpt-4o-mini")

class ChatIn(BaseModel):
    message: str
    history: list[str] = []

@app.get("/health")
def health():
    return {"status":"ok","provider":PROVIDER,"model":MODEL}

@app.post("/chat")
def chat(data: ChatIn):
    prov = get_provider(PROVIDER, MODEL)
    reply = prov.chat(data.message, data.history or [])
    return {"reply": reply}
