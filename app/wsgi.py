"""
Bu modül, Streamlit uygulamasını WSGI/ASGI uyumlu bir web uygulamasına dönüştürür.
Bu sayede Gunicorn veya Uvicorn gibi production-ready sunucular kullanabilir.
"""

import os
import sys
import subprocess
from aiohttp import web
import asyncio
import threading
import signal
import time

# Streamlit'i çalıştıran thread
def run_streamlit():
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    args = ["streamlit", "run", 
            "../streamlit_app.py", 
            "--server.port=8501",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false", 
            "--server.maxUploadSize=5",
            "--server.runOnSave=true",
            "--server.fileWatcherType=auto"]
    
    process = subprocess.Popen(args)
    return process

# Streamlit process başlat
streamlit_process = run_streamlit()

# Düzenli olarak sistemin çalışıp çalışmadığını kontrol eden heartbeat
async def heartbeat_checker():
    while True:
        # Log çıktısı
        print(f"[{time.ctime()}] Heartbeat kontrol ediliyor...")
        
        try:
            # Streamlit süreci çalışıyor mu kontrol et
            if streamlit_process.poll() is not None:
                print("Streamlit süreci çökmüş, yeniden başlatılıyor...")
                # Streamlit'i yeniden başlat
                global streamlit_process
                streamlit_process = run_streamlit()
                
        except Exception as e:
            print(f"Heartbeat hatası: {e}")
        
        # 60 saniye bekle
        await asyncio.sleep(60)

# Web sunucusunun varsayılan rotası
async def handle(request):
    return web.Response(text="Streamlit uygulaması çalışıyor! Lütfen tarayıcınızdan erişin.")

# Web uygulaması oluştur
app = web.Application()
app.router.add_get("/", handle)
app.router.add_get("/health", handle)  # Sağlık kontrolü endpoint'i

# WSGI/ASGI adaptörü
def wsgi_app(environ, start_response):
    """WSGI uyumlu bir uygulama döndür."""
    path = environ.get('PATH_INFO', '').lstrip('/')
    
    if path == '' or path == 'health':
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [b'Streamlit uygulamasi calisiyor! Lutfen tarayicinizdan erisin.']
    
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Sayfa bulunamadi']

# Uygulama başlangıcında heartbeat başlat
@app.on_startup.append
async def start_heartbeat(_):
    app['heartbeat_task'] = asyncio.create_task(heartbeat_checker())

# Uygulama kapandığında temizlik yap
@app.on_cleanup.append
async def cleanup_background_tasks(_):
    app['heartbeat_task'].cancel()
    await app['heartbeat_task']
    
    # Streamlit sürecini durdur
    if streamlit_process:
        streamlit_process.terminate()
        try:
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            streamlit_process.kill()

# Sinyal yakalama fonksiyonları - CTRL+C için
def signal_handler(sig, frame):
    print('Uygulama kapatılıyor...')
    if streamlit_process:
        streamlit_process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)