FROM python:3.10-slim AS base

ENV PATH /opt/venv/bin:$PATH
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

FROM base AS builder
RUN python -m venv /opt/venv
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

FROM base
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY main.py .

ARG PORT=8000
ENV PORT $PORT
EXPOSE $PORT

CMD exec uvicorn --host 0.0.0.0 --port $PORT main:app