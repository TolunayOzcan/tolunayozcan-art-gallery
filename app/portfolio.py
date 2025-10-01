import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.graph_objects as go
import sys
import numpy as np
import threading
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Sklearn imports (for Churn Prediction)
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ Sklearn kurulu değil - Churn Prediction özelliği sınırlı olacak")

# Environment optimizations
os.environ['MPLBACKEND'] = 'Agg'

# Network Graph imports
try:
    import networkx as nx
    import plotly.graph_objects as go
    NETWORK_AVAILABLE = True
except ImportError as e:
    st.warning(f"NetworkX/Plotly yüklenemedi: {e}")
    NETWORK_AVAILABLE = False

# Import için yolu düzenleme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Güvenli scraper import (Cloud ortamında hata engelleme)
try:
    from scraper import scrape_ekonomi_verileri, scrape_borsa_verileri, scrape_kripto_verileri
except Exception as e:
    st.warning(f"Scraper import edilemedi, demo veriler kullanılacak: {e}")
    def scrape_ekonomi_verileri():
        return pd.DataFrame({'Gösterge': ['Demo'], 'Değer': [100]})
    def scrape_borsa_verileri():
        return pd.DataFrame({'Hisse': ['DEMO'], 'Fiyat': [100]})
    def scrape_kripto_verileri():
        return pd.DataFrame({'Kripto': ['DEMO'], 'Fiyat': [100]})

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
    initial_sidebar_state="collapsed"
)

# CSS dosyasını okuyup inject et (güvenli)
def load_css(css_file):
    try:
        if os.path.exists(css_file):
            with open(css_file, "r", encoding="utf-8") as f:
                css = f"<style>{f.read()}</style>"
                st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"style.css yüklenemedi: {e}")

# Font eklemek için
def local_css():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto+Mono:wght@300;400;500;600;700&display=swap">
    """, unsafe_allow_html=True)

# CSS'i yükle
load_css("app/style.css")
local_css()

# Streamlit animasyonlarını tamamen gizle
st.markdown("""
<style>
/* Streamlit loading animasyonlarını tamamen gizle */
.stSpinner,
.stProgress,
.stAlert,
.stToast,
div[data-testid="stNotificationContentInfo"],
div[data-testid="stNotificationContentWarning"],
div[data-testid="stNotificationContentError"],
div[data-testid="stNotificationContentSuccess"],
.element-container div[data-stale="true"],
.stApp > div[data-testid="stHeader"],
.stDeployButton,
.stDecoration,
div[data-testid="stStatusWidget"],
div[data-testid="stSpinner"],
div[class*="spinner"],
div[class*="loading"],
div[class*="progress"],
.loading-spinner,
.stApp div[data-testid="stSpinner"] * {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    animation: none !important;
    -webkit-animation: none !important;
    -moz-animation: none !important;
    -o-animation: none !important;
    -ms-animation: none !important;
}

/* Tüm animasyonları global olarak devre dışı bırak */
*, *::before, *::after {
    -webkit-animation-duration: 0s !important;
    -webkit-animation-delay: 0s !important;
    -webkit-transition-duration: 0s !important;
    -webkit-transition-delay: 0s !important;
    -moz-animation-duration: 0s !important;
    -moz-animation-delay: 0s !important;
    -moz-transition-duration: 0s !important;
    -moz-transition-delay: 0s !important;
    -o-animation-duration: 0s !important;
    -o-animation-delay: 0s !important;
    -o-transition-duration: 0s !important;
    -o-transition-delay: 0s !important;
    animation-duration: 0s !important;
    animation-delay: 0s !important;
    transition-duration: 0s !important;
    transition-delay: 0s !important;
}

/* Sayfa yeniden yüklenme animasyonunu gizle */
.stAppViewContainer div[data-testid="stHeader"] {
    display: none !important;
}

/* Streamlit menü ve footer'ı gizle */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}



/* Sarı renk içeren herhangi bir elementi gizle */
*[style*="yellow"], 
*[style*="#FFFF"], 
*[style*="#FFF0"], 
*[style*="rgb(255, 255"], 
*[class*="yellow"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)





