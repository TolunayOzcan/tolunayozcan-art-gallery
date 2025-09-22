# Tolunay Özcan Veri Sanatı Portfolyosu

Bu repo, GitHub Pages ve Streamlit Cloud entegrasyonuyla çalışan bir veri bilimi portfolyosunu içermektedir. Projede JavaScript tabanlı bir Single Page Application (SPA) ve Streamlit kullanılarak geliştirilmiş interaktif bir veri analizi uygulaması bulunmaktadır.

## Proje Yapısı

- **Web Uygulaması (GitHub Pages)**: tolunayozcan.art üzerinde barındırılan JavaScript tabanlı SPA
- **Veri Uygulaması (Streamlit Cloud)**: tolunayozcan.streamlit.app üzerinde barındırılan Streamlit uygulaması

## Portfolyo İçeriği

- **Ana Sayfa**: Genel bilgiler ve portföy hakkında açıklamalar
- **Analizler**: Çeşitli veri kümeleri üzerinde yapılmış analiz çalışmaları
- **Canlı Veriler**: Web kazıma yoluyla anlık olarak alınan güncel ekonomi, borsa ve kripto verileri
- **Veri Bilimi**: Makine öğrenmesi ve veri bilimi örnek çalışmaları
  - Random Forest Sınıflandırma
  - A/B Test Analizi
  - Müşteri Segmentasyonu
  - Regresyon Analizi

## Web Uygulaması (GitHub Pages)

Web uygulaması aşağıdaki dosyaları içerir:

- `index.html`: Ana giriş sayfası
- `js/main.js`: Ana JavaScript dosyası (SPA router ve genel fonksiyonlar)
- `js/pages.js`: Sayfa içeriklerini tanımlayan JavaScript dosyası

### Özellikler

- Modern, profesyonel ve minimal tasarım
- Tamamen responsive yapı
- Single Page Application (SPA) mimarisi
- Akıcı sayfa geçişleri ve animasyonlar
- Streamlit uygulamasına kolay geçiş

## Teknolojiler

- **Web**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Veri**: Python, Streamlit, Pandas, NumPy, Plotly
- **Görselleştirme**: Plotly, Matplotlib, Seaborn
- **Veri İşleme**: Pandas, NumPy, BeautifulSoup
- **Makine Öğrenmesi**: Scikit-Learn, TensorFlow

## Çalıştırma

### Web Uygulaması

Web uygulamasını yerel ortamda çalıştırmak için herhangi bir HTTP sunucusu kullanabilirsiniz:

```bash
# Python ile basit bir HTTP sunucusu
python -m http.server 8000
```

### Streamlit Uygulaması

```bash
# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
streamlit run app/portfolio.py
```

## Canlı Demo

- **Web Uygulaması**: [https://tolunayozcan.art](https://tolunayozcan.art)
- **Streamlit Uygulaması**: [https://tolunayozcan.streamlit.app](https://tolunayozcan.streamlit.app)