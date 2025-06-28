from flask import Flask, render_template_string, render_template, request, jsonify, send_from_directory
import random
import os
import ssl

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

def create_self_signed_cert():
    """Kendi kendine imzalanmış SSL sertifikası oluştur"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Private key oluştur
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Sertifika oluştur
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "TR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Istanbul"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Istanbul"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Matematik App"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress("127.0.0.1"),
            ]),
            critical=False,
        ).sign(key, hashes.SHA256(), default_backend())
        
        # Dosyalara yaz
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
            
        with open("key.pem", "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            
        return True
    except ImportError:
        print("⚠️ cryptography kütüphanesi bulunamadı. pip install cryptography ile yükleyin.")
        return False
    except Exception as e:
        print(f"❌ SSL sertifikası oluşturulamadı: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Study sunucusu başlatılıyor...")
    
    # SSL sertifikası kontrolü
    if not (os.path.exists("cert.pem") and os.path.exists("key.pem")):
        print("🔐 SSL sertifikası oluşturuluyor...")
        if create_self_signed_cert():
            print("✅ SSL sertifikası başarıyla oluşturuldu!")
        else:
            print("❌ SSL sertifikası oluşturulamadı. HTTP modunda çalışıyor...")
            print("📱 Tarayıcınızda http://localhost:5000 adresine gidin")
            app.run(host='0.0.0.0', port=5000, debug=True)
            exit()
    
    print("🔒 HTTPS modunda başlatılıyor...")
    print("📱 Tarayıcınızda https://localhost:5000 adresine gidin")
    print("⚠️ Güvenlik uyarısını 'Gelişmiş' -> 'localhost'a git' ile geçin")
    print("🌐 Ağdaki diğer cihazlardan erişmek için: https://[cihaz-ip]:5000")
    print("📲 PWA olarak ana ekrana ekleyebilirsiniz!")
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)