# Global grafik arka plan şeffaflık fonksiyonu
def make_transparent_bg(fig):
    """Plotly grafiklerinin arka planını şeffaf yapar"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        xaxis=dict(
            gridcolor='rgba(148,163,184,0.2)',
            zerolinecolor='rgba(148,163,184,0.3)'
        ),
        yaxis=dict(
            gridcolor='rgba(148,163,184,0.2)',
            zerolinecolor='rgba(148,163,184,0.3)'
        )
    )
    return fig

# D3Graph Visualization Functions
def create_networkx_plotly_graph(G, title, node_colors=None):
    """NetworkX grafiğini Plotly ile interaktif görselleştir"""
    # Grafik konumlarını hesapla
    pos = nx.spring_layout(G, seed=42)
    
    # Kenarları çiz
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Düğümleri çiz
    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        # Bağlantı sayısını göster
        adjacencies = list(G.neighbors(node))
        node_text.append(f'{node}<br>Bağlantı: {len(adjacencies)}')
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[node for node in G.nodes()],
        textposition="middle center",
        hovertext=node_text,
        marker=dict(
            size=20,
            color=node_colors if node_colors else 'lightblue',
            line=dict(width=2, color='black'),
            colorscale='Viridis'
        )
    )
    
    # Figürü oluştur
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                        title=title,
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Düğümlere tıklayarak detay görebilirsiniz",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002,
                            xanchor="left", yanchor="bottom",
                            font=dict(color="gray", size=12)
                        )],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                   ))
    
    return fig

def create_d3graph_visualizations():
    """NetworkX + Plotly ile interaktif ağ görselleştirmeleri"""
    st.header("🌐 İnteraktif Ağ Görselleştirmeleri")
    st.write("NetworkX ve Plotly kullanılarak oluşturulan gerçek zamanlı interaktif grafikleri")
    
    if not NETWORK_AVAILABLE:
        st.error("❌ NetworkX veya Plotly yüklenemedi")
        return
    
    st.success("✅ Ağ görselleştirme kütüphaneleri hazır!")
    
    # Grafik türü seçimi
    graph_type = st.selectbox(
        "Grafik Türünü Seçin:",
        ["Organizasyon Ağı", "Beceri Ağı", "Proje İlişkileri", "Departman Bağlantıları"],
        help="Görmek istediğiniz ağ grafiği türünü seçin",
        key="hr_graph_type_selector"
    )
    
    st.info(f"📊 Seçili grafik: **{graph_type}** - Gerçek zamanlı veri akışı aktif!")
    
    if graph_type == "Organizasyon Ağı":
        create_organization_network()
    elif graph_type == "Beceri Ağı":
        create_skill_network()
    elif graph_type == "Proje İlişkileri":
        create_project_network()
    elif graph_type == "Departman Bağlantıları":
        create_department_network()

def create_organization_network():
    """NetworkX ile organizasyon ağ grafiği"""
    st.subheader("📊 Organizasyon Ağı")
    st.info("Şirket hiyerarşisi ve departman yapıları - Gerçek zamanlı veri akışı")
    
    try:
        # NetworkX graf oluştur
        G = nx.DiGraph()
        
        # Örnek organizasyon verisi
        edges = [
            ('CEO', 'HR Manager'), ('CEO', 'IT Manager'), ('CEO', 'Sales Manager'),
            ('HR Manager', 'HR Specialist'), ('HR Manager', 'Recruiter'),
            ('IT Manager', 'Developer'), ('IT Manager', 'Analyst'),
            ('Sales Manager', 'Sales Rep'), ('Sales Manager', 'Account Manager')
        ]
        
        G.add_edges_from(edges)
        
        st.success("✅ Organizasyon verisi yüklendi!")
        
        # Veri tablosu göster
        import pandas as pd
        org_data = pd.DataFrame(edges, columns=['Yönetici', 'Çalışan'])
        st.dataframe(org_data, width="stretch")
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🏢 Organizasyon Şeması")
        st.plotly_chart(fig, use_container_width=True, key="chart_1")
        
        st.success("💼 İnteraktif organizasyon ağı başarıyla yüklendi!")
        st.info("💡 Düğümlere tıklayarak detayları görebilirsiniz")
        
    except Exception as e:
        st.error(f"Organizasyon ağı hatası: {str(e)}")
        st.info("💼 Veri yeniden işleniyor...")

def create_skill_network():
    """NetworkX ile beceri ağ grafiği"""
    st.subheader("🎯 Beceri Ağı")
    st.info("Çalışan yetenekleri ve teknoloji becerileri arasındaki ilişki haritası")
    
    try:
        # NetworkX graf oluştur
        G = nx.Graph()
        
        # Beceri verisi (sabit seed için tutarlılık)
        skills = ['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Visualization', 'Statistics']
        employees = ['Ahmet', 'Ayşe', 'Mehmet', 'Fatma', 'Ali', 'Zeynep']
        
        np.random.seed(42)
        edges = []
        for emp in employees:
            for skill in np.random.choice(skills, size=np.random.randint(2, 4), replace=False):
                edges.append((emp, skill))
        
        G.add_edges_from(edges)
        
        st.success("✅ Beceri verisi hazırlandı!")
        
        # Beceri matrisi göster
        import pandas as pd
        skill_data = pd.DataFrame(edges, columns=['Çalışan', 'Beceri'])
        st.dataframe(skill_data, width="stretch")
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🎯 Beceri-Çalışan İlişki Ağı")
        st.plotly_chart(fig, use_container_width=True, key="chart_2")
        
        st.success("🌐 Beceri ağı yüklendi!")
        
    except Exception as e:
        st.error(f"Beceri ağı hatası: {str(e)}")
        st.info("💡 Veri yeniden işleniyor...")

def create_project_network():
    """NetworkX ile proje ilişkileri ağ grafiği"""
    st.subheader("🚀 Proje İlişkileri")
    st.info("Projeler ve kullanılan teknolojiler arasındaki bağlantı haritası")
    
    try:
        # NetworkX graf oluştur
        G = nx.Graph()
        
        # Proje verisi (sabit seed)
        projects = ['Web App', 'Mobile App', 'Data Pipeline', 'Analytics Dashboard', 'ML Model']
        technologies = ['React', 'Python', 'Docker', 'AWS', 'PostgreSQL', 'Streamlit', 'Plotly']
        
        np.random.seed(123)
        edges = []
        for proj in projects:
            for tech in np.random.choice(technologies, size=np.random.randint(2, 4), replace=False):
                edges.append((proj, tech))
        
        G.add_edges_from(edges)
        
        st.success("✅ Proje verileri hazırlandı!")
        
        # Proje-teknoloji matrisi
        import pandas as pd
        project_data = pd.DataFrame(edges, columns=['Proje', 'Teknoloji'])
        st.dataframe(project_data, width="stretch")
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🚀 Proje-Teknoloji Bağlantı Ağı")
        st.plotly_chart(fig, use_container_width=True, key="chart_3")
        
        st.success("🌐 Proje ağı başarıyla yüklendi!")
        
    except Exception as e:
        st.error(f"Proje ağı hatası: {str(e)}")
        st.info("🛠️ Teknik sorun gideriliyor...")

def create_department_network():
    """NetworkX ile departman bağlantıları ağ grafiği"""
    st.subheader("🏢 Departman Bağlantıları")
    st.info("Departmanlar arası işbirliği ve iletişim yoğunluğu")
    
    try:
        # NetworkX graf oluştur
        G = nx.Graph()
        
        # Departman arası işbirliği
        collaborations = [
            ('İK', 'IT', 3), ('İK', 'Finans', 2), ('Satış', 'Pazarlama', 5),
            ('IT', 'Operasyon', 4), ('Finans', 'Operasyon', 3), ('Pazarlama', 'IT', 2),
            ('İK', 'Operasyon', 2), ('Satış', 'Finans', 3), ('IT', 'Pazarlama', 2)
        ]
        
        # Ağırlıklı kenarlar ekle
        for dept1, dept2, weight in collaborations:
            G.add_edge(dept1, dept2, weight=weight)
        
        st.success("✅ Departman verileri yüklendi!")
        
        # Departman işbirliği tablosu
        import pandas as pd
        dept_data = pd.DataFrame(collaborations, columns=['Departman 1', 'Departman 2', 'İşbirliği Seviyesi'])
        st.dataframe(dept_data, width="stretch")
        
        # En yoğun işbirliği
        max_collab = dept_data.loc[dept_data['İşbirliği Seviyesi'].idxmax()]
        st.metric(
            "En Yoğun İşbirliği", 
            f"{max_collab['Departman 1']} ↔️ {max_collab['Departman 2']}",
            f"Seviye: {max_collab['İşbirliği Seviyesi']}"
        )
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🏢 Departman İşbirliği Ağı")
        st.plotly_chart(fig, use_container_width=True, key="chart_4")
        
        st.success("🌐 Departman ağı aktif!")
        
    except Exception as e:
        st.error(f"Departman ağı hatası: {str(e)}")
        st.info("🔄 Sistem yeniden bağlanıyor...")

# Sidebar kaldırıldı - Profil bilgileri Hakkımda kısmına taşındı

# Basit tab tasarımı
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.3);
        border-radius: 15px;
        padding: 6px;
        margin: 0 auto 1rem auto;
        display: flex;
        justify-content: center;
        width: fit-content;
        max-width: 100%;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0 24px;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Roboto', sans-serif;
        background: transparent;
        border: none;
        color: #94A3B8;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #E2E8F0;
    }
    
    .stTabs {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)



# Direkt tab menüsü ile başla

# Büyük tab menüsü - Header altında
menu = st.tabs(["🏠 Anasayfa", "📊 İstatistik", "🔄 Api entegrasyon", "🧪 Veri Bilimi", "👥 İK Analitik", "📊 RFM Analizi", "🔄 Cohort", "⚠️ Churn"])




with menu[0]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    
    # Profil bölümü
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0;">
        """, unsafe_allow_html=True)
        
        # Profil fotoğrafı kontrolü
        try:
            # Fotoğraf dosyasını bul
            photo_found = False
            photo_name = ""
            
            if os.path.exists("lpp.jpeg"):
                photo_name = "lpp.jpeg"
                photo_found = True
            elif os.path.exists("app/lpp.jpeg"):
                photo_name = "app/lpp.jpeg"
                photo_found = True
            elif os.path.exists("pp2.jpeg"):
                photo_name = "pp2.jpeg"
                photo_found = True
            elif os.path.exists("app/pp2.jpeg"):
                photo_name = "app/pp2.jpeg"
                photo_found = True
            elif os.path.exists("pp.jpg"):
                photo_name = "pp.jpg"
                photo_found = True
            elif os.path.exists("app/pp.jpg"):
                photo_name = "app/pp.jpg"
                photo_found = True
            
            if photo_found:
                # Base64 encode fotoğraf
                import base64
                with open(photo_name, "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                
                # Gradient çerçeveli fotoğraf HTML
                st.markdown(f"""
                <div style="
                    width: 220px;
                    height: 220px;
                    margin: 0 auto;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #A855F7 100%);
                    padding: 10px;
                    box-shadow: 
                        0 0 30px rgba(59, 130, 246, 0.6),
                        0 0 60px rgba(139, 92, 246, 0.4),
                        0 15px 50px rgba(59, 130, 246, 0.3);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <img src="data:image/jpeg;base64,{img_base64}" 
                         style="
                             width: 200px;
                             height: 200px;
                             border-radius: 50%;
                             object-fit: cover;
                             border: 3px solid rgba(255, 255, 255, 0.3);
                         " />
                </div>
                """, unsafe_allow_html=True)
            else:
                # TÖ avatarı
                st.markdown("""
                <div style="width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #8B5CF6); padding: 3px; box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3); display: flex; align-items: center; justify-content: center;">
                    <div style="width: 100%; height: 100%; border-radius: 50%; background: linear-gradient(135deg, #1E40AF, #7C3AED); display: flex; align-items: center; justify-content: center; color: white; font-size: 60px; font-weight: bold; font-family: 'Roboto', sans-serif;">
                        TÖ
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            # Hata durumunda TÖ avatarı
            st.markdown("""
            <div style="width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #8B5CF6); padding: 3px; box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3); display: flex; align-items: center; justify-content: center;">
                <div style="width: 100%; height: 100%; border-radius: 50%; background: linear-gradient(135deg, #1E40AF, #7C3AED); display: flex; align-items: center; justify-content: center; color: white; font-size: 60px; font-weight: bold; font-family: 'Roboto', sans-serif;">
                    TÖ
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # İsim ve sosyal medya
        st.markdown("""
            <h2 style="
                margin: 1rem 0 0.3rem 0; 
                font-size: 1.4rem; 
                font-family: 'Roboto', sans-serif; 
                font-style: normal; 
                font-weight: normal;
                line-height: 1.2; 
                background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 50%, #7C3AED 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
            ">Tolunay ÖZCAN</h2>
            <h2 style="
                margin: 0.5rem 0 1rem 0; 
                font-size: 1.4rem; 
                font-family: 'Roboto', sans-serif; 
                font-style: normal; 
                font-weight: normal;
                line-height: 1.2; 
                background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 50%, #7C3AED 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
            ">Data Analyst</h2>
            
        </div>
        """, unsafe_allow_html=True)
        
        # Sosyal medya linkleri - Alt alta
        st.write(" ")  # Boşluk
        
        # Alt alta sosyal medya linkleri - Gerçek logolarla
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 0.8rem; margin-top: 1rem;">
            <a href="https://www.linkedin.com/in/tolunayozcan/" target="_blank" style="
                display: flex; align-items: center; gap: 0.5rem; text-decoration: none; 
                color: #0A66C2; font-weight: 500; font-size: 1rem; transition: all 0.2s ease;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
                LinkedIn
            </a>
            <a href="https://github.com/TolunayOzcan" target="_blank" style="
                display: flex; align-items: center; gap: 0.5rem; text-decoration: none; 
                color: #333; font-weight: 500; font-size: 1rem; transition: all 0.2s ease;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                GitHub
            </a>
            <a href="mailto:tolunayozcan95@gmail.com" style="
                display: flex; align-items: center; gap: 0.5rem; text-decoration: none; 
                color: #EA4335; font-weight: 500; font-size: 1rem; transition: all 0.2s ease;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-.904.732-1.636 1.636-1.636h1.82L12 11.64l8.545-7.819h1.82c.904 0 1.636.732 1.636 1.636z"/>
                </svg>
                Gmail
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h2 style="color: #8B5CF6 !important; font-weight: bold !important; font-family: 'Roboto', sans-serif !important; text-shadow: none !important; background: none !important; margin-top: 1rem;">Hakkımda</h2>
        <p style="font-size: 1.1rem; line-height: 1.6; text-align: justify;">Veri analizi ve görselleştirme alanında 4+ yıllık deneyime sahip Kıdemli Veri Analistiyim. SQL, Python ve VBA 
        konularında uzman seviyede bilgi sahibi. CRM veri analizi, İK analitik çözümleri, çağrı merkezi ve operasyonel 
        raporlama konularında kapsamlı deneyim. Veri odaklı karar alma süreçlerini destekleyen analitik çözümler 
        geliştirme konusunda uzman.</p>
        
        <p><strong>🎯 Uzmanlık Alanlarım:</strong></p>
        <ul style="font-size: 1rem; line-height: 1.5;">
            <li>📊 SQL ve veritabanı yönetimi</li>
            <li>🐍 Python ile veri analizi ve görselleştirme</li>
            <li>⚡ VBA ile otomasyon çözümleri</li>
            <li>🎨 CRM ve İK veri analizleri</li>
            <li>📈 Operasyonel raporlama ve dashboard geliştirme</li>
        </ul>
        """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Site İlişki Haritası - TEK KAPSAMLI DİAGRAM
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #8B5CF6; font-family: Roboto; font-style: italic;'>🗺️ Tüm Site Yapısı - Tek Büyük Diagram</h3>", unsafe_allow_html=True)
    
    # Plotly ile tek kapsamlı site diagramı
    fig = go.Figure()
    
    # MERKEZ - Ana Portal (Marker ayrı)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(size=180, color='#8B5CF6', opacity=0.6,
                   line=dict(width=6, color='white'),
                   symbol='star'),
        showlegend=False,
        name='Ana Portal',
        hovertemplate='<b>🏠 Ana Portal</b><br>Tüm özelliklerin merkezi<br>• Profil & İletişim<br>• Site navigasyonu<br>• Hub\'lara giriş<extra></extra>'
    ))
    
    # MERKEZ - Text ayrı trace (KESINLIKLE GÖRÜNÜR)
    fig.add_trace(go.Scatter(
        x=[0], y=[-2],
        mode='text',
        text=['🏠 MERKEZ PORTAL'],
        textfont=dict(size=20, color='white', family='Inter, sans-serif'),
        showlegend=False,
        hoverinfo='none',
        name='Merkez Text'
    ))
    
    # Tüm site yapısı tek diagramda
    site_data = [
        # KUZEY - İstatistik Hub
        {
            'hub': {'name': '📊<br><b>İSTATİSTİK</b><br>Hub', 'x': 0, 'y': 5.5, 'color': '#3B82F6'},
            'features': [
                {'name': '🎨 Sanatçı<br>Değerleri', 'x': -3, 'y': 7.5, 'color': '#60A5FA'},
                {'name': '📊 Sankey<br>Diyagram', 'x': 3, 'y': 7.5, 'color': '#60A5FA'},
                {'name': '📈 Korelasyon<br>Analizi', 'x': 0, 'y': 8.5, 'color': '#60A5FA'},
                {'name': '📋 Veri<br>Tabloları', 'x': -1.5, 'y': 7, 'color': '#60A5FA'},
                {'name': '🎯 Trend<br>Analizi', 'x': 1.5, 'y': 7, 'color': '#60A5FA'}
            ]
        },
        # DOĞU - API Hub  
        {
            'hub': {'name': '🌐<br><b>API VERİLERİ</b><br>Hub', 'x': 5.5, 'y': 0, 'color': '#10B981'},
            'features': [
                {'name': '� Ekonomi<br>API', 'x': 7.5, 'y': 3, 'color': '#34D399'},
                {'name': '📈 Borsa<br>API', 'x': 7.5, 'y': -3, 'color': '#34D399'},
                {'name': '🌤️ Hava<br>API', 'x': 8.5, 'y': 0, 'color': '#34D399'},
                {'name': '🌐 Web<br>Scraping', 'x': 7, 'y': 1.5, 'color': '#34D399'},
                {'name': '💾 Cache<br>Sistemi', 'x': 7, 'y': -1.5, 'color': '#34D399'}
            ]
        },
        # GÜNEY - Veri Bilimi Hub
        {
            'hub': {'name': '🔬<br><b>VERİ BİLİMİ</b><br>Hub', 'x': 0, 'y': -5.5, 'color': '#F59E0B'},
            'features': [
                {'name': '🤖 ML<br>Modelleri', 'x': -3, 'y': -7.5, 'color': '#FBBF24'},
                {'name': '📊 Regresyon<br>Analizi', 'x': 3, 'y': -7.5, 'color': '#FBBF24'},
                {'name': '🧹 Veri<br>Temizleme', 'x': 0, 'y': -8.5, 'color': '#FBBF24'},
                {'name': '🎯 Tahmin<br>Modelleri', 'x': -1.5, 'y': -7, 'color': '#FBBF24'},
                {'name': '📈 Sınıflandırma<br>Algoritmaları', 'x': 1.5, 'y': -7, 'color': '#FBBF24'}
            ]
        },
        # BATI - İK Hub
        {
            'hub': {'name': '👥<br><b>İK ANALİTİK</b><br>Hub', 'x': -5.5, 'y': 0, 'color': '#EF4444'},
            'features': [
                {'name': '📋 Performans<br>Raporu', 'x': -7.5, 'y': 3, 'color': '#F87171'},
                {'name': '🎯 İK<br>Dashboard', 'x': -7.5, 'y': -3, 'color': '#F87171'},
                {'name': '📊 İşgören<br>İstatistik', 'x': -8.5, 'y': 0, 'color': '#F87171'},
                {'name': '📈 Attrition<br>Analizi', 'x': -7, 'y': 1.5, 'color': '#F87171'},
                {'name': '💼 HR<br>Metrikleri', 'x': -7, 'y': -1.5, 'color': '#F87171'}
            ]
        }
    ]
    
    # Tüm hub'ları ve özelliklerini tek diagramda çiz
    for section in site_data:
        hub = section['hub']
        
        # Hub kısa ismini al (HTML etiketlerini kaldır)
        hub_short_name = hub['name'].replace('<br>', ' ').replace('<b>', '').replace('</b>', '').replace('👥', '').replace('📊', '').replace('🔗', '').replace('🧠', '').strip()
        
        # Merkezden hub'a ana bağlantı
        fig.add_shape(
            type="line",
            x0=0, y0=0, x1=hub['x'], y1=hub['y'],
            line=dict(color='rgba(139, 92, 246, 0.7)', width=8),
        )
        
        # İlişki çizgisinin orta noktasına modern etiket kutusu
        mid_x = (0 + hub['x']) / 2
        mid_y = (0 + hub['y']) / 2
        connection_label = f"{hub_short_name}"
        
        # Gradient arka plan kutusu
        # Modern etiket kutusu (şeffaf arka plan)
        fig.add_trace(go.Scatter(
            x=[mid_x], y=[mid_y],
            mode='markers+text',
            marker=dict(size=62, color='rgba(255,255,255,0.22)', 
                       line=dict(width=1.5, color='rgba(139,92,246,0.55)'),
                       symbol='square'),
            text=[connection_label],
            textfont=dict(size=10, color='white', family='Inter, sans-serif'),
            textposition='middle center',
            showlegend=False,
            hoverinfo='none',
            name=f'Connection Box {connection_label}'
        ))
        
        # Ana hub (Marker ayrı)
        hub_short_name = hub['name'].replace('<br><b>', ' ').replace('</b><br>Hub', '').replace('<b>', '').replace('</b>', '')
        fig.add_trace(go.Scatter(
            x=[hub['x']], y=[hub['y']],
            mode='markers',
            marker=dict(size=150, color=hub['color'], opacity=0.45,
                       line=dict(width=5, color='white'),
                       symbol='hexagon'),
            showlegend=False,
            name=hub_short_name,
            hovertemplate=f'<b>{hub_short_name}</b><br>Ana kategori hub\'ı<br>Tüm alt özelliklerin merkezi<extra></extra>'
        ))
        
        # Hub text ayrı trace (KESINLIKLE GÖRÜNÜR)
        fig.add_trace(go.Scatter(
            x=[hub['x']], y=[hub['y']-2.0],
            mode='text',
            text=[hub_short_name],
            textfont=dict(size=18, color='white', family='Inter, sans-serif'),
            showlegend=False,
            hoverinfo='none',
            name=f'Hub Text {hub_short_name}'
        ))
        
        # Alt özellikler
        for feature in section['features']:
            # Hub'dan özelliğe bağlantı
            fig.add_shape(
                type="line",
                x0=hub['x'], y0=hub['y'], 
                x1=feature['x'], y1=feature['y'],
                line=dict(color='rgba(107, 114, 128, 0.5)', width=3),
            )
            
            # Hub-Feature bağlantısının orta noktasına minimal etiket
            mid_x = (hub['x'] + feature['x']) / 2
            mid_y = (hub['y'] + feature['y']) / 2
            feature_short_name = feature['name'].replace('<br>', ' ').replace('📋', '').replace('🎯', '').replace('📊', '').replace('📈', '').replace('💼', '').replace('🔗', '').replace('💰', '').replace('🌍', '').replace('🧠', '').replace('📉', '').replace('🎨', '').replace('👨‍💼', '').replace('🎭', '').strip()
            
            # Sadece kısa isim göster (daha temiz görünüm)
            display_name = feature_short_name.split()[0] if feature_short_name else ''
            
            # Minimal pill-shaped arka plan
            fig.add_trace(go.Scatter(
                x=[mid_x], y=[mid_y],
                mode='markers+text',
                marker=dict(size=46, color='rgba(255,255,255,0.18)', 
                           line=dict(width=1.2, color=hub['color']),
                           symbol='circle', opacity=0.8),
                text=[display_name],
                textfont=dict(size=9, color='white', family='Inter, sans-serif'),
                textposition='middle center',
                showlegend=False,
                hoverinfo='none',
                name=f'Feature Connection Box {display_name}'
            ))
            
            # Özellik node'u (Marker ayrı)
            feature_short_name = feature['name'].replace('<br>', ' ')
            fig.add_trace(go.Scatter(
                x=[feature['x']], y=[feature['y']],
                mode='markers',
                marker=dict(size=100, color=feature['color'], opacity=0.45,
                           line=dict(width=3, color='white'),
                           symbol='circle'),
                showlegend=False,
                name=feature_short_name,
                hovertemplate=f'<b>{feature_short_name}</b><br>Özel özellik ve işlev<br>Detaylı analizler<extra></extra>'
            ))
            
            # Özellik text ayrı trace (KESINLIKLE GÖRÜNÜR)
            fig.add_trace(go.Scatter(
                x=[feature['x']], y=[feature['y']-1.4],
                mode='text',
                text=[feature_short_name],
                textfont=dict(size=13, color='white', family='Inter, sans-serif'),
                showlegend=False,
                hoverinfo='none',
                name=f'Feature Text {feature_short_name}'
            ))
    
    # Layout ayarları - TEXT'LER KEİİNLİKLE SÜREKLI GÖRÜNÜR
    fig.update_layout(
        title={
            'text': '🗺️ Modern Portfolio Site Yapısı',
            'x': 0.5,
            'font': {'size': 20, 'color': 'white', 'family': 'Inter, sans-serif'}
        },
        xaxis=dict(
            showgrid=False, 
            showticklabels=False, 
            zeroline=False,
            range=[-18, 18],
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=False, 
            showticklabels=False, 
            zeroline=False,
            range=[-18, 18],
            fixedrange=True
        ),
        plot_bgcolor='rgba(30,39,46,0.95)',
        paper_bgcolor='rgba(20,25,31,0.95)',
    height=1150,  # Daha yüksek
        showlegend=False,
        margin=dict(t=100, l=80, r=80, b=80),  # Daha geniş margin
        font=dict(family='Roboto', size=14, color='white'),  # Genel font büyük
        hovermode='closest',
        dragmode=False,
        modebar=dict(remove=['select2d', 'lasso2d', 'autoScale2d', 'pan2d', 'zoom2d']),
        uniformtext=dict(minsize=12, mode='show')  # Text'ler kesinlikle görünsün
    )
    
    fig = make_transparent_bg(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tek Diagram Açıklaması
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin-top: 15px;'>
        <h4 style='color: white; margin: 0 0 10px 0;'>🗺️ Site Yapısı Tek Diagram Açıklaması</h4>
        <p style='color: white; margin: 0; font-size: 14px;'>
            <strong>⭐ Mor Merkez:</strong> Ana Portfolio Hub - Tüm özelliklerin başlangıç noktası<br>
            <strong>� Ana Hub'lar:</strong> 4 ana kategori - İstatistik, API, Veri Bilimi, İK Analitik<br>
            <strong>⚪ Alt Özellikler:</strong> Her hub'ın altındaki özel işlevler ve sayfalar<br><br>
            Bu tek diagram, tüm site yapısını ve tab'ların içindeki tüm özellikleri bir arada gösterir.
            Her öğeyi hover'layarak detaylarını görebilirsiniz. 🎯
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)

with menu[1]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>Analytics</h2>", unsafe_allow_html=True)
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
            margin=dict(t=50, b=50, l=40, r=40),
        )
        fig1 = make_transparent_bg(fig1)
        st.plotly_chart(fig1, use_container_width=True, key="chart_5")
        
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
        st.dataframe(df2, width="stretch")
        
        # Daha profesyonel çizgi grafik
        fig2 = px.line(df2, x="kategori", y="sayi", 
                     markers=True,
                     line_shape="spline",
                     color_discrete_sequence=['#1E88E5'],
                     title="Kategori Bazında Eser Sayıları")
        fig2.update_layout(
            xaxis_title="Kategori",
            yaxis_title="Eser Sayısı",
            margin=dict(t=50, b=50, l=40, r=40),
        )
        fig2 = make_transparent_bg(fig2)
        st.plotly_chart(fig2, use_container_width=True, key="chart_6")
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
            margin=dict(t=50, b=50, l=40, r=40),
            height=500,
        )
        sankey_fig = make_transparent_bg(sankey_fig)
        
        st.plotly_chart(sankey_fig, use_container_width=True, key="chart_7")
    st.markdown("""</div>""", unsafe_allow_html=True)

with menu[2]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>Api entegrasyon</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>Bu sayfada çeşitli API'lerden gerçek zamanlı veriler çekilmekte ve analiz edilmektedir. 
    CoinGecko, ExchangeRate-API ve diğer public API'lerden güncel finansal veriler sağlanır.</p>
    """, unsafe_allow_html=True)
    
    # API Service import ve başlatma
    api_status = {"success": False, "error": None}
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from api_services import api_service
        api_status["success"] = True
        st.success("✅ API servisleri başarıyla yüklendi!")
    except Exception as e:
        api_status["error"] = str(e)
        st.error(f"❌ API servisleri yüklenemedi: {e}")
        st.info("Fallback demo veriler kullanılacak.")
    
    st.markdown("""</div>""", unsafe_allow_html=True)

    if api_status["success"]:
        # Real-time Kripto Para Verileri
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>🚀 Gerçek Zamanlı Kripto Para Verileri</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>CoinGecko API'den canlı veri çekimi</strong></p>", unsafe_allow_html=True)
        
        try:
            with st.spinner('Kripto para verileri çekiliyor...'):
                crypto_df = api_service.get_crypto_data()
                
            if not crypto_df.empty:
                st.dataframe(crypto_df, width="stretch")
                
                # Kripto para grafiği
                if 'Değişim 24h' in crypto_df.columns:
                    crypto_df_chart = crypto_df.copy()
                    crypto_df_chart['degisim_numeric'] = crypto_df_chart['Değişim 24h'].str.rstrip('%').astype('float')
                    
                    fig = px.bar(crypto_df_chart, x='Sembol', y='degisim_numeric',
                                title='Kripto Para 24 Saatlik Değişim (%)',
                                text='Değişim 24h',
                                color='degisim_numeric',
                                color_continuous_scale=['red', 'white', 'green'])
                    
                    fig.update_layout(
                        xaxis_title="Kripto Para",
                        yaxis_title="Değişim (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        margin=dict(t=50, b=20, l=20, r=20)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="chart_8")
            else:
                st.warning("Kripto para verileri alınamadı.")
                
        except Exception as e:
            st.error(f"Kripto para veri hatası: {e}")
            
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Döviz Kurları ve Hisse Senetleri
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""<div class="card">""", unsafe_allow_html=True)
            st.markdown("<h3>💱 Döviz Kurları</h3>", unsafe_allow_html=True)
            st.markdown("<p><strong>ExchangeRate-API'den güncel kurlar</strong></p>", unsafe_allow_html=True)
            
            try:
                with st.spinner('Döviz kurları güncelleniyor...'):
                    exchange_df = api_service.get_exchange_rates()
                    
                if not exchange_df.empty:
                    st.dataframe(exchange_df, width="stretch")
                    
                    # Döviz kurları grafiği
                    exchange_df_chart = exchange_df.copy()
                    exchange_df_chart['Kur'] = exchange_df_chart['Kur'].astype('float')
                    
                    fig = px.bar(exchange_df_chart, x='Döviz Çifti', y='Kur',
                                title='USD Bazında Döviz Kurları',
                                text='Kur')
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickangle=45),
                        margin=dict(t=50, b=80, l=20, r=20)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="chart_9")
                else:
                    st.warning("Döviz kuru verileri alınamadı.")
                    
            except Exception as e:
                st.error(f"Döviz kuru veri hatası: {e}")
                
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""<div class="card">""", unsafe_allow_html=True)
            st.markdown("<h3>📈 Hisse Senedi Verileri</h3>", unsafe_allow_html=True)
            st.markdown("<p><strong>Demo hisse senedi verileri</strong></p>", unsafe_allow_html=True)
            
            try:
                stock_df = api_service.get_stock_data()
                
                if not stock_df.empty:
                    st.dataframe(stock_df, width="stretch")
                    
                    # Hisse senedi değişim grafiği
                    stock_df_chart = stock_df.copy()
                    stock_df_chart['degisim_numeric'] = stock_df_chart['Değişim'].str.rstrip('%').astype('float')
                    
                    fig = px.scatter(stock_df_chart, x='Hisse', y='degisim_numeric',
                                   title='Hisse Senedi Günlük Değişim (%)',
                                   text='Değişim',
                                   size_max=15)
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=50, b=20, l=20, r=20)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="chart_10")
                else:
                    st.warning("Hisse senedi verileri alınamadı.")
                    
            except Exception as e:
                st.error(f"Hisse senedi veri hatası: {e}")
                
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Hava Durumu API
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>🌤️ Hava Durumu Verisi</h3>", unsafe_allow_html=True)
        
        city = st.selectbox("Şehir Seçin:", ["Istanbul", "Ankara", "Izmir", "London", "New York"], key="api_weather_city_selector")
        
        try:
            weather_data = api_service.get_weather_data(city)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sıcaklık", f"{weather_data['temperature']}°C")
            with col2:
                st.metric("Nem", f"{weather_data['humidity']}%")
            with col3:
                st.metric("Rüzgar", f"{weather_data['wind_speed']} km/h")
            with col4:
                st.metric("Basınç", f"{weather_data['pressure']} hPa")
            
            st.info(f"📍 {weather_data['city']} - {weather_data['description']}")
            st.caption(f"Son güncelleme: {weather_data['timestamp']}")
            
        except Exception as e:
            st.error(f"Hava durumu veri hatası: {e}")
            
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Son Haberler
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>📰 Son Haberler</h3>", unsafe_allow_html=True)
        
        try:
            news_data = api_service.get_news_headlines()
            
            for news in news_data:
                with st.expander(f"📰 {news['title']}"):
                    st.write(news['description'])
                    st.caption(f"Kaynak: {news['source']} | {news['publishedAt']}")
                    
        except Exception as e:
            st.error(f"Haber veri hatası: {e}")
        
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # API Status
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>🔧 API Durum Bilgisi</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("✅ CoinGecko API")
            st.caption("Kripto para verileri")
        with col2:
            st.success("✅ ExchangeRate API")
            st.caption("Döviz kurları")
        with col3:
            st.info("ℹ️ Demo APIs")
            st.caption("Hisse & Haber verileri")
        
        st.markdown("""</div>""", unsafe_allow_html=True)
        
    else:
        # Fallback - eski sistem
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>⚠️ Fallback Sistem</h3>", unsafe_allow_html=True)
        st.warning("API servisleri yüklenemediği için demo veriler gösteriliyor.")
        
        # Eski ekonomi verileri
        ekonomi_df = scrape_ekonomi_verileri()
        
        if not ekonomi_df.empty:
            st.markdown("<p><strong>Demo Ekonomik Veriler</strong></p>", unsafe_allow_html=True)
            st.dataframe(ekonomi_df, width="stretch")
        
        st.markdown("""</div>""", unsafe_allow_html=True)
    try:
        from app.api_services import api_service
        
        # Real-time Kripto Para Verileri
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>🚀 Gerçek Zamanlı Kripto Para Verileri</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>CoinGecko API'den canlı veri çekimi</strong></p>", unsafe_allow_html=True)
        
        with st.spinner('Kripto para verileri çekiliyor...'):
            crypto_df = api_service.get_crypto_data()
            
        if not crypto_df.empty:
            st.dataframe(crypto_df, width="stretch")
            
            # Kripto para grafiği
            if 'Değişim 24h' in crypto_df.columns:
                crypto_df['degisim_numeric'] = crypto_df['Değişim 24h'].str.rstrip('%').astype('float')
                colors = ['#F44336' if x < 0 else '#4CAF50' for x in crypto_df['degisim_numeric']]
                
                fig = px.bar(crypto_df, x='Sembol', y='degisim_numeric',
                            title='Kripto Para 24 Saatlik Değişim (%)',
                            text='Değişim 24h',
                            color='degisim_numeric',
                            color_continuous_scale=['red', 'green'])
                
                fig.update_layout(
                    xaxis_title="Kripto Para",
                    yaxis_title="Değişim (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    margin=dict(t=50, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True, key="chart_11")
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Döviz Kurları
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""<div class="card">""", unsafe_allow_html=True)
            st.markdown("<h3>💱 Döviz Kurları</h3>", unsafe_allow_html=True)
            st.markdown("<p><strong>ExchangeRate-API'den güncel kurlar</strong></p>", unsafe_allow_html=True)
            
            with st.spinner('Döviz kurları güncelleniyor...'):
                exchange_df = api_service.get_exchange_rates()
                
            if not exchange_df.empty:
                st.dataframe(exchange_df, width="stretch")
                
                # Döviz kurları grafiği
                fig = px.bar(exchange_df, x='Döviz Çifti', y='Kur',
                            title='USD Bazında Döviz Kurları',
                            text='Kur')
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(tickangle=45),
                    margin=dict(t=50, b=80, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True, key="chart_12")
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""<div class="card">""", unsafe_allow_html=True)
            st.markdown("<h3>📈 Hisse Senedi Verileri</h3>", unsafe_allow_html=True)
            st.markdown("<p><strong>Demo hisse senedi verileri</strong></p>", unsafe_allow_html=True)
            
            stock_df = api_service.get_stock_data()
            
            if not stock_df.empty:
                st.dataframe(stock_df, width="stretch")
                
                # Hisse senedi değişim grafiği
                stock_df['degisim_numeric'] = stock_df['Değişim'].str.rstrip('%').astype('float')
                
                fig = px.scatter(stock_df, x='Hisse', y='degisim_numeric',
                               title='Hisse Senedi Günlük Değişim (%)',
                               text='Değişim',
                               size_max=15)
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True, key="chart_13")
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Hava Durumu API
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>🌤️ Hava Durumu Verisi</h3>", unsafe_allow_html=True)
        
        city = st.selectbox("Şehir Seçin:", ["Istanbul", "Ankara", "Izmir", "London", "New York"], key="fallback_weather_city_selector")
        
        weather_data = api_service.get_weather_data(city)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sıcaklık", f"{weather_data['temperature']}°C")
        with col2:
            st.metric("Nem", f"{weather_data['humidity']}%")
        with col3:
            st.metric("Rüzgar", f"{weather_data['wind_speed']} km/h")
        with col4:
            st.metric("Basınç", f"{weather_data['pressure']} hPa")
        
        st.info(f"📍 {weather_data['city']} - {weather_data['description']}")
        st.caption(f"Son güncelleme: {weather_data['timestamp']}")
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Son Haberler
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>📰 Son Haberler</h3>", unsafe_allow_html=True)
        
        news_data = api_service.get_news_headlines()
        
        for news in news_data:
            with st.expander(f"📰 {news['title']}"):
                st.write(news['description'])
                st.caption(f"Kaynak: {news['source']} | {news['publishedAt']}")
        
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # API Status
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>🔧 API Durum Bilgisi</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("✅ CoinGecko API")
            st.caption("Kripto para verileri")
        with col2:
            st.success("✅ ExchangeRate API")
            st.caption("Döviz kurları")
        with col3:
            st.info("ℹ️ Demo APIs")
            st.caption("Hisse & Haber verileri")
        
        st.markdown("""</div>""", unsafe_allow_html=True)
        
    except ImportError as e:
        st.error(f"API servisleri yüklenemedi: {e}")
        # Fallback to old system
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>Ekonomi Göstergeleri</h3>", unsafe_allow_html=True)
        ekonomi_df = scrape_ekonomi_verileri()
        
