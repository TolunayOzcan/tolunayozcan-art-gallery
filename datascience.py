"""
Veri bilimi analiz ve görselleştirmeleri için yardımcı fonksiyonlar.
Bu modül, örnek veri bilimi analizleri ve görselleştirmeleri için kullanılır.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix, accuracy_score, r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler

def generate_classification_data():
    """
    İkili sınıflandırma için örnek veri seti oluşturur.
    
    Returns:
        tuple: X, y (özellikler ve etiketler)
    """
    X, y = make_classification(
        n_samples=500,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_classes=2,
        random_state=42
    )
    
    feature_names = [f'Özellik_{i+1}' for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)
    
    return X_df, y

def generate_regression_data():
    """
    Regresyon için örnek veri seti oluşturur.
    
    Returns:
        tuple: X, y (özellikler ve hedef değişken)
    """
    X, y = make_regression(
        n_samples=500,
        n_features=5,
        n_informative=3,
        noise=5,
        random_state=42
    )
    
    feature_names = [f'Değişken_{i+1}' for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)
    
    return X_df, y

def generate_ab_test_data():
    """
    A/B testi için örnek veri seti oluşturur.
    
    Returns:
        pd.DataFrame: A/B testi verileri
    """
    np.random.seed(42)
    
    # A grubu verileri
    n_A = 500
    conversions_A = np.random.binomial(1, 0.12, n_A)
    group_A = pd.DataFrame({
        'kullanici_id': range(1, n_A + 1),
        'grup': 'A',
        'donusum': conversions_A,
        'harcama': np.where(conversions_A == 1, np.random.normal(75, 20, n_A), 0)
    })
    
    # B grubu verileri (dönüşüm oranı daha yüksek)
    n_B = 500
    conversions_B = np.random.binomial(1, 0.15, n_B)
    group_B = pd.DataFrame({
        'kullanici_id': range(n_A + 1, n_A + n_B + 1),
        'grup': 'B',
        'donusum': conversions_B,
        'harcama': np.where(conversions_B == 1, np.random.normal(80, 20, n_B), 0)
    })
    
    # Verileri birleştirme
    ab_data = pd.concat([group_A, group_B], ignore_index=True)
    
    return ab_data

def generate_customer_segmentation_data():
    """
    Müşteri segmentasyonu için örnek veri seti oluşturur.
    
    Returns:
        pd.DataFrame: Müşteri verileri
    """
    np.random.seed(42)
    
    n_customers = 500
    
    # Farklı müşteri segmentleri oluşturma
    segments = ['Yüksek Değer', 'Orta Değer', 'Düşük Değer', 'Yeni Müşteri']
    segment_probs = [0.2, 0.4, 0.3, 0.1]
    
    customer_data = pd.DataFrame({
        'musteri_id': range(1, n_customers + 1),
        'segment': np.random.choice(segments, n_customers, p=segment_probs),
    })
    
    # Segmentlere göre farklı değerler atama
    for _, row in customer_data.iterrows():
        if row['segment'] == 'Yüksek Değer':
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'yillik_harcama'] = np.random.normal(2000, 500)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'alisveris_sikligi'] = np.random.normal(20, 5)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'musteri_suresi'] = np.random.normal(5, 1.5)
        elif row['segment'] == 'Orta Değer':
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'yillik_harcama'] = np.random.normal(1000, 300)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'alisveris_sikligi'] = np.random.normal(10, 3)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'musteri_suresi'] = np.random.normal(3, 1)
        elif row['segment'] == 'Düşük Değer':
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'yillik_harcama'] = np.random.normal(500, 150)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'alisveris_sikligi'] = np.random.normal(5, 2)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'musteri_suresi'] = np.random.normal(2, 1)
        else:  # Yeni Müşteri
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'yillik_harcama'] = np.random.normal(300, 100)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'alisveris_sikligi'] = np.random.normal(2, 1)
            customer_data.loc[customer_data['musteri_id'] == row['musteri_id'], 'musteri_suresi'] = np.random.normal(0.5, 0.2)
    
    # Değerlerin pozitif olmasını sağlama
    customer_data['yillik_harcama'] = customer_data['yillik_harcama'].clip(lower=0)
    customer_data['alisveris_sikligi'] = customer_data['alisveris_sikligi'].clip(lower=1)
    customer_data['musteri_suresi'] = customer_data['musteri_suresi'].clip(lower=0.1)
    
    return customer_data

def create_random_forest_plot(X, y, test_size=0.25):
    """
    Random Forest sınıflandırma modeli eğitir ve özellik önemlerini gösteren bir grafik oluşturur.
    
    Args:
        X (pd.DataFrame): Özellikler
        y (array): Etiketler
        test_size (float): Test veri seti oranı
    
    Returns:
        tuple: Eğitilmiş model ve fig (grafik nesnesi)
    """
    # Veriyi eğitim ve test olarak bölme
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Random Forest modeli eğitme
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Model performansı
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Özellik önemlerini grafikleme
    feature_importance = pd.DataFrame({
        'Özellik': X.columns,
        'Önem': rf_model.feature_importances_
    }).sort_values('Önem', ascending=False)
    
    fig = px.bar(feature_importance, x='Önem', y='Özellik', orientation='h',
                 title=f'Random Forest Özellik Önemleri (Model Doğruluğu: {accuracy:.2%})',
                 color='Önem', color_continuous_scale='Blues')
    
    fig.update_layout(
        xaxis_title="Özellik Önemi",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(autorange="reversed"),
        margin=dict(t=50, b=50, l=20, r=20),
    )
    
    return rf_model, fig

def create_ab_test_plot(ab_data):
    """
    A/B testi sonuçlarını görselleştiren grafikler oluşturur.
    
    Args:
        ab_data (pd.DataFrame): A/B testi verileri
    
    Returns:
        tuple: İki grafik nesnesi (dönüşüm grafiği, ortalama harcama grafiği)
    """
    # Grup bazında dönüşüm oranlarını hesaplama
    conversion_rates = ab_data.groupby('grup')['donusum'].mean().reset_index()
    conversion_rates['oran'] = conversion_rates['donusum'] * 100
    
    # Dönüşüm oranları grafiği
    fig1 = px.bar(conversion_rates, x='grup', y='oran',
                 title='A/B Testi: Dönüşüm Oranları (%)',
                 color='grup', color_discrete_map={'A': '#1E88E5', 'B': '#5E35B1'},
                 text=conversion_rates['oran'].round(2).astype(str) + '%')
    
    fig1.update_layout(
        xaxis_title="Test Grubu",
        yaxis_title="Dönüşüm Oranı (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=50, b=50, l=20, r=20),
    )
    
    fig1.update_traces(textposition='outside', textfont_size=12)
    
    # Ortalama harcama grafiği
    # Sadece dönüşüm olan kullanıcıların ortalama harcamalarını hesaplama
    spending_data = ab_data[ab_data['donusum'] == 1].groupby('grup')['harcama'].mean().reset_index()
    
    fig2 = px.bar(spending_data, x='grup', y='harcama',
                 title='A/B Testi: Ortalama Harcama (TL)',
                 color='grup', color_discrete_map={'A': '#1E88E5', 'B': '#5E35B1'},
                 text=spending_data['harcama'].round(2).astype(str) + ' TL')
    
    fig2.update_layout(
        xaxis_title="Test Grubu",
        yaxis_title="Ortalama Harcama (TL)",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=50, b=50, l=20, r=20),
    )
    
    fig2.update_traces(textposition='outside', textfont_size=12)
    
    return fig1, fig2

def create_segmentation_plot(customer_data):
    """
    Müşteri segmentasyonu verilerini görselleştiren 3D scatter plot oluşturur.
    
    Args:
        customer_data (pd.DataFrame): Müşteri segmentasyonu verileri
    
    Returns:
        plotly.graph_objects.Figure: 3D scatter plot
    """
    # 3D Scatter Plot
    fig = px.scatter_3d(
        customer_data, 
        x='yillik_harcama', 
        y='alisveris_sikligi', 
        z='musteri_suresi',
        color='segment',
        color_discrete_map={
            'Yüksek Değer': '#2E7D32',
            'Orta Değer': '#1976D2',
            'Düşük Değer': '#FFA000',
            'Yeni Müşteri': '#D32F2F'
        },
        opacity=0.7,
        title='Müşteri Segmentasyonu 3D Görünüm'
    )
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Yıllık Harcama (TL)',
            yaxis_title='Alışveriş Sıklığı (yıllık)',
            zaxis_title='Müşteri Süresi (yıl)',
            xaxis=dict(backgroundcolor='rgb(250, 250, 250)', gridcolor='rgba(230,230,230,0.8)'),
            yaxis=dict(backgroundcolor='rgb(250, 250, 250)', gridcolor='rgba(230,230,230,0.8)'),
            zaxis=dict(backgroundcolor='rgb(250, 250, 250)', gridcolor='rgba(230,230,230,0.8)'),
        ),
        margin=dict(l=0, r=0, b=0, t=50),
    )
    
    return fig

def create_regression_plot(X, y, test_size=0.25):
    """
    Regresyon modeli eğitir ve gerçek vs tahmin karşılaştırma grafiği oluşturur.
    
    Args:
        X (pd.DataFrame): Özellikler
        y (array): Hedef değişken
        test_size (float): Test veri seti oranı
    
    Returns:
        tuple: Eğitilmiş model ve fig (grafik nesnesi)
    """
    # Veriyi eğitim ve test olarak bölme
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Random Forest regresyon modeli eğitme
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Test seti üzerinde tahminler
    y_pred = rf_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Gerçek vs Tahmin grafiği
    results_df = pd.DataFrame({
        'Gerçek': y_test,
        'Tahmin': y_pred,
        'Hata': np.abs(y_test - y_pred)
    })
    
    fig = px.scatter(results_df, x='Gerçek', y='Tahmin', color='Hata', 
                    color_continuous_scale='RdYlGn_r',
                    title=f'Regresyon Modeli: Gerçek vs Tahmin (R²: {r2:.2f}, RMSE: {rmse:.2f})')
    
    # İdeal tahmin çizgisi (x=y)
    min_val = min(results_df['Gerçek'].min(), results_df['Tahmin'].min())
    max_val = max(results_df['Gerçek'].max(), results_df['Tahmin'].max())
    fig.add_trace(
        go.Scatter(x=[min_val, max_val], y=[min_val, max_val], 
                  mode='lines', line=dict(color='grey', dash='dash'),
                  name='İdeal Tahmin')
    )
    
    fig.update_layout(
        xaxis_title="Gerçek Değer",
        yaxis_title="Tahmin Edilen Değer",
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=50, l=20, r=20),
    )
    
    return rf_model, fig