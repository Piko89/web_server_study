from flask import Flask, render_template_string, render_template, request, jsonify
import random

app = Flask(__name__)




# Oyun sayfası HTML şablonu
OYUN_TEMPLATE = """

"""

def rastgele_iki_basamakli():
    """10-99 arası rastgele sayı üretir"""
    return random.randint(10, 99)

def rastgele_bir_basamakli():
    """1-9 arası rastgele sayı üretir"""
    return random.randint(1, 9)

def sayi_uret(tip):
    """Oyun tipine göre sayı çifti üretir"""
    if tip == 'kolay':
        # Bir basamak × Bir basamak
        return rastgele_bir_basamakli(), rastgele_bir_basamakli()
    elif tip == 'orta':
        # İki basamak × Bir basamak
        return rastgele_iki_basamakli(), rastgele_bir_basamakli()
    elif tip == 'zor':
        # İki basamak × İki basamak
        return rastgele_iki_basamakli(), rastgele_iki_basamakli()

@app.route('/')
def ana_sayfa():
    return render_template('secim.html')

@app.route('/oyun_carpma')
def oyun_sayfasi():
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    
    if tip == 'kolay':
        seviye_adi = "Bir Basamak × Bir Basamak"
    elif tip == 'orta':
        seviye_adi = "İki Basamak × Bir Basamak"
    elif tip == 'zor':
        seviye_adi = "İki Basamak × İki Basamak"
    
    return render_template('oyun_carpma.html', 
                                sayi1=sayi1, sayi2=sayi2, 
                                tip=tip, seviye_adi=seviye_adi)

@app.route('/yeni-soru')
def yeni_soru():
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    return jsonify({
        'sayi1': sayi1,
        'sayi2': sayi2
    })

if __name__ == '__main__':
    print("🚀 Çarpma öğrenme sunucusu başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresine gidin")
    print("🌐 Ağdaki diğer cihazlardan erişmek için: http://[raspberry-pi-ip]:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)