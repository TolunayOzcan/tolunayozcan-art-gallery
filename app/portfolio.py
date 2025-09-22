import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Veri Sanatı Portföyü", layout="wide")

# Sol menü
with st.sidebar:
    st.title("Hakkımda")
    st.markdown(
        """
        Veri analizi ve görselleştirme alanında 4+ yıllık deneyime sahip Kıdemli Veri Analistiyim. SQL, Python ve VBA konularında uzman seviyede bilgi sahibi. CRM veri analizi, İK analitik çözümleri, çağrı merkezi ve operasyonel raporlama konularında kapsamlı deneyim. Veri odaklı karar alma süreçlerini destekleyen analitik çözümler geliştirme konusunda uzman.
        """
    )

st.title("Tolunay Özcan - Veri Sanatı Portföyü")
st.markdown("""
Veri sanatı ve görselleştirme alanında çalışmalarımı bu portföyde bulabilirsiniz. Aşağıda bazı örnek projelerimi görebilirsiniz.
""")

# --- Örnek Grafikler ---
st.subheader("Örnek Veri Görselleştirmeleri")

# 1. Sanatçıların Değerleri
csv1 = "app/gallery/ornek_veri1.csv"
if os.path.exists(csv1):
    df1 = pd.read_csv(csv1)
    st.markdown("**Sanatçılara Göre Değerler**")
    st.bar_chart(df1.set_index("name")['value'])

# 2. Sanat Eserleri Kategorileri
csv2 = "app/gallery/ornek_veri2.csv"
if os.path.exists(csv2):
    df2 = pd.read_csv(csv2)
    st.markdown("**Sanat Eserleri Kategorileri**")
    st.dataframe(df2)
    st.line_chart(df2.set_index("kategori")['sayi'])

# 3. Sankey Diyagramı
csv3 = "app/gallery/ornek_sankey.csv"
if os.path.exists(csv3):
    df3 = pd.read_csv(csv3)
    st.markdown("**Veri Akışı - Sankey Diyagramı**")
    all_labels = list(pd.unique(df3[['source', 'target']].values.ravel('K')))
    label_to_index = {label: i for i, label in enumerate(all_labels)}
    sankey_fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels
        ),
        link=dict(
            source=[label_to_index[s] for s in df3['source']],
            target=[label_to_index[t] for t in df3['target']],
            value=df3['value']
        )
    )])
    st.plotly_chart(sankey_fig, use_container_width=True)

# Örnek görsellerin bulunduğu klasör
gallery_path = "app/gallery"

if not os.path.exists(gallery_path):
    st.info("Henüz galeriye görsel eklenmedi.")
else:
    images = [img for img in os.listdir(gallery_path) if img.endswith((".png", ".jpg", ".jpeg"))]
    if images:
        cols = st.columns(3)
        for idx, img_name in enumerate(images):
            img_path = os.path.join(gallery_path, img_name)
            with cols[idx % 3]:
                st.image(Image.open(img_path), caption=img_name, use_column_width=True)
    else:
        st.info("Galeri klasöründe görsel bulunamadı.")

st.markdown("""
---
İletişim: [LinkedIn](https://www.linkedin.com/in/tolunayozcan/) | [GitHub](https://github.com/TolunayOzcan)
""")
