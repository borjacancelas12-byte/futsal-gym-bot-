import os
from fastapi import FastAPI, Request
from bot import create_application

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró la variable de entorno BOT_TOKEN")

telegram_app = create_application(TOKEN)

app = FastAPI()

# Usamos la variable de Render para obtener el dominio automáticamente
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
if not RENDER_EXTERNAL_URL:
    raise ValueError("No se encontró la variable de entorno RENDER_EXTERNAL_URL")

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

# Configura webhook al iniciar FastAPI
@app.on_event("startup")
async def on_startup():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook configurado en: {WEBHOOK_URL}")

# Endpoint para recibir updates de Telegram
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    await telegram_app.update_queue.put(update)
    return {"ok": True}

# Healthcheck
@app.get("/")
async def root():
    return {"status": "ok"}
