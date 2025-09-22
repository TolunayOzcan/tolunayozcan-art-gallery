import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Veri Sanatı Portföyü", layout="wide")
st.title("Tolunay Özcan - Veri Sanatı Portföyü")
st.markdown("""
## Hakkımda
Veri sanatı ve görselleştirme alanında çalışmalarımı bu portföyde bulabilirsiniz. Aşağıda bazı örnek projelerimi görebilirsiniz.
""")

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
