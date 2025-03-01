import os
from dotenv import load_dotenv
import telebot

# Cargar variables de entorno
load_dotenv()

# Token del bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Crear instancia del bot
bot = telebot.TeleBot(BOT_TOKEN)
