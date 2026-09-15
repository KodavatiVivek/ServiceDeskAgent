FROM python:3.11-slim

WORKDIR /app

COPY services/audit-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/audit-service/app ./app
COPY libs ./libs

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
