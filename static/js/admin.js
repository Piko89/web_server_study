// Admin Panel JavaScript

let tumKullanicilar = [];

// Sayfayı başlat
document.addEventListener('DOMContentLoaded', function() {
    istatistikleriYukle();
    kullaniclariYukle();
    
    // Modal kapatma
    const modal = document.getElementById('modal');
    const kapatButonu = document.querySelector('.modal-kapat');
    
    kapatButonu.onclick = function() {
        modal.style.display = 'none';
    };
    
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
    
    // Arama kutusunu dinle
    document.getElementById('arama-kutusu').addEventListener('input', function(e) {
        aramaYap(e.target.value);
    });
});

// Genel istatistikleri yükle
function istatistikleriYukle() {
    fetch('/api/admin/istatistikler')
        .then(response => response.json())
        .then(data => {
            document.getElementById('toplam-kullanici').textContent = data.toplam_kullanici;
            document.getElementById('toplam-cevap').textContent = data.toplam_cevap;
            document.getElementById('dogru-cevap').textContent = data.dogru_cevap;
            document.getElementById('yanlis-cevap').textContent = data.yanlis_cevap;
            document.getElementById('basari-orani').textContent = data.basari_orani + '%';
        })
        .catch(error => console.error('Hata:', error));
}

// Kullanıcıları yükle
function kullaniclariYukle() {
    fetch('/api/admin/kullanicilar')
        .then(response => response.json())
        .then(data => {
            tumKullanicilar = data;
            tabloyuDoldur(data);
        })
        .catch(error => console.error('Hata:', error));
}

// Tabloyu doldur
function tabloyuDoldur(kullanicilar) {
    const tbody = document.getElementById('tablo-body');
    
    if (kullanicilar.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">Henüz veri yok</td></tr>';
        return;
    }
    
    tbody.innerHTML = kullanicilar.map(k => {
        let basariSinifi = 'basari-dusuk';
        if (k.basari_orani >= 75) basariSinifi = 'basari-yuksek';
        else if (k.basari_orani >= 50) basariSinifi = 'basari-orta';
        
        return `
            <tr>
                <td>${escapeHtml(k.kullanici_adi)}</td>
                <td>${k.toplam_cevap}</td>
                <td>${k.dogru_cevap}</td>
                <td>${k.yanlis_cevap}</td>
                <td><span class="basari-degeri ${basariSinifi}">${k.basari_orani}%</span></td>
                <td>
                    <button class="detay-buton" onclick="detaylariGoster(${k.id})">Detay</button>
                </td>
            </tr>
        `;
    }).join('');
}

// Detayları göster
function detaylariGoster(kullaniciId) {
    fetch(`/api/admin/kullanici/${kullaniciId}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('modal');
            const baslik = document.getElementById('modal-baslik');
            const kullaniciInfo = document.getElementById('modal-kullanici-info');
            const gunlukStats = document.getElementById('modal-gunluk-stats');
            const islemStats = document.getElementById('modal-islem-stats');
            const cevaplarTablou = document.getElementById('modal-cevaplar-tablosu').getElementsByTagName('tbody')[0];
            
            // Kullanıcı ID'sini global değişkene kaydet (silme için)
            window.secimiKullaniciId = kullaniciId;
            
            // Başlığı güncelle
            baslik.textContent = data.kullanici.kullanici_adi + ' - Detaylı Bilgi';
            
            // Kullanıcı bilgisini göster
            const tarih = new Date(data.kullanici.olusturulma_tarihi).toLocaleDateString('tr-TR');
            kullaniciInfo.innerHTML = `
                <div class="kullanici-info-item">
                    <span class="kullanici-info-label">👤 Adı:</span> ${escapeHtml(data.kullanici.kullanici_adi)}
                </div>
                <div class="kullanici-info-item">
                    <span class="kullanici-info-label">📅 Katılma Tarihi:</span> ${tarih}
                </div>
            `;
            
            // Günlük istatistikleri yükle
            gunlukIstatistikleriYukle(kullaniciId, gunlukStats);
            
            // İşlem istatistiklerini göster
            if (data.islem_istatistikleri.length === 0) {
                islemStats.innerHTML = '<p>Henüz veri yok</p>';
            } else {
                islemStats.innerHTML = data.islem_istatistikleri.map(i => {
                    const emojiler = {
                        'toplama': '➕',
                        'çıkarma': '➖',
                        'çarpma': '✖️',
                        'bölme': '➗',
                        'cikar': '➖',
                        'carpma': '✖️',
                        'bolme': '➗',
                        'topla': '➕'
                    };
                    const emoji = emojiler[i.islem_tipi] || '📝';
                    return `
                        <div class="islem-stat-kart">
                            <div class="islem-tipi-adi">${emoji} ${islemAdiDuzelt(i.islem_tipi)}</div>
                            <div class="islem-stat-row">
                                <div class="islem-stat-item">
                                    <span>Toplam</span>
                                    <span class="islem-stat-degeri">${i.toplam}</span>
                                </div>
                                <div class="islem-stat-item">
                                    <span>Doğru</span>
                                    <span class="islem-stat-degeri" style="color: #4CAF50;">${i.dogru}</span>
                                </div>
                                <div class="islem-stat-item">
                                    <span>Yanlış</span>
                                    <span class="islem-stat-degeri" style="color: #f44336;">${i.yanlis}</span>
                                </div>
                                <div class="islem-stat-item">
                                    <span>Başarı</span>
                                    <span class="islem-stat-degeri">${i.basari_orani}%</span>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            // Son cevapları göster
            if (data.son_cevaplar.length === 0) {
                cevaplarTablou.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 20px;">Henüz cevap yok</td></tr>';
            } else {
                cevaplarTablou.innerHTML = data.son_cevaplar.map(c => {
                    const soru = `${c.sayi1} ${islemSembolü(c.islem_tipi)} ${c.sayi2}`;
                    const sonuc = c.dogru_mu ? 
                        '<span class="sonuc-dogru">✅ Doğru</span>' : 
                        '<span class="sonuc-yanlis">❌ Yanlış</span>';
                    const tarih = new Date(c.cevap_tarihi).toLocaleString('tr-TR');
                    
                    return `
                        <tr>
                            <td>${islemAdiDuzelt(c.islem_tipi)}</td>
                            <td>${soru}</td>
                            <td>${c.kullanici_cevabi}</td>
                            <td>${c.dogru_cevap}</td>
                            <td>${sonuc}</td>
                            <td>${c.zorluk}</td>
                            <td>${tarih}</td>
                        </tr>
                    `;
                }).join('');
            }
            
            modal.style.display = 'block';
        })
        .catch(error => console.error('Hata:', error));
}

