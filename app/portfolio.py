import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.graph_objects as go
import sys
import base64
import numpy as np
import threading
import time
from datetime import datetime

# Import için yolu düzenleme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper import scrape_ekonomi_verileri, scrape_borsa_verileri, scrape_kripto_verileri

# Sürekli çalışma için heartbeat mekanizmasını ekle
try:
    from app.heartbeat import heartbeat_manager
    # Uygulama başladığında heartbeat başlat
    heartbeat_manager.start()
except ImportError as e:
    st.warning(f"Heartbeat mekanizması yüklenemedi: {e}")

# HR Analytics modülünü import et
try:
    from app.hr_analytics import (generate_employee_data, create_attrition_department_chart,
                               create_salary_distribution_chart, create_performance_distribution_chart,
                               create_hiring_trends_chart, create_department_demographics_chart,
                               create_satisfaction_vs_attrition_chart)
except ImportError as e:
    st.error(f"HR Analytics modül import hatası: {e}")

# datascience fonksiyonlarını import etme - sklearn olmayan sürümü kullan
try:
    from app.datascience_no_sklearn import (generate_classification_data, generate_regression_data,
                                    generate_ab_test_data, generate_customer_segmentation_data,
                                    create_random_forest_plot, create_ab_test_plot, 
                                    create_segmentation_plot, create_regression_plot,
                                    accuracy_score)
except ImportError as e:
    st.error(f"Modül import hatası: {e}")
    
    # Acil durum için temel fonksiyonları tanımlayalım
    def generate_classification_data():
        df = pd.DataFrame({
            'yaş': np.random.normal(40, 10, 100),
            'gelir': np.random.normal(5000, 1000, 100)
        })
        return df, np.random.randint(0, 2, 100)
        
    def create_random_forest_plot(X, y):
        fig = px.bar(x=['yaş', 'gelir'], y=[0.6, 0.4], title="Özellik Önemleri")
        return None, fig
        
    def generate_ab_test_data():
        return pd.DataFrame({'grup': ['A', 'B'], 'donusum': [0.1, 0.15], 'harcama': [100, 120]})
        
    def create_ab_test_plot(data):
        fig1 = px.bar(data, x='grup', y='donusum', title="Dönüşüm Oranları")
        fig2 = px.bar(data, x='grup', y='harcama', title="Harcama Miktarları") 
        return fig1, fig2
        
    def generate_customer_segmentation_data():
        return pd.DataFrame({
            'musteri_id': [f"ID{i}" for i in range(100)],
            'yillik_harcama': np.random.normal(1000, 500, 100),
            'alisveris_sikligi': np.random.normal(10, 5, 100),
            'musteri_suresi': np.random.normal(3, 1, 100),
            'segment': np.random.choice(['Yüksek Değer', 'Orta Değer', 'Düşük Değer', 'Yeni Müşteri'], 100)
        })
        
    def create_segmentation_plot(data):
        return px.scatter_3d(data, x='yillik_harcama', y='alisveris_sikligi', z='musteri_suresi', color='segment')
        
    def generate_regression_data():
        df = pd.DataFrame({
            'reklam_harcaması': np.random.normal(1000, 300, 100),
            'müşteri_memnuniyeti': np.random.normal(8, 1, 100)
        })
        return df, np.random.normal(5000, 1000, 100)
        
    def create_regression_plot(X, y):
        y_pred = y + np.random.normal(0, 500, len(y))
        fig = px.scatter(x=y, y=y_pred, title="Gerçek vs Tahmin")
        return None, fig
        
    def accuracy_score(y_true, y_pred):
        return sum(np.array(y_true) == np.array(y_pred)) / len(y_true)

import plotly.express as px

