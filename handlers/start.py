from telebot import types
from config import bot

def handle_start(message):
    chat_id = message.chat.id
    
    # Crear botones inline
    markup = types.InlineKeyboardMarkup()
    btn_cuentas = types.InlineKeyboardButton("📝 Generar Cuenta de Cobro", callback_data="cuenta")
    btn_pagos = types.InlineKeyboardButton("💰 Calcular Pago Inyecciones", callback_data="pago_inyecciones")

    # Agregar botones al teclado
    markup.add(btn_cuentas, btn_pagos)

    # Enviar mensaje con botones
    bot.send_message(chat_id, "¡Hola! Soy tu bot de cuentas de cobro. Elige una opción:", reply_markup=markup)

# Manejar la selección de botones
@bot.callback_query_handler(func=lambda call: call.data in ["cuenta", "pago_inyecciones"])
def handle_menu_selection(call):
    if call.data == "cuenta":
        from handlers import handle_cuentas
        handle_cuentas(call.message)
    elif call.data == "pago_inyecciones":
        from handlers import handle_pagos_inyecciones
        handle_pagos_inyecciones(call.message)