// Arama yap
function aramaYap(terim) {
    if (!terim) {
        tabloyuDoldur(tumKullanicilar);
        return;
    }
    
    const sonuc = tumKullanicilar.filter(k => 
        k.kullanici_adi.toLowerCase().includes(terim.toLowerCase())
    );
    
    tabloyuDoldur(sonuc);
}

// İşlem sembolü
function islemSembolü(tipi) {
    const semboller = {
        'toplama': '+',
        'çıkarma': '-',
        'çarpma': '×',
        'bölme': '÷',
        'cikar': '-',
        'carpma': '×',
        'bolme': '÷',
        'topla': '+'
    };
    return semboller[tipi] || '?';
}

// İşlem adını düzelt
function islemAdiDuzelt(tipi) {
    const adlar = {
        'toplama': 'Toplama',
        'çıkarma': 'Çıkarma',
        'çarpma': 'Çarpma',
        'bölme': 'Bölme',
        'cikar': 'Çıkarma',
        'carpma': 'Çarpma',
        'bolme': 'Bölme',
        'topla': 'Toplama'
    };
    return adlar[tipi] || tipi;
}

// XSS koruması
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Günlük istatistikleri yükle  
function gunlukIstatistikleriYukle(kullaniciId, container) {
    fetch(`/api/admin/gunluk/${kullaniciId}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                container.innerHTML = '<p>Henüz günlük veri yok</p>';
                return;
            }
            
            const html = data.map(g => `
                <div class="gunluk-stat-satiri" onclick="gunlukSorulariGoster('${g.tarih}', '${kullaniciId}', this)">
                    <div class="gunluk-tarih">📅 ${formatTarih(g.tarih)}</div>
                    <div class="gunluk-veriler">
                        <div class="gunluk-veri-item">
                            <span class="gunluk-veri-label">Toplam</span>
                            <span class="gunluk-veri-deger">${g.toplam_soru}</span>
                        </div>
                        <div class="gunluk-veri-item">
                            <span class="gunluk-veri-label">✅ Doğru</span>
                            <span class="gunluk-veri-deger" style="color: #4CAF50;">${g.dogru_soru}</span>
                        </div>
                        <div class="gunluk-veri-item">
                            <span class="gunluk-veri-label">❌ Yanlış</span>
                            <span class="gunluk-veri-deger" style="color: #f44336;">${g.yanlis_soru}</span>
                        </div>
                        <div class="gunluk-veri-item">
                            <span class="gunluk-veri-label">Başarı</span>
                            <span class="gunluk-veri-deger">${calculateBasari(g.dogru_soru, g.toplam_soru)}%</span>
                        </div>
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = html;
        })
        .catch(error => console.error('Günlük veri yönetme hatası:', error));
}

