FROM python:3.9-slim

WORKDIR /app

# Sistem paketleri (sağlıklı build/log/healthcheck için)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/portfolio.py", "--server.port=8501", "--server.address=0.0.0.0"]