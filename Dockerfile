FROM python:3.12.10-alpine3.21

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev netcat-openbsd \
    && pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Copia y da permisos al script de espera de PostgreSQL
COPY wait_for_postgres.sh /wait_for_postgres.sh
RUN chmod +x /wait_for_postgres.sh

CMD ["/wait_for_postgres.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
