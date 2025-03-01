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

# Crear carpetas necesarias
RUN mkdir -p storage/cuentas_de_cobro
RUN mkdir -p storage/plantillas

# Copiar archivos de plantillas desde la máquina al contenedor
COPY torage/plantillas/ storage/plantillas/

# Copiar código fuente
COPY . .

CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "main.py"]
