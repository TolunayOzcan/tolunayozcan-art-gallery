import time
import threading
import requests
import os

class HeartbeatManager:
    """
    Bu sınıf, uygulamanın sürekli çalışır durumda kalmasını sağlamak için
    periyodik olarak "kalp atışları" gönderir. Bu, uygulamanın kendisinin
    otomatik olarak uyanık kalmasını sağlar.
    """
    
    def __init__(self, interval=60):
        """
        Heartbeat yöneticisini başlatır.
        
        Args:
            interval (int): Kalp atışları arasındaki süre (saniye cinsinden)
        """
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = None
        self.app_url = os.environ.get("APP_URL", "http://localhost:8501")
        
    def _get_app_url(self):
        """
        Uygulama URL'sini alır. Eğer Streamlit Cloud'da çalışıyorsa,
        APP_URL ortam değişkenini kullanır.
        """
        if "STREAMLIT_SHARING_PORT" in os.environ:
            # Streamlit Cloud'da çalışıyoruz
            return f"https://{os.environ.get('STREAMLIT_APP_URL', 'localhost:8501')}"
        return self.app_url
    
    def _heartbeat_worker(self):
        """
        Periyodik olarak uygulamaya istekler göndererek canlı kalmasını sağlar.
        """
        while not self.stop_event.is_set():
            try:
                url = self._get_app_url()
                # Uygulamanın ana sayfasına istek gönder
                requests.get(url, timeout=10)
                print(f"[HeartbeatManager] Kalp atışı gönderildi - {time.strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"[HeartbeatManager] Hata: {e}")
            
            # Bir sonraki kalp atışına kadar bekle
            time.sleep(self.interval)
    
    def start(self):
        """Heartbeat işlemini başlatır."""
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._heartbeat_worker, daemon=True)
            self.thread.start()
            print("[HeartbeatManager] Heartbeat başlatıldı.")
    
    def stop(self):
        """Heartbeat işlemini durdurur."""
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join(timeout=5)
            print("[HeartbeatManager] Heartbeat durduruldu.")

# Singleton örneği
heartbeat_manager = HeartbeatManager(interval=120)  # 2 dakikada bir kontrol et