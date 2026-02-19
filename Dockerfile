FROM python:3.11-slim

WORKDIR /app

# Copy requirements first
COPY backend/requirements.txt .

# Install Python packages (no system deps needed!)
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code to root
COPY backend/ ./

# Create temp directory
RUN mkdir -p /app/temp

# Set environment
ENV PYTHONPATH=/app
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
