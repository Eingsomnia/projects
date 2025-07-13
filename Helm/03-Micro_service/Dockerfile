# Dockerfile
FROM python:3.10-slim

LABEL maintainer="chayodom@storemesh.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["python", "server.py"]