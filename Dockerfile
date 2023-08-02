FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY app .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]