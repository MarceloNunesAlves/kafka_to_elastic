FROM python:3.9-slim-buster

# Configuração do ambiente
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    libjpeg62 \
    openjdk-11-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN mkdir app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./utils /app/utils
COPY ./main.py /app/main.py

ENTRYPOINT python main.py