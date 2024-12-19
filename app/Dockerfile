# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias necesarias
#RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto 5000
EXPOSE 5000

# Ejecuta el comando para iniciar Flask
CMD ["python", "pre_processing.py"]
