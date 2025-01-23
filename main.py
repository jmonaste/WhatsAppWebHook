import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import PlainTextResponse

# Cargar variables del archivo .env
load_dotenv()

app = FastAPI()

# Lee el valor desde la variable de entorno
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")

@app.get("/webhook")
def verify_webhook(request: Request):
    hub_mode = request.query_params.get("hub.mode")
    hub_challenge = request.query_params.get("hub.challenge")
    hub_verify_token = request.query_params.get("hub.verify_token")
    
    print("Received verify token:", hub_verify_token)
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Invalid verification token")

@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("Mensaje entrante de WhatsApp:", body)
    return {"status": "ok"}