st.set_page_config(
    page_title="Tolunay Özcan | Veri Sanatı",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS dosyasını okuyup inject et
def load_css(css_file):
    with open(css_file, "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# Font eklemek için
def local_css():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap">
    """, unsafe_allow_html=True)

# CSS'i yükle
load_css("app/style.css")
local_css()

# Sol menü
with st.sidebar:
    st.markdown("""
    <div style="text-align:center">
        <h1 style="margin-bottom:0">Tolunay Özcan</h1>
        <p style="color:#757575; margin-top:0">Kıdemli Veri Analisti</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.subheader("Hakkımda")
    st.markdown(
        """
        Veri analizi ve görselleştirme alanında 4+ yıllık deneyime sahip Kıdemli Veri Analistiyim. SQL, Python ve VBA konularında uzman seviyede bilgi sahibi. CRM veri analizi, İK analitik çözümleri, çağrı merkezi ve operasyonel raporlama konularında kapsamlı deneyim. Veri odaklı karar alma süreçlerini destekleyen analitik çözümler geliştirme konusunda uzman.
        """
    )
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.subheader("İletişim")
    st.markdown("""
        <a href="https://www.linkedin.com/in/tolunayozcan/" target="_blank" style="text-decoration:none;">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" style="margin-right:10px;">
                LinkedIn
            </div>
        </a>
        <a href="https://github.com/TolunayOzcan" target="_blank" style="text-decoration:none;">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20" style="margin-right:10px;">
                GitHub
            </div>
        </a>
        <a href="mailto:ornek@email.com" style="text-decoration:none;">
            <div style="display:flex; align-items:center;">
                <img src="https://cdn-icons-png.flaticon.com/512/561/561127.png" width="20" style="margin-right:10px;">
                E-posta
            </div>
        </a>
    """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

# Ana içerik
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Veri Sanatı Portföyü</h1>
    <p style="color: #757575; font-size: 1.2rem;">Veri analizi ve görselleştirme üzerine çalışmalarım</p>
</div>
""", unsafe_allow_html=True)

# Menü sekmeleri - Daha büyük ve görünür butonlar
st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# Daha büyük sekme butonları
menu = st.tabs(["📊 Anasayfa", "📈 Analizler", "🔄 Canlı Veriler", "🧪 Veri Bilimi", "👥 İK Analitiği"])

with menu[0]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("""
    <h2>Hoş Geldiniz</h2>
    <p>Veri sanatı ve görselleştirme alanında çalışmalarımı bu portföyde bulabilirsiniz. 
    Veri odaklı hikaye anlatımı ve görselleştirme teknikleriyle karmaşık verileri anlamlı içgörülere dönüştürüyorum.</p>
    
    <p>Portföyümde bulunan çalışmalar:</p>
    <ul>
        <li>Özel tasarlanmış veri görselleştirmeleri</li>
        <li>İnteraktif dashboard projeleri</li>
        <li>Gerçek zamanlı veri analizleri</li>
        <li>Sektörel trend analiz raporları</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Metrikler ekle
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="card metric-card-1" style="text-align:center; background-color: #E1BEE7;">""", unsafe_allow_html=True)
        st.metric(label="Tamamlanan Proje", value="24+", delta="3 son ayda")
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="card metric-card-2" style="text-align:center; background-color: #C5CAE9;">""", unsafe_allow_html=True)
        st.metric(label="Veri Kaynakları", value="15", delta="5 yeni eklendi")
        st.markdown("""</div>""", unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<div class="card metric-card-3" style="text-align:center; background-color: #BBDEFB;">""", unsafe_allow_html=True)
        st.metric(label="Memnuniyet Oranı", value="97%", delta="2% geçen yıla göre")
        st.markdown("""</div>""", unsafe_allow_html=True)

with menu[1]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>Veri Görselleştirme Galeri</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>Bu bölümde çeşitli veri görselleştirme örneklerini bulabilirsiniz. Her görselleştirme, 
    veri hikayesini en etkili şekilde anlatmak için özel olarak tasarlanmıştır.</p>
    """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

    # 1. Sanatçıların Değerleri
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    csv1 = "app/gallery/ornek_veri1.csv"
    if os.path.exists(csv1):
        df1 = pd.read_csv(csv1)
        st.markdown("<h3>Sanatçılara Göre Değerler</h3>", unsafe_allow_html=True)
        
        # Daha profesyonel görünümlü plotly grafik
        fig1 = px.bar(df1, x="name", y="value", 
                     color="value",
                     color_continuous_scale=px.colors.sequential.Blues,
                     title="Sanatçıların Piyasa Değerleri")
        fig1.update_layout(
            xaxis_title="Sanatçı",
            yaxis_title="Değer (Bin TL)",
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)'),
            margin=dict(t=50, b=50, l=40, r=40),
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Ek bilgi/açıklama
        st.markdown("""
        <p><small>Bu grafik, sanat piyasasında öne çıkan sanatçıların güncel piyasa değerlerini göstermektedir.
        Değerleri, son satış fiyatları ve piyasa trendleri kullanılarak hesaplanmıştır.</small></p>
        """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

    # 2. Sanat Eserleri Kategorileri
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    csv2 = "app/gallery/ornek_veri2.csv"
    if os.path.exists(csv2):
        df2 = pd.read_csv(csv2)
        st.markdown("<h3>Sanat Eserleri Kategorileri</h3>", unsafe_allow_html=True)
        
        # Daha profesyonel tablo
        st.markdown("<p>Kategori bazında eser sayıları:</p>", unsafe_allow_html=True)
        st.dataframe(df2, use_container_width=True)
        
        # Daha profesyonel çizgi grafik
        fig2 = px.line(df2, x="kategori", y="sayi", 
                     markers=True,
                     line_shape="spline",
                     color_discrete_sequence=['#1E88E5'],
                     title="Kategori Bazında Eser Sayıları")
        fig2.update_layout(
            xaxis_title="Kategori",
            yaxis_title="Eser Sayısı",
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)'),
            margin=dict(t=50, b=50, l=40, r=40),
        )
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

    # 3. Sankey Diyagramı
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    csv3 = "app/gallery/ornek_sankey.csv"
    if os.path.exists(csv3):
        df3 = pd.read_csv(csv3)
        st.markdown("<h3>Veri Akış Diyagramı</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p>Sanat eseri üretim ve sergileme sürecinde verilerin akışını gösteren Sankey diyagramı.
        Bu görselleştirme, süreçler arasındaki ilişkileri ve veri akışının yoğunluğunu göstermektedir.</p>
        """, unsafe_allow_html=True)
        
        all_labels = list(pd.unique(df3[["source", "target"]].values.ravel("K")))
        label_to_index = {label: i for i, label in enumerate(all_labels)}
        
        # Daha profesyonel Sankey
        sankey_fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="#555555", width=0.5),
                label=all_labels,
                color="#1E88E5"
            ),
            link=dict(
                source=[label_to_index[s] for s in df3["source"]],
                target=[label_to_index[t] for t in df3["target"]],
                value=df3["value"],
                color=['rgba(30, 136, 229, 0.4)'] * len(df3)
            )
        )])
        
        sankey_fig.update_layout(
            title="Veri Akış Süreçleri",
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=50, l=40, r=40),
            height=500,
        )
        
        st.plotly_chart(sankey_fig, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

with menu[2]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>Canlı Finansal Veriler</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>Bu sayfada çeşitli finansal kaynaklardan elde edilen güncel veriler ve analizleri görebilirsiniz. 
    Veriler, en son piyasa hareketlerini ve ekonomik göstergeleri yansıtır.</p>
    """, unsafe_allow_html=True)
    st.info("Not: Bu veriler örnek amaçlıdır ve gerçek zamanlı veri çekimi yerine demo veriler gösterilmektedir.")
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Ekonomi Göstergeleri
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Ekonomi Göstergeleri</h3>", unsafe_allow_html=True)
    ekonomi_df = scrape_ekonomi_verileri()
    
    if not ekonomi_df.empty:
        # Veri tablosu stil iyileştirmesiyle
        st.markdown("<p><strong>Güncel Ekonomik Veriler</strong></p>", unsafe_allow_html=True)
        st.dataframe(ekonomi_df, use_container_width=True)
        
        # Önem derecesine göre gösterge sayısı - geliştirilmiş grafik
        if 'onem' in ekonomi_df.columns:
            onem_counts = ekonomi_df['onem'].value_counts().reset_index()
            onem_counts.columns = ['Önem Derecesi', 'Sayı']
            
            fig = px.pie(onem_counts, values='Sayı', names='Önem Derecesi', 
                        title='Ekonomik Göstergelerin Önem Derecesine Göre Dağılımı',
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        hole=0.4)
            
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(t=50, b=50, l=20, r=20),
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            fig.update_traces(textinfo='percent+label', pull=[0.05, 0, 0], 
                             marker=dict(line=dict(color='#FFFFFF', width=2)))
            
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Borsa ve Kripto Verileri Yan Yana
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>Borsa Verileri</h3>", unsafe_allow_html=True)
        borsa_df = scrape_borsa_verileri()
        
        if not borsa_df.empty:
            # Stilize edilmiş tablo
            st.markdown("<p><strong>Güncel Borsa Endeksleri</strong></p>", unsafe_allow_html=True)
            st.dataframe(borsa_df, use_container_width=True)
            
            # Borsa değişim yüzdesi grafiği - geliştirilmiş
            if 'endeks' in borsa_df.columns and 'degisim_yuzde' in borsa_df.columns:
                # Yüzde işaretini kaldırıp sayısal değere dönüştür
                borsa_df['degisim_yuzde_numeric'] = borsa_df['degisim_yuzde'].str.rstrip('%').astype('float')
                
                # Değerlere göre renklendirme için koşullar
                colors = ['#F44336' if x < 0 else '#4CAF50' for x in borsa_df['degisim_yuzde_numeric']]
                
                fig = px.bar(borsa_df, x='endeks', y='degisim_yuzde_numeric',
                            title='Günlük Değişim (%)',
                            text='degisim_yuzde')
                
                fig.update_layout(
                    xaxis_title="",
                    yaxis_title="Değişim (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)'),
                    margin=dict(t=50, b=20, l=20, r=20)
                )
                
                fig.update_traces(marker_color=colors, textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>Kripto Para Verileri</h3>", unsafe_allow_html=True)
        kripto_df = scrape_kripto_verileri()
        
        if not kripto_df.empty:
            st.markdown("<p><strong>Güncel Kripto Piyasası</strong></p>", unsafe_allow_html=True)
            st.dataframe(kripto_df, use_container_width=True)
            
            # Kripto para değişim grafiği - geliştirilmiş
            if 'kripto' in kripto_df.columns and 'degisim24h' in kripto_df.columns:
                # Yüzde işaretini kaldırıp sayısal değere dönüştür
                kripto_df['degisim_numeric'] = kripto_df['degisim24h'].str.rstrip('%').astype('float')
                
                # Değerlere göre renklendirme için koşullar
                colors = ['#F44336' if x < 0 else '#4CAF50' for x in kripto_df['degisim_numeric']]
                
                fig = px.bar(kripto_df, x='kripto', y='degisim_numeric',
                            title='24 Saatlik Değişim (%)',
                            text='degisim24h')
                
                fig.update_layout(
                    xaxis_title="",
                    yaxis_title="Değişim (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)'),
                    margin=dict(t=50, b=20, l=20, r=20)
                )
                
                fig.update_traces(marker_color=colors, textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Son Güncellenme Bilgisi
    st.markdown("""<div style="text-align:center; margin-top:20px;">
        <p style="color:#757575; font-size:0.9rem;">Son güncellenme: 22 Eylül 2025, 14:30</p>
    </div>""", unsafe_allow_html=True)

with menu[3]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>Veri Bilimi Örnekleri</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>Bu bölümde veri bilimi ve makine öğrenimi projelerinden örnekler bulabilirsiniz.
    Her bir örnek, farklı veri bilimi tekniklerini ve algoritmaları göstermektedir.</p>
    """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Random Forest Sınıflandırma
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Random Forest Sınıflandırma Modeli</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Random Forest, çok sayıda karar ağacının birleşiminden oluşan güçlü bir sınıflandırma ve regresyon algoritmasıdır.
    Bu örnek, ikili sınıflandırma problemi için Random Forest modelinin özellik önemlerini göstermektedir.</p>
    """, unsafe_allow_html=True)
    
    # Random Forest modeli ve görselleştirme
    with st.spinner("Random Forest modeli hazırlanıyor..."):
        X, y = generate_classification_data()
        rf_model, rf_fig = create_random_forest_plot(X, y)
        st.plotly_chart(rf_fig, use_container_width=True)
    
    # Model açıklaması ve ek bilgi
    with st.expander("Model Detayları"):
        st.write("**Random Forest Modeli Parametreleri:**")
        st.code("""
        RandomForestClassifier(
            n_estimators=100,  # Ağaç sayısı
            random_state=42,   # Sonuçların tekrarlanabilirliği için
        )
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Model Doğruluğu", value=f"{accuracy_score(y, rf_model.predict(X)):.2%}")
        with col2:
            st.metric(label="Özellik Sayısı", value=f"{X.shape[1]}")
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # A/B Test Analizi
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>A/B Test Analizi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>A/B testleri, iki farklı versiyon arasındaki performans farkını ölçmek için kullanılır.
    Bu örnek, bir web sitesi değişikliğinin dönüşüm oranları ve ortalama harcamalar üzerindeki etkisini göstermektedir.</p>
    """, unsafe_allow_html=True)
    
    # A/B test verileri ve görselleştirmeler
    with st.spinner("A/B test analizi hazırlanıyor..."):
        ab_data = generate_ab_test_data()
        conversion_fig, spending_fig = create_ab_test_plot(ab_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(conversion_fig, use_container_width=True)
        with col2:
            st.plotly_chart(spending_fig, use_container_width=True)
    
    # Test sonuçları ve anlamı
    with st.expander("Test Sonuçları"):
        st.write("""
        **Test Sonuçlarının Yorumu:**
        
        B grubu hem dönüşüm oranında hem de ortalama harcamada daha iyi performans göstermiştir. 
        Bu sonuçlara göre, B varyasyonunun kullanılması önerilir.
        
        **İstatistiksel Anlamlılık:**
        
        * Dönüşüm oranı farkı: % 25 anlamlılık
        * Ortalama harcama farkı: % 6.7 anlamlılık
        """)
        
        # Özet tablo
        ab_summary = pd.DataFrame({
            'Grup': ['A', 'B'],
            'Kullanıcı Sayısı': [ab_data[ab_data['grup'] == 'A'].shape[0], ab_data[ab_data['grup'] == 'B'].shape[0]],
            'Dönüşüm Sayısı': [ab_data[ab_data['grup'] == 'A']['donusum'].sum(), ab_data[ab_data['grup'] == 'B']['donusum'].sum()],
            'Dönüşüm Oranı (%)': [ab_data[ab_data['grup'] == 'A']['donusum'].mean() * 100, ab_data[ab_data['grup'] == 'B']['donusum'].mean() * 100],
            'Ortalama Harcama (TL)': [ab_data[(ab_data['grup'] == 'A') & (ab_data['donusum'] == 1)]['harcama'].mean(), 
                                    ab_data[(ab_data['grup'] == 'B') & (ab_data['donusum'] == 1)]['harcama'].mean()]
        })
        st.dataframe(ab_summary.round(2), use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Müşteri Segmentasyonu
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Müşteri Segmentasyonu</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Müşteri segmentasyonu, müşterileri benzer özelliklere sahip gruplara ayırma işlemidir.
    Bu örnek, müşterileri harcama, alışveriş sıklığı ve müşteri süresi değişkenlerine göre segmentlere ayırmaktadır.</p>
    """, unsafe_allow_html=True)
    
    # Segmentasyon verileri ve 3D görselleştirme
    with st.spinner("Müşteri segmentasyonu hazırlanıyor..."):
        segment_data = generate_customer_segmentation_data()
        segment_fig = create_segmentation_plot(segment_data)
        st.plotly_chart(segment_fig, use_container_width=True)
    
    # Segment özeti ve açıklama
    with st.expander("Segment Detayları"):
        st.write("""
        **Müşteri Segmentleri:**
        
        * **Yüksek Değer:** Yüksek harcama, yüksek alışveriş sıklığı ve uzun müşteri süresi
        * **Orta Değer:** Orta seviye harcama, orta sıklık ve orta müşteri süresi
        * **Düşük Değer:** Düşük harcama, düşük sıklık ve kısa müşteri süresi
        * **Yeni Müşteri:** Düşük harcama, düşük sıklık ve çok kısa müşteri süresi
        """)
        
        # Segment özeti tablosu
        segment_summary = segment_data.groupby('segment').agg({
            'musteri_id': 'count',
            'yillik_harcama': 'mean',
            'alisveris_sikligi': 'mean',
            'musteri_suresi': 'mean'
        }).reset_index()
        
        segment_summary.columns = ['Segment', 'Müşteri Sayısı', 'Ort. Yıllık Harcama (TL)', 
                                'Ort. Alışveriş Sıklığı (yıllık)', 'Ort. Müşteri Süresi (yıl)']
        
        st.dataframe(segment_summary.round(2), use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Regresyon Modeli
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Regresyon Analizi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Regresyon analizi, değişkenler arasındaki ilişkileri modelleyerek tahmin yapma yöntemidir.
    Bu örnek, Random Forest regresyon modelinin gerçek ve tahmin edilen değerler arasındaki ilişkiyi göstermektedir.</p>
    """, unsafe_allow_html=True)
    
    # Regresyon modeli ve görselleştirme
    with st.spinner("Regresyon modeli hazırlanıyor..."):
        X_reg, y_reg = generate_regression_data()
        reg_model, reg_fig = create_regression_plot(X_reg, y_reg)
        st.plotly_chart(reg_fig, use_container_width=True)
    
    # Model performans detayları
    with st.expander("Model Performansı"):
        st.write("""
        **Performans Metrikleri:**
        
        * **R²:** Modelin açıklayıcılık gücünü gösterir (1.0 ideal)
        * **RMSE:** Tahmin hatalarının karekök ortalaması (düşük değer daha iyi)
        
        **Model Parametreleri:**
        """)
        
        st.code("""
        RandomForestRegressor(
            n_estimators=100,  # Ağaç sayısı
            random_state=42    # Sonuçların tekrarlanabilirliği için
        )
        """)
        
        # En önemli özellikler
        feature_importance = pd.DataFrame({
            'Özellik': X_reg.columns,
            'Önem': reg_model.feature_importances_
        }).sort_values('Önem', ascending=False)
        
        st.write("**En Önemli Özellikler:**")
        st.dataframe(feature_importance, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
with menu[4]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>İnsan Kaynakları Analitiği</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>İnsan kaynakları verilerinizden değer elde etmeye yönelik analitik çözümler sunuyorum.
    İşgücü planlaması, çalışan deneyimi optimizasyonu, işe alım süreçleri ve performans değerlendirme gibi
    konularda veri odaklı içgörüler sağlıyorum.</p>
    """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # HR verilerini oluştur
    with st.spinner('İK verileri hazırlanıyor...'):
        employee_data = generate_employee_data(n_employees=200)
    
    # İşten Ayrılma Analizi
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Departmanlara Göre İşten Ayrılma Analizi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Çalışan devir oranı (attrition), şirketlerin sürdürülebilirliği için kritik bir metriktir.
    Bu analiz, hangi departmanların daha yüksek işten ayrılma oranlarına sahip olduğunu gösterir ve
    insan kaynakları stratejilerinin iyileştirilmesi için odak noktaları sağlar.</p>
    """, unsafe_allow_html=True)
    
    # İşten ayrılma grafiği
    fig_attrition = create_attrition_department_chart(employee_data)
    st.plotly_chart(fig_attrition, use_container_width=True)
    
    # İşten ayrılma nedenleri dağılımı
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("İşten Ayrılma Nedenleri")
        reasons_data = employee_data[employee_data['işten_ayrılma']]['ayrılma_nedeni'].value_counts().reset_index()
        reasons_data.columns = ['Ayrılma Nedeni', 'Çalışan Sayısı']
        
        fig_reasons = px.pie(
            reasons_data,
            values='Çalışan Sayısı',
            names='Ayrılma Nedeni',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_reasons.update_layout(height=350)
        st.plotly_chart(fig_reasons, use_container_width=True)
        
    with col2:
        st.subheader("Özet Metrikler")
        total_attrition_rate = employee_data['işten_ayrılma'].mean() * 100
        st.metric(
            label="Genel İşten Ayrılma Oranı", 
            value=f"{total_attrition_rate:.1f}%",
            delta=f"{total_attrition_rate - 17.0:.1f}%" if total_attrition_rate != 17.0 else None,
            delta_color="inverse"
        )
        
        high_risk_dept = employee_data.groupby('departman')['işten_ayrılma'].mean().idxmax()
        high_risk_rate = employee_data[employee_data['departman'] == high_risk_dept]['işten_ayrılma'].mean() * 100
        
        st.metric(
            label="En Riskli Departman", 
            value=high_risk_dept,
            delta=f"{high_risk_rate:.1f}%"
        )
        
        avg_satisfaction = employee_data['tatmin_skoru'].mean()
        st.metric(
            label="Ortalama Çalışan Memnuniyeti", 
            value=f"{avg_satisfaction:.1f}/10",
            delta=f"{avg_satisfaction - 7.0:.1f}" if avg_satisfaction != 7.0 else None
        )
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Maaş Dağılımı Analizi
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Departmanlara Göre Maaş Dağılımı</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Maaş dağılımı analizi, şirket içi ücret politikalarının adil ve rekabetçi olup olmadığını değerlendirmenize yardımcı olur.
    Bu grafik, departmanlar arasındaki maaş farklılıklarını ve aykırı değerleri gösterir.</p>
    """, unsafe_allow_html=True)
    
    fig_salary = create_salary_distribution_chart(employee_data)
    st.plotly_chart(fig_salary, use_container_width=True)
    
    # Maaş özet istatistikleri
    st.subheader("Maaş Özet İstatistikleri")
    salary_stats = employee_data.groupby('departman')['aylık_maaş'].agg(['mean', 'median', 'min', 'max']).reset_index()
    salary_stats.columns = ['Departman', 'Ortalama', 'Medyan', 'Minimum', 'Maksimum']
    
    # Formatla (TL ekle ve yuvarla)
    for col in ['Ortalama', 'Medyan', 'Minimum', 'Maksimum']:
        salary_stats[col] = salary_stats[col].apply(lambda x: f"{x:,.0f} TL")
    
    st.dataframe(salary_stats, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Performans Dağılımı
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Performans Puan Dağılımı</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Çalışanların performans puanlarının dağılımı, şirketin genel performans değerlendirme eğilimlerini anlamanıza yardımcı olur.
    Bu analiz, performans değerlendirme sisteminin etkinliğini ve potansiyel önyargıları değerlendirmenize olanak tanır.</p>
    """, unsafe_allow_html=True)
    
    fig_performance = create_performance_distribution_chart(employee_data)
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Performans ve maaş ilişkisi
    st.subheader("Performans ve Maaş İlişkisi")
    fig_perf_salary = px.scatter(
        employee_data,
        x='performans_puanı',
        y='aylık_maaş',
        color='departman',
        size='şirket_deneyimi_yıl',
        hover_data=['pozisyon', 'cinsiyet', 'yaş'],
        opacity=0.7,
        title='Performans Puanı ve Maaş İlişkisi'
    )
    
    fig_perf_salary.update_layout(
        height=500,
        xaxis_title='Performans Puanı',
        yaxis_title='Aylık Maaş (TL)'
    )
    
    st.plotly_chart(fig_perf_salary, use_container_width=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # İşe Alım Trendleri ve Departman Demografisi
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>İşe Alım Trendleri</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p>İşe alım trendleri, şirketin büyüme dinamiklerini ve işe alım stratejilerindeki değişiklikleri gösterir.
        Bu grafik, yıllar içinde işe alınan çalışan sayılarını göstermektedir.</p>
        """, unsafe_allow_html=True)
        
        fig_hiring = create_hiring_trends_chart(employee_data)
        st.plotly_chart(fig_hiring, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>Departman ve Cinsiyet Dağılımı</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p>Departman ve cinsiyet dağılımı, şirketin çeşitlilik ve kapsayıcılık konusundaki durumunu değerlendirir.
        Bu analiz, cinsiyet dengesi açısından iyileştirme gerektiren alanları belirlemenize yardımcı olur.</p>
        """, unsafe_allow_html=True)
        
        fig_demographics = create_department_demographics_chart(employee_data)
        st.plotly_chart(fig_demographics, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Tatmin Skoru ve İşten Ayrılma İlişkisi
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Tatmin Skoru ve İşten Ayrılma İlişkisi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Çalışan tatmini ve işten ayrılma arasındaki ilişki, insan kaynakları stratejileri için kritik bir içgörü sağlar.
    Bu analiz, tatmin skorlarının işten ayrılma olasılığı üzerindeki etkisini gösterir.</p>
    """, unsafe_allow_html=True)
    
    fig_satisfaction = create_satisfaction_vs_attrition_chart(employee_data)
    st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    st.markdown("""
    <p><strong>Analiz Sonucu:</strong> Çalışanların tatmin skorları düştükçe, işten ayrılma olasılıklarının 
    belirgin şekilde arttığı görülmektedir. Tatmin skoru 5'in altında olan çalışanlarda 
    işten ayrılma riski önemli ölçüde yükselmektedir.</p>
    
    <p><strong>Öneriler:</strong></p>
    <ul>
        <li>Düşük tatmin skoruna sahip çalışanlarla düzenli geribildirim görüşmeleri yapılmalı</li>
        <li>Çalışan memnuniyeti anketleri ile sorun alanları belirlenip çözüm stratejileri geliştirilmeli</li>
        <li>Departman yöneticilerine çalışan bağlılığını artırma konusunda eğitimler verilmeli</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)