with menu[3]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>Data science</h2>", unsafe_allow_html=True)
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
        st.plotly_chart(rf_fig, use_container_width=True, key="chart_14")
    
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
            st.plotly_chart(conversion_fig, use_container_width=True, key="chart_15")
        with col2:
            st.plotly_chart(spending_fig, use_container_width=True, key="chart_16")
    
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
        st.dataframe(ab_summary.round(2), width="stretch")
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
        st.plotly_chart(segment_fig, use_container_width=True, key="chart_17")
    
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
        
        st.dataframe(segment_summary.round(2), width="stretch")
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
        st.plotly_chart(reg_fig, use_container_width=True, key="chart_18")
    
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
        st.dataframe(feature_importance, width="stretch")
    st.markdown("""</div>""", unsafe_allow_html=True)
    
with menu[4]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2>HR analytics</h2>", unsafe_allow_html=True)
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
    st.plotly_chart(fig_attrition, use_container_width=True, key="chart_19")
    
    # Özet metrikler
    st.subheader("Özet Metrikler")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_attrition_rate = employee_data['işten_ayrılma'].mean() * 100
        st.metric(
            label="Genel İşten Ayrılma Oranı", 
            value=f"{total_attrition_rate:.1f}%",
            delta=f"{total_attrition_rate - 17.0:.1f}%" if total_attrition_rate != 17.0 else None,
            delta_color="inverse"
        )
        
    with col2:
        high_risk_dept = employee_data.groupby('departman')['işten_ayrılma'].mean().idxmax()
        high_risk_rate = employee_data[employee_data['departman'] == high_risk_dept]['işten_ayrılma'].mean() * 100
        
        st.metric(
            label="En Riskli Departman", 
            value=high_risk_dept,
            delta=f"{high_risk_rate:.1f}%"
        )
        
    with col3:
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
    st.plotly_chart(fig_salary, use_container_width=True, key="chart_21")
    
    # Maaş özet istatistikleri
    st.subheader("Maaş Özet İstatistikleri")
    salary_stats = employee_data.groupby('departman')['aylık_maaş'].agg(['mean', 'median', 'min', 'max']).reset_index()
    salary_stats.columns = ['Departman', 'Ortalama', 'Medyan', 'Minimum', 'Maksimum']
    
    # Formatla (TL ekle ve yuvarla)
    for col in ['Ortalama', 'Medyan', 'Minimum', 'Maksimum']:
        salary_stats[col] = salary_stats[col].apply(lambda x: f"{x:,.0f} TL")
    
    st.dataframe(salary_stats, width="stretch")
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Performans Dağılımı
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Performans Puan Dağılımı</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Çalışanların performans puanlarının dağılımı, şirketin genel performans değerlendirme eğilimlerini anlamanıza yardımcı olur.
    Bu analiz, performans değerlendirme sisteminin etkinliğini ve potansiyel önyargıları değerlendirmenize olanak tanır.</p>
    """, unsafe_allow_html=True)
    
    fig_performance = create_performance_distribution_chart(employee_data)
    st.plotly_chart(fig_performance, use_container_width=True, key="chart_22")
    
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
        yaxis_title='Aylık Maaş (TL)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_perf_salary, use_container_width=True, key="chart_23")
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
        st.plotly_chart(fig_hiring, use_container_width=True, key="chart_24")
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown("<h3>Departman ve Cinsiyet Dağılımı</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p>Departman ve cinsiyet dağılımı, şirketin çeşitlilik ve kapsayıcılık konusundaki durumunu değerlendirir.
        Bu analiz, cinsiyet dengesi açısından iyileştirme gerektiren alanları belirlemenize yardımcı olur.</p>
        """, unsafe_allow_html=True)
        
        fig_demographics = create_department_demographics_chart(employee_data)
        st.plotly_chart(fig_demographics, use_container_width=True, key="chart_25")
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Tatmin Skoru ve İşten Ayrılma İlişkisi
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>Tatmin Skoru ve İşten Ayrılma İlişkisi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>Çalışan tatmini ve işten ayrılma arasındaki ilişki, insan kaynakları stratejileri için kritik bir içgörü sağlar.
    Bu analiz, tatmin skorlarının işten ayrılma olasılığı üzerindeki etkisini gösterir.</p>
    """, unsafe_allow_html=True)
    
    fig_satisfaction = create_satisfaction_vs_attrition_chart(employee_data)
    st.plotly_chart(fig_satisfaction, use_container_width=True, key="chart_26")
    
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
    
    # İşten Ayrılma Nedenleri - En Alta Taşındı
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>📊 İşten Ayrılma Nedenleri Analizi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>İşten ayrılma nedenlerinin analizi, şirketin hangi alanlarda iyileştirme yapması gerektiğini belirlemede kritiktir.
    Bu grafik, en sık karşılaşılan ayrılma nedenlerini göstererek, proaktif önlemler almanıza yardımcı olur.</p>
    """, unsafe_allow_html=True)
    
    # İşten ayrılma nedenleri grafiği - Güzel renkler
    reasons_data = employee_data[employee_data['işten_ayrılma']]['ayrılma_nedeni'].value_counts().reset_index()
    reasons_data.columns = ['Ayrılma Nedeni', 'Çalışan Sayısı']
    
    # Mor, pudra, somon renk paleti
    custom_colors = [
        '#8B5CF6',  # Mor
        '#F8BBD9',  # Pudra pembe
        '#FA8072',  # Somon
        '#DDA0DD',  # Plum
        '#F0A5A5',  # Açık somon
        '#C8A2C8',  # Lavanta
        '#FFB6C1',  # Açık pembe
        '#D8BFD8'   # Thistle
    ]
    
    fig_reasons = px.pie(
        reasons_data,
        values='Çalışan Sayısı',
        names='Ayrılma Nedeni',
        hole=0.4,
        color_discrete_sequence=custom_colors
    )
    
    fig_reasons.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#E2E8F0'),
        title={
            'text': 'İşten Ayrılma Nedenleri Dağılımı',
            'x': 0.5,
            'font': {'size': 16, 'color': '#8B5CF6'}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    fig_reasons.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Sayı: %{value}<br>Oran: %{percent}<extra></extra>'
    )
    
    st.plotly_chart(fig_reasons, use_container_width=True, key="chart_20")
    
    # İşten ayrılma nedenleri önerileri
    st.markdown("""
    <div style='background: linear-gradient(135deg, #8B5CF6 0%, #F8BBD9 50%, #FA8072 100%); padding: 15px; border-radius: 10px; margin-top: 15px;'>
        <h4 style='color: white; margin: 0 0 10px 0;'>🎯 Ayrılma Nedenlerine Yönelik Öneriler</h4>
        <p style='color: white; margin: 0; font-size: 14px;'>
            En sık ayrılma nedenlerini analiz ederek, çalışan bağlılığını artırıcı stratejiler geliştirebilir, 
            proaktif önlemlerle işten ayrılma oranlarını azaltabilirsiniz.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # İşten Ayrılma Nedenleri - En Alta Taşındı
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h3>📉 İşten Ayrılma Nedenleri Analizi</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p>İşten ayrılma nedenlerinin analizi, şirketin hangi alanlarda iyileştirme yapması gerektiğini belirlemede kritiktir.
    Bu grafik, en sık karşılaşılan ayrılma nedenlerini göstererek, proaktif önlemler almanıza yardımcı olur.</p>
    """, unsafe_allow_html=True)
    
    # İşten ayrılma nedenleri grafiği - Güzel renkler
    reasons_data = employee_data[employee_data['işten_ayrılma']]['ayrılma_nedeni'].value_counts().reset_index()
    reasons_data.columns = ['Ayrılma Nedeni', 'Çalışan Sayısı']
    
    # Mor, pudra, somon renk paleti
    custom_colors = [
        '#8B5CF6',  # Mor
        '#F8BBD9',  # Pudra pembe
        '#FA8072',  # Somon
        '#DDA0DD',  # Plum
        '#F0A5A5',  # Açık somon
        '#C8A2C8',  # Lavanta
        '#FFB6C1',  # Açık pembe
        '#D8BFD8'   # Thistle
    ]
    
    fig_reasons = px.pie(
        reasons_data,
        values='Çalışan Sayısı',
        names='Ayrılma Nedeni',
        hole=0.4,
        color_discrete_sequence=custom_colors
    )
    
    fig_reasons.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#E2E8F0'),
        title={
            'text': 'İşten Ayrılma Nedenleri Dağılımı',
            'x': 0.5,
            'font': {'size': 16, 'color': '#8B5CF6'}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    fig_reasons.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Sayı: %{value}<br>Oran: %{percent}<extra></extra>'
    )
    
    st.plotly_chart(fig_reasons, use_container_width=True, key="chart_reasons_bottom")
    
    # İşten ayrılma nedenleri önerileri
    st.markdown("""
    <div style='background: linear-gradient(135deg, #8B5CF6 0%, #F8BBD9 50%, #FA8072 100%); padding: 15px; border-radius: 10px; margin-top: 15px;'>
        <h4 style='color: white; margin: 0 0 10px 0;'>🎯 Ayrılma Nedenlerine Yönelik Öneriler</h4>
        <p style='color: white; margin: 0; font-size: 14px;'>
            En sık ayrılma nedenlerini analiz ederek, çalışan bağlılığını artırıcı stratejiler geliştirebilir, 
            proaktif önlemlerle işten ayrılma oranlarını azaltabilirsiniz.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)

with menu[5]:  # RFM Analizi sekmesi
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #8B5CF6; font-family: Roboto; margin-bottom: 2rem;'>📊 RFM Segmentasyon Analizi</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;'>E-ticaret müşterilerini Recency, Frequency, Monetary değerlerine göre segmentlere ayırma</p>", unsafe_allow_html=True)
    
    # Doğrudan analizi başlat
    with st.spinner("� RFM Analizi başlatılıyor..."):
        # Gerekli kütüphaneler
        import matplotlib.pyplot as plt
        import seaborn as sns
        import warnings
        from datetime import datetime, timedelta
        
        warnings.filterwarnings('ignore')
        
        # Stil ayarları
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # 1. VERİ SETİ OLUŞTURMA (Gerçekçi E-ticaret Verisi)
        np.random.seed(42)
        
        # 1000 müşteri verisi oluştur
        n_customers = 1000
        customer_ids = [f'C{str(i).zfill(5)}' for i in range(1, n_customers + 1)]
        
        # Farklı müşteri davranış profilleri
        data = []
        current_date = datetime(2024, 10, 1)
        
        for cid in customer_ids:
            # Müşteri tipi belirleme
            customer_type = np.random.choice(['şampiyon', 'sadık', 'risk_altında', 'kayıp', 'yeni'], 
                                             p=[0.15, 0.25, 0.20, 0.25, 0.15])
            
            if customer_type == 'şampiyon':
                n_orders = np.random.randint(15, 40)
                last_order_days = np.random.randint(1, 30)
                avg_order_value = np.random.uniform(500, 2000)
            elif customer_type == 'sadık':
                n_orders = np.random.randint(8, 20)
                last_order_days = np.random.randint(20, 60)
                avg_order_value = np.random.uniform(300, 1000)
            elif customer_type == 'risk_altında':
                n_orders = np.random.randint(5, 15)
                last_order_days = np.random.randint(90, 180)
                avg_order_value = np.random.uniform(200, 800)
            elif customer_type == 'kayıp':
                n_orders = np.random.randint(2, 8)
                last_order_days = np.random.randint(180, 365)
                avg_order_value = np.random.uniform(100, 500)
            else:  # yeni
                n_orders = np.random.randint(1, 3)
                last_order_days = np.random.randint(1, 45)
                avg_order_value = np.random.uniform(150, 600)
            
            for _ in range(n_orders):
                order_date = current_date - timedelta(days=np.random.randint(last_order_days, last_order_days + 200))
                order_value = avg_order_value * np.random.uniform(0.7, 1.3)
                
                data.append({
                    'MusteriID': cid,
                    'SiparisTarihi': order_date,
                    'SiparisUcreti': round(order_value, 2)
                })
        
        df = pd.DataFrame(data)
        
    st.success(f"✓ Toplam {len(df)} sipariş, {df['MusteriID'].nunique()} benzersiz müşteri")
    st.success(f"✓ Tarih Aralığı: {df['SiparisTarihi'].min().date()} - {df['SiparisTarihi'].max().date()}")
    
    # Ham veri önizleme
    st.markdown("### 📋 Ham Veri Önizleme")
    st.dataframe(df.head(10), width='stretch')
    
    with st.spinner("🔄 RFM metrikleri hesaplanıyor..."):
        # 2. RFM METRİKLERİNİ HESAPLAMA
        analysis_date = current_date + timedelta(days=1)
        
        rfm = df.groupby('MusteriID').agg({
            'SiparisTarihi': lambda x: (analysis_date - x.max()).days,  # Recency
            'SiparisUcreti': ['count', 'sum']  # Frequency ve Monetary
        }).reset_index()
        
        rfm.columns = ['MusteriID', 'Yenilik', 'Siklik', 'Parasal']
        
        # 3. RFM SKORLAMASI (1-5 arası)
        # Recency için ters sıralama (düşük recency = yüksek skor)
        rfm['Y_Skoru'] = pd.qcut(rfm['Yenilik'], q=5, labels=[5, 4, 3, 2, 1])
        
        # Frequency ve Monetary için normal sıralama
        rfm['S_Skoru'] = pd.qcut(rfm['Siklik'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        rfm['P_Skoru'] = pd.qcut(rfm['Parasal'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        
        # RFM Skoru oluşturma
        rfm['RFM_Skoru'] = rfm['Y_Skoru'].astype(str) + rfm['S_Skoru'].astype(str) + rfm['P_Skoru'].astype(str)
        rfm['RFM_Skoru_Toplam'] = rfm['Y_Skoru'].astype(int) + rfm['S_Skoru'].astype(int) + rfm['P_Skoru'].astype(int)
        
        # 4. MÜŞTERİ SEGMENTLERİ OLUŞTURMA
        def rfm_segment(row):
            r, f, m = int(row['Y_Skoru']), int(row['S_Skoru']), int(row['P_Skoru'])
            
            if r >= 4 and f >= 4 and m >= 4:
                return 'Şampiyonlar'
            elif r >= 3 and f >= 3 and m >= 3:
                return 'Sadık Müşteriler'
            elif r >= 4 and f <= 2:
                return 'Yeni Müşteriler'
            elif r >= 3 and f >= 2 and m >= 2:
                return 'Potansiyel Sadık'
            elif r <= 2 and f >= 3 and m >= 3:
                return 'Risk Altında'
            elif r <= 2 and f >= 4 and m >= 4:
                return 'Kaybedilmemeli'
            elif r <= 2 and f <= 2:
                return 'Kayıp Müşteriler'
            elif r >= 3 and f <= 2 and m <= 2:
                return 'Umut Verici'
            else:
                return 'İlgi Gerekli'
        
        rfm['Segment'] = rfm.apply(rfm_segment, axis=1)
    
    st.success("✓ RFM skorları başarıyla oluşturuldu")
    
    # RFM İstatistikleri tablosu
    st.markdown("### 📈 RFM İstatistikleri")
    st.dataframe(rfm.describe().round(2), width='stretch')
    
    # Metrik kartları
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam Müşteri", len(rfm))
    with col2:
        st.metric("Ortalama Yenilik", f"{rfm['Yenilik'].mean():.0f} gün")
    with col3:
        st.metric("Ortalama Sıklık", f"{rfm['Siklik'].mean():.1f}")
    with col4:
        st.metric("Ortalama Parasal", f"{rfm['Parasal'].mean():.0f} TL")
    
    # Segmentasyon sonuçları
    st.markdown("### 🎯 Segmentasyon Sonuçları")
    segment_summary = rfm.groupby('Segment').agg({
        'MusteriID': 'count',
        'Yenilik': 'mean',
        'Siklik': 'mean',
        'Parasal': 'mean'
    }).round(2)
    
    segment_summary.columns = ['Müşteri Sayısı', 'Ort. Yenilik', 'Ort. Sıklık', 'Ort. Parasal']
    segment_summary = segment_summary.sort_values('Müşteri Sayısı', ascending=False)
    
    st.dataframe(segment_summary, width='stretch')
    
    # 5. GÖRSELLEŞTİRMELER
    st.markdown("### 📊 Görselleştirmeler")
    
    # 6 adet grafik oluştur
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Segment Dağılımı
    ax1 = plt.subplot(2, 3, 1)
    segment_counts = rfm['Segment'].value_counts()
    colors = plt.cm.Set3(range(len(segment_counts)))
    wedges, texts, autotexts = ax1.pie(segment_counts.values, labels=segment_counts.index, 
                                         autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Müşteri Segment Dağılımı', fontsize=14, fontweight='bold', pad=20)
    
    # 2. Segment bazında ortalama Parasal
    ax2 = plt.subplot(2, 3, 2)
    segment_monetary = rfm.groupby('Segment')['Parasal'].mean().sort_values(ascending=True)
    bars = ax2.barh(segment_monetary.index, segment_monetary.values, color=plt.cm.viridis(np.linspace(0, 1, len(segment_monetary))))
    ax2.set_xlabel('Ortalama Harcama (TL)', fontsize=10)
    ax2.set_title('Segment Bazında Ortalama Müşteri Değeri', fontsize=14, fontweight='bold', pad=20)
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2, f'{width:,.0f} TL', 
                 ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 3. YSP Scatter Plot (Y vs S)
    ax3 = plt.subplot(2, 3, 3)
    scatter = ax3.scatter(rfm['Yenilik'], rfm['Siklik'], 
                         c=rfm['Parasal'], s=100, alpha=0.6, cmap='YlOrRd', edgecolors='black', linewidth=0.5)
    ax3.set_xlabel('Yenilik (Gün)', fontsize=10)
    ax3.set_ylabel('Sıklık (Sipariş Sayısı)', fontsize=10)
    ax3.set_title('Yenilik vs Sıklık (Renk: Parasal)', fontsize=14, fontweight='bold', pad=20)
    plt.colorbar(scatter, ax=ax3, label='Toplam Harcama (TL)')
    
    # 4. YSP Skor Dağılımı
    ax4 = plt.subplot(2, 3, 4)
    rfm['RFM_Skoru_Toplam'].hist(bins=13, color='skyblue', edgecolor='black', ax=ax4)
    ax4.set_xlabel('Toplam YSP Skoru', fontsize=10)
    ax4.set_ylabel('Müşteri Sayısı', fontsize=10)
    ax4.set_title('YSP Skor Dağılımı', fontsize=14, fontweight='bold', pad=20)
    ax4.axvline(rfm['RFM_Skoru_Toplam'].mean(), color='red', linestyle='--', linewidth=2, label=f'Ortalama: {rfm["RFM_Skoru_Toplam"].mean():.1f}')
    ax4.legend()
    
    # 5. Segment bazında müşteri sayısı ve toplam gelir
    ax5 = plt.subplot(2, 3, 5)
    segment_revenue = rfm.groupby('Segment').agg({
        'MusteriID': 'count',
        'Parasal': 'sum'
    }).reset_index()
    segment_revenue.columns = ['Segment', 'Musteri_Sayisi', 'Toplam_Gelir']
    
    x = np.arange(len(segment_revenue))
    width = 0.35
    
    ax5_twin = ax5.twinx()
    bars1 = ax5.bar(x - width/2, segment_revenue['Musteri_Sayisi'], width, label='Müşteri Sayısı', color='steelblue', alpha=0.8)
    bars2 = ax5_twin.bar(x + width/2, segment_revenue['Toplam_Gelir'], width, label='Toplam Gelir', color='coral', alpha=0.8)
    
    ax5.set_xlabel('Segment', fontsize=10)
    ax5.set_ylabel('Müşteri Sayısı', fontsize=10, color='steelblue')
    ax5_twin.set_ylabel('Toplam Gelir (TL)', fontsize=10, color='coral')
    ax5.set_title('Segment: Müşteri Sayısı ve Toplam Gelir', fontsize=14, fontweight='bold', pad=20)
    ax5.set_xticks(x)
    ax5.set_xticklabels(segment_revenue['Segment'], rotation=45, ha='right')
    ax5.tick_params(axis='y', labelcolor='steelblue')
    ax5_twin.tick_params(axis='y', labelcolor='coral')
    
    # 6. En İyi 10 Müşteri
    ax6 = plt.subplot(2, 3, 6)
    top_customers = rfm.nlargest(10, 'Parasal')[['MusteriID', 'Parasal', 'Segment']]
    bars = ax6.barh(range(len(top_customers)), top_customers['Parasal'].values)
    ax6.set_yticks(range(len(top_customers)))
    ax6.set_yticklabels([f"{cid}\n({seg})" for cid, seg in zip(top_customers['MusteriID'], top_customers['Segment'])], fontsize=8)
    ax6.set_xlabel('Toplam Harcama (TL)', fontsize=10)
    ax6.set_title('En İyi 10 Değerli Müşteri', fontsize=14, fontweight='bold', pad=20)
    ax6.invert_yaxis()
    
    for i, (bar, val) in enumerate(zip(bars, top_customers['Parasal'].values)):
        color = plt.cm.RdYlGn(i / len(top_customers))
        bar.set_color(color)
        ax6.text(val, i, f' {val:,.0f} TL', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    
    # Streamlit'te matplotlib figürünü göster
    st.pyplot(fig)
    
    # 6. STRATEJİK ÖNERİLER
    st.markdown("### 🎯 Stratejik Öneriler")
    
    strategies = {
        'Şampiyonlar': '🏆 VIP programlar, özel indirimler, early access',
        'Sadık Müşteriler': '💎 Sadakat programları, referans kampanyaları',
        'Risk Altında': '⚠️  Geri kazanma kampanyaları, anket, özel teklifler',
        'Kaybedilmemeli': '🚨 Acil müdahale, kişiselleştirilmiş teklifler',
        'Kayıp Müşteriler': '💔 Win-back kampanyaları, agresif indirimler',
        'Yeni Müşteriler': '🌟 Onboarding programı, ilk alışveriş teşvikleri',
        'Potansiyel Sadık': '📈 Cross-sell, upsell fırsatları',
        'Umut Verici': '🎯 Hedefli kampanyalar, engagement artırma',
        'İlgi Gerekli': '👀 Re-engagement kampanyaları'
    }
    
    for segment in rfm['Segment'].unique():
        count = len(rfm[rfm['Segment'] == segment])
        revenue = rfm[rfm['Segment'] == segment]['Parasal'].sum()
        
        with st.expander(f"{segment} ({count} müşteri, {revenue:,.0f} TL gelir)"):
            st.write(f"**Strateji:** {strategies.get(segment, 'Özel strateji gerekli')}")
            
            # Segment detay metrikleri
            segment_data = rfm[rfm['Segment'] == segment]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Ort. Yenilik", f"{segment_data['Yenilik'].mean():.0f} gün")
            with col2:
                st.metric("Ort. Sıklık", f"{segment_data['Siklik'].mean():.1f}")
            with col3:
                st.metric("Ort. Parasal", f"{segment_data['Parasal'].mean():.0f} TL")
    
    # 7. DOKÜMANTASYON ve CSV İNDİRME
    st.markdown("### 📥 Belge ve Veri İndirme")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin-bottom: 1rem;'>
        <h4 style='color: white; margin: 0 0 10px 0;'>📚 RFM Analizi Kapsamlı Belgesi</h4>
        <p style='color: white; margin: 0; font-size: 14px;'>
            Bu analizin detaylı açıklaması, metodolojisi, segment tanımları ve stratejik önerileri içeren 
            kapsamlı belgeyi indirebilirsiniz. Belge RFM analizinin tüm teknik detaylarını ve iş faydalarını içerir.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # RFM Dokümantasyon
        try:
            with open('RFM_Analizi_Belgesi.md', 'r', encoding='utf-8') as f:
                doc_content = f.read()
            
            st.download_button(
                label="📚 RFM Analizi Belgesi (.md)",
                data=doc_content,
                file_name="RFM_Analizi_Kapsamli_Belge.md",
                mime="text/markdown",
                help="RFM Analizinin detaylı açıklaması ve metodolojisi",
                use_container_width=True
            )
        except FileNotFoundError:
            st.info("📚 RFM Belge dosyası bulunamadı")
    
    with col2:
        # CSV indirme
        csv = rfm.to_csv(index=False)
        st.download_button(
            label="� RFM Detay CSV İndir",
            data=csv,
            file_name=f"rfm_detay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col3:
        # Segment özet CSV indirme
        segment_csv = segment_summary.to_csv()
        st.download_button(
            label="📈 Segment Özet CSV İndir",
            data=segment_csv,
            file_name=f"segment_ozet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Analiz özeti
    st.markdown("### ✅ Analiz Tamamlandı!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Analiz Edilen Müşteri", len(rfm))
    with col2:
        st.metric("Oluşturulan Segment", len(rfm['Segment'].unique()))
    with col3:
        st.metric("Toplam Gelir", f"{rfm['Parasal'].sum():,.0f} TL")
    
    st.markdown("""</div>""", unsafe_allow_html=True)

# 7. COHORT RETENTION ANALİZİ SEKMESİ
with menu[6]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🔄 Cohort Retention Analizi</h1>
        <p style='color: white; margin: 0.5rem 0; font-size: 1.2rem; opacity: 0.9;'>Müşteri Edinme Cohortlarını Takip Ederek Retention Oranlarını Analiz Etme</p>
        <p style='color: white; margin: 0; font-size: 0.9rem; opacity: 0.8;'>📅 Updated: October 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;'>Müşteri edinme cohortlarını takip ederek retention oranlarını analiz etme</p>", unsafe_allow_html=True)
    
    # Veri oluşturma
    st.markdown("### 🎯 Cohort Verisi Oluşturma")
    
    with st.spinner("📊 Cohort verisi oluşturuluyor..."):
        # 1. VERİ SETİ OLUŞTURMA
        np.random.seed(42)
        
        # 12 aylık cohort verisi oluştur
        start_date = datetime(2024, 1, 1)
        n_customers_per_cohort = np.random.randint(150, 300, 12)  # Her ay için farklı müşteri sayısı
        
        data = []
        
        for cohort_month in range(12):
            cohort_date = start_date + timedelta(days=cohort_month * 30)
            n_customers = n_customers_per_cohort[cohort_month]
            
            # Her cohort için müşteriler
            for customer_idx in range(n_customers):
                customer_id = f'C{cohort_month:02d}{customer_idx:04d}'
                
                # İlk alışveriş (cohort ayı)
                first_purchase = cohort_date + timedelta(days=np.random.randint(0, 30))
                data.append({
                    'CustomerID': customer_id,
                    'OrderDate': first_purchase,
                    'OrderValue': np.random.uniform(50, 500),
                    'CohortMonth': cohort_date
                })
                
                # Retention simülasyonu (azalan olasılıkla tekrar alışveriş)
                retention_probability = 0.7  # İlk ay %70 retention
                
                for month in range(1, 12):
                    if np.random.random() < retention_probability:
                        # Bu müşteri bu ayda da alışveriş yaptı
                        purchase_date = cohort_date + timedelta(days=month * 30 + np.random.randint(0, 30))
                        
                        # Sadece analiz tarihinden önce olan siparişleri ekle
                        if purchase_date <= datetime(2024, 10, 1):
                            data.append({
                                'CustomerID': customer_id,
                                'OrderDate': purchase_date,
                                'OrderValue': np.random.uniform(50, 500),
                                'CohortMonth': cohort_date
                            })
                    
                    # Her ay retention olasılığı azalır
                    retention_probability *= 0.85
        
        df_cohort = pd.DataFrame(data)
    
    st.success(f"✓ Toplam {len(df_cohort)} sipariş")
    st.success(f"✓ {df_cohort['CustomerID'].nunique()} benzersiz müşteri")
    st.success(f"✓ Tarih Aralığı: {df_cohort['OrderDate'].min().date()} - {df_cohort['OrderDate'].max().date()}")
    
    # Ham veri önizleme
    st.markdown("### 📋 Ham Veri Önizleme")
    st.dataframe(df_cohort.head(10), width='stretch')
    
    with st.spinner("🔄 Cohort analizleri hesaplanıyor..."):
        # 2. COHORT TANIMLAMA
        # Her müşterinin ilk alışveriş tarihi (cohort)
        df_cohort['OrderMonth'] = df_cohort['OrderDate'].dt.to_period('M')
        df_cohort['CohortMonth'] = df_cohort['CohortMonth'].dt.to_period('M')
        
        # Her müşteri için cohort tanımla
        customer_cohort = df_cohort.groupby('CustomerID')['OrderMonth'].min().reset_index()
        customer_cohort.columns = ['CustomerID', 'CohortMonth']
        
        # Ana dataframe'e cohort bilgisini ekle
        df_cohort = df_cohort.merge(customer_cohort, on='CustomerID', how='left', suffixes=('', '_First'))
        
        # Cohort index hesapla (müşterinin ilk alışverişinden kaç ay geçti)
        df_cohort['CohortIndex'] = (df_cohort['OrderMonth'] - df_cohort['CohortMonth']).apply(lambda x: x.n)
        
        # 3. COHORT ANALİZİ - MÜŞTERİ SAYISI
        # Her cohort ve index için benzersiz müşteri sayısı
        cohort_data = df_cohort.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()
        cohort_data.columns = ['CohortMonth', 'CohortIndex', 'CustomerCount']
        
        # Pivot tablo oluştur
        cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerCount')
        
        # Retention oranları hesapla (ilk aya göre %)
        cohort_retention = cohort_counts.divide(cohort_counts[0], axis=0) * 100
        
        # 4. COHORT ANALİZİ - GELİR
        cohort_revenue = df_cohort.groupby(['CohortMonth', 'CohortIndex'])['OrderValue'].sum().reset_index()
        cohort_revenue_pivot = cohort_revenue.pivot(index='CohortMonth', columns='CohortIndex', values='OrderValue')
    
    # Cohort bilgileri gösterimi
    st.markdown("### 📊 Cohort Retention Tablosu")
    st.markdown("**Retention Oranları (%):**")
    st.dataframe(cohort_retention.round(1), width='stretch')
    
    # 5. GÖRSELLEŞTİRMELER
    st.markdown("### 📈 Cohort Retention Dashboard")
    
    # Grafikleri oluştur
    fig = plt.figure(figsize=(20, 14))
    
    # 1. Retention Heatmap
    ax1 = plt.subplot(3, 2, 1)
    sns.heatmap(cohort_retention, annot=True, fmt='.0f', cmap='RdYlGn', 
                cbar_kws={'label': 'Retention %'}, vmin=0, vmax=100, ax=ax1,
                linewidths=0.5, linecolor='gray')
    ax1.set_title('Cohort Retention Heatmap (%)', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Ay (Cohort\'tan itibaren)', fontsize=11)
    ax1.set_ylabel('Cohort Ayı', fontsize=11)
    
    # 2. Retention Eğrileri
    ax2 = plt.subplot(3, 2, 2)
    for cohort in cohort_retention.index[:6]:  # İlk 6 cohort
        ax2.plot(cohort_retention.columns, cohort_retention.loc[cohort], 
                 marker='o', label=f'{cohort}', linewidth=2, markersize=6)
    ax2.set_xlabel('Ay', fontsize=11)
    ax2.set_ylabel('Retention Oranı (%)', fontsize=11)
    ax2.set_title('Cohort Retention Eğrileri', fontsize=16, fontweight='bold', pad=20)
    ax2.legend(title='Cohort', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 105)
    
    # 3. Ortalama Retention Trendi
    ax3 = plt.subplot(3, 2, 3)
    avg_retention = cohort_retention.mean()
    ax3.plot(avg_retention.index, avg_retention.values, marker='o', color='darkblue', 
             linewidth=3, markersize=8, label='Ortalama Retention')
    ax3.fill_between(avg_retention.index, avg_retention.values, alpha=0.3, color='skyblue')
    ax3.set_xlabel('Ay', fontsize=11)
    ax3.set_ylabel('Ortalama Retention (%)', fontsize=11)
    ax3.set_title('Tüm Cohortlar İçin Ortalama Retention Trendi', fontsize=16, fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 105)
    
    # Kritik retention noktaları ekle
    for i, val in enumerate(avg_retention.values):
        if i in [0, 1, 3, 6]:  # 0, 1, 3, 6. aylar
            ax3.annotate(f'{val:.1f}%', xy=(i, val), xytext=(5, 5), 
                        textcoords='offset points', fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # 4. Cohort Boyutları (İlk müşteri sayısı)
    ax4 = plt.subplot(3, 2, 4)
    cohort_sizes = cohort_counts[0].sort_index()
    bars = ax4.bar(range(len(cohort_sizes)), cohort_sizes.values, color='teal', alpha=0.7, edgecolor='black')
    ax4.set_xticks(range(len(cohort_sizes)))
    ax4.set_xticklabels([str(c) for c in cohort_sizes.index], rotation=45, ha='right')
    ax4.set_xlabel('Cohort Ayı', fontsize=11)
    ax4.set_ylabel('İlk Müşteri Sayısı', fontsize=11)
    ax4.set_title('Cohort Büyüklükleri (İlk Ay)', fontsize=16, fontweight='bold', pad=20)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 5. Kümülatif Retention
    ax5 = plt.subplot(3, 2, 5)
    cumulative_customers = cohort_counts.sum(axis=0)
    ax5.plot(cumulative_customers.index, cumulative_customers.values, 
             marker='s', color='crimson', linewidth=3, markersize=8)
    ax5.fill_between(cumulative_customers.index, cumulative_customers.values, 
                     alpha=0.3, color='pink')
    ax5.set_xlabel('Ay', fontsize=11)
    ax5.set_ylabel('Toplam Aktif Müşteri', fontsize=11)
    ax5.set_title('Tüm Cohortlarda Aylık Toplam Aktif Müşteri', fontsize=16, fontweight='bold', pad=20)
    ax5.grid(True, alpha=0.3)
    
    # 6. Revenue Heatmap
    ax6 = plt.subplot(3, 2, 6)
    sns.heatmap(cohort_revenue_pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Toplam Gelir (TL)'}, ax=ax6,
                linewidths=0.5, linecolor='gray')
    ax6.set_title('Cohort Gelir Heatmap (TL)', fontsize=16, fontweight='bold', pad=20)
    ax6.set_xlabel('Ay (Cohort\'tan itibaren)', fontsize=11)
    ax6.set_ylabel('Cohort Ayı', fontsize=11)
    
    plt.tight_layout()
    
    # Streamlit'te grafikleri göster
    st.pyplot(fig, use_container_width=True)
    
    # 6. RETENTION ANALİZ RAPORU
    st.markdown("### 📊 Retention Analiz Raporu")
    
    # Ay 1, 3, 6 retention oranları
    month_1_retention = avg_retention[1] if 1 in avg_retention.index else 0
    month_3_retention = avg_retention[3] if 3 in avg_retention.index else 0
    month_6_retention = avg_retention[6] if 6 in avg_retention.index else 0
    
    # Metrikleri göster
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("1. Ay Retention", f"{month_1_retention:.1f}%")
    with col2:
        st.metric("3. Ay Retention", f"{month_3_retention:.1f}%")
    with col3:
        st.metric("6. Ay Retention", f"{month_6_retention:.1f}%")
    
    # En iyi ve en kötü cohortlar
    avg_retention_by_cohort = cohort_retention.mean(axis=1).sort_values(ascending=False)
    best_cohort = avg_retention_by_cohort.index[0]
    worst_cohort = avg_retention_by_cohort.index[-1]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 15px; border-radius: 10px; margin-bottom: 1rem;'>
            <h4 style='color: white; margin: 0 0 10px 0;'>🏆 En İyi Cohort</h4>
            <p style='color: white; margin: 0; font-size: 14px;'>
                <strong>{best_cohort}</strong><br>
                Ortalama Retention: {avg_retention_by_cohort[best_cohort]:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); padding: 15px; border-radius: 10px; margin-bottom: 1rem;'>
            <h4 style='color: white; margin: 0 0 10px 0;'>⚠️ En Düşük Cohort</h4>
            <p style='color: white; margin: 0; font-size: 14px;'>
                <strong>{worst_cohort}</strong><br>
                Ortalama Retention: {avg_retention_by_cohort[worst_cohort]:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Retention drop analizi
    retention_drops = []
    for i in range(len(avg_retention) - 1):
        drop = avg_retention.values[i] - avg_retention.values[i + 1]
        retention_drops.append((i, i+1, drop))
    
    # En büyük düşüş
    biggest_drop = max(retention_drops, key=lambda x: x[2])
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); padding: 15px; border-radius: 10px; margin-bottom: 1rem;'>
        <h4 style='color: white; margin: 0 0 10px 0;'>📉 En Büyük Retention Düşüşü</h4>
        <p style='color: white; margin: 0; font-size: 14px;'>
            {biggest_drop[0]}. aydan {biggest_drop[1]}. aya: <strong>-{biggest_drop[2]:.1f}%</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 7. STRATEJİK ÖNERİLER
    st.markdown("### 💡 Stratejik Öneriler")
    
    strategies = []
    
    if month_1_retention < 60:
        strategies.append({
            'title': '⚠️ 1. AY KRİTİK',
            'items': [
                'Onboarding sürecini güçlendirin',
                'İlk 30 gün içinde email/SMS kampanyaları',
                'İlk alışverişte pozitif deneyim sağlayın'
            ]
        })
    
    if month_3_retention < 40:
        strategies.append({
            'title': '⚠️ 3. AY RİSKLİ',
            'items': [
                '60-90 gün arası müşterilere özel kampanyalar',
                'Cross-sell/upsell fırsatları sunun',
                'Müşteri memnuniyeti anketi gönderin'
            ]
        })
    
    if month_6_retention < 25:
        strategies.append({
            'title': '⚠️ 6. AY DÜŞÜK',
            'items': [
                'Sadakat programı oluşturun',
                'Re-engagement kampanyaları başlatın',
                'VIP statüsü ve özel avantajlar sunun'
            ]
        })
    
    # Genel öneriler her zaman gösterilir
    strategies.append({
        'title': '📈 Genel Öneriler',
        'items': [
            'En iyi cohort\'ların özelliklerini analiz edin',
            'Churn riskli müşterileri erken tespit edin',
            'Aylık retention hedefleri belirleyin',
            'A/B testleri ile retention stratejilerini optimize edin'
        ]
    })
    
    for strategy in strategies:
        with st.expander(strategy['title']):
            for item in strategy['items']:
                st.write(f"• {item}")
    
    # 8. COHORT LTV (Lifetime Value) TAHMİNİ
    st.markdown("### 💰 Cohort Lifetime Value (LTV) Tahmini")
    
    cohort_ltv = cohort_revenue_pivot.sum(axis=1) / cohort_counts[0]
    
    # LTV tablosu
    ltv_data = []
    for cohort, ltv in cohort_ltv.items():
        ltv_data.append({'Cohort': str(cohort), 'LTV (TL)': f"{ltv:,.2f}"})
    
    ltv_df = pd.DataFrame(ltv_data)
    st.dataframe(ltv_df, width='stretch')
    
    avg_ltv = cohort_ltv.mean()
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%); padding: 20px; border-radius: 10px; margin: 1rem 0; text-align: center;'>
        <h3 style='color: white; margin: 0 0 10px 0;'>💰 Genel Ortalama LTV</h3>
        <h2 style='color: white; margin: 0; font-size: 2rem;'>{avg_ltv:,.2f} TL</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 9. VERI İNDİRME
    st.markdown("### 📥 Cohort Analizi Veri İndirme")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Retention oranları CSV
        retention_csv = cohort_retention.to_csv()
        st.download_button(
            label="📊 Retention Oranları CSV",
            data=retention_csv,
            file_name=f"cohort_retention_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Müşteri sayıları CSV
        counts_csv = cohort_counts.to_csv()
        st.download_button(
            label="👥 Müşteri Sayıları CSV",
            data=counts_csv,
            file_name=f"cohort_counts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        # Gelir analizi CSV
        revenue_csv = cohort_revenue_pivot.to_csv()
        st.download_button(
            label="💰 Gelir Analizi CSV",
            data=revenue_csv,
            file_name=f"cohort_revenue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Analiz özeti
    st.markdown("### ✅ Cohort Analizi Tamamlandı!")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Analiz Edilen Cohort", len(cohort_retention))
    with col2:
        st.metric("Takip Süresi (Ay)", len(cohort_retention.columns))
    with col3:
        st.metric("Toplam Müşteri", df_cohort['CustomerID'].nunique())
    with col4:
        st.metric("Toplam Gelir", f"{df_cohort['OrderValue'].sum():,.0f} TL")
    
    st.markdown("""</div>""", unsafe_allow_html=True)

# 8. CHURN PREDICTION ANALİZİ SEKMESİ
with menu[7]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>⚠️ Churn Prediction & Analizi</h1>
        <p style='color: white; margin: 0.5rem 0; font-size: 1.2rem; opacity: 0.9;'>Müşteri Kaybı Riskini Tahmin Etme ve Önleme Stratejileri</p>
        <p style='color: white; margin: 0; font-size: 0.9rem; opacity: 0.8;'>🤖 Machine Learning Powered</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;'>Müşteri kaybı riskini tahmin etme ve önleme stratejileri</p>", unsafe_allow_html=True)
    
    # Churn veri seti oluşturma
    st.markdown("### 🎯 Churn Verisi Oluşturma")
    
    with st.spinner("🤖 Churn prediction verisi oluşturuluyor..."):
        # 1. VERİ SETİ OLUŞTURMA
        np.random.seed(42)
        
        n_customers = 2000
        current_date = datetime(2024, 10, 1)
        
        data = []
        
        for i in range(n_customers):
            customer_id = f'C{str(i).zfill(5)}'
            
            # Müşteri profili belirleme
            if np.random.random() < 0.30:  # %30 churn olmuş müşteri
                is_churned = 1
                days_since_last = np.random.randint(90, 365)
                total_orders = np.random.randint(1, 8)
                avg_order_value = np.random.uniform(50, 300)
                total_spent = total_orders * avg_order_value
                customer_lifetime_days = np.random.randint(60, 400)
                complaints = np.random.randint(0, 4)
                support_tickets = np.random.randint(0, 5)
                discount_usage = np.random.randint(0, 3)
                email_open_rate = np.random.uniform(0, 0.4)
                last_nps_score = np.random.randint(1, 6)
            else:  # %70 aktif müşteri
                is_churned = 0
                days_since_last = np.random.randint(1, 89)
                total_orders = np.random.randint(3, 50)
                avg_order_value = np.random.uniform(100, 1000)
                total_spent = total_orders * avg_order_value
                customer_lifetime_days = np.random.randint(90, 800)
                complaints = np.random.randint(0, 2)
                support_tickets = np.random.randint(0, 3)
                discount_usage = np.random.randint(1, 8)
                email_open_rate = np.random.uniform(0.3, 0.9)
                last_nps_score = np.random.randint(6, 11)
            
            # Türkiye'ye özgü kategoriler
            product_categories = ['Elektronik', 'Giyim', 'Ev & Yaşam', 'Kitap', 'Spor', 'Kozmetik']
            preferred_category = np.random.choice(product_categories)
            
            payment_methods = ['Kredi Kartı', 'Havale', 'Kapıda Ödeme', 'Mobil Ödeme']
            preferred_payment = np.random.choice(payment_methods, p=[0.5, 0.2, 0.2, 0.1])
            
            cities = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Konya']
            city = np.random.choice(cities, p=[0.35, 0.15, 0.12, 0.1, 0.08, 0.1, 0.1])
            
            data.append({
                'CustomerID': customer_id,
                'DaysSinceLastOrder': days_since_last,
                'TotalOrders': total_orders,
                'AvgOrderValue': round(avg_order_value, 2),
                'TotalSpent': round(total_spent, 2),
                'CustomerLifetimeDays': customer_lifetime_days,
                'OrderFrequency': round(total_orders / (customer_lifetime_days / 30), 2),
                'Complaints': complaints,
                'SupportTickets': support_tickets,
                'DiscountUsage': discount_usage,
                'EmailOpenRate': round(email_open_rate, 2),
                'LastNPSScore': last_nps_score,
                'PreferredCategory': preferred_category,
                'PreferredPayment': preferred_payment,
                'City': city,
                'IsChurned': is_churned
            })
        
        df_churn = pd.DataFrame(data)
    
    st.success(f"✓ {len(df_churn)} müşteri verisi oluşturuldu")
    churn_rate = df_churn['IsChurned'].mean() * 100
    st.success(f"✓ Churn Oranı: {churn_rate:.1f}%")
    
    # Veri özeti
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam Müşteri", len(df_churn))
    with col2:
        st.metric("Aktif Müşteri", len(df_churn[df_churn['IsChurned']==0]))
    with col3:
        st.metric("Churn Olmuş", len(df_churn[df_churn['IsChurned']==1]))
    with col4:
        st.metric("Churn Oranı", f"{churn_rate:.1f}%")
    
    # Ham veri önizleme
    st.markdown("### 📋 Ham Veri Önizleme")
    st.dataframe(df_churn.head(10), width='stretch')
    
    with st.spinner("🤖 Machine Learning modeli eğitiliyor..."):
        # 2. MAKİNE ÖĞRENMESİ MODELİ
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
        from sklearn.preprocessing import StandardScaler
        
        # Kategorik değişkenleri encode et
        df_encoded = df_churn.copy()
        df_encoded['PreferredCategory_Encoded'] = pd.Categorical(df_churn['PreferredCategory']).codes
        df_encoded['PreferredPayment_Encoded'] = pd.Categorical(df_churn['PreferredPayment']).codes
        df_encoded['City_Encoded'] = pd.Categorical(df_churn['City']).codes
        
        # Feature seçimi
        numeric_features = ['DaysSinceLastOrder', 'TotalOrders', 'AvgOrderValue', 'TotalSpent',
                           'CustomerLifetimeDays', 'OrderFrequency', 'Complaints', 'SupportTickets',
                           'DiscountUsage', 'EmailOpenRate', 'LastNPSScore']
        
        features = numeric_features + ['PreferredCategory_Encoded', 'PreferredPayment_Encoded', 'City_Encoded']
        X = df_encoded[features]
        y = df_encoded['IsChurned']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
        
        # Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Random Forest Model
        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
        model.fit(X_train_scaled, y_train)
        
        # Tahminler
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Model performansı
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = (y_pred == y_test).mean()
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'Feature': features,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        # Tüm müşteriler için risk skoru
        X_all_scaled = scaler.transform(df_encoded[features])
        df_churn['ChurnRiskScore'] = model.predict_proba(X_all_scaled)[:, 1] * 100
        
        # Risk segmentleri
        df_churn['RiskSegment'] = pd.cut(df_churn['ChurnRiskScore'], 
                                        bins=[0, 25, 50, 75, 100],
                                        labels=['Düşük Risk', 'Orta Risk', 'Yüksek Risk', 'Kritik Risk'])
    
    st.success("✓ Model eğitimi tamamlandı")
    
    # Model performans metrikleri
    st.markdown("### 🤖 Model Performansı")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", f"{accuracy*100:.1f}%")
    with col2:
        st.metric("ROC-AUC Score", f"{roc_auc:.3f}")
    with col3:
        st.metric("En Önemli Faktör", feature_importance.iloc[0]['Feature'][:15] + "...")
    
    # 3. GÖRSELLEŞTİRMELER
    st.markdown("### 📈 Churn Prediction Dashboard")
    
    # Grafikleri oluştur
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Churn Dağılımı
    ax1 = plt.subplot(3, 3, 1)
    churn_dist = df_churn['IsChurned'].value_counts()
    colors_churn = ['#2ecc71', '#e74c3c']
    wedges, texts, autotexts = ax1.pie(churn_dist.values, labels=['Aktif', 'Churn'], 
                                         autopct='%1.1f%%', colors=colors_churn, startangle=90,
                                         explode=(0, 0.1))
    ax1.set_title('Churn Dağılımı', fontsize=14, fontweight='bold', pad=20)
    
    # 2. Risk Segment Dağılımı
    ax2 = plt.subplot(3, 3, 2)
    risk_counts = df_churn['RiskSegment'].value_counts().sort_index()
    colors_risk = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
    bars = ax2.bar(range(len(risk_counts)), risk_counts.values, color=colors_risk, edgecolor='black')
    ax2.set_xticks(range(len(risk_counts)))
    ax2.set_xticklabels(risk_counts.index, rotation=45, ha='right')
    ax2.set_ylabel('Müşteri Sayısı', fontsize=10)
    ax2.set_title('Risk Segment Dağılımı', fontsize=14, fontweight='bold', pad=20)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 3. Feature Importance
    ax3 = plt.subplot(3, 3, 3)
    top_features = feature_importance.head(8)
    bars = ax3.barh(range(len(top_features)), top_features['Importance'].values, 
                    color=plt.cm.viridis(np.linspace(0, 1, len(top_features))))
    ax3.set_yticks(range(len(top_features)))
    ax3.set_yticklabels(top_features['Feature'].values, fontsize=9)
    ax3.set_xlabel('Importance', fontsize=10)
    ax3.set_title('En Önemli Özellikler', fontsize=14, fontweight='bold', pad=20)
    ax3.invert_yaxis()
    
    # 4. Confusion Matrix
    ax4 = plt.subplot(3, 3, 4)
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax4, 
                xticklabels=['Aktif', 'Churn'], yticklabels=['Aktif', 'Churn'])
    ax4.set_ylabel('Gerçek', fontsize=10)
    ax4.set_xlabel('Tahmin', fontsize=10)
    ax4.set_title('Confusion Matrix', fontsize=14, fontweight='bold', pad=20)
    
    # 5. ROC Curve
    ax5 = plt.subplot(3, 3, 5)
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    ax5.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    ax5.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    ax5.set_xlim([0.0, 1.0])
    ax5.set_ylim([0.0, 1.05])
    ax5.set_xlabel('False Positive Rate', fontsize=10)
    ax5.set_ylabel('True Positive Rate', fontsize=10)
    ax5.set_title('ROC Curve', fontsize=14, fontweight='bold', pad=20)
    ax5.legend(loc="lower right")
    ax5.grid(True, alpha=0.3)
    
    # 6. Churn vs Aktif - Ortalama Metrikler
    ax6 = plt.subplot(3, 3, 6)
    comparison_metrics = ['TotalOrders', 'AvgOrderValue', 'EmailOpenRate', 'LastNPSScore']
    churn_means = df_churn[df_churn['IsChurned']==1][comparison_metrics].mean()
    active_means = df_churn[df_churn['IsChurned']==0][comparison_metrics].mean()
    
    x = np.arange(len(comparison_metrics))
    width = 0.35
    
    bars1 = ax6.bar(x - width/2, active_means.values, width, label='Aktif', color='#2ecc71', alpha=0.8)
    bars2 = ax6.bar(x + width/2, churn_means.values, width, label='Churn', color='#e74c3c', alpha=0.8)
    
    ax6.set_ylabel('Ortalama Değer', fontsize=10)
    ax6.set_title('Churn vs Aktif Müşteri Karşılaştırması', fontsize=14, fontweight='bold', pad=20)
    ax6.set_xticks(x)
    ax6.set_xticklabels(['Sipariş\nSayısı', 'Sipariş\nDeğeri', 'Email\nAçma', 'NPS\nSkoru'], fontsize=9)
    ax6.legend()
    
    # 7. Days Since Last Order Dağılımı
    ax7 = plt.subplot(3, 3, 7)
    ax7.hist(df_churn[df_churn['IsChurned']==0]['DaysSinceLastOrder'], bins=30, alpha=0.6, label='Aktif', color='#2ecc71', edgecolor='black')
    ax7.hist(df_churn[df_churn['IsChurned']==1]['DaysSinceLastOrder'], bins=30, alpha=0.6, label='Churn', color='#e74c3c', edgecolor='black')
    ax7.set_xlabel('Son Siparişten Bu Yana Geçen Gün', fontsize=10)
    ax7.set_ylabel('Müşteri Sayısı', fontsize=10)
    ax7.set_title('Son Sipariş Tarihi Dağılımı', fontsize=14, fontweight='bold', pad=20)
    ax7.legend()
    ax7.axvline(90, color='red', linestyle='--', linewidth=2)
    
    # 8. Churn Risk Score Dağılımı
    ax8 = plt.subplot(3, 3, 8)
    ax8.hist(df_churn['ChurnRiskScore'], bins=50, color='coral', edgecolor='black', alpha=0.7)
    ax8.set_xlabel('Churn Risk Skoru (%)', fontsize=10)
    ax8.set_ylabel('Müşteri Sayısı', fontsize=10)
    ax8.set_title('Churn Risk Skoru Dağılımı', fontsize=14, fontweight='bold', pad=20)
    ax8.axvline(df_churn['ChurnRiskScore'].mean(), color='red', linestyle='--', linewidth=2, 
               label=f'Ortalama: {df_churn["ChurnRiskScore"].mean():.1f}%')
    ax8.legend()
    
    # 9. Şehir Bazında Churn Oranı
    ax9 = plt.subplot(3, 3, 9)
    city_churn = df_churn.groupby('City')['IsChurned'].mean().sort_values(ascending=False) * 100
    bars = ax9.bar(range(len(city_churn)), city_churn.values, 
                   color=plt.cm.RdYlGn_r(city_churn.values / 100))
    ax9.set_xticks(range(len(city_churn)))
    ax9.set_xticklabels(city_churn.index, rotation=45, ha='right')
    ax9.set_ylabel('Churn Oranı (%)', fontsize=10)
    ax9.set_title('Şehir Bazında Churn Oranı', fontsize=14, fontweight='bold', pad=20)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax9.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    
    # Streamlit'te grafikleri göster
    st.pyplot(fig, use_container_width=True)
    
    # 4. YÜKSEK RİSKLİ MÜŞTERİLER
    st.markdown("### ⚠️ Yüksek Riskli Müşteriler (Top 20)")
    
    high_risk = df_churn[df_churn['ChurnRiskScore'] >= 75].sort_values('ChurnRiskScore', ascending=False).head(20)
    
    if len(high_risk) > 0:
        st.dataframe(high_risk[['CustomerID', 'ChurnRiskScore', 'DaysSinceLastOrder', 'TotalOrders', 
                               'TotalSpent', 'LastNPSScore', 'RiskSegment']].round(2), width='stretch')
        
        st.warning(f"⚠️ {len(high_risk)} müşteri kritik risk seviyesinde!")
    else:
        st.success("✅ Kritik risk seviyesinde müşteri bulunmuyor.")
    
    # 5. STRATEJİK ÖNERİLER
    st.markdown("### 💡 Risk Segmentine Göre Aksiyon Planı")
    
    # Risk segment özeti
    segment_summary = df_churn.groupby('RiskSegment').agg({
        'CustomerID': 'count',
        'TotalSpent': 'sum',
        'ChurnRiskScore': 'mean'
    }).round(2)
    segment_summary.columns = ['Müşteri Sayısı', 'Toplam Gelir (TL)', 'Ort. Risk Skoru (%)']
    
    st.dataframe(segment_summary, width='stretch')
    
    # Aksiyon planları
    strategies = [
        {
            'segment': '🟢 DÜŞÜK RİSK (0-25%)',
            'actions': [
                'Otomatik teşekkür emailleri',
                'Referans programı davetleri',
                'Yeni ürün lansmanları hakkında bilgilendirme'
            ]
        },
        {
            'segment': '🟡 ORTA RİSK (25-50%)',
            'actions': [
                'Kişiselleştirilmiş ürün önerileri',
                'Özel indirim kuponları (%10-15)',
                'Engagement artırma kampanyaları'
            ]
        },
        {
            'segment': '🟠 YÜKSEK RİSK (50-75%)',
            'actions': [
                'Acil müdahale ekibi ataması',
                'Özel indirimler (%20-30)',
                'Telefon ile müşteri memnuniyeti görüşmesi',
                'Ücretsiz kargo avantajı'
            ]
        },
        {
            'segment': '🔴 KRİTİK RİSK (75-100%)',
            'actions': [
                'VIP müşteri temsilcisi ataması',
                'Agresif geri kazanma kampanyası',
                'Özel hediye veya bonuslar',
                'Bireysel sorun çözme görüşmesi'
            ]
        }
    ]
    
    for strategy in strategies:
        with st.expander(strategy['segment']):
            for action in strategy['actions']:
                st.write(f"• {action}")
    
    # 6. ÖNEMLİ BULGULAR
    st.markdown("### 📊 Önemli Bulgular")
    
    findings = [
        f"**En kritik faktör:** {feature_importance.iloc[0]['Feature']}",
        f"**90+ gün sipariş vermeyen:** {len(df_churn[df_churn['DaysSinceLastOrder'] >= 90])} müşteri",
        f"**Düşük NPS skoru (<6):** {len(df_churn[df_churn['LastNPSScore'] < 6])} müşteri",
        f"**Yüksek şikayet (>2):** {len(df_churn[df_churn['Complaints'] > 2])} müşteri",
        f"**En yüksek churn şehri:** {city_churn.index[0]} ({city_churn.iloc[0]:.1f}%)"
    ]
    
    for finding in findings:
        st.write(f"• {finding}")
    
    # 7. VERI İNDİRME
    st.markdown("### 📥 Churn Prediction Veri İndirme")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Tüm müşteri risk skorları
        risk_data = df_churn[['CustomerID', 'ChurnRiskScore', 'RiskSegment', 'DaysSinceLastOrder', 
                             'TotalOrders', 'TotalSpent', 'LastNPSScore', 'EmailOpenRate', 
                             'Complaints', 'City', 'IsChurned']]
        risk_csv = risk_data.to_csv(index=False)
        st.download_button(
            label="📊 Müşteri Risk Skorları CSV",
            data=risk_csv,
            file_name=f"churn_risk_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Yüksek riskli müşteriler
        if len(high_risk) > 0:
            high_risk_csv = high_risk.to_csv(index=False)
            st.download_button(
                label="⚠️ Yüksek Riskli Müşteriler CSV",
                data=high_risk_csv,
                file_name=f"high_risk_customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Yüksek riskli müşteri yok")
    
    with col3:
        # Feature importance
        importance_csv = feature_importance.to_csv(index=False)
        st.download_button(
            label="🎯 Feature Importance CSV",
            data=importance_csv,
            file_name=f"feature_importance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Analiz özeti
    st.markdown("### ✅ Churn Prediction Analizi Tamamlandı!")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Analiz Edilen Müşteri", len(df_churn))
    with col2:
        st.metric("Model Accuracy", f"{accuracy*100:.1f}%")
    with col3:
        st.metric("ROC-AUC Score", f"{roc_auc:.3f}")
    with col4:
        high_risk_count = len(df_churn[df_churn['ChurnRiskScore'] >= 75])
        st.metric("Kritik Risk Müşteri", high_risk_count)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
