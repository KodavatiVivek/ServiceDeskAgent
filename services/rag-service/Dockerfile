FROM python:3.11-slim

WORKDIR /app

COPY services/rag-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/rag-service/app ./app
COPY data ./data
COPY libs ./libs

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
