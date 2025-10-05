# Dockerfile for FastAPI application
FROM python:3.12-slim
WORKDIR /app
COPY ./demoApp /app
# Use requirements.txt if available
RUN pip install --no-cache-dir -r requirements.txt
# If not using requirements.txt, install dependencies directly
# RUN pip install --no-cache-dir fastapi uvicorn
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

