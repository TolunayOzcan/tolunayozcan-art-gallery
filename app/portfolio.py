import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.graph_objects as go
import sys
import base64

# Import için yolu düzenleme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper import scrape_ekonomi_verileri, scrape_borsa_verileri, scrape_kripto_verileri
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
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap">
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

# Menü sekmeleri
menu = st.tabs(["📊 Anasayfa", "📈 Analizler", "🔄 Canlı Veriler"])

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
        st.markdown("""<div class="card" style="text-align:center">""", unsafe_allow_html=True)
        st.metric(label="Tamamlanan Proje", value="24+", delta="3 son ayda")
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="card" style="text-align:center">""", unsafe_allow_html=True)
        st.metric(label="Veri Kaynakları", value="15", delta="5 yeni eklendi")
        st.markdown("""</div>""", unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<div class="card" style="text-align:center">""", unsafe_allow_html=True)
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