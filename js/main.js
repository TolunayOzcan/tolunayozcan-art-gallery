/**
 * Tolunay Özcan Portfolyo Uygulaması
 * Main JavaScript dosyası
 */

// DOM içeriği yüklendiğinde çalışacak
document.addEventListener('DOMContentLoaded', () => {
    // Sayfa yüklendiğinde yumuşak bir görünüm efekti
    fadeInContent();
    
    // Yönlendirme butonlarını ayarla
    setupNavigation();
    
    // Portfolyo sayfasında otomatik yönlendirmeyi ayarla
    setupAutomaticRedirect();
});

/**
 * Sayfa içeriğini yumuşak bir şekilde gösterme
 */
function fadeInContent() {
    const container = document.querySelector('.container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        container.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 200);
    }
}

/**
 * Sayfa navigasyonunu ayarla
 */
function setupNavigation() {
    const buttons = document.querySelectorAll('.button');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transition = 'all 0.3s ease';
        });
    });
}

/**
 * Portfolyo sayfasında ilerleme çubuğu ve otomatik yönlendirme
 */
function setupAutomaticRedirect() {
    const progressBar = document.getElementById('progress-bar');
    const portfolyoBtn = document.getElementById('portfolyo-btn');
    
    if (progressBar && portfolyoBtn) {
        // İlerleme çubuğu animasyonu
        setTimeout(() => {
            progressBar.style.width = '100%';
        }, 200);
        
        // 2 saniye sonra portfolyo butonuna tıkla
        setTimeout(() => {
            portfolyoBtn.click();
        }, 2000);
    }
}

/**
 * SPA (Single Page Application) Router
 * Sayfalar arası geçişleri yönetir
 */
class Router {
    constructor() {
        this.routes = {};
        this.currentPage = null;
        
        // Popstate olay dinleyicisi ekle (tarayıcı geri/ileri butonları için)
        window.addEventListener('popstate', (e) => this.navigate(window.location.pathname));
    }
    
    // Rota ekle
    addRoute(path, pageFunction) {
        this.routes[path] = pageFunction;
    }
    
    // Sayfayı değiştir
    navigate(path, pushState = true) {
        // Eğer rota tanımlıysa içeriği güncelle
        if (this.routes[path]) {
            if (pushState) {
                window.history.pushState({}, "", path);
            }
            
            this.currentPage = path;
            const pageContent = this.routes[path]();
            
            const appElement = document.getElementById('app');
            if (appElement) {
                appElement.innerHTML = pageContent;
                fadeInContent();
            }
        } else {
            console.error(`Route not found: ${path}`);
        }
    }
    
    // Mevcut URL'ye göre sayfayı yükle
    loadCurrentPage() {
        this.navigate(window.location.pathname, false);
    }
}

// Router'ı global olarak kullanılabilir yap
window.appRouter = new Router();