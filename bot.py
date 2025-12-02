# bot.py
import os
import logging
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import handlers
from database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE")
RENDER_EXTERNAL_URL = os.environ.get("https://futsal-gym-bot.onrender.com")  # ej: https://mi-servicio.onrender.com
PORT = int(os.environ.get("PORT", "8443"))  # Render provee PORT en env; por defecto 8443 para pruebas
WEBHOOK_PATH = f"/{TOKEN}"  # path seguro con token

if not TOKEN or not RENDER_EXTERNAL_URL:
    logger.error("Faltan variables de entorno. Define TOKEN y RENDER_EXTERNAL_URL.")
    raise SystemExit("Define TOKEN y RENDER_EXTERNAL_URL")

WEBHOOK_URL = RENDER_EXTERNAL_URL.rstrip("/") + WEBHOOK_PATH

async def main():
    # init DB
    await init_db()

    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", handlers.start))
    # CallbackQuery handlers
    app.add_handler(CallbackQueryHandler(handlers.menu_posicion, pattern="menu_posicion"))
    app.add_handler(CallbackQueryHandler(handlers.menu_objetivo, pattern="menu_objetivo"))
    app.add_handler(CallbackQueryHandler(handlers.elegir_posicion, pattern="pos_.*"))
    app.add_handler(CallbackQueryHandler(handlers.elegir_objetivo, pattern="obj_.*"))
    app.add_handler(CallbackQueryHandler(handlers.hoy, pattern="hoy"))

    # start webhook
    logger.info("Arrancando webhook en %s (path: %s) ...", WEBHOOK_URL, WEBHOOK_PATH)
    # Listen on 0.0.0.0 so Render can reach it
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        webhook_path=WEBHOOK_PATH,
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("Error arrancando bot: %s", e)
        raise
