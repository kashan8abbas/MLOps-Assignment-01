# Placeholder Dockerfile for future CI/CD
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts
COPY data ./data
COPY models ./models
COPY README.md .

ENV FLASK_APP=app.app:app
ENV MODEL_PATH=/app/models/model.pkl

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


