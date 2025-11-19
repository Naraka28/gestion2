FROM python:3.11-slim

# Evita prompts de APT
ENV DEBIAN_FRONTEND=noninteractive

# Instalar solo lo necesario (una sola capa)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        libzmq3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar SOLO requirements primero para usar caché
COPY requirements.txt .

# Instalar dependencias Python aprovechando caché
RUN pip install --no-cache-dir -r requirements.txt

# Ahora sí copiar la app
COPY . .

EXPOSE 80

CMD ["python", "main.py"]
