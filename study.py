from flask import Flask, render_template_string, render_template, request, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

def rastgele_iki_basamakli():
    """10-99 arası rastgele sayı üretir"""
    return random.randint(10, 99)

def rastgele_bir_basamakli():
    """1-9 arası rastgele sayı üretir"""
    return random.randint(1, 9)

def sayi_uret(tip):
    """Oyun tipine göre sayı çifti üretir ve ilk sayı ikinci sayıdan büyük olur"""
    if tip == 'kolay':
        a, b = rastgele_bir_basamakli(), rastgele_bir_basamakli()
    elif tip == 'orta':
        a, b = rastgele_iki_basamakli(), rastgele_bir_basamakli()
    elif tip == 'zor':
        a, b = rastgele_iki_basamakli(), rastgele_iki_basamakli()
    # Büyük olanı birinci sıraya al
    if a < b:
        a, b = b, a
    return a, b

# PWA için manifest.json dosyasını servis et
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

# PWA için service worker'ı servis et
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

# PWA için ikonları servis et
@app.route('/static/icons/<path:filename>')
def icons(filename):
    return send_from_directory('static/icons', filename)

@app.route('/')
def ana_sayfa():
    return render_template('secim.html')

@app.route('/oyun_carpma')
def oyun_carpma():
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

@app.route('/oyun_topla')
def oyun_topla():
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    
    if tip == 'kolay':
        seviye_adi = "Bir Basamak + Bir Basamak"
    elif tip == 'orta':
        seviye_adi = "İki Basamak + Bir Basamak"
    elif tip == 'zor':
        seviye_adi = "İki Basamak + İki Basamak"
    
    return render_template('oyun_topla.html', 
                                sayi1=sayi1, sayi2=sayi2, 
                                tip=tip, seviye_adi=seviye_adi)

@app.route('/oyun_cikar')
def oyun_cikar():
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    
    if tip == 'kolay':
        seviye_adi = "Bir Basamak - Bir Basamak"
    elif tip == 'orta':
        seviye_adi = "İki Basamak - Bir Basamak"
    elif tip == 'zor':
        seviye_adi = "İki Basamak - İki Basamak"
    
    return render_template('oyun_cikar.html', 
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

@app.route('/oyun_bolme')
def oyun_bolme():
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    sayi1= sayi1 * sayi2

    if tip == 'kolay':
        seviye_adi = "Kolay Bölme"
    elif tip == 'orta':
        seviye_adi = "İki Basamak ÷ Bir Basamak"
    elif tip == 'zor':
        seviye_adi = "İki Basamak ÷ İki Basamak"
    
    return render_template('oyun_bolme.html', 
                                sayi1=sayi1, sayi2=sayi2, 
                                tip=tip, seviye_adi=seviye_adi)

@app.route('/yeni-soru-bolme')
def yeni_soru_bolme():
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    sayi1= sayi1 * sayi2
    return jsonify({
        'sayi1': sayi1,
        'sayi2': sayi2
    })

if __name__ == '__main__':
    print("🚀 Study sunucusu başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresine gidin")
    print("🌐 Ağdaki diğer cihazlardan erişmek için: http://[cihaz-ip]:5000")
    print("📲 PWA olarak ana ekrana ekleyebilirsiniz!")
    app.run(host='0.0.0.0', port=5000, debug=True)