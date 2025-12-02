from fastapi import FastAPI, Request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os
from datetime import datetime
from rutinas import rutinas
import asyncio

# -----------------------
# Configuración
# -----------------------
BOT_TOKEN = os.getenv("Futsalgymbot_token")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, None, workers=0, use_context=True)
app = FastAPI()

# Diccionario para guardar la posición de cada usuario {chat_id: posicion}
usuarios = {}

# Teclado de posiciones
posiciones_teclado = ReplyKeyboardMarkup(
    [["portero", "defensa"], ["medio", "delantero"]],
    one_time_keyboard=True,
    resize_keyboard=True
)

# -----------------------
# Handlers
# -----------------------
def start(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(
        "¡Hola! Soy Futsalgymbot 🤖\n"
        "Dime tu posición para enviarte tu rutina diaria (fútbol + gym):",
        reply_markup=posiciones_teclado
    )
    usuarios[chat_id] = None  # Guardamos chat_id sin posición aún

def recibir_posicion(update, context):
    chat_id = update.message.chat_id
    posicion = update.message.text.lower()
    if posicion not in rutinas:
        update.message.reply_text(
            "No conozco esa posición. Por favor elige: portero, defensa, medio o delantero.",
            reply_markup=posiciones_teclado
        )
        return

    usuarios[chat_id] = posicion
    update.message.reply_text(f"¡Perfecto! Guardé tu posición como **{posicion}**. Recibirás tu rutina diaria.", parse_mode="Markdown")
    enviar_rutina(chat_id, posicion)

def enviar_rutina(chat_id, posicion):
    futbol = rutinas[posicion]["futbol"]
    gym = rutinas[posicion]["gym"]

    mensaje = "🏟️ **Rutina de Fútbol:**\n"
    for ejercicio, video in futbol:
        mensaje += f"- {ejercicio}\n  {video}\n"

    mensaje += "\n💪 **Rutina de Gym:**\n"
    for ejercicio, video in gym:
        mensaje += f"- {ejercicio}\n  {video}\n"

    bot.send_message(chat_id, text=mensaje, parse_mode="Markdown")

# Agregamos handlers
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, recibir_posicion))

# -----------------------
# Webhook
# -----------------------
@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        return {"status": "invalid token"}
    data = await request.json()
    update = Update.de_json(data, bot)
    dp.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Futsalgymbot funcionando!"}

# -----------------------
# Envío diario automático
# -----------------------
async def enviar_diario():
    await asyncio.sleep(5)  # Pequeño retraso al inicio
    while True:
        ahora = datetime.now()
        # Enviar a las 9 AM hora del servidor
        if ahora.hour == 9 and ahora.minute == 0:
            for chat_id, posicion in usuarios.items():
                if posicion:
                    enviar_rutina(chat_id, posicion)
            await asyncio.sleep(60)  # Esperar 1 min para evitar repetición
        await asyncio.sleep(20)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(enviar_diario())
