import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def generate_classification_data():
    """İkili sınıflandırma için örnek veri seti oluşturur."""
    # scikit-learn kullanmadan doğrudan mock veri oluştur
    np.random.seed(42)
    n_samples = 500
    
    # Özellikler için rastgele veriler oluştur
    features = {
        'yaş': np.random.normal(40, 10, n_samples),
        'gelir': np.random.normal(50000, 15000, n_samples),
        'kredi_skoru': np.random.normal(700, 100, n_samples),
        'harcama_oranı': np.random.normal(0.3, 0.1, n_samples),
        'üyelik_süresi': np.random.normal(5, 3, n_samples),
        'etkileşim': np.random.normal(100, 30, n_samples)
    }
    
    X = pd.DataFrame(features)
    
    # Sınıf etiketlerini oluştur
    y = np.random.randint(0, 2, n_samples)
    
    return X, y

def create_random_forest_plot(X, y):
    """Random Forest modelini simüle eden bir görselleştirme oluşturur."""
    # Gerçek bir model olmadan özellik önemlerini simüle et
    np.random.seed(42)
    feature_importance = pd.DataFrame({
        'özellik': X.columns,
        'önem': np.array([0.35, 0.25, 0.18, 0.12, 0.07, 0.03])  # Sabit değerler
    }).sort_values('önem', ascending=False)
    
    # Özellik önemlerini görselleştirme
    fig = px.bar(
        feature_importance,
        x='önem',
        y='özellik',
        orientation='h',
        title='Random Forest Özellik Önemleri',
        color='önem',
        color_continuous_scale='Blues',
        labels={'önem': 'Önem Skoru', 'özellik': 'Özellik'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=20,
        font_size=14,
        height=500
    )
    
    # Model yerine basit bir sınıflandırıcı döndür
    class MockModel:
        def __init__(self):
            self.feature_importances_ = np.array([0.35, 0.25, 0.18, 0.12, 0.07, 0.03])
            
        def predict(self, X):
            # Basit bir tahmin fonksiyonu
            return np.random.randint(0, 2, len(X))
    
    model = MockModel()
    return model, fig

def generate_ab_test_data():
    """A/B test için örnek veri seti oluşturur."""
    # Parametreler
    n_samples = 1000
    conversion_rate_a = 0.12
    conversion_rate_b = 0.15
    
    # Kullanıcı grupları
    np.random.seed(42)
    data = pd.DataFrame({
        'kullanici_id': range(n_samples),
        'grup': np.random.choice(['A', 'B'], size=n_samples)
    })
    
    # Dönüşüm durumları
    data['donusum'] = data['grup'].apply(
        lambda x: np.random.choice(
            [0, 1],
            p=[1-conversion_rate_a, conversion_rate_a] if x == 'A' else [1-conversion_rate_b, conversion_rate_b]
        )
    )
    
    # Harcama miktarları (dönüşüm varsa)
    data['harcama'] = 0
    data.loc[(data['grup'] == 'A') & (data['donusum'] == 1), 'harcama'] = np.random.normal(150, 30, size=((data['grup'] == 'A') & (data['donusum'] == 1)).sum())
    data.loc[(data['grup'] == 'B') & (data['donusum'] == 1), 'harcama'] = np.random.normal(160, 35, size=((data['grup'] == 'B') & (data['donusum'] == 1)).sum())
    
    return data

def create_ab_test_plot(data):
    """A/B test sonuçlarını görselleştirir."""
    # Dönüşüm oranları grafiği
    conversion_rates = data.groupby('grup')['donusum'].mean().reset_index()
    conversion_rates['donusum'] = conversion_rates['donusum'] * 100  # Yüzde cinsinden
    
    conversion_fig = px.bar(
        conversion_rates,
        x='grup',
        y='donusum',
        color='grup',
        title='Dönüşüm Oranları (%)',
        labels={'donusum': 'Dönüşüm Oranı (%)', 'grup': 'Grup'},
        text_auto='.2f',
        color_discrete_map={'A': '#5A9BD5', 'B': '#ED7D31'}
    )
    
    conversion_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    # Ortalama harcama grafiği
    spending_data = data[data['donusum'] == 1].groupby('grup')['harcama'].mean().reset_index()
    
    spending_fig = px.bar(
        spending_data,
        x='grup',
        y='harcama',
        color='grup',
        title='Ortalama Harcama (TL)',
        labels={'harcama': 'Ortalama Harcama (TL)', 'grup': 'Grup'},
        text_auto='.2f',
        color_discrete_map={'A': '#5A9BD5', 'B': '#ED7D31'}
    )
    
    spending_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return conversion_fig, spending_fig

def generate_customer_segmentation_data():
    """Müşteri segmentasyonu için örnek veri seti oluşturur."""
    np.random.seed(42)
    n_samples = 500
    
    # Yüksek değerli müşteriler
    high_value = pd.DataFrame({
        'musteri_id': [f'H{i}' for i in range(100)],
        'yillik_harcama': np.random.normal(5000, 1000, 100),
        'alisveris_sikligi': np.random.normal(20, 5, 100),
        'musteri_suresi': np.random.normal(5, 1, 100),
        'segment': 'Yüksek Değer'
    })
    
    # Orta değerli müşteriler
    mid_value = pd.DataFrame({
        'musteri_id': [f'M{i}' for i in range(200)],
        'yillik_harcama': np.random.normal(2500, 500, 200),
        'alisveris_sikligi': np.random.normal(10, 3, 200),
        'musteri_suresi': np.random.normal(3, 1, 200),
        'segment': 'Orta Değer'
    })
    
    # Düşük değerli müşteriler
    low_value = pd.DataFrame({
        'musteri_id': [f'L{i}' for i in range(150)],
        'yillik_harcama': np.random.normal(1000, 300, 150),
        'alisveris_sikligi': np.random.normal(5, 2, 150),
        'musteri_suresi': np.random.normal(2, 0.5, 150),
        'segment': 'Düşük Değer'
    })
    
    # Yeni müşteriler
    new_customers = pd.DataFrame({
        'musteri_id': [f'N{i}' for i in range(50)],
        'yillik_harcama': np.random.normal(800, 200, 50),
        'alisveris_sikligi': np.random.normal(3, 1, 50),
        'musteri_suresi': np.random.normal(0.5, 0.2, 50),
        'segment': 'Yeni Müşteri'
    })
    
    # Veri setlerini birleştir
    data = pd.concat([high_value, mid_value, low_value, new_customers], ignore_index=True)
    
    # Negatif değerleri düzelt
    for col in ['yillik_harcama', 'alisveris_sikligi', 'musteri_suresi']:
        data.loc[data[col] < 0, col] = 0
    
    return data

def create_segmentation_plot(data):
    """Müşteri segmentasyonunu 3D görselleştirme ile sunar."""
    fig = px.scatter_3d(
        data,
        x='yillik_harcama',
        y='alisveris_sikligi',
        z='musteri_suresi',
        color='segment',
        hover_name='musteri_id',
        labels={
            'yillik_harcama': 'Yıllık Harcama (TL)',
            'alisveris_sikligi': 'Alışveriş Sıklığı (yıllık)',
            'musteri_suresi': 'Müşteri Süresi (yıl)',
            'segment': 'Müşteri Segmenti'
        },
        color_discrete_map={
            'Yüksek Değer': '#1F77B4',  # Mavi
            'Orta Değer': '#FF7F0E',    # Turuncu
            'Düşük Değer': '#2CA02C',   # Yeşil
            'Yeni Müşteri': '#D62728'   # Kırmızı
        }
    )
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Yıllık Harcama (TL)',
            yaxis_title='Alışveriş Sıklığı (yıllık)',
            zaxis_title='Müşteri Süresi (yıl)'
        ),
        height=700,
        margin=dict(l=0, r=0, b=0, t=30),
        title='Müşteri Segmentasyonu 3D Görünümü'
    )
    
    return fig

