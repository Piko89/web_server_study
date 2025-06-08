let mevcutSayi1 = window.oyunVeri.mevcutSayi1;
let mevcutSayi2 = window.oyunVeri.mevcutSayi2;
let oyunTipi = window.oyunVeri.oyunTipi;
let dogruSayisi = 0;
let yanlisSayisi = 0;
let soruCevaplandi = false;

function cevapKontrol() {
    const cevap = parseInt(document.getElementById('cevap').value);
    const dogruCevap = mevcutSayi1 * mevcutSayi2;
    const sonucDiv = document.getElementById('sonuc');

    if (isNaN(cevap)) {
        alert('Lütfen bir sayı giriniz!');
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
    soruCevaplandi = true; // Sorunun cevaplandığını işaretle
}

function yeniSoru() {
    fetch('/yeni-soru?tip=' + oyunTipi)
        .then(response => response.json())
        .then(data => {
            mevcutSayi1 = data.sayi1;
            mevcutSayi2 = data.sayi2;
            document.getElementById('soru').textContent = data.sayi1 + ' × ' + data.sayi2 + ' = ?';
            document.getElementById('cevap').value = '';
            document.getElementById('sonuc').style.display = 'none';
            soruCevaplandi = false; // Yeni soru için sıfırla
        });
}

// Enter tuşuna basıldığında cevapla
document.getElementById('cevap').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        cevapKontrol();
    }
});