FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir watchdog requests pyyaml

CMD ["python", "watcher.py"]