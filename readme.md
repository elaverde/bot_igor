# 📌 Deploy de Bot de Telegram con Docker

Este proyecto contiene un **Bot de Telegram** que se ejecuta dentro de un contenedor Docker.

## 🚀 Construcción y ejecución con Docker

### 🔹 1. Construir la imagen

Ejecuta el siguiente comando para crear la imagen de Docker:

```bash
docker build -t telegram-bot .
```
### 🔹 2. Ejecutar el contenedor

Para iniciar el bot con las variables de entorno definidas en .env, usa:

```bash
docker run --env-file .env -v $(pwd):/app telegram-bot
```
## 📂 Estructura del proyect

📁 proyecto/
│── 📄 Dockerfile          # Configuración del contenedor
│── 📄 bot.py              # Código principal del bot
│── 📄 requirements.txt    # Dependencias de Python
│── 📄 .env                # Variables de entorno del bot
│── 📂 handlers/           # Manejadores de comandos
│── 📂 libs/               # Librerías personalizadas
│── 📂 storage/            # Archivos generados


⚙️ Configuración
### Editar el archivo .env con las credenciales del bot:

TELEGRAM_BOT_TOKEN=tu_token_aqui

### Instalar dependencias (si lo ejecutas sin Docker)

```bash
pip install -r requirements.txt
```

🔄 Reinicio automático en cambios
El bot se ejecuta con watchmedo, lo que permite reiniciar automáticamente en caso de cambios en el código:

```bash
watchmedo auto-restart --patterns="*.py" --recursive -- python bot.py
```

📌 Notas
Docker simplifica la ejecución sin necesidad de instalar dependencias manualmente.
Asegúrate de tener Docker instalado antes de ejecutar los comandos.
El volumen -v $(pwd):/app permite que los cambios en el código se reflejen sin reconstruir la imagen.