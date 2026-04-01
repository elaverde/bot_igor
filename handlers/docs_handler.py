import os
from config import bot

PATHDOCS = os.getenv("PATHDOCS", "/app")
BACKUP_CHAT_ID = os.getenv("BACKUP_CHAT_ID")

def handle_doc(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📎 Envía el documento .docx que quieres subir al servidor:")
    bot.register_next_step_handler(message, recibir_doc)

def recibir_doc(message):
    chat_id = message.chat.id

    if not message.document:
        bot.send_message(chat_id, "⚠️ No recibí ningún documento. Usa /doc e intenta de nuevo.")
        return

    if not message.document.file_name.endswith(".docx"):
        bot.send_message(chat_id, "⚠️ Solo se aceptan archivos .docx.")
        return

    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)

    destino = os.path.join(PATHDOCS, "storage", "plantillas", file_name)
    with open(destino, "wb") as f:
        f.write(downloaded)

    bot.send_message(chat_id, f"✅ Documento guardado: `{file_name}`", parse_mode="Markdown")

    if BACKUP_CHAT_ID:
        with open(destino, "rb") as f:
            bot.send_document(BACKUP_CHAT_ID, f, caption=f"📁 Plantilla subida: {file_name}")
