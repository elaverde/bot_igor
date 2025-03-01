FROM python:3.9-slim  

WORKDIR /app

# Instalar LibreOffice en la imagen
RUN apt-get update && apt-get install -y \
    libreoffice-core \
    libreoffice-writer \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt watchfiles  



# Copiar código fuente
COPY . .

CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "main.py"]
