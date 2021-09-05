FROM python:3.8-slim-buster

ENV PYTHONPATH=/app/server

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /server /app

WORKDIR /app

CMD ["python", "app.py"]