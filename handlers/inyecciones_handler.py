import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from libs.pago_inyecciones import PagoInyecciones

user_data = {}

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

def ask_mes(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    markup = InlineKeyboardMarkup(row_width=3)
    botones = [InlineKeyboardButton(m, callback_data=f"inj_mes_{m}") for m in MESES]
    markup.add(*botones)
    bot.send_message(chat_id, "📅 Selecciona el mes:", reply_markup=markup)

def handle_mes_callback(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    mes = call.data.replace("inj_mes_", "")
    user_data[chat_id]["mes"] = mes
    bot.edit_message_text(f"📅 Mes: {mes}", chat_id, call.message.message_id)
    _ask_anio(call.message, chat_id)

def _ask_anio(message, chat_id):
    anio_actual = datetime.datetime.now().year
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(f"📆 {anio_actual}", callback_data=f"inj_anio_{anio_actual}"),
        InlineKeyboardButton("✏️ Ingresar año", callback_data="inj_anio_manual")
    )
    bot.send_message(chat_id, "¿Qué año?", reply_markup=markup)

def handle_anio_callback(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if call.data == "inj_anio_manual":
        bot.edit_message_text("✏️ Ingresa el año (ej: 2025):", chat_id, call.message.message_id)
        bot.register_next_step_handler(call.message, recibir_anio_manual)
    else:
        anio = int(call.data.replace("inj_anio_", ""))
        bot.edit_message_text(f"📆 Año: {anio}", chat_id, call.message.message_id)
        _calcular(chat_id, anio, call.message)

def recibir_anio_manual(message):
    chat_id = message.chat.id
    try:
        anio = int(message.text)
        _calcular(chat_id, anio, message)
    except ValueError:
        bot.send_message(chat_id, "⚠️ Año inválido, ingresa un número (ej: 2025):")
        bot.register_next_step_handler(message, recibir_anio_manual)

def _calcular(chat_id, anio, message):
    datos = user_data[chat_id]
    datos["anio"] = anio
    try:
        pago = PagoInyecciones(datos["mes"], datos["anio"])
        resultado = pago.calcular_pago()
        bot.send_message(chat_id, f"💰 El pago total para {datos['mes']} de {datos['anio']} es: {resultado}")
    except ValueError as e:
        bot.send_message(chat_id, f"⚠️ Error: {str(e)}")

def handle_pagos_inyecciones(message):
    ask_mes(message)
