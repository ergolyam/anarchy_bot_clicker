FROM python:3.12-alpine

RUN apk add --no-cache gcc musl-dev uv

WORKDIR /app

COPY pyproject.toml uv.lock /app

RUN uv sync

COPY . /app

ENV PYTHONUNBUFFERED=1

ENV SESSIONS_PATH=/app/sessions

CMD ["uv", "run", "main.py"]

