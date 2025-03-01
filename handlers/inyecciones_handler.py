import os
from config import bot
from libs.pago_inyecciones import PagoInyecciones

# Diccionario para guardar los datos temporales de cada usuario
user_data = {}

def ask_mes(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "📅 Ingresa el mes (nombre o número, ej: 'marzo' o '03'):")
    bot.register_next_step_handler(message, ask_anio)

def ask_anio(message):
    chat_id = message.chat.id
    user_data[chat_id]["mes"] = message.text
    bot.send_message(chat_id, "🔢 Ingresa el año (ej: 2025):")
    bot.register_next_step_handler(message, calcular_pago)

def calcular_pago(message):
    chat_id = message.chat.id
    user_data[chat_id]["anio"] = int(message.text)
    datos = user_data[chat_id]

    try:
        pago = PagoInyecciones(datos["mes"], datos["anio"])
        resultado = pago.calcular_pago()
        bot.send_message(chat_id, f"💰 El pago total para {datos['mes']} de {datos['anio']} es: {resultado}")
    except ValueError as e:
        bot.send_message(chat_id, f"⚠️ Error: {str(e)}")

# Asignar el manejador al comando /pago_inyecciones
def handle_pagos_inyecciones(message):
    ask_mes(message)
