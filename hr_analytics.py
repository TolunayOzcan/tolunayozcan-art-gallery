import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_employee_data(n_employees=200):
    """Çalışan verilerini simüle eder ve bir DataFrame döndürür."""
    np.random.seed(42)
    
    # Departmanlar ve pozisyonlar
    departments = ['İnsan Kaynakları', 'Pazarlama', 'Satış', 'Finans', 'Bilgi Teknolojileri', 'Operasyon']
    positions = {
        'İnsan Kaynakları': ['İK Uzmanı', 'İK Yöneticisi', 'İK Direktörü', 'İK Asistanı'],
        'Pazarlama': ['Pazarlama Uzmanı', 'Marka Yöneticisi', 'Pazarlama Direktörü', 'Pazarlama Asistanı', 'Dijital Pazarlama Uzmanı'],
        'Satış': ['Satış Temsilcisi', 'Satış Yöneticisi', 'Satış Direktörü', 'Müşteri Temsilcisi'],
        'Finans': ['Muhasebe Uzmanı', 'Finans Yöneticisi', 'Finans Direktörü', 'Mali Analist'],
        'Bilgi Teknolojileri': ['Yazılım Geliştirici', 'IT Yöneticisi', 'Sistem Uzmanı', 'Veri Analisti', 'IT Destek Uzmanı'],
        'Operasyon': ['Operasyon Uzmanı', 'Operasyon Yöneticisi', 'Lojistik Uzmanı', 'Saha Yöneticisi']
    }
    
    # Temel bilgiler için veri oluşturma
    employee_ids = [f"EMP{i:04d}" for i in range(1, n_employees + 1)]
    departments_list = np.random.choice(departments, size=n_employees, p=[0.1, 0.2, 0.25, 0.15, 0.2, 0.1])
    
    # Pozisyonları departmanlara göre atama
    positions_list = [np.random.choice(positions[dept]) for dept in departments_list]
    
    # Demografik veriler
    genders = np.random.choice(['Erkek', 'Kadın'], size=n_employees, p=[0.55, 0.45])
    ages = np.random.normal(35, 8, n_employees).astype(int)
    ages = np.clip(ages, 22, 65)  # Yaş sınırlaması
    
    # Deneyim ve şirketteki süre (yıl)
    tenure_years = np.random.gamma(shape=2.0, scale=2.5, size=n_employees)
    tenure_years = np.clip(tenure_years, 0.1, 20).round(1)  # 0.1 ile 20 yıl arası
    
    experience_years = tenure_years + np.random.gamma(shape=3.0, scale=2.0, size=n_employees)
    experience_years = np.clip(experience_years, tenure_years, 40).round(1)  # En az şirketteki süre kadar, en fazla 40 yıl
    
    # İşe giriş tarihleri
    today = datetime.now()
    hire_dates = [(today - timedelta(days=int(365 * years))) for years in tenure_years]
    hire_dates = [date.strftime('%Y-%m-%d') for date in hire_dates]
    
    # Eğitim durumu
    education_levels = np.random.choice(
        ['Lise', 'Önlisans', 'Lisans', 'Yüksek Lisans', 'Doktora'], 
        size=n_employees, 
        p=[0.1, 0.15, 0.5, 0.2, 0.05]
    )
    
    # Maaş ve performans bilgileri
    base_salaries = {
        'İK Uzmanı': 12000, 'İK Yöneticisi': 18000, 'İK Direktörü': 35000, 'İK Asistanı': 9000,
        'Pazarlama Uzmanı': 13000, 'Marka Yöneticisi': 19000, 'Pazarlama Direktörü': 32000, 'Pazarlama Asistanı': 8500, 'Dijital Pazarlama Uzmanı': 15000,
        'Satış Temsilcisi': 10000, 'Satış Yöneticisi': 20000, 'Satış Direktörü': 35000, 'Müşteri Temsilcisi': 9000,
        'Muhasebe Uzmanı': 14000, 'Finans Yöneticisi': 22000, 'Finans Direktörü': 38000, 'Mali Analist': 16000,
        'Yazılım Geliştirici': 18000, 'IT Yöneticisi': 25000, 'Sistem Uzmanı': 16000, 'Veri Analisti': 17000, 'IT Destek Uzmanı': 12000,
        'Operasyon Uzmanı': 11000, 'Operasyon Yöneticisi': 18000, 'Lojistik Uzmanı': 12000, 'Saha Yöneticisi': 14000
    }
    
    # Pozisyon baz maaşı + deneyim faktörü + rastgele varyasyon
    salaries = [
        base_salaries[pos] * (1 + exp * 0.03) * np.random.uniform(0.9, 1.1)
        for pos, exp in zip(positions_list, experience_years)
    ]
    salaries = [round(s, -2) for s in salaries]  # En yakın yüzlüğe yuvarlama
    
    # Performans puanları (1-5 arası)
    performance_scores = np.clip(np.random.normal(3.5, 0.8, n_employees), 1, 5).round(1)
    
    # Terfi sayısı
    promotion_counts = np.random.poisson(lam=tenure_years/3)
    promotion_counts = np.clip(promotion_counts, 0, 5)  # En fazla 5 terfi
    
    # İşten ayrılma durumu ve nedeni
    attrition_rate = 0.15  # %15 işten ayrılma oranı
    attrition = np.random.choice([True, False], size=n_employees, p=[attrition_rate, 1-attrition_rate])
    
    attrition_reasons = [
        np.random.choice(
            ['Daha İyi Teklif', 'İş/Yaşam Dengesi', 'Kariyer İlerlemesi', 'Yönetici ile Uyuşmazlık', 'Taşınma', 'Emeklilik', 'Diğer'],
            p=[0.3, 0.15, 0.25, 0.1, 0.1, 0.05, 0.05]
        ) if attr else 'Aktif Çalışan'
        for attr in attrition
    ]
    
    # Tatmin ve bağlılık skorları (1-10 arası)
    satisfaction_scores = np.clip(np.random.normal(7, 1.5, n_employees), 1, 10).round(1)
    
    # Fazla mesai
    overtime = np.random.choice([True, False], size=n_employees, p=[0.3, 0.7])
    
    # DataFrame oluşturma
    employee_data = pd.DataFrame({
        'çalışan_id': employee_ids,
        'departman': departments_list,
        'pozisyon': positions_list,
        'cinsiyet': genders,
        'yaş': ages,
        'eğitim': education_levels,
        'şirket_deneyimi_yıl': tenure_years,
        'toplam_deneyim_yıl': experience_years,
        'işe_giriş_tarihi': hire_dates,
        'aylık_maaş': salaries,
        'performans_puanı': performance_scores,
        'terfi_sayısı': promotion_counts,
        'işten_ayrılma': attrition,
        'ayrılma_nedeni': attrition_reasons,
        'tatmin_skoru': satisfaction_scores,
        'fazla_mesai': overtime
    })
    
    return employee_data

