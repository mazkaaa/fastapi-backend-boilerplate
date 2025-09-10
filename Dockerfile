## Build a small production image for the FastAPI app
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install minimal system deps (if you need additional system libs, add them here)
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create a non-root user and ensure ownership of the app files
RUN useradd --create-home appuser \
  && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Run with uvicorn. Use production-grade server or process manager in real deployments.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
