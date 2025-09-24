FROM python:3.9-slim

WORKDIR /app

# Sistem paketleri
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Port ortam değişkeni
ENV PORT=8501
EXPOSE $PORT

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:$PORT/_stcore/health || exit 1

# Streamlit başlat
CMD streamlit run app/portfolio.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false