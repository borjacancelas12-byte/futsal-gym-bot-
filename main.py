import os
from fastapi import FastAPI, Request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

TOKEN = os.environ.get("Futsalgymbot")
bot = Bot(token=TOKEN)
app = FastAPI()
dispatcher = Dispatcher(bot, None, workers=0)

# --- Datos ---
ejercicios = {
    "Fuerza": {
        "Básico": {"desc": "Sentadillas sin peso, zancadas.", "video": "https://www.youtube.com/watch?v=1g6aGmUzrQs"},
        "Intermedio": {"desc": "Sentadillas con mancuerna, peso muerto ligero.", "video": "https://www.youtube.com/watch?v=E1vANqJ_Q6k"},
        "Avanzado": {"desc": "Sentadillas con barra, saltos pliométricos.", "video": "https://www.youtube.com/watch?v=1oed-UmAxFs"}
    },
    "Core": {
        "Básico": {"desc": "Plancha frontal y lateral.", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
        "Intermedio": {"desc": "Crunches y giros rusos.", "video": "https://www.youtube.com/watch?v=wkD8rjkodUI"},
        "Avanzado": {"desc": "Plancha con desplazamientos y ab rollouts.", "video": "https://www.youtube.com/watch?v=ElT5s5OyAhc"}
    },
    "Cardio": {
        "Básico": {"desc": "Sprints cortos y cambios de dirección.", "video": "https://www.youtube.com/watch?v=Z3ZLJf1ZwSk"},
        "Intermedio": {"desc": "Circuitos HIIT específicos para futsal.", "video": "https://www.youtube.com/watch?v=ml6cT4AZdqI"},
        "Avanzado": {"desc": "Pliometría avanzada y sprints con resistencia.", "video": "https://www.youtube.com/watch?v=8Q2sHjxtd8A"}
    },
    "Técnica": {
        "Básico": {"desc": "Pases y control de balón.", "video": "https://www.youtube.com/watch?v=Q4D7zBQm0VI"},
        "Intermedio": {"desc": "Regates y conducciones rápidas.", "video": "https://www.youtube.com/watch?v=CxZmvXzGJ7o"},
        "Avanzado": {"desc": "Movimientos de pivote y talladas precisas.", "video": "https://www.youtube.com/watch?v=Zi4C_XQ4m3k"}
    }
}

posiciones = {
    "Portero": "Defiende el arco. Reflejos rápidos y buena comunicación.",
    "Ala": "Jugador rápido por bandas. Ataca y defiende.",
    "Cierre": "Defensa central. Organiza la defensa.",
    "Pívot": "Delantero principal. Marca goles y protege el balón."
}

talladas = {
    "Tajada corta": "Movimiento rápido para quitar espacio al rival.",
    "Tajada larga": "Control del balón en profundidad. Útil en transición."
}

# --- Menús ---
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Ejercicios", callback_data="menu_ejercicios")],
        [InlineKeyboardButton("Posiciones", callback_data="posiciones")],
        [InlineKeyboardButton("Talladas", callback_data="talladas")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("¡Bienvenido a FutsalGym Bot! Elige una opción:", reply_markup=reply_markup)

def menu_ejercicios(update: Update, context):
    query = update.callback_query
    keyboard = []
    for categoria in ejercicios.keys():
        keyboard.append([InlineKeyboardButton(categoria, callback_data=f"ej_{categoria}")])
    query.edit_message_text("Elige categoría de ejercicios:", reply_markup=InlineKeyboardMarkup(keyboard))

def categoria_ejercicio(update: Update, context):
    query = update.callback_query
    categoria = query.data.split("_")[1]
    keyboard = []
    for nivel in ejercicios[categoria].keys():
        keyboard.append([InlineKeyboardButton(nivel, callback_data=f"nivel_{categoria}_{nivel}")])
    query.edit_message_text(f"Ejercicios de {categoria}, elige nivel:", reply_markup=InlineKeyboardMarkup(keyboard))

def nivel_ejercicio(update: Update, context):
    query = update.callback_query
    _, categoria, nivel = query.data.split("_")
    info = ejercicios[categoria][nivel]
    text = f"*{categoria} - {nivel}*\n{info['desc']}\nVideo: {info['video']}"
    query.edit_message_text(text=text, parse_mode="Markdown")

def posiciones_callback(update: Update, context):
    query = update.callback_query
    text = "*Posiciones en Futsal:*\n\n"
    for pos, desc in posiciones.items():
        text += f"*{pos}*: {desc}\n\n"
    query.edit_message_text(text=text, parse_mode="Markdown")

def talladas_callback(update: Update, context):
    query = update.callback_query
    text = "*Técnicas de Talladas:*\n\n"
    for t, desc in talladas.items():
        text += f"*{t}*: {desc}\n\n"
    query.edit_message_text(text=text, parse_mode="Markdown")

def echo(update: Update, context):
    update.message.reply_text(f"Has dicho: {update.message.text}\nUsa /start para ver opciones.")

# --- Scheduler para rutinas diarias ---
def rutina_diaria():
    for chat_id in registered_chats:
        bot.send_message(chat_id, "📅 ¡Es hora de tu rutina diaria de FutsalGym! Usa /start para ver opciones.")

registered_chats = set()

def register_chat(update: Update, context):
    registered_chats.add(update.message.chat_id)

scheduler = BackgroundScheduler()
scheduler.add_job(rutina_diaria, "cron", hour=10)  # Todos los días a las 10am
scheduler.start()

# --- Handlers ---
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("registrar", register_chat))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CallbackQueryHandler(menu_ejercicios, pattern="menu_ejercicios"))
dispatcher.add_handler(CallbackQueryHandler(posiciones_callback, pattern="posiciones"))
dispatcher.add_handler(CallbackQueryHandler(talladas_callback, pattern="talladas"))
dispatcher.add_handler(CallbackQueryHandler(categoria_ejercicio, pattern="ej_"))
dispatcher.add_handler(CallbackQueryHandler(nivel_ejercicio, pattern="nivel_"))

# --- Webhook ---
@app.post(f"/webhook/{TOKEN}")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Bot online"}
