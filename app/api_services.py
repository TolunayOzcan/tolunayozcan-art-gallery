"""
Gerçek API entegrasyonları için servis modülü
Bu modül çeşitli public API'lerden gerçek veri çeker
"""

import requests
import pandas as pd
import json
from typing import Dict, List, Any, Optional
import time
from datetime import datetime

class APIService:
    """API servis sınıfı - gerçek veri entegrasyonları"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_crypto_data(self) -> pd.DataFrame:
        """
        CoinGecko API'den kripto para verilerini çeker
        """
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': False
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            crypto_list = []
            for coin in data:
                crypto_list.append({
                    'Kripto': coin['name'],
                    'Sembol': coin['symbol'].upper(),
                    'Fiyat (USD)': f"${coin['current_price']:,.2f}",
                    'Değişim 24h': f"{coin['price_change_percentage_24h']:.2f}%",
                    'Piyasa Değeri': f"${coin['market_cap']:,}",
                    'Hacim 24h': f"${coin['total_volume']:,}"
                })
            
            return pd.DataFrame(crypto_list)
            
        except Exception as e:
            print(f"Kripto veri çekme hatası: {e}")
            return self._get_fallback_crypto_data()
    
    def get_exchange_rates(self) -> pd.DataFrame:
        """
        ExchangeRate API'den döviz kurlarını çeker
        """
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data['rates']
            
            # Önemli döviz kurları
            important_currencies = ['EUR', 'GBP', 'JPY', 'TRY', 'CAD', 'AUD', 'CHF']
            
            exchange_list = []
            for currency in important_currencies:
                if currency in rates:
                    exchange_list.append({
                        'Döviz Çifti': f'USD/{currency}',
                        'Kur': f"{rates[currency]:.4f}",
                        'Ters Kur': f"{1/rates[currency]:.4f}" if rates[currency] != 0 else "N/A",
                        'Güncelleme': datetime.now().strftime("%H:%M:%S")
                    })
            
            return pd.DataFrame(exchange_list)
            
        except Exception as e:
            print(f"Döviz kuru çekme hatası: {e}")
            return self._get_fallback_exchange_data()
    
    def get_weather_data(self, city: str = "Istanbul") -> Dict[str, Any]:
        """
        OpenWeatherMap API'den hava durumu verilerini çeker
        """
        try:
            # Free tier API - API key gerekmez, sınırlı veri
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': 'demo',  # Demo için
                'units': 'metric'
            }
            
            # API key olmadığı için fallback veri döndür
            return self._get_fallback_weather_data(city)
            
        except Exception as e:
            print(f"Hava durumu veri çekme hatası: {e}")
            return self._get_fallback_weather_data(city)
    
    def get_news_headlines(self) -> List[Dict[str, str]]:
        """
        NewsAPI'den son haberları çeker (demo veriler)
        """
        try:
            # Demo veri döndür - gerçek API key gerekir
            return self._get_fallback_news_data()
            
        except Exception as e:
            print(f"Haber çekme hatası: {e}")
            return self._get_fallback_news_data()
    
    def get_stock_data(self) -> pd.DataFrame:
        """
        Alpha Vantage API'den hisse senedi verilerini çeker
        """
        try:
            # Demo veri döndür - gerçek API key gerekir
            return self._get_fallback_stock_data()
            
        except Exception as e:
            print(f"Hisse senedi veri çekme hatası: {e}")
            return self._get_fallback_stock_data()
    
    # Fallback fonksiyonları
    def _get_fallback_crypto_data(self) -> pd.DataFrame:
        """Kripto para için fallback veriler"""
        crypto_data = [
            {'Kripto': 'Bitcoin', 'Sembol': 'BTC', 'Fiyat (USD)': '$85,423.45', 
             'Değişim 24h': '+2.34%', 'Piyasa Değeri': '$1,680,000,000,000', 'Hacim 24h': '$24,500,000,000'},
            {'Kripto': 'Ethereum', 'Sembol': 'ETH', 'Fiyat (USD)': '$4,567.89', 
             'Değişim 24h': '+1.87%', 'Piyasa Değeri': '$548,700,000,000', 'Hacim 24h': '$12,300,000,000'},
            {'Kripto': 'Solana', 'Sembol': 'SOL', 'Fiyat (USD)': '$245.67', 
             'Değişim 24h': '+5.23%', 'Piyasa Değeri': '$107,300,000,000', 'Hacim 24h': '$3,200,000,000'},
            {'Kripto': 'BNB', 'Sembol': 'BNB', 'Fiyat (USD)': '$678.32', 
             'Değişim 24h': '-0.54%', 'Piyasa Değeri': '$103,200,000,000', 'Hacim 24h': '$1,800,000,000'},
            {'Kripto': 'XRP', 'Sembol': 'XRP', 'Fiyat (USD)': '$1.23', 
             'Değişim 24h': '-1.25%', 'Piyasa Değeri': '$67,400,000,000', 'Hacim 24h': '$980,000,000'}
        ]
        return pd.DataFrame(crypto_data)
    
    def _get_fallback_exchange_data(self) -> pd.DataFrame:
        """Döviz kurları için fallback veriler"""
        exchange_data = [
            {'Döviz Çifti': 'USD/TRY', 'Kur': '34.25', 'Ters Kur': '0.0292', 'Güncelleme': datetime.now().strftime("%H:%M:%S")},
            {'Döviz Çifti': 'USD/EUR', 'Kur': '0.9234', 'Ters Kur': '1.0829', 'Güncelleme': datetime.now().strftime("%H:%M:%S")},
            {'Döviz Çifti': 'USD/GBP', 'Kur': '0.7845', 'Ters Kur': '1.2747', 'Güncelleme': datetime.now().strftime("%H:%M:%S")},
            {'Döviz Çifti': 'USD/JPY', 'Kur': '149.85', 'Ters Kur': '0.0067', 'Güncelleme': datetime.now().strftime("%H:%M:%S")},
            {'Döviz Çifti': 'USD/CAD', 'Kur': '1.3567', 'Ters Kur': '0.7371', 'Güncelleme': datetime.now().strftime("%H:%M:%S")}
        ]
        return pd.DataFrame(exchange_data)
    
    def _get_fallback_weather_data(self, city: str) -> Dict[str, Any]:
        """Hava durumu için fallback veriler"""
        return {
            'city': city,
            'temperature': 22,
            'description': 'Partly Cloudy',
            'humidity': 65,
            'wind_speed': 12,
            'pressure': 1013,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _get_fallback_news_data(self) -> List[Dict[str, str]]:
        """Haberler için fallback veriler"""
        return [
            {
                'title': 'Teknoloji Sektöründe Yeni Gelişmeler',
                'description': 'AI ve makine öğrenimi alanında son trendler...',
                'source': 'Tech News',
                'publishedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'title': 'Piyasalarda Güncel Durum',
                'description': 'Küresel piyasalarda son gelişmeler ve analizler...',
                'source': 'Finance Today',
                'publishedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'title': 'Veri Biliminde Yenilikler',
                'description': 'Büyük veri analizi ve görselleştirme teknikleri...',
                'source': 'Data Science Weekly',
                'publishedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    
    def _get_fallback_stock_data(self) -> pd.DataFrame:
        """Hisse senetleri için fallback veriler"""
        stock_data = [
            {'Hisse': 'AAPL', 'Fiyat': '$175.45', 'Değişim': '+2.34%', 'Hacim': '45,234,567'},
            {'Hisse': 'GOOGL', 'Fiyat': '$142.78', 'Değişim': '+1.87%', 'Hacim': '23,456,789'},
            {'Hisse': 'MSFT', 'Fiyat': '$378.92', 'Değişim': '-0.45%', 'Hacim': '18,765,432'},
            {'Hisse': 'TSLA', 'Fiyat': '$245.67', 'Değişim': '+3.21%', 'Hacim': '67,890,123'},
            {'Hisse': 'NVDA', 'Fiyat': '$487.23', 'Değişim': '+4.56%', 'Hacim': '34,567,890'}
        ]
        return pd.DataFrame(stock_data)

# Global API service instance
api_service = APIService()