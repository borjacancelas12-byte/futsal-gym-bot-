import os
from fastapi import FastAPI, Request
from bot import create_application

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró la variable de entorno BOT_TOKEN")

telegram_app = create_application(TOKEN)

app = FastAPI()

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://<TU_DOMINIO_RENDOR>.onrender.com{WEBHOOK_PATH}"  # Cambia con tu dominio

# Configura webhook al iniciar FastAPI
@app.on_event("startup")
async def on_startup():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

# Endpoint para recibir updates
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    await telegram_app.update_queue.put(update)
    return {"ok": True}

# Healthcheck
@app.get("/")
async def root():
    return {"status": "ok"}
