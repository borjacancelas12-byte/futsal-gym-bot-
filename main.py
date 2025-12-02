import os
import logging
from fastapi import FastAPI, Request, HTTPException
from bot import create_application

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token del bot
TOKEN = os.environ.get("Futsalgymbot")
if not TOKEN:
    logging.error("No se encontró la variable de entorno Futsalgymbot")
    raise ValueError("No se encontró la variable de entorno Futsalgymbot")

# Crear la aplicación de Telegram
telegram_app = create_application(TOKEN)

# Crear FastAPI
app = FastAPI()

# URL pública de Render
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
if not RENDER_EXTERNAL_URL:
    logging.error("No se encontró la variable de entorno RENDER_EXTERNAL_URL")
    raise ValueError("No se encontró la variable de entorno RENDER_EXTERNAL_URL")

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

# Configurar webhook al iniciar FastAPI
@app.on_event("startup")
async def on_startup():
    try:
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        logging.info(f"Webhook configurado correctamente en: {WEBHOOK_URL}")
    except Exception as e:
        logging.error(f"Error al configurar webhook: {e}")
        raise

# Endpoint para recibir updates de Telegram
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    try:
        update = await request.json()
        await telegram_app.update_queue.put(update)
        return {"ok": True}
    except Exception as e:
        logging.error(f"Error al procesar update: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Healthcheck
@app.get("/")
async def root():
    return {"status": "ok"}

