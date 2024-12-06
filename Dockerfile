FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPYCACHEPREFIX=/tmp

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD gunicorn --bind :$PORT src.main:app --workers 1 --threads 8 --timeout 0 --reload -t 60
