import os
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from database import init_db
import handlers

# Opcional: en desarrollo usar python-dotenv y descomentar:
# from dotenv import load_dotenv
# load_dotenv()

# Leer token desde variable de entorno (requerido)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError(
        "La variable de entorno TOKEN no está definida. "
        "Define TOKEN en tu entorno (p. ej. en .env durante desarrollo)."
    )

# ALLOWED_ID puede venir por variable de entorno (fallback al valor anterior)
ALLOWED_ID = int(os.getenv("ALLOWED_ID", "980036030"))

# Si handlers necesita acceder a ALLOWED_ID, puedes asignarlo aquí:
# handlers.ALLOWED_ID = ALLOWED_ID

async def main():
    await init_db()

    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", handlers.start))

    # Menús
    app.add_handler(CallbackQueryHandler(handlers.menu_posicion, pattern="menu_posicion"))
    app.add_handler(CallbackQueryHandler(handlers.menu_objetivo, pattern="menu_objetivo"))

    # Posiciones
    app.add_handler(CallbackQueryHandler(handlers.elegir_posicion, pattern="pos_.*"))

    # Objetivos
    app.add_handler(CallbackQueryHandler(handlers.elegir_objetivo, pattern="obj_.*"))

    # Rutina diaria
    app.add_handler(CallbackQueryHandler(handlers.hoy, pattern="hoy"))

    print("🤖 Bot funcionando...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())