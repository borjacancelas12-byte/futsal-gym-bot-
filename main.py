import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

# -------------------------------
# CARGA DE VARIABLES DE ENTORNO
# -------------------------------
load_dotenv()
TOKEN = os.getenv("Futsalgymbot")

# -------------------------------
# INICIALIZACIÓN DE FASTAPI
# -------------------------------
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bot activo"}

# -------------------------------
# FUNCIONES DEL BOT
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot de futsal. Usa /rutinas para ver tus entrenamientos o /ayuda para más información."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Iniciar el bot\n"
        "/rutinas - Ver rutinas disponibles\n"
        "/ayuda - Ver esta ayuda"
    )

async def rutinas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Rutina 1", callback_data="rutina_1")],
        [InlineKeyboardButton("Rutina 2", callback_data="rutina_2")],
        [InlineKeyboardButton("Volver", callback_data="menu_principal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Selecciona una rutina:", reply_markup=reply_markup)

# Callback para botones
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "rutina_1":
        await query.edit_message_text("Aquí está la información de la Rutina 1 🏃‍♂️")
    elif query.data == "rutina_2":
        await query.edit_message_text("Aquí está la información de la Rutina 2 🏋️‍♂️")
    elif query.data == "menu_principal":
        keyboard = [
            [InlineKeyboardButton("Rutina 1", callback_data="rutina_1")],
            [InlineKeyboardButton("Rutina 2", callback_data="rutina_2")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Selecciona una rutina:", reply_markup=reply_markup)

# -------------------------------
# SCHEDULER PARA RECORDATORIOS
# -------------------------------
scheduler.add_job(
    recordatorio_diario,
    "cron",
    hour=18,
    minute=0,
    kwargs={"context": "valor_que_necesites"}
)
scheduler.add_job(recordatorio_diario, "cron", hour=18, minute=0)  # Todos los días a las 18:00
scheduler.start()

# -------------------------------
# INICIALIZACIÓN DEL BOT
# -------------------------------
application = ApplicationBuilder().token(TOKEN).build()

# Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("rutinas", rutinas))
application.add_handler(CommandHandler("ayuda", ayuda))
application.add_handler(CallbackQueryHandler(callback_handler))

# -------------------------------
# EJECUCIÓN
# -------------------------------
if __name__ == "__main__":
    import asyncio
    from telegram.ext import Application

    async def main():
        await application.initialize()
        await application.start()
        await application.updater.start_polling()  # Para desarrollo local
        await application.idle()

    asyncio.run(main())


# --- Comandos del bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de futsal y gym 🏋️⚽")

async def rutinas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aquí tienes tus rutinas de entrenamiento:\n"
        "1. Calentamiento\n2. Fútbol en cancha\n3. Ejercicios de fuerza\n4. Estiramientos"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Saludo inicial\n"
        "/rutinas - Mostrar rutinas\n"
        "/ayuda - Mostrar ayuda"
    )

# Registrar comandos
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("rutinas", rutinas))
application.add_handler(CommandHandler("ayuda", ayuda))

# --- Recordatorios / Scheduler ---
scheduler = BackgroundScheduler()
def recordatorio():
    chat_id = os.getenv("ADMIN_CHAT_ID")
    if chat_id:
        # Enviar mensaje usando application.bot
        application.bot.send_message(chat_id=int(chat_id), text="Recordatorio diario: ¡Entrena hoy! 💪⚽")
scheduler.add_job(recordatorio, 'interval', hours=24)
scheduler.start()

# --- Webhook endpoint para FastAPI ---
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update


# --- Comandos del bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de futsal y gym 🏋️⚽")

async def rutinas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aquí tienes tus rutinas de entrenamiento:\n"
        "1. Calentamiento\n2. Fútbol en cancha\n3. Ejercicios de fuerza\n4. Estiramientos"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Saludo inicial\n"
        "/rutinas - Mostrar rutinas\n"
        "/ayuda - Mostrar ayuda"
    )

# Registrar comandos
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("rutinas", rutinas))
application.add_handler(CommandHandler("ayuda", ayuda))

# --- Recordatorios / Scheduler ---
scheduler = BackgroundScheduler()
def recordatorio():
    # Este mensaje se enviará automáticamente a un chat
    chat_id = os.getenv("ADMIN_CHAT_ID", None)
    if chat_id:
        bot.send_message(chat_id=chat_id, text="Recordatorio diario: ¡Entrena hoy! 💪⚽")
scheduler.add_job(recordatorio, 'interval', hours=24)
scheduler.start()

# --- Webhook endpoint para FastAPI ---
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# --- Comando para comprobar que el bot funciona ---
@app.get("/")
async def root():
    return {"status": "Bot online"}

# --- Configurar webhook al arrancar la app ---
@app.on_event("startup")
async def on_startup():
    await bot.delete_webhook()
    await bot.set_webhook(url=WEBHOOK_URL)

