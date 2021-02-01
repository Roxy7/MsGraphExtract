FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

ENV TIMEOUT=0
ENV GRACEFUL_TIMEOUT=0
ENV LOG_LEVEL="debug"

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./api/ .