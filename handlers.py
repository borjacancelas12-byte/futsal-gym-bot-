from rutinas import get_rutina

async def start_command(update, context):
    await update.message.reply_text(
        "Hola! ¿Qué quieres hoy?\n"
        "- /hoy para obtener una rutina según tu posición ⚽💪"
    )

async def hoy_command(update, context):
    await update.message.reply_text("¿Cuál es tu posición?\n"
                                    "pivot / cierre / ala / portero")

    return
