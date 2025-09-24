#!/bin/bash
# DNS Test Script for tolunayozcan.art

echo "🔍 DNS Durumu Kontrol Ediliyor..."
echo "================================="

# GitHub Pages beklenen IP'ler
EXPECTED_IPS=(
    "185.199.108.153"
    "185.199.109.153" 
    "185.199.110.153"
    "185.199.111.153"
)

echo "📋 GitHub Pages Beklenen IP'ler:"
printf '%s\n' "${EXPECTED_IPS[@]}"
echo ""

echo "🌐 tolunayozcan.art DNS Durumu:"
if getent hosts tolunayozcan.art; then
    echo "✅ Root domain çözümleniyor"
else
    echo "❌ Root domain çözümlenmiyor"
fi

echo ""
echo "🌐 www.tolunayozcan.art DNS Durumu:"
if getent hosts www.tolunayozcan.art; then
    echo "✅ WWW subdomain çözümleniyor"
else
    echo "❌ WWW subdomain çözümlenmiyor"
fi

echo ""
echo "🔗 GitHub Pages kontrolü:"
if getent hosts tolunayozcan.github.io; then
    echo "✅ GitHub Pages erişilebilir"
else
    echo "❌ GitHub Pages erişilemiyor"
fi

echo ""
echo "⏰ DNS yayılımı 15-60 dakika sürebilir."
echo "📝 GoDaddy'de A records'ları doğru girdiğinizden emin olun."