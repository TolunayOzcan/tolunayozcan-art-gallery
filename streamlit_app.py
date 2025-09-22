# Bu dosya, uygulamanın Streamlit Cloud'da nasıl başlatılacağını tanımlar

# Gereksinimler
import streamlit as st
import os
import sys
import threading
import time
import signal
import requests

# Portfolio uygulamasını import et
from app.portfolio import *

# Sürekli çalışma için watchdog thread'i
class WatchdogThread(threading.Thread):
    def __init__(self, interval=60):
        threading.Thread.__init__(self)
        self.interval = interval
        self.daemon = True
        self.stopped = threading.Event()
        
    def run(self):
        while not self.stopped.wait(self.interval):
            try:
                # Kendi kendine ping at
                url = f"http://localhost:{os.environ.get('PORT', '8501')}"
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Watchdog ping: {url}")
                requests.get(url, timeout=10)
            except Exception as e:
                print(f"Watchdog error: {e}")

# Sinyal yakalayıcılar
def handle_exit(signum, frame):
    print("Uygulama kapatılıyor...")
    sys.exit(0)

# SIGINT ve SIGTERM sinyallerini yakala
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# Streamlit Cloud'da uygulamanın başlangıç noktası
if __name__ == "__main__":
    # Watchdog thread'ini başlat (ENV ile kontrol edilir)
    if os.getenv("ENABLE_WATCHDOG", "0").lower() in ("1", "true", "yes"):
        watchdog = WatchdogThread(interval=int(os.getenv("WATCHDOG_INTERVAL", "120")))
        watchdog.start()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Watchdog aktif.")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Watchdog devre dışı (ENABLE_WATCHDOG=0).")
    
    # Uygulamanın ana sayfası zaten yüklenmiş durumda
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Streamlit uygulaması başlatıldı.")
    
    # Streamlit Cloud bu dosyayı otomatik olarak bulacak ve çalıştıracaktır
    # Bu dosya yüklendiğinde portfolio.py içindeki tüm kodlar otomatik olarak çalışır