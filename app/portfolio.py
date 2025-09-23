import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.graph_objects as go
import sys
import numpy as np
import threading
import time
from datetime import datetime

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
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;700;800;900&family=Exo+2:wght@300;400;500;600;700;800;900&display=swap">
    """, unsafe_allow_html=True)

# CSS'i yükle
load_css("app/style.css")
local_css()

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
        st.dataframe(org_data, use_container_width=True)
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🏢 Organizasyon Şeması")
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("� İnteraktif organizasyon ağı başarıyla yüklendi!")
        st.info("💡 Düğümlere tıklayarak detayları görebilirsiniz")
        
    except Exception as e:
        st.error(f"Organizasyon ağı hatası: {str(e)}")
        st.info("� Veri yeniden işleniyor...")

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
        st.dataframe(skill_data, use_container_width=True)
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🎯 Beceri-Çalışan İlişki Ağı")
        st.plotly_chart(fig, use_container_width=True)
        
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
        st.dataframe(project_data, use_container_width=True)
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🚀 Proje-Teknoloji Bağlantı Ağı")
        st.plotly_chart(fig, use_container_width=True)
        
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
        st.dataframe(dept_data, use_container_width=True)
        
        # En yoğun işbirliği
        max_collab = dept_data.loc[dept_data['İşbirliği Seviyesi'].idxmax()]
        st.metric(
            "En Yoğun İşbirliği", 
            f"{max_collab['Departman 1']} ↔️ {max_collab['Departman 2']}",
            f"Seviye: {max_collab['İşbirliği Seviyesi']}"
        )
        
        # İnteraktif Plotly grafiği
        fig = create_networkx_plotly_graph(G, "🏢 Departman İşbirliği Ağı")
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("🌐 Departman ağı aktif!")
        
    except Exception as e:
        st.error(f"Departman ağı hatası: {str(e)}")
        st.info("🔄 Sistem yeniden bağlanıyor...")

# Sol menü - Profil fotoğrafı ve kompakt tasarım
with st.sidebar:
    # Profil avatarı (TÖ yazılı)
    st.markdown("""
    <div style="text-align:center; padding: 0.6rem 0;">
        <div style="width: 80px; height: 80px; margin: 0 auto 0.8rem auto; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #8B5CF6); padding: 3px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); display: flex; align-items: center; justify-content: center;">
            <div style="width: 100%; height: 100%; border-radius: 50%; background: linear-gradient(135deg, #1E40AF, #7C3AED); display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: bold; font-family: 'Trebuchet MS', sans-serif;">
                TÖ
            </div>
        </div>
        <h2 style="margin: 0; font-size: 0.95rem; font-family: 'Trebuchet MS', sans-serif; line-height: 1.2;">Tolunay ÖZCAN</h2>
        <p style="color:#757575; margin: 0.1rem 0; font-size: 0.75rem; font-family: 'Trebuchet MS', sans-serif;">Data Analyst</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kompakt iletişim bölümü
    st.markdown("""
    <div style="text-align:center; padding: 0.3rem 0;">
        <a href="https://www.linkedin.com/in/tolunayozcan/" target="_blank" style="text-decoration:none; margin: 0 6px;">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" title="LinkedIn">
        </a>
        <a href="https://github.com/TolunayOzcan" target="_blank" style="text-decoration:none; margin: 0 6px;">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20" title="GitHub">
        </a>
        <a href="mailto:tolunayozcan95@gmail.com" style="text-decoration:none; margin: 0 6px;">
            <img src="https://cdn-icons-png.flaticon.com/512/561/561127.png" width="20" title="E-posta">
        </a>
    </div>
    """, unsafe_allow_html=True)

