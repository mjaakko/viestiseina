FROM python:3.7-alpine

WORKDIR /app

COPY application /app/application
COPY requirements.txt /app

RUN apk add --no-cache musl-dev gcc postgresql-dev && \
    pip install -r requirements.txt && \
    adduser -D app

USER app

CMD gunicorn --bind 0.0.0.0:8000 --preload --workers 1 application:app
