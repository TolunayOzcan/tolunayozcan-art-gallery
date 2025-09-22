/**
 * Tolunay Özcan Portfolyo Uygulaması
 * SPA (Single Page Application) Sayfaları
 */

// Ana Sayfa içeriği
function homePage() {
    return `
    <div class="container">
        <div class="accent-shape"></div>
        <div class="content">
            <header>
                <h1>Tolunay Özcan</h1>
                <h2>Veri Bilimi Portfolyosu</h2>
            </header>
            
            <p>Veri görselleştirme, ileri analitik ve makine öğrenimi üzerine yaptığım çalışmalarımı içeren interaktif portfolyoma hoş geldiniz. Verinin bilgiyi, bilginin ise değeri nasıl şekillendirdiğini keşfedin.</p>
            
            <div class="button-container">
                <a href="#" class="button primary-button" onclick="window.appRouter.navigate('/portfolio'); return false;">Portfolyoyu Görüntüle</a>
                <a href="https://github.com/TolunayOzcan/tolunayozcan-art-gallery" class="button secondary-button">GitHub Repo</a>
            </div>
            
            <div class="footer">
                <div>© 2025 Tolunay Özcan</div>
                <div>Veri Bilimci & Analist</div>
            </div>
        </div>
    </div>
    `;
}

// Portfolyo ana sayfası içeriği
function portfolioPage() {
    return `
    <div class="container portfolio-container">
        <div class="portfolio-header">
            <h1>Veri Bilimi Portfolyosu</h1>
            <h2>Interaktif Veri Analizleri ve Görselleştirmeler</h2>
        </div>
        
        <div class="tabs">
            <button class="tab-button active" data-tab="hr">HR Analitiği</button>
            <button class="tab-button" data-tab="ml">Makine Öğrenmesi</button>
            <button class="tab-button" data-tab="economy">Ekonomik Veriler</button>
        </div>
        
        <div class="tab-content">
            <div class="tab-pane active" id="hr-dashboard">
                <!-- HR Analitiği içeriği JavaScript ile eklenecek -->
            </div>
            
            <div class="tab-pane" id="ml-dashboard" style="display: none;">
                <!-- Makine Öğrenmesi içeriği JavaScript ile eklenecek -->
            </div>
            
            <div class="tab-pane" id="economy-dashboard" style="display: none;">
                <div class="coming-soon">
                    <h3>Yakında Eklenecek</h3>
                    <p>Ekonomik veri analizleri ve grafikleri yakında burada olacak.</p>
                </div>
            </div>
        </div>
        
        <div class="button-container">
            <a href="#" class="button secondary-button" onclick="window.appRouter.navigate('/'); return false;">Ana Sayfaya Dön</a>
        </div>
    </div>
    `;
}

// Hata sayfası içeriği (404)
function notFoundPage() {
    return `
    <div class="container">
        <h1>Sayfa Bulunamadı</h1>
        <h2>Aradığınız sayfa mevcut değil</h2>
        
        <div class="status-card">
            <p>Aradığınız sayfa taşınmış veya kaldırılmış olabilir.</p>
        </div>
        
        <div class="button-container">
            <a href="#" class="button primary-button" onclick="window.appRouter.navigate('/'); return false;">Ana Sayfaya Dön</a>
        </div>
    </div>
    `;
}