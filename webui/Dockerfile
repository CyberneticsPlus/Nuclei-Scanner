FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y docker.io
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app .

CMD ["python", "app.py"]
