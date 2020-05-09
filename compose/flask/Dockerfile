FROM python:3.7-slim-buster

ENV PYTHONPATH=/app/server

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /server /app

WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]