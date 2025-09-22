import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.graph_objects as go
import sys

# Import için yolu düzenleme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper import scrape_ekonomi_verileri, scrape_borsa_verileri, scrape_kripto_verileri
import plotly.express as px

st.set_page_config(page_title="Veri Sanatı Portföyü", layout="wide")

# Sol menü
with st.sidebar:
    st.title("Hakkımda")
    st.markdown(
        """
        Veri analizi ve görselleştirme alanında 4+ yıllık deneyime sahip Kıdemli Veri Analistiyim. SQL, Python ve VBA konularında uzman seviyede bilgi sahibi. CRM veri analizi, İK analitik çözümleri, çağrı merkezi ve operasyonel raporlama konularında kapsamlı deneyim. Veri odaklı karar alma süreçlerini destekleyen analitik çözümler geliştirme konusunda uzman.
        """
    )

# Menü sekmeleri
menu = st.tabs(["Anasayfa", "Analizler", "Canlı Veriler"])

with menu[0]:
    st.title("Tolunay Özcan - Veri Sanatı Portföyü")
    st.markdown("""
    Veri sanatı ve görselleştirme alanında çalışmalarımı bu portföyde bulabilirsiniz. Aşağıda bazı örnek projelerimi görebilirsiniz.
    """)

with menu[1]:
    st.subheader("Örnek Veri Görselleştirmeleri")

    # 1. Sanatçıların Değerleri
    csv1 = "app/gallery/ornek_veri1.csv"
    if os.path.exists(csv1):
        df1 = pd.read_csv(csv1)
        st.markdown("**Sanatçılara Göre Değerler**")
        st.bar_chart(df1.set_index("name")["value"])

    # 2. Sanat Eserleri Kategorileri
    csv2 = "app/gallery/ornek_veri2.csv"
    if os.path.exists(csv2):
        df2 = pd.read_csv(csv2)
        st.markdown("**Sanat Eserleri Kategorileri**")
        st.dataframe(df2)
        st.line_chart(df2.set_index("kategori")["sayi"])

    # 3. Sankey Diyagramı
    csv3 = "app/gallery/ornek_sankey.csv"
    if os.path.exists(csv3):
        df3 = pd.read_csv(csv3)
        st.markdown("**Veri Akışı - Sankey Diyagramı**")
        all_labels = list(pd.unique(df3[["source", "target"]].values.ravel("K")))
        label_to_index = {label: i for i, label in enumerate(all_labels)}
        sankey_fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_labels
            ),
            link=dict(
                source=[label_to_index[s] for s in df3["source"]],
                target=[label_to_index[t] for t in df3["target"]],
                value=df3["value"]
            )
        )])
        st.plotly_chart(sankey_fig, use_container_width=True)

with menu[2]:
    st.subheader("Canlı Web Verileri")
    
    st.info("Bu sekme, farklı kaynaklardan çekilen canlı verileri göstermektedir. Not: Gerçek veri çekimi yerine örnek veriler gösterilmektedir.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Ekonomi Göstergeleri")
        ekonomi_df = scrape_ekonomi_verileri()
        
        if not ekonomi_df.empty:
            st.dataframe(ekonomi_df)
            
            # Önem derecesine göre gösterge sayısı
            if 'onem' in ekonomi_df.columns:
                onem_counts = ekonomi_df['onem'].value_counts().reset_index()
                onem_counts.columns = ['Önem Derecesi', 'Sayı']
                
                fig = px.pie(onem_counts, values='Sayı', names='Önem Derecesi', 
                            title='Ekonomik Göstergelerin Önem Derecesine Göre Dağılımı')
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Borsa Verileri")
        borsa_df = scrape_borsa_verileri()
        
        if not borsa_df.empty:
            st.dataframe(borsa_df)
            
            # Borsa değişim yüzdesi grafiği
            if 'endeks' in borsa_df.columns and 'degisim_yuzde' in borsa_df.columns:
                # Yüzde işaretini kaldırıp sayısal değere dönüştür
                borsa_df['degisim_yuzde_numeric'] = borsa_df['degisim_yuzde'].str.rstrip('%').astype('float')
                
                fig = px.bar(borsa_df, x='endeks', y='degisim_yuzde_numeric',
                            title='Borsa Endeksleri Günlük Değişim (%)',
                            color='degisim_yuzde_numeric',
                            color_continuous_scale=['red', 'lightgrey', 'green'],
                            color_continuous_midpoint=0)
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Kripto Para Verileri")
    kripto_df = scrape_kripto_verileri()
    
    if not kripto_df.empty:
        st.dataframe(kripto_df)
        
        # Kripto para değişim grafiği
        if 'kripto' in kripto_df.columns and 'degisim24h' in kripto_df.columns:
            # Yüzde işaretini kaldırıp sayısal değere dönüştür
            kripto_df['degisim_numeric'] = kripto_df['degisim24h'].str.rstrip('%').astype('float')
            
            fig = px.bar(kripto_df, x='kripto', y='degisim_numeric',
                        title='Kripto Para 24 Saatlik Değişim (%)',
                        color='degisim_numeric',
                        color_continuous_scale=['red', 'lightgrey', 'green'],
                        color_continuous_midpoint=0)
            st.plotly_chart(fig, use_container_width=True)