def create_attrition_department_chart(df):
    """Departmanlara göre işten ayrılma oranlarını gösteren grafik."""
    dept_attrition = df.groupby('departman')['işten_ayrılma'].mean().reset_index()
    dept_attrition['işten_ayrılma'] = dept_attrition['işten_ayrılma'] * 100  # Yüzde olarak
    
    fig = px.bar(
        dept_attrition.sort_values('işten_ayrılma', ascending=False),
        x='departman',
        y='işten_ayrılma',
        title='Departmanlara Göre İşten Ayrılma Oranları (%)',
        labels={'departman': 'Departman', 'işten_ayrılma': 'İşten Ayrılma Oranı (%)'},
        text_auto='.1f',
        color='işten_ayrılma',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig

def create_salary_distribution_chart(df):
    """Departmanlara göre maaş dağılımını gösteren grafik."""
    fig = px.box(
        df,
        x='departman',
        y='aylık_maaş',
        title='Departmanlara Göre Maaş Dağılımı',
        labels={'departman': 'Departman', 'aylık_maaş': 'Aylık Maaş (TL)'},
        color='departman',
        points='all'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=False
    )
    
    return fig

def create_performance_distribution_chart(df):
    """Performans puanlarının dağılımını gösteren grafik."""
    performance_dist = df['performans_puanı'].value_counts().reset_index()
    performance_dist.columns = ['performans_puanı', 'çalışan_sayısı']
    
    fig = px.bar(
        performance_dist.sort_values('performans_puanı'),
        x='performans_puanı',
        y='çalışan_sayısı',
        title='Performans Puanlarının Dağılımı',
        labels={'performans_puanı': 'Performans Puanı', 'çalışan_sayısı': 'Çalışan Sayısı'},
        text_auto=True,
        color='performans_puanı',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig

def create_hiring_trends_chart(df):
    """Yıllara göre işe alım trendlerini gösteren grafik."""
    df['işe_alım_yılı'] = pd.to_datetime(df['işe_giriş_tarihi']).dt.year
    hiring_trends = df['işe_alım_yılı'].value_counts().reset_index()
    hiring_trends.columns = ['yıl', 'işe_alım_sayısı']
    
    fig = px.line(
        hiring_trends.sort_values('yıl'),
        x='yıl',
        y='işe_alım_sayısı',
        title='Yıllara Göre İşe Alım Trendleri',
        labels={'yıl': 'Yıl', 'işe_alım_sayısı': 'İşe Alım Sayısı'},
        markers=True,
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        xaxis=dict(
            tickmode='linear',
            tick0=hiring_trends['yıl'].min(),
            dtick=1
        )
    )
    
    return fig

def create_department_demographics_chart(df):
    """Departman ve cinsiyete göre çalışan dağılımını gösteren grafik."""
    dept_gender = df.groupby(['departman', 'cinsiyet']).size().reset_index(name='çalışan_sayısı')
    
    fig = px.bar(
        dept_gender,
        x='departman',
        y='çalışan_sayısı',
        color='cinsiyet',
        title='Departman ve Cinsiyete Göre Çalışan Dağılımı',
        labels={'departman': 'Departman', 'çalışan_sayısı': 'Çalışan Sayısı', 'cinsiyet': 'Cinsiyet'},
        text_auto=True,
        barmode='group',
        color_discrete_map={'Erkek': '#2C74B3', 'Kadın': '#E6A4B4'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_satisfaction_vs_attrition_chart(df):
    """Tatmin skoru ve işten ayrılma arasındaki ilişkiyi gösteren grafik."""
    satisfaction_attrition = df.groupby('tatmin_skoru')['işten_ayrılma'].mean().reset_index()
    satisfaction_attrition['işten_ayrılma'] = satisfaction_attrition['işten_ayrılma'] * 100  # Yüzde olarak
    
    fig = px.line(
        satisfaction_attrition.sort_values('tatmin_skoru'),
        x='tatmin_skoru',
        y='işten_ayrılma',
        title='Tatmin Skoru ve İşten Ayrılma İlişkisi',
        labels={'tatmin_skoru': 'Tatmin Skoru', 'işten_ayrılma': 'İşten Ayrılma Oranı (%)'},
        markers=True,
    )
    
    # Regresyon çizgisi ekle
    fig.add_trace(
        go.Scatter(
            x=[satisfaction_attrition['tatmin_skoru'].min(), satisfaction_attrition['tatmin_skoru'].max()],
            y=[satisfaction_attrition['işten_ayrılma'].max(), satisfaction_attrition['işten_ayrılma'].min()],
            mode='lines',
            line=dict(dash='dash', color='red'),
            name='Trend Çizgisi'
        )
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig