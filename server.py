from fastapi import FastAPI, Request
import openai
import requests
from fastapi.responses import JSONResponse

app = FastAPI()

VERIFY_TOKEN = "monkeybot123"  # Подтверждающий маркер
ACCESS_TOKEN = "your_instagram_access_token"
openai.api_key = "your_openai_api_key"

@app.get("/")
def home():
    return JSONResponse({"status": "Бот работает!"}, media_type="application/json; charset=utf-8")

# Верификация вебхука Instagram API
@app.get("/webhook")
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return JSONResponse({"error": "Ошибка верификации"}, ensure_ascii=False)
