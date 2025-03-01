from config import bot
from handlers import handle_start, handle_cuentas, handle_pagos_inyecciones

# Asignar manejadores a los comandos
bot.message_handler(commands=["start"])(handle_start)
bot.message_handler(commands=["cuenta"])(handle_cuentas)
bot.message_handler(commands=["pago_inyecciones"])(handle_pagos_inyecciones) 
# Iniciar el bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
