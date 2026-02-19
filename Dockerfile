FROM python:3.11-slim

WORKDIR /app

# Install Tesseract OCR with English and wget for downloading Thai data
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download Thai language data manually
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata \
    && cd /usr/share/tesseract-ocr/4.00/tessdata \
    && wget -q https://github.com/tesseract-ocr/tessdata/raw/main/tha.traineddata \
    && wget -q https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# Copy requirements first
COPY backend/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code to root
COPY backend/ ./

# Create temp directory
RUN mkdir -p /app/temp

# Set environment
ENV PYTHONPATH=/app
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
