"""
Web kazıma işlemleri için fonksiyonlar içeren modül.
Bu modül, çeşitli web sitelerinden veri kazıma ve analiz için kullanılır.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict, Any, Tuple

def get_headers() -> Dict[str, str]:
    """
    Web istekleri için gerçekçi HTTP başlıkları döndürür.
    
    Returns:
        Dict[str, str]: HTTP başlık bilgileri
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

def fetch_page(url: str) -> str:
    """
    Belirtilen URL'den web sayfasını indirir.
    
    Args:
        url (str): İndirilecek web sayfasının URL'si
    
    Returns:
        str: HTML içeriği
    """
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Hata: {url} adresinden veri alınamadı. Hata: {e}")
        return ""

def scrape_ekonomi_verileri() -> pd.DataFrame:
    """
    Ekonomi verilerini içeren bir web sayfasından verileri kazır.
    
    Returns:
        pd.DataFrame: Ekonomik göstergeler veri seti
    """
    url = "https://www.investing.com/economic-calendar/"
    html = fetch_page(url)
    
    if not html:
        return pd.DataFrame(columns=['Zaman', 'Ülke', 'Gösterge', 'Önem', 'Gerçek', 'Beklenti'])
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Veri kazıma işlemi (gerçek siteler için düzenlenmelidir)
    ekonomi_verileri = []
    
    try:
        # Örnek veri oluşturuluyor (gerçek kazıma kodu yerine)
        # Gerçek bir uygulama için bu kısım hedef sitenin yapısına göre özelleştirilmelidir
        veriler = [
            {"zaman": "08:00", "ulke": "Türkiye", "gosterge": "TÜFE", "onem": "Yüksek", "gercek": "9.8%", "beklenti": "10.1%"},
            {"zaman": "10:00", "ulke": "Almanya", "gosterge": "İşsizlik Oranı", "onem": "Orta", "gercek": "5.2%", "beklenti": "5.3%"},
            {"zaman": "15:30", "ulke": "ABD", "gosterge": "GSYİH", "onem": "Yüksek", "gercek": "2.1%", "beklenti": "1.9%"},
            {"zaman": "17:00", "ulke": "Avrupa", "gosterge": "Faiz Kararı", "onem": "Yüksek", "gercek": "4.25%", "beklenti": "4.25%"},
            {"zaman": "09:30", "ulke": "İngiltere", "gosterge": "PMI", "onem": "Orta", "gercek": "51.2", "beklenti": "50.8"}
        ]
        
        ekonomi_verileri = veriler
        
    except Exception as e:
        print(f"Veri ayrıştırma hatası: {e}")
    
    # DataFrame oluştur
    df = pd.DataFrame(ekonomi_verileri)
    return df

def scrape_borsa_verileri() -> pd.DataFrame:
    """
    Borsa verilerini içeren bir web sayfasından verileri kazır.
    
    Returns:
        pd.DataFrame: Borsa verileri veri seti
    """
    url = "https://www.investing.com/indices/major-indices"
    html = fetch_page(url)
    
    if not html:
        return pd.DataFrame(columns=['Endeks', 'Son', 'Yüksek', 'Düşük', 'Değişim', 'Değişim%', 'Zaman'])
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Örnek veri oluşturuluyor (gerçek kazıma kodu yerine)
    borsa_verileri = [
        {"endeks": "BIST 100", "son": "9,452.87", "yuksek": "9,523.45", "dusuk": "9,380.21", "degisim": "+124.56", "degisim_yuzde": "+1.32%", "zaman": "17:45:00"},
        {"endeks": "S&P 500", "son": "5,875.23", "yuksek": "5,890.12", "dusuk": "5,840.33", "degisim": "+25.78", "degisim_yuzde": "+0.44%", "zaman": "17:45:00"},
        {"endeks": "DAX", "son": "18,980.54", "yuksek": "19,020.87", "dusuk": "18,920.13", "degisim": "+130.42", "degisim_yuzde": "+0.69%", "zaman": "17:45:00"},
        {"endeks": "Nikkei 225", "son": "41,320.67", "yuksek": "41,450.23", "dusuk": "41,120.34", "degisim": "-87.45", "degisim_yuzde": "-0.21%", "zaman": "09:45:00"},
        {"endeks": "FTSE 100", "son": "8,234.12", "yuksek": "8,256.78", "dusuk": "8,201.34", "degisim": "+45.87", "degisim_yuzde": "+0.56%", "zaman": "16:45:00"}
    ]
    
    # DataFrame oluştur
    df = pd.DataFrame(borsa_verileri)
    return df

def scrape_kripto_verileri() -> pd.DataFrame:
    """
    Kripto para verilerini içeren bir web sayfasından verileri kazır.
    
    Returns:
        pd.DataFrame: Kripto para veri seti
    """
    url = "https://coinmarketcap.com/"
    html = fetch_page(url)
    
    if not html:
        return pd.DataFrame(columns=['Kripto', 'Fiyat', 'Değişim24h', 'Hacim24h', 'Piyasa Değeri'])
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Örnek veri oluşturuluyor (gerçek kazıma kodu yerine)
    kripto_verileri = [
        {"kripto": "Bitcoin", "fiyat": "85,423.45", "degisim24h": "+2.3%", "hacim24h": "24.5B", "piyasa_degeri": "1.68T"},
        {"kripto": "Ethereum", "fiyat": "4,567.89", "degisim24h": "+1.8%", "hacim24h": "12.3B", "piyasa_degeri": "548.7B"},
        {"kripto": "Solana", "fiyat": "245.67", "degisim24h": "+5.2%", "hacim24h": "3.2B", "piyasa_degeri": "107.3B"},
        {"kripto": "BNB", "fiyat": "678.32", "degisim24h": "-0.5%", "hacim24h": "1.8B", "piyasa_degeri": "103.2B"},
        {"kripto": "XRP", "fiyat": "1.23", "degisim24h": "-1.2%", "hacim24h": "980M", "piyasa_degeri": "67.4B"}
    ]
    
    # DataFrame oluştur
    df = pd.DataFrame(kripto_verileri)
    return df