rutinas = {
    "Básico": {
        "Fuerza": {
            "Tren Superior": [
                {"ejercicio": "Flexiones de brazos", "series": "3x12", "video": "https://www.youtube.com/watch?v=_l3ySVKYVJ8"},
                {"ejercicio": "Remo con mancuerna", "series": "3x10", "video": "https://www.youtube.com/watch?v=kBWAon7ItDw"}
            ],
            "Tren Inferior": [
                {"ejercicio": "Sentadillas sin peso", "series": "3x15", "video": "https://www.youtube.com/watch?v=aclHkVaku9U"},
                {"ejercicio": "Zancadas", "series": "3x12", "video": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"}
            ],
            "Core": [
                {"ejercicio": "Plancha frontal", "series": "3x30s", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
                {"ejercicio": "Plancha lateral", "series": "3x30s por lado", "video": "https://www.youtube.com/watch?v=Kq4Gcx7s7Tw"}
            ]
        },
        "Cardio": [
            {"ejercicio": "Sprints cortos", "series": "5x20m", "video": "https://www.youtube.com/watch?v=Z3ZLJf1ZwSk"},
            {"ejercicio": "Cambio de dirección", "series": "5x10 rep", "video": "https://www.youtube.com/watch?v=FjRmzuNkg4c"}
        ],
        "Técnica": [
            {"ejercicio": "Pases cortos", "series": "10 min", "video": "https://www.youtube.com/watch?v=Q4D7zBQm0VI"},
            {"ejercicio": "Control de balón", "series": "10 min", "video": "https://www.youtube.com/watch?v=JYnb5xHtz-8"}
        ]
    },
    "Intermedio": {
        "Fuerza": {
            "Tren Superior": [
                {"ejercicio": "Flexiones con palmada", "series": "4x12", "video": "https://www.youtube.com/watch?v=IODxDxX7oi4"},
                {"ejercicio": "Press de hombros con mancuernas", "series": "4x10", "video": "https://www.youtube.com/watch?v=B-aVuyhvLHU"}
            ],
            "Tren Inferior": [
                {"ejercicio": "Sentadillas con mancuernas", "series": "4x12", "video": "https://www.youtube.com/watch?v=SW_C1A-rejs"},
                {"ejercicio": "Peso muerto ligero", "series": "3x10", "video": "https://www.youtube.com/watch?v=r4MzxtBKyNE"}
            ],
            "Core": [
                {"ejercicio": "Crunches", "series": "4x15", "video": "https://www.youtube.com/watch?v=wkD8rjkodUI"},
                {"ejercicio": "Giros rusos", "series": "3x20", "video": "https://www.youtube.com/watch?v=wkD8rjkodUI"}
            ]
        },
        "Cardio": [
            {"ejercicio": "Circuitos HIIT", "series": "15 min", "video": "https://www.youtube.com/watch?v=ml6cT4AZdqI"},
            {"ejercicio": "Sprints con resistencia", "series": "6x30m", "video": "https://www.youtube.com/watch?v=8Q2sHjxtd8A"}
        ],
        "Técnica": [
            {"ejercicio": "Regates rápidos", "series": "15 min", "video": "https://www.youtube.com/watch?v=CxZmvXzGJ7o"},
            {"ejercicio": "Pases largos", "series": "10 min", "video": "https://www.youtube.com/watch?v=CxZmvXzGJ7o"}
        ]
    },
    "Avanzado": {
        # Rutina avanzada similar pero con más intensidad, más repeticiones y combinaciones
    }
}
def menu_rutinas(update: Update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Básico", callback_data="rutina_Básico")],
        [InlineKeyboardButton("Intermedio", callback_data="rutina_Intermedio")],
        [InlineKeyboardButton("Avanzado", callback_data="rutina_Avanzado")]
    ]
    query.edit_message_text("Elige tu nivel para ver la rutina semanal:", reply_markup=InlineKeyboardMarkup(keyboard))

def mostrar_rutina(update: Update, context):
    query = update.callback_query
    nivel = query.data.split("_")[1]
    texto = f"*Rutina de {nivel}*\n\n"
    for categoria, grupos in rutinas[nivel].items():
        texto += f"*{categoria}*\n"
        if isinstance(grupos, dict):  # Fuerza
            for grupo, ejercicios_list in grupos.items():
                texto += f"_{grupo}_\n"
                for e in ejercicios_list:
                    texto += f"- {e['ejercicio']} ({e['series']}) [Video]({e['video']})\n"
        else:  # Cardio / Técnica
            for e in grupos:
                texto += f"- {e['ejercicio']} ({e['series']}) [Video]({e['video']})\n"
        texto += "\n"
    query.edit_message_text(texto, parse_mode="Markdown")

dispatcher.add_handler(CallbackQueryHandler(menu_rutinas, pattern="menu_rutinas"))
dispatcher.add_handler(CallbackQueryHandler(mostrar_rutina, pattern="rutina_"))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Ver Rutinas", callback_data="menu_rutinas")]]
    await update.message.reply_text("¡Bienvenido a FutsalGymBot!", reply_markup=InlineKeyboardMarkup(keyboard))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Ver Rutinas", callback_data="menu_rutinas")]]
    await update.message.reply_text("¡Bienvenido a FutsalGymBot!", reply_markup=InlineKeyboardMarkup(keyboard))
async def menu_rutinas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Básico", callback_data="rutina_Básico")],
        [InlineKeyboardButton("Intermedio", callback_data="rutina_Intermedio")],
        [InlineKeyboardButton("Avanzado", callback_data="rutina_Avanzado")]
    ]
    await query.edit_message_text("Elige tu nivel para ver la rutina semanal:", reply_markup=InlineKeyboardMarkup(keyboard))

async def mostrar_rutina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    nivel = query.data.split("_")[1]
    texto = f"*Rutina de {nivel}*\n\n"
    for categoria, grupos in rutinas[nivel].items():
        texto += f"*{categoria}*\n"
        if isinstance(grupos, dict):
            for grupo, ejercicios_list in grupos.items():
                texto += f"_{grupo}_\n"
                for e in ejercicios_list:
                    texto += f"- {e['ejercicio']} ({e['series']}) [Video]({e['video']})\n"
        else:
            for e in grupos:
                texto += f"- {e['ejercicio']} ({e['series']}) [Video]({e['video']})\n"
        texto += "\n"
    await query.edit_message_text(texto, parse_mode="Markdown")
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(menu_rutinas, pattern="menu_rutinas"))
app.add_handler(CallbackQueryHandler(mostrar_rutina, pattern="rutina_"))

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
