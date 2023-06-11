FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc


COPY app/requirements.txt .


RUN pip install -r requirements.txt


COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]