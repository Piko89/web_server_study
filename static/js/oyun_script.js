let mevcutSayi1 = window.oyunVeri.mevcutSayi1;
let mevcutSayi2 = window.oyunVeri.mevcutSayi2;
let oyunTipi = window.oyunVeri.oyunTipi;
let islemTuru = window.oyunVeri.islemTuru; // 'topla', 'cikar', 'carpma', 'bolme'
let dogruSayisi = 0;
let yanlisSayisi = 0;
let soruCevaplandi = false;
let kullaniciAdi = kullaniciAdiAl();

function kullaniciAdiAl() {
    let adi = localStorage.getItem('kullaniciAdi');
    if (!adi) {
        adi = prompt('Lütfen adınızı girin:', 'Öğrenci');
        if (adi) {
            localStorage.setItem('kullaniciAdi', adi);
        } else {
            adi = 'Anonim';
            localStorage.setItem('kullaniciAdi', adi);
        }
    }
    return adi;
}

function dogruCevabiHesapla(sayi1, sayi2, islem) {
    switch (islem) {
        case 'topla': return sayi1 + sayi2;
        case 'cikar': return sayi1 - sayi2;
        case 'carpma': return sayi1 * sayi2;
        case 'bolme': return sayi1 / sayi2;
        default: return 0;
    }
}

function isaretAl(islem) {
    switch (islem) {
        case 'topla': return '+';
        case 'cikar': return '-';
        case 'carpma': return '×';
        case 'bolme': return '÷';
        default: return '?';
    }
}

function cevapKontrol() {
    const cevapStr = document.getElementById('cevap').value;
    const cevap = parseInt(cevapStr, 10);
    const dogruCevap = dogruCevabiHesapla(mevcutSayi1, mevcutSayi2, islemTuru);
    const sonucDiv = document.getElementById('sonuc');

    if (isNaN(cevap) || cevapStr.trim() === '') {
        alert('Lütfen geçerli bir sayı giriniz!');
        return;
    }

    // Eğer soru zaten cevaplandıysa, tekrar puan verme
    if (soruCevaplandi) {
        return;
    }

    if (cevap === dogruCevap) {
        sonucDiv.innerHTML = '🎉 Tebrikler! Doğru cevap: ' + dogruCevap;
        sonucDiv.className = 'sonuc dogru';
        dogruSayisi++;
        document.getElementById('dogru-sayisi').textContent = dogruSayisi;
    } else {
        sonucDiv.innerHTML = '❌ Yanlış! Doğru cevap: ' + dogruCevap;
        sonucDiv.className = 'sonuc yanlis';
        yanlisSayisi++;
        document.getElementById('yanlis-sayisi').textContent = yanlisSayisi;
    }

    sonucDiv.style.display = 'block';
    soruCevaplandi = true;
    
    // Cevabı kaydet (API'ye gönderişte islemTuru kullanıyoruz)
    cevapKaydet(islemTuru, mevcutSayi1, mevcutSayi2, cevap, dogruCevap, oyunTipi);
}

function cevapKaydet(islemTipi, sayi1, sayi2, kullaniciCevabi, dogruCevap, zorluk) {
    if (!['topla', 'cikar', 'carpma', 'bolme'].includes(islemTipi)) return; // Basit istemci tarafı validasyonu

    fetch('/api/cevap-kaydet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            kullanici_adi: kullaniciAdi,
            islem_tipi: islemTipi,
            sayi1: sayi1,
            sayi2: sayi2,
            kullanici_cevabi: kullaniciCevabi,
            dogru_cevap: dogruCevap,
            zorluk: zorluk
        })
    })
    .then(response => response.json())
    .catch(error => console.error('Cevap kaydedilirken hata:', error));
}

function yeniSoru() {
    fetch(`/yeni-soru/${islemTuru}?tip=${oyunTipi}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ağ yanıtı uygun değil');
            }
            return response.json();
        })
        .then(data => {
            mevcutSayi1 = data.sayi1;
            mevcutSayi2 = data.sayi2;
            const isaret = isaretAl(islemTuru);
            document.getElementById('soru').textContent = `${mevcutSayi1} ${isaret} ${mevcutSayi2} = ?`;
            document.getElementById('cevap').value = '';
            document.getElementById('sonuc').style.display = 'none';
            document.getElementById('cevap').focus();
            soruCevaplandi = false; // Yeni soru için sıfırla
        })
        .catch(error => {
            console.error('Soru yüklenemedi:', error);
            alert('Yeni soru yüklenirken bir hata oluştu. Lütfen tekrar deneyin.');
        });
}

// Enter tuşuna basıldığında cevapla
document.getElementById('cevap').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        cevapKontrol();
    }
});
