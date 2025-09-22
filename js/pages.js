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

// Portfolyo geçiş sayfası içeriği
function portfolioPage() {
    return `
    <div class="container">
        <h1>Portfolyo Yükleniyor</h1>
        <h2>Veri bilimi uygulaması hazırlanıyor</h2>
        
        <div class="status-card">
            <p>Streamlit uygulaması yeni pencerede açılacak. Lütfen tarayıcınızın açılır pencere izinlerini kontrol edin.</p>
            <div class="progress-container">
                <div class="progress-bar" id="progress-bar"></div>
            </div>
        </div>
        
        <p>Tarayıcı ayarlarınıza bağlı olarak, pencere açılmazsa aşağıdaki butonu kullanabilirsiniz.</p>
        
        <div class="button-container">
            <a href="https://tolunayozcan.streamlit.app/" class="button primary-button" id="portfolyo-btn" target="_blank">Uygulamayı Aç</a>
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