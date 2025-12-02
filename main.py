import os
from fastapi import FastAPI, Request
from bot import create_application

TOKEN = os.getenv(8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "missecret")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

app = FastAPI()
telegram_app = create_application(TOKEN)

@app.on_event("startup")
async def startup_event():
    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/webhook/{WEBHOOK_SECRET}"
        await telegram_app.bot.set_webhook(url=webhook_url)
        print("Webhook configured:", webhook_url)


@app.post("/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        return {"status": "unauthorized"}

    update = await request.json()
    await telegram_app.update_queue.put(update)
    return {"ok": True}


@app.get("/")
def home():
    return {"status": "Bot running"}