def generate_regression_data():
    """Regresyon için örnek veri seti oluşturur."""
    np.random.seed(42)
    n_samples = 200
    
    # Özellikler için rastgele veriler oluştur
    features = {
        'reklam_harcaması': np.random.normal(1000, 300, n_samples),
        'müşteri_memnuniyeti': np.random.normal(8, 1, n_samples),
        'ürün_kalitesi': np.random.normal(7, 1.5, n_samples),
        'pazar_rekabeti': np.random.normal(6, 2, n_samples),
        'fiyat_optimizasyonu': np.random.normal(5, 1, n_samples)
    }
    
    X = pd.DataFrame(features)
    
    # Hedef değişkeni oluştur
    y = (
        0.5 * X['reklam_harcaması'] + 
        0.3 * X['müşteri_memnuniyeti'] * 100 + 
        0.2 * X['ürün_kalitesi'] * 80 - 
        0.1 * X['pazar_rekabeti'] * 50 + 
        0.05 * X['fiyat_optimizasyonu'] * 120
    ) + np.random.normal(0, 500, n_samples)
    
    return X, y

def create_regression_plot(X, y):
    """Regresyon modeli simülasyonu ve sonuçları görselleştirir."""
    # Basit bir tahmin yap
    np.random.seed(42)
    y_pred = y + np.random.normal(0, 300, len(y))  # Gerçek değerlere biraz gürültü ekle
    
    # Gerçek vs Tahmin grafiği
    fig = px.scatter(
        x=y,
        y=y_pred,
        labels={'x': 'Gerçek Değerler', 'y': 'Tahmin Edilen Değerler'},
        title='Regresyon Modeli: Gerçek vs Tahmin'
    )
    
    # Mükemmel tahmin çizgisi (y=x)
    fig.add_trace(
        go.Scatter(
            x=[y.min(), y.max()],
            y=[y.min(), y.max()],
            mode='lines',
            name='Mükemmel Tahmin',
            line=dict(color='red', dash='dash')
        )
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    # Mock model
    class MockRegressor:
        def __init__(self):
            self.feature_importances_ = np.array([0.40, 0.30, 0.15, 0.10, 0.05])
            
        def predict(self, X):
            # Basit bir tahmin fonksiyonu (gerçek değerlere yakın)
            return np.random.normal(y.mean(), y.std(), len(X))
    
    model = MockRegressor()
    return model, fig

# sklearn özellikleri için dummy fonksiyon
def accuracy_score(y_true, y_pred):
    """sklearn olmadığında kullanılacak basit bir doğruluk hesaplama fonksiyonu"""
    return sum(np.array(y_true) == np.array(y_pred)) / len(y_true)