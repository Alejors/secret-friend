FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPYCACHEPREFIX=/tmp

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", ":8000", "src.main:app", "--reload"]
