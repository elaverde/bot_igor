import os
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from libs import Uground

BACKUP_CHAT_ID = os.getenv("BACKUP_CHAT_ID")


CONTADOR_PATH = os.path.join(os.path.dirname(__file__), "..", "storage", "contador.json")

def leer_contador():
    if os.path.exists(CONTADOR_PATH):
        with open(CONTADOR_PATH, "r") as f:
            return json.load(f).get("n_cobro", 0)
    return 0

def guardar_contador(n):
    with open(CONTADOR_PATH, "w") as f:
        json.dump({"n_cobro": n}, f)


# Diccionario para guardar los datos temporales de cada usuario
user_data = {}

def ask_fecha(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📅 Hoy", callback_data="fecha_hoy"),
        InlineKeyboardButton("✏️ Ingresar fecha", callback_data="fecha_manual")
    )
    bot.send_message(chat_id, "¿Qué fecha usar?", reply_markup=markup)

def handle_fecha_callback(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if call.data == "fecha_hoy":
        user_data[chat_id]["fecha"] = "hoy"
        bot.edit_message_text("📅 Fecha: último día del mes actual", chat_id, call.message.message_id)
        bot.send_message(chat_id, "✍️ Ingresa el concepto de la cuenta de cobro:")
        bot.register_next_step_handler(call.message, ask_n_cobro)

    elif call.data == "fecha_manual":
        bot.edit_message_text("✏️ Ingresa la fecha en formato 'dd-mm-yyyy':", chat_id, call.message.message_id)
        bot.register_next_step_handler(call.message, ask_concepto)

def ask_concepto(message):
    chat_id = message.chat.id
    user_data[chat_id]["fecha"] = message.text
    bot.send_message(chat_id, "✍️ Ingresa el concepto de la cuenta de cobro:")
    bot.register_next_step_handler(message, ask_n_cobro)

def ask_n_cobro(message):
    chat_id = message.chat.id
    user_data[chat_id]["concepto"] = message.text

    siguiente = leer_contador() + 1
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(f"🔢 Consecutivo ({siguiente})", callback_data=f"ncobro_auto"),
        InlineKeyboardButton("✏️ Ingresar número", callback_data="ncobro_manual")
    )
    bot.send_message(chat_id, f"¿Qué número de cobro usar?", reply_markup=markup)

def handle_ncobro_callback(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if call.data == "ncobro_auto":
        siguiente = leer_contador() + 1
        user_data[chat_id]["n_cobro"] = str(siguiente)
        bot.edit_message_text(f"🔢 Número de cobro: {siguiente}", chat_id, call.message.message_id)
        _generar(call.message, chat_id)

    elif call.data == "ncobro_manual":
        bot.edit_message_text("✏️ Ingresa el número de cobro:", chat_id, call.message.message_id)
        bot.register_next_step_handler(call.message, generar_cuenta)

def generar_cuenta(message):
    chat_id = message.chat.id
    user_data[chat_id]["n_cobro"] = message.text
    _generar(message, chat_id)

def _generar(message, chat_id):
    datos = user_data[chat_id]
    print(f"📌 Datos recibidos: {datos}")

    doc = Uground()
    doc.leer_parametros(datos["fecha"], datos["n_cobro"], datos["concepto"])

    print(f"📌 Fecha en doc: {doc.fecha}")
    print(f"📌 Concepto en doc: {doc.concepto}")
    print(f"📌 Número de cobro en doc: {doc.n_cobro}")

    pdf_path = doc.generar_cuenta_cobro_uground()
    print(f"📁 Ruta PDF: {pdf_path}")

    guardar_contador(int(datos["n_cobro"]))

    with open(pdf_path, "rb") as pdf_file:
        bot.send_document(message.chat.id, pdf_file)

    if BACKUP_CHAT_ID:
        with open(pdf_path, "rb") as pdf_file:
            bot.send_document(BACKUP_CHAT_ID, pdf_file)

    bot.send_message(message.chat.id, "✅ ¡Cuenta de cobro generada y enviada!")

def handle_cuentas(message):
    ask_fecha(message)
