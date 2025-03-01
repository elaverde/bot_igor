import os
from config import bot
from libs import Uground


# Diccionario para guardar los datos temporales de cada usuario
user_data = {}

def ask_fecha(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "📅 Ingresa la fecha en formato 'dd-mm-yyyy' o escribe 'hoy':")
    bot.register_next_step_handler(message, ask_concepto)

def ask_concepto(message):
    chat_id = message.chat.id
    user_data[chat_id]["fecha"] = message.text
    bot.send_message(chat_id, "✍️ Ingresa el concepto de la cuenta de cobro:")
    bot.register_next_step_handler(message, ask_n_cobro)

def ask_n_cobro(message):
    chat_id = message.chat.id
    user_data[chat_id]["concepto"] = message.text
    bot.send_message(chat_id, "🔢 Ingresa el número de cobro:")
    bot.register_next_step_handler(message, generar_cuenta)

def generar_cuenta(message):
    chat_id = message.chat.id
    user_data[chat_id]["n_cobro"] = message.text
    datos = user_data[chat_id]

    print(f"📌 Datos recibidos: {datos}")  # ✅ Verifica que los datos no estén vacíos

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc = Uground(base_dir)
    
    # Verificar que los datos lleguen correctamente a la función
    doc.leer_parametros(datos["fecha"], datos["n_cobro"], datos["concepto"])

    print(f"📌 Fecha en doc: {doc.fecha}")  # ✅ Verificar que los valores se asignaron correctamente
    print(f"📌 Concepto en doc: {doc.concepto}")
    print(f"📌 Número de cobro en doc: {doc.n_cobro}")

    # Generar cuenta de cobro y obtener la ruta del PDF
    pdf_path = doc.generar_cuenta_cobro_uground()
    print(f"📁 Ruta PDF: {pdf_path}")  # ✅ Verificar que el archivo se genere correctamente

    # Enviar el archivo PDF al usuario
    with open(pdf_path, "rb") as pdf_file:
        bot.send_document(message.chat.id, pdf_file)

    bot.send_message(message.chat.id, "✅ ¡Cuenta de cobro generada y enviada!")

# Asignar el manejador al comando /cuenta
def handle_cuentas(message):
    ask_fecha(message)
