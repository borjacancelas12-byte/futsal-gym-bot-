from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import set_posicion, set_objetivo, get_user
from rutinas import rutinas_por_posicion, rutinas_por_objetivo

# ----------- START -------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📌 Elegir Posición", callback_data="menu_posicion")],
        [InlineKeyboardButton("🎯 Elegir Objetivo", callback_data="menu_objetivo")],
        [InlineKeyboardButton("🔥 Mi Rutina de Hoy", callback_data="hoy")]
    ]
    await update.message.reply_text(
        "¡Hola! ¿Qué quieres hacer?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ----------- Menú de posición -------------
async def menu_posicion(update: Update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Portero", callback_data="pos_portero")],
        [InlineKeyboardButton("Cierre", callback_data="pos_cierre")],
        [InlineKeyboardButton("Ala", callback_data="pos_ala")],
        [InlineKeyboardButton("Pivote", callback_data="pos_pivote")]
    ]
    await query.edit_message_text(
        "Elige tu posición:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ----------- Guardar posición -------------
async def elegir_posicion(update: Update, context):
    query = update.callback_query
    await query.answer()

    posicion = query.data.split("_")[1]  # portero, cierre...
    await set_posicion(query.from_user.id, posicion)

    await query.edit_message_text(f"Perfecto, ahora estás registrado como *{posicion}*.", parse_mode="Markdown")

# ----------- Menú de objetivos -------------
async def menu_objetivo(update: Update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Fuerza", callback_data="obj_fuerza")],
        [InlineKeyboardButton("Cardio", callback_data="obj_cardio")],
        [InlineKeyboardButton("Pretemporada", callback_data="obj_pretemporada")],
        [InlineKeyboardButton("Explosividad", callback_data="obj_explosividad")]
    ]
    await query.edit_message_text(
        "Elige tu objetivo:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ----------- Guardar objetivo -------------
async def elegir_objetivo(update: Update, context):
    query = update.callback_query
    await query.answer()

    objetivo = query.data.split("_")[1]
    await set_objetivo(query.from_user.id, objetivo)

    await query.edit_message_text(f"Objetivo *{objetivo}* guardado 🔥", parse_mode="Markdown")

# ----------- Mostrar rutina de hoy -------------
async def hoy(update: Update, context):
    query = update.callback_query
    await query.answer()

    user = await get_user(query.from_user.id)

    if not user:
        await query.edit_message_text("Primero elige tu posición y objetivo.", parse_mode="Markdown")
        return

    posicion, objetivo = user

    texto = "🔥 *Tu rutina de hoy*\n\n"

    if posicion:
        texto += rutinas_por_posicion[posicion] + "\n\n"
    if objetivo:
        texto += rutinas_por_objetivo[objetivo]

    await query.edit_message_text(texto, parse_mode="Markdown")
