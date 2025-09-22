/**
 * Tolunay Özcan Portfolyo Uygulaması
 * Veri görselleştirme modülü
 */

/**
 * Demo veriler - Gerçek uygulamada bu veriler bir API'den çekilebilir
 */
const demoData = {
    // HR Analitiği için örnek veriler
    hrData: {
        employeeCount: 452,
        departmentDistribution: [
            { department: 'Mühendislik', count: 120 },
            { department: 'Pazarlama', count: 85 },
            { department: 'Satış', count: 95 },
            { department: 'İnsan Kaynakları', count: 32 },
            { department: 'Finans', count: 45 },
            { department: 'Müşteri Hizmetleri', count: 75 }
        ],
        turnoverRate: [
            { year: 2020, rate: 12.5 },
            { year: 2021, rate: 10.2 },
            { year: 2022, rate: 8.7 },
            { year: 2023, rate: 7.9 },
            { year: 2024, rate: 7.2 },
            { year: 2025, rate: 6.8 }
        ],
        salaryRanges: {
            'Mühendislik': { min: 15000, avg: 22500, max: 35000 },
            'Pazarlama': { min: 12000, avg: 18000, max: 28000 },
            'Satış': { min: 10000, avg: 17500, max: 30000 },
            'İnsan Kaynakları': { min: 11000, avg: 16000, max: 25000 },
            'Finans': { min: 14000, avg: 20000, max: 32000 },
            'Müşteri Hizmetleri': { min: 9000, avg: 13500, max: 20000 }
        }
    },
    
    // Canlı ekonomik veriler - Normalde API'den çekilecek
    economyData: {
        inflation: [
            { month: 'Ocak', rate: 5.2 },
            { month: 'Şubat', rate: 5.4 },
            { month: 'Mart', rate: 5.3 },
            { month: 'Nisan', rate: 5.5 },
            { month: 'Mayıs', rate: 5.7 },
            { month: 'Haziran', rate: 5.8 }
        ],
        exchangeRates: {
            'USD/TRY': 32.54,
            'EUR/TRY': 35.22,
            'GBP/TRY': 41.86
        },
        stockMarket: [
            { name: 'BIST100', value: 9785.25, change: 1.2 },
            { name: 'BIST30', value: 12045.36, change: 0.8 },
            { name: 'BIST Bankacılık', value: 5632.18, change: -0.5 }
        ]
    },
    
    // ML Model performans verileri
    mlPerformance: {
        models: [
            { name: 'Random Forest', accuracy: 0.89, precision: 0.87, recall: 0.90, f1: 0.88 },
            { name: 'Gradient Boost', accuracy: 0.91, precision: 0.92, recall: 0.89, f1: 0.90 },
            { name: 'Neural Network', accuracy: 0.86, precision: 0.84, recall: 0.88, f1: 0.86 },
            { name: 'SVM', accuracy: 0.83, precision: 0.81, recall: 0.85, f1: 0.83 },
            { name: 'Logistic Regression', accuracy: 0.79, precision: 0.77, recall: 0.82, f1: 0.79 }
        ],
        featureImportance: [
            { feature: 'Yaş', importance: 0.23 },
            { feature: 'Gelir', importance: 0.18 },
            { feature: 'Eğitim Seviyesi', importance: 0.15 },
            { feature: 'Meslek', importance: 0.12 },
            { feature: 'İkamet Süresi', importance: 0.09 },
            { feature: 'Kredi Skoru', importance: 0.14 },
            { feature: 'Mevcut Borç', importance: 0.09 }
        ]
    }
};

/**
 * HR Analytics Dashboard içeriğini oluşturur
 */
function createHRDashboard(elementId) {
    const container = document.getElementById(elementId);
    
    if (!container) {
        console.error(`Element ID ${elementId} bulunamadı`);
        return;
    }
    
    // Dashboard içeriği
    const dashboard = document.createElement('div');
    dashboard.className = 'dashboard';
    
    // Toplam çalışan sayısı kartı
    const employeeCard = document.createElement('div');
    employeeCard.className = 'dashboard-card';
    employeeCard.innerHTML = `
        <h3>Toplam Çalışan</h3>
        <div class="card-value">${demoData.hrData.employeeCount}</div>
    `;
    
    // Departman dağılımı kartı
    const deptCard = document.createElement('div');
    deptCard.className = 'dashboard-card';
    deptCard.innerHTML = `
        <h3>Departman Dağılımı</h3>
        <div id="dept-chart" class="chart-container"></div>
    `;
    
    // İşten ayrılma oranı kartı
    const turnoverCard = document.createElement('div');
    turnoverCard.className = 'dashboard-card wide-card';
    turnoverCard.innerHTML = `
        <h3>İşten Ayrılma Oranı (Yıllık)</h3>
        <div id="turnover-chart" class="chart-container"></div>
    `;
    
    // Maaş aralıkları kartı
    const salaryCard = document.createElement('div');
    salaryCard.className = 'dashboard-card wide-card';
    salaryCard.innerHTML = `
        <h3>Departman Bazlı Maaş Aralıkları</h3>
        <div id="salary-chart" class="chart-container"></div>
    `;
    
    // Dashboard'a kartları ekle
    dashboard.appendChild(employeeCard);
    dashboard.appendChild(deptCard);
    dashboard.appendChild(turnoverCard);
    dashboard.appendChild(salaryCard);
    
    container.appendChild(dashboard);
    
    // Chart.js ile grafikleri çiz
    setTimeout(() => {
        drawDepartmentChart();
        drawTurnoverChart();
        drawSalaryChart();
    }, 100);
}

