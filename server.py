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
    return JSONResponse(content={"status": "Бот работает!"}, media_type="application/json; charset=utf-8")

# Верификация вебхука Instagram API
@app.get("/webhook")
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return JSONResponse(content={"error": "Ошибка верификации"}, media_type="application/json; charset=utf-8")
@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("Получен вебхук:", data)  # Выведет данные в логи
    return JSONResponse({"status": "ok"}, media_type="application/json; charset=utf-8")
import uvicorn

@app.post("/webhook")
async def webhook_post(request: Request):
    data = await request.json()
    print("Получен POST-запрос:", data)  # Вывод данных в логи
    return JSONResponse({"status": "ok"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)