FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8050

CMD ["python", "app.py"]