// Günün sorularını göster
function gunlukSorulariGoster(tarih, kullaniciId, element) {
    // Aktif sınıfını güncelle
    document.querySelectorAll('.gunluk-stat-satiri').forEach(el => el.classList.remove('aktif'));
    element.classList.add('aktif');
    
    fetch(`/api/admin/gunluk-sorular/${kullaniciId}/${tarih}`)
        .then(response => response.json())
        .then(data => {
            const baslik = document.getElementById('gunun-sorulari-baslik');
            const container = document.getElementById('modal-gunluk-sorular');
            
            baslik.style.display = 'block';
            baslik.textContent = `${formatTarih(tarih)} - Tüm Soruları (${data.length} soru)`;
            
            if (data.length === 0) {
                container.innerHTML = '<p>Bu gün sorusu yok</p>';
                container.style.display = 'block';
                return;
            }
            
            // Zorluk seviyelerine göre grupla
            const zorlukGruplari = {
                'kolay': { ad: '🌟 Kolay', sorular: [], dogru: 0, yanlis: 0 },
                'orta': { ad: '🎈 Orta', sorular: [], dogru: 0, yanlis: 0 },
                'zor': { ad: '📚 Zor', sorular: [], dogru: 0, yanlis: 0 }
            };
            
            data.forEach(c => {
                const zorluk = c.zorluk.toLowerCase();
                if (zorlukGruplari[zorluk]) {
                    zorlukGruplari[zorluk].sorular.push(c);
                    if (c.dogru_mu) {
                        zorlukGruplari[zorluk].dogru++;
                    } else {
                        zorlukGruplari[zorluk].yanlis++;
                    }
                }
            });
            
            // HTML tablosu oluştur
            let html = '';
            
            Object.values(zorlukGruplari).forEach(grup => {
                if (grup.sorular.length === 0) return;
                
                const toplam = grup.sorular.length;
                const basari = Math.round((grup.dogru / toplam) * 100);
                
                html += `
                    <div style="margin-bottom: 30px; background: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                        <h4 style="margin-top: 0; color: #667eea;">${grup.ad} Seviyesi - ${toplam} soru (✅ ${grup.dogru} doğru / ❌ ${grup.yanlis} yanlış / 🎯 ${basari}%)</h4>
                        <table class="gunluk-sorular-tablosu">
                            <thead>
                                <tr>
                                    <th>Saat</th>
                                    <th>İşlem</th>
                                    <th>Soru</th>
                                    <th>Cevabı</th>
                                    <th>Doğru Cevap</th>
                                    <th>Sonuç</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${grup.sorular.map(c => {
                                    const saat = new Date(c.cevap_tarihi).toLocaleTimeString('tr-TR', {hour: '2-digit', minute:'2-digit'});
                                    const soru = `${c.sayi1} ${islemSembolü(c.islem_tipi)} ${c.sayi2}`;
                                    const sonuc = c.dogru_mu ? 
                                        '<span class="soru-dogru">✅ Doğru</span>' : 
                                        '<span class="soru-yanlis">❌ Yanlış</span>';
                                    
                                    return `
                                        <tr>
                                            <td>${saat}</td>
                                            <td>${islemAdiDuzelt(c.islem_tipi)}</td>
                                            <td><strong>${soru}</strong></td>
                                            <td>${c.kullanici_cevabi}</td>
                                            <td><strong>${c.dogru_cevap}</strong></td>
                                            <td>${sonuc}</td>
                                        </tr>
                                    `;
                                }).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            container.style.display = 'block';
        })
        .catch(error => {
            console.error('Günlük sorular yüklenirken hata:', error);
            alert('Sorular yüklenirken hata oluştu');
        });
}

// Tarih formatı
function formatTarih(tarih) {
    return new Date(tarih + 'T00:00:00').toLocaleDateString('tr-TR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Başarı oranı hesapla
function calculateBasari(dogru, toplam) {
    return toplam > 0 ? Math.round((dogru / toplam) * 100) : 0;
}

// Kullanıcı silme - modal göster
function kullaniclariSil() {
    const silModal = document.getElementById('sil-modal');
    const secimiKullaniciAdi = tumKullanicilar.find(k => k.id === window.secimiKullaniciId);
    
    if (secimiKullaniciAdi) {
        document.getElementById('sil-kullanici-adi').textContent = escapeHtml(secimiKullaniciAdi.kullanici_adi);
        silModal.style.display = 'block';
    }
}

// Silme iptal
function silmeIptal() {
    document.getElementById('sil-modal').style.display = 'none';
}

// Silme onayla
function silmeOnayla() {
    const kullaniciId = window.secimiKullaniciId;
    
    fetch(`/api/admin/kullanici/${kullaniciId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('✅ Kullanıcı ve verisi başarıyla silindi');
            document.getElementById('sil-modal').style.display = 'none';
            document.getElementById('modal').style.display = 'none';
            istatistikleriYukle();
            kullaniclariYukle();
        }
    })
    .catch(error => {
        console.error('Silme hatası:', error);
        alert('❌ Silme işleminde hata oluştu');
    });
}

// Modal kapatma - pencere dışına tıklandığında
window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal');
    const silModal = document.getElementById('sil-modal');
    
    if (event.target === modal) {
        modal.style.display = 'none';
    }
    if (event.target === silModal) {
        silModal.style.display = 'none';
    }
});

