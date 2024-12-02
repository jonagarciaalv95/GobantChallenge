# Usamos la imagen base de Python 3.10 slim
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para psycopg2 y otras bibliotecas
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  # Limpiar para reducir el tamaño de la imagen

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar todos los archivos de la aplicación al contenedor
COPY . /app

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Exponer el puerto 5000 para la aplicación Flask (si es necesario)
EXPOSE 5000

# Comando para ejecutar los dos scripts de manera secuencial
CMD python migration_data.py && python main.py
