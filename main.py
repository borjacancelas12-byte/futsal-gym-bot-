# main.py
import os
from fastapi import FastAPI, Request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Tu token de Telegram
TOKEN = os.environ.get("Futsalgymbot")  # IMPORTANTE: variable de entorno en Render

bot = Bot(token=TOKEN)
app = FastAPI()

# Dispatcher de telegram
dispatcher = Dispatcher(bot, None, workers=0)

# --- Handlers ---
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Opción 1", callback_data="opt1")],
        [InlineKeyboardButton("Opción 2", callback_data="opt2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("¡Bot funcionando! Elige una opción:", reply_markup=reply_markup)

def echo(update: Update, context):
    update.message.reply_text(f"Has dicho: {update.message.text}")

def button_callback(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Has pulsado: {query.data}")

# Añadimos handlers al dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CallbackQueryHandler(button_callback))

# --- Webhook para Telegram ---
@app.post(f"/webhook/{TOKEN}")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return {"ok": True}

# --- Ruta de prueba ---
@app.get("/")
async def root():
    return {"status": "Bot online"}

# ----------------------------
# Rutinas completas
# ----------------------------
rutinas = {
    "portero": {
        "futbol": [
            {"ejercicio": "Reacción y reflejos", "youtube": "https://www.youtube.com/watch?v=Y1a4L6V1ZyY"},
            {"ejercicio": "Desplazamientos laterales", "youtube": "https://www.youtube.com/watch?v=2g8S56Oa0jk"},
            {"ejercicio": "Bloqueos y salidas", "youtube": "https://www.youtube.com/watch?v=8bLJk7R5L0A"}
        ],
        "gym": [
            {"ejercicio": "Sentadillas con salto", "youtube": "https://www.youtube.com/watch?v=U3HlEF_E9fo"},
            {"ejercicio": "Plancha lateral", "youtube": "https://www.youtube.com/watch?v=K2VljzCC16g"},
            {"ejercicio": "Flexiones", "youtube": "https://www.youtube.com/watch?v=IODxDxX7oi4"}
        ]
    },
    "ala": {
        "futbol": [
            {"ejercicio": "Regate y control de balón", "youtube": "https://www.youtube.com/watch?v=4rL7QsxY8aU"},
            {"ejercicio": "Pases y cambios de ritmo", "youtube": "https://www.youtube.com/watch?v=3dH3FZsE5hQ"},
            {"ejercicio": "Finalización rápida", "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        ],
        "gym": [
            {"ejercicio": "Burpees", "youtube": "https://www.youtube.com/watch?v=TU8QYVW0gDU"},
            {"ejercicio": "Zancadas", "youtube": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"},
            {"ejercicio": "Escaladores", "youtube": "https://www.youtube.com/watch?v=nmwgirgXLYM"}
        ]
    },
    "pívot": {
        "futbol": [
            {"ejercicio": "Protección de balón", "youtube": "https://www.youtube.com/watch?v=9m3HfZ5vO9c"},
            {"ejercicio": "Remates de pivote", "youtube": "https://www.youtube.com/watch?v=kFv2p5KytzM"},
            {"ejercicio": "Movimientos de desmarque", "youtube": "https://www.youtube.com/watch?v=8hP9D6kZseM"}
        ],
        "gym": [
            {"ejercicio": "Peso muerto con mancuernas", "youtube": "https://www.youtube.com/watch?v=ytGaGIn3SjE"},
            {"ejercicio": "Press de hombros", "youtube": "https://www.youtube.com/watch?v=B-aVuyhvLHU"},
            {"ejercicio": "Abdominales", "youtube": "https://www.youtube.com/watch?v=1fbU_MkV7NE"}
        ]
    },
    "cierre": {
        "futbol": [
            {"ejercicio": "Marcaje y presión", "youtube": "https://www.youtube.com/watch?v=Hb9Fz7kKkJo"},
            {"ejercicio": "Anticipación de pases", "youtube": "https://www.youtube.com/watch?v=QzB5HIX-KYI"},
            {"ejercicio": "Despejes y coberturas", "youtube": "https://www.youtube.com/watch?v=a3M0Gn1kb1U"}
        ],
        "gym": [
            {"ejercicio": "Sentadillas", "youtube": "https://www.youtube.com/watch?v=aclHkVaku9U"},
            {"ejercicio": "Peso muerto rumano", "youtube": "https://www.youtube.com/watch?v=2SHsk9AzdjA"},
            {"ejercicio": "Plancha frontal", "youtube": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
        ]
    }
}

# ----------------------------
# Handlers
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy Futsalgymbot 🤖⚽\n"
        "Dime tu posición (portero, ala, pívot, cierre) y te daré la rutina completa de hoy (fútbol + gym)."
    )

async def rutina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pos = update.message.text.lower()
    if pos in rutinas:
        msg = f"💪 Rutina diaria para *{pos.capitalize()}*:\n\n"
        # Ejercicios de fútbol
        msg += "⚽ *Ejercicios de Fútbol:*\n"
        for e in rutinas[pos]["futbol"]:
            msg += f"- {e['ejercicio']} 🎥 [Video]({e['youtube']})\n"
        # Ejercicios de gym
        msg += "\n🏋️‍♂️ *Ejercicios de Gym:*\n"
        for e in rutinas[pos]["gym"]:
            msg += f"- {e['ejercicio']} 🎥 [Video]({e['youtube']})\n"
        await update.message.reply_markdown(msg)
    else:
        await update.message.reply_text(
            "No reconozco esa posición. Escribe: portero, ala, pívot o cierre."
        )

# ----------------------------
# Agregar handlers a la app
# ----------------------------
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rutina))

# ----------------------------
# Endpoint para webhook
# ----------------------------
@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "invalid token"}
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# ----------------------------
# Endpoint para test
# ----------------------------
@app.get("/")
def root():
    return {"status": "Futsalgymbot online!"}


