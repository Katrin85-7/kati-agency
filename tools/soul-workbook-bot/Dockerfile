FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PDF_DIR=/app/pdfs \
    DATA_DIR=/data \
    PORT=8080

EXPOSE 8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py chs.py config.py db.py ./
COPY pdfs/ /app/pdfs/

RUN mkdir -p /data

CMD ["python", "bot.py"]