# Büyük ve animasyonlu tab bar tasarımı - En üstte ortalanmış
st.markdown("""
<style>
    /* Tab bar büyük ve animasyonlu tasarım - Ortalanmış */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(30, 41, 59, 0.4);
        border-radius: 20px;
        padding: 8px;
        margin: 0 auto 1.5rem auto;
        box-shadow: 
            0 4px 20px rgba(59, 130, 246, 0.15),
            0 0 0 1px rgba(139, 92, 246, 0.3),
            0 0 10px rgba(139, 92, 246, 0.2),
            inset 0 0 0 1px rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(139, 92, 246, 0.4);
        display: flex;
        justify-content: center;
        width: fit-content;
        max-width: 100%;
        position: relative;
        animation: neonGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes neonGlow {
        0% {
            box-shadow: 
                0 4px 20px rgba(59, 130, 246, 0.15),
                0 0 0 1px rgba(139, 92, 246, 0.3),
                0 0 10px rgba(139, 92, 246, 0.2),
                inset 0 0 0 1px rgba(139, 92, 246, 0.1);
        }
        100% {
            box-shadow: 
                0 4px 20px rgba(59, 130, 246, 0.25),
                0 0 0 1px rgba(139, 92, 246, 0.5),
                0 0 20px rgba(139, 92, 246, 0.4),
                0 0 40px rgba(139, 92, 246, 0.1),
                inset 0 0 0 1px rgba(139, 92, 246, 0.2);
        }
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: 600;
        font-family: 'Trebuchet MS', sans-serif;
        background: transparent;
        border: none;
        color: #94A3B8;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .stTabs [data-baseweb="tab"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.6s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px) scale(1.05);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.15);
        color: #E2E8F0;
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.2);
    }
    .stTabs [data-baseweb="tab"]:hover:before {
        left: 100%;
    }
    .stTabs [aria-selected="true"]:before {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        0% { left: -100%; }
        50% { left: 100%; }
        100% { left: 100%; }
    }
    
    /* Tab container'ı ortala */
    .stTabs {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Büyük tab menüsü - En üstte
menu = st.tabs(["👤 Hakkımda", "� Analytics", "�🔄 Api entegrasyon", "🧪 Data science", "👥 HR analytics"])




with menu[0]:
    st.markdown("""<div class="card">""", unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #8B5CF6 !important; font-weight: bold !important; font-family: 'Trebuchet MS', sans-serif !important; text-shadow: none !important; background: none !important;">Hakkımda</h2>
    <p>Veri analizi ve görselleştirme alanında 4+ yıllık deneyime sahip Kıdemli Veri Analistiyim. SQL, Python ve VBA 
    konularında uzman seviyede bilgi sahibi. CRM veri analizi, İK analitik çözümleri, çağrı merkezi ve operasyonel 
    raporlama konularında kapsamlı deneyim. Veri odaklı karar alma süreçlerini destekleyen analitik çözümler 
    geliştirme konusunda uzman.</p>
    
    <p><strong>Uzmanlık Alanlarım:</strong></p>
    <ul>
        <li>SQL ve veritabanı yönetimi</li>
        <li>Python ile veri analizi ve görselleştirme</li>
        <li>VBA ile otomasyon çözümleri</li>
        <li>CRM ve İK veri analizleri</li>
        <li>Operasyonel raporlama ve dashboard geliştirme</li>
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
            margin=dict(t=50, b=50, l=40, r=40),
        )
        fig2 = make_transparent_bg(fig2)
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
            margin=dict(t=50, b=50, l=40, r=40),
            height=500,
        )
        sankey_fig = make_transparent_bg(sankey_fig)
        
        st.plotly_chart(sankey_fig, use_container_width=True)
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
                st.dataframe(crypto_df, use_container_width=True)
                
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
                    
                    st.plotly_chart(fig, use_container_width=True)
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
                    st.dataframe(exchange_df, use_container_width=True)
                    
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
                    
                    st.plotly_chart(fig, use_container_width=True)
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
                    st.dataframe(stock_df, use_container_width=True)
                    
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
                    
                    st.plotly_chart(fig, use_container_width=True)
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
            st.dataframe(ekonomi_df, use_container_width=True)
        
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
            st.dataframe(crypto_df, use_container_width=True)
            
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
                
                st.plotly_chart(fig, use_container_width=True)
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
                st.dataframe(exchange_df, use_container_width=True)
                
                # Döviz kurları grafiği
                fig = px.bar(exchange_df, x='Döviz Çifti', y='Kur',
                            title='USD Bazında Döviz Kurları',
                            text='Kur')
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(tickangle=45),
                    margin=dict(t=50, b=80, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""<div class="card">""", unsafe_allow_html=True)
            st.markdown("<h3>📈 Hisse Senedi Verileri</h3>", unsafe_allow_html=True)
            st.markdown("<p><strong>Demo hisse senedi verileri</strong></p>", unsafe_allow_html=True)
            
            stock_df = api_service.get_stock_data()
            
            if not stock_df.empty:
                st.dataframe(stock_df, use_container_width=True)
                
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
                
                st.plotly_chart(fig, use_container_width=True)
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
        fig_reasons.update_layout(
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
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
        yaxis_title='Aylık Maaş (TL)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
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

# D3Graph Tab (menu[5])
with menu[4]:
    create_d3graph_visualizations()