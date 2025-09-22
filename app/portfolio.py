import streamlit as st
from PIL import Image
import os
import pandas as pd

st.set_page_config(page_title="Veri Sanatı Portföyü", layout="wide")
st.title("Tolunay Özcan - Veri Sanatı Portföyü")
st.markdown("""
## Hakkımda
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
