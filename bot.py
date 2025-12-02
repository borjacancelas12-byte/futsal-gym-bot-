from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from database import init_db
import handlers

TOKEN = "8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE"

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
    import asyncio
    asyncio.run(main())