/**
 * Departman dağılımı pasta grafiği
 */
function drawDepartmentChart() {
    const ctx = document.getElementById('dept-chart');
    
    if (!ctx) return;
    
    const data = demoData.hrData.departmentDistribution;
    const labels = data.map(item => item.department);
    const values = data.map(item => item.count);
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#4C72B0', '#55A868', '#C44E52', '#8172B3', 
                    '#CCB974', '#64B5CD'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

/**
 * İşten ayrılma oranı çizgi grafiği
 */
function drawTurnoverChart() {
    const ctx = document.getElementById('turnover-chart');
    
    if (!ctx) return;
    
    const data = demoData.hrData.turnoverRate;
    const years = data.map(item => item.year);
    const rates = data.map(item => item.rate);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'İşten Ayrılma Oranı (%)',
                data: rates,
                borderColor: '#4C72B0',
                backgroundColor: 'rgba(76, 114, 176, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 15,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

/**
 * Maaş aralıkları grafiği
 */
function drawSalaryChart() {
    const ctx = document.getElementById('salary-chart');
    
    if (!ctx) return;
    
    const salaries = demoData.hrData.salaryRanges;
    const departments = Object.keys(salaries);
    
    const minSalaries = departments.map(dept => salaries[dept].min);
    const avgSalaries = departments.map(dept => salaries[dept].avg);
    const maxSalaries = departments.map(dept => salaries[dept].max);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: departments,
            datasets: [
                {
                    label: 'Minimum',
                    data: minSalaries,
                    backgroundColor: 'rgba(76, 114, 176, 0.8)'
                },
                {
                    label: 'Ortalama',
                    data: avgSalaries,
                    backgroundColor: 'rgba(85, 168, 104, 0.8)'
                },
                {
                    label: 'Maksimum',
                    data: maxSalaries,
                    backgroundColor: 'rgba(196, 78, 82, 0.8)'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Maaş (₺)'
                    }
                }
            }
        }
    });
}

/**
 * Makine Öğrenmesi performans metriklerini göster
 */
function createMLDashboard(elementId) {
    const container = document.getElementById(elementId);
    
    if (!container) {
        console.error(`Element ID ${elementId} bulunamadı`);
        return;
    }
    
    // Dashboard içeriği
    const dashboard = document.createElement('div');
    dashboard.className = 'dashboard';
    
    // Model performans karşılaştırma kartı
    const modelCard = document.createElement('div');
    modelCard.className = 'dashboard-card wide-card';
    modelCard.innerHTML = `
        <h3>Model Performans Karşılaştırması</h3>
        <div id="model-performance-chart" class="chart-container"></div>
    `;
    
    // Özellik önem sıralaması kartı
    const featureCard = document.createElement('div');
    featureCard.className = 'dashboard-card wide-card';
    featureCard.innerHTML = `
        <h3>Özellik Önem Sıralaması</h3>
        <div id="feature-importance-chart" class="chart-container"></div>
    `;
    
    // Dashboard'a kartları ekle
    dashboard.appendChild(modelCard);
    dashboard.appendChild(featureCard);
    
    container.appendChild(dashboard);
    
    // Chart.js ile grafikleri çiz
    setTimeout(() => {
        drawModelPerformanceChart();
        drawFeatureImportanceChart();
    }, 100);
}

/**
 * Model performans radar grafiği
 */
function drawModelPerformanceChart() {
    const ctx = document.getElementById('model-performance-chart');
    
    if (!ctx) return;
    
    const models = demoData.mlPerformance.models;
    const modelNames = models.map(model => model.name);
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
            datasets: models.map((model, index) => {
                const colors = [
                    'rgba(76, 114, 176, 0.7)', 
                    'rgba(85, 168, 104, 0.7)',
                    'rgba(196, 78, 82, 0.7)', 
                    'rgba(129, 114, 179, 0.7)',
                    'rgba(204, 185, 116, 0.7)'
                ];
                
                return {
                    label: model.name,
                    data: [model.accuracy, model.precision, model.recall, model.f1],
                    backgroundColor: colors[index % colors.length],
                    borderColor: colors[index % colors.length].replace('0.7', '1'),
                    borderWidth: 1
                };
            })
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        stepSize: 0.2
                    }
                }
            }
        }
    });
}

/**
 * Özellik önem grafiği
 */
function drawFeatureImportanceChart() {
    const ctx = document.getElementById('feature-importance-chart');
    
    if (!ctx) return;
    
    const features = demoData.mlPerformance.featureImportance;
    const featureNames = features.map(f => f.feature);
    const importanceValues = features.map(f => f.importance);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: featureNames,
            datasets: [{
                label: 'Özellik Önemi',
                data: importanceValues,
                backgroundColor: 'rgba(76, 114, 176, 0.8)',
                borderColor: 'rgba(76, 114, 176, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    max: 0.25,
                    title: {
                        display: true,
                        text: 'Önem Skoru'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}