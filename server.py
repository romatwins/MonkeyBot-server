from fastapi import FastAPI, Request
import openai
import requests

app = FastAPI()

VERIFY_TOKEN = "monkeybot123"  # Подтверждающий маркер
ACCESS_TOKEN = "your_instagram_access_token"

openai.api_key = "your_openai_api_key"

@app.get("/")
def home():
    from fastapi.responses import JSONResponse

return JSONResponse({"status": "Бот работает!"}, ensure_ascii=False)

# Верификация вебхука Instagram API
@app.get("/webhook")
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return {"error": "Ошибка верификации"}

# Получение сообщений от Instagram
@app.post("/webhook")
async def handle_message(request: Request):
    data = await request.json()
    
    for entry in data.get("entry", []):
        for message_event in entry.get("messaging", []):
            if "message" in message_event:
                sender_id = message_event["sender"]["id"]
                text = message_event["message"]["text"]

                # Генерируем ответ через GPT
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": text}]
                )
                reply = response["choices"][0]["message"]["content"]

                send_message(sender_id, reply)
    
    return {"status": "ok"}

# Функция отправки ответа в Instagram
def send_message(user_id, message):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={ACCESS_TOKEN}"
    payload = {"recipient": {"id": user_id}, "message": {"text": message}}
    requests.post(url, json=payload)
