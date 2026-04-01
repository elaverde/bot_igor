import os
from config import bot

# Crear carpetas necesarias si no existen
PATHDOCS = os.getenv("PATHDOCS", "/app")
os.makedirs(os.path.join(PATHDOCS, "storage", "plantillas"), exist_ok=True)
os.makedirs(os.path.join(PATHDOCS, "storage", "cuentas_de_cobro"), exist_ok=True)
from handlers import handle_start, handle_cuentas, handle_fecha_callback, handle_ncobro_callback, handle_pagos_inyecciones, handle_mes_callback, handle_anio_callback, handle_doc

# Asignar manejadores a los comandos
bot.message_handler(commands=["start"])(handle_start)
bot.message_handler(commands=["cuenta"])(handle_cuentas)
bot.message_handler(commands=["pago_inyecciones", "pago"])(handle_pagos_inyecciones)
bot.message_handler(commands=["doc"])(handle_doc)
bot.callback_query_handler(func=lambda call: call.data.startswith("fecha_"))(handle_fecha_callback)
bot.callback_query_handler(func=lambda call: call.data.startswith("ncobro_"))(handle_ncobro_callback)
bot.callback_query_handler(func=lambda call: call.data.startswith("inj_mes_"))(handle_mes_callback)
bot.callback_query_handler(func=lambda call: call.data.startswith("inj_anio_"))(handle_anio_callback)

# Iniciar el bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
