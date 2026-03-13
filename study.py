from flask import Flask, render_template_string, render_template, request, jsonify
import random
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# Veritabanı ayarları
DB_NAME = 'oyun_verisi.db'

def baglanti_al():
    """Veritabanı bağlantısı oluşturur"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def veritabani_olustur():
    """Veritabanı tablolarını oluşturur"""
    if not os.path.exists(DB_NAME):
        conn = baglanti_al()
        cursor = conn.cursor()
        
        # Kullanıcılar tablosu
        cursor.execute('''
            CREATE TABLE kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                olusturulma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cevaplar tablosu (son 20 soru)
        cursor.execute('''
            CREATE TABLE cevaplar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                islem_tipi TEXT NOT NULL,
                sayi1 INTEGER NOT NULL,
                sayi2 INTEGER NOT NULL,
                kullanici_cevabi INTEGER NOT NULL,
                dogru_cevap INTEGER NOT NULL,
                dogru_mu BOOLEAN NOT NULL,
                zorluk TEXT NOT NULL,
                cevap_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
            )
        ''')
        
        # Günlük istatistikler tablosu (1 ay veri)
        cursor.execute('''
            CREATE TABLE gunluk_istatistikler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                tarih DATE NOT NULL,
                toplam_soru INTEGER DEFAULT 0,
                dogru_soru INTEGER DEFAULT 0,
                yanlis_soru INTEGER DEFAULT 0,
                olusturulma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id),
                UNIQUE(kullanici_id, tarih)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Veritabanı oluşturuldu")
    else:
        # Mevcut veritabanında tablo yoksa oluştur
        conn = baglanti_al()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gunluk_istatistikler'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE gunluk_istatistikler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_id INTEGER NOT NULL,
                    tarih DATE NOT NULL,
                    toplam_soru INTEGER DEFAULT 0,
                    dogru_soru INTEGER DEFAULT 0,
                    yanlis_soru INTEGER DEFAULT 0,
                    olusturulma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id),
                    UNIQUE(kullanici_id, tarih)
                )
            ''')
            conn.commit()
            print("✅ Günlük istatistikler tablosu oluşturuldu")

# Başlangıçta veritabanı oluştur
veritabani_olustur()

def eski_verileri_sil():
    """1 aydan eski verileri siler"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        bir_ay_once = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # 1 aydan eski cevapları sil
        cursor.execute('DELETE FROM cevaplar WHERE DATE(cevap_tarihi) < ?', (bir_ay_once,))
        
        # 1 aydan eski günlük istatistikleri sil
        cursor.execute('DELETE FROM gunluk_istatistikler WHERE DATE(tarih) < ?', (bir_ay_once,))
        
        if cursor.rowcount > 0:
            print(f"🗑️ {cursor.rowcount} eski kayıt silindi")
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Eski veri silinirken hata: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def kullanici_bazinda_son_20yi_sil(kullanici_id):
    """Bu fonksiyon artık kullanılmıyor - tüm verileri 1 ay tutuyor"""
    pass


def gunluk_istatistik_guncelle(kullanici_id, dogru_mu):
    """Günlük istatistikleri günceller"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        bugun = datetime.now().strftime('%Y-%m-%d')
        
        if dogru_mu:
            cursor.execute('''
                INSERT INTO gunluk_istatistikler (kullanici_id, tarih, toplam_soru, dogru_soru)
                VALUES (?, ?, 1, 1)
                ON CONFLICT(kullanici_id, tarih) 
                DO UPDATE SET 
                    toplam_soru = toplam_soru + 1,
                    dogru_soru = dogru_soru + 1
            ''', (kullanici_id, bugun))
        else:
            cursor.execute('''
                INSERT INTO gunluk_istatistikler (kullanici_id, tarih, toplam_soru, yanlis_soru)
                VALUES (?, ?, 1, 1)
                ON CONFLICT(kullanici_id, tarih) 
                DO UPDATE SET 
                    toplam_soru = toplam_soru + 1,
                    yanlis_soru = yanlis_soru + 1
            ''', (kullanici_id, bugun))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Günlük istatistik güncellenirken hata: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

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

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/sw.js')
def service_worker():
    return app.send_static_file('sw.js')

@app.route('/')
def ana_sayfa():
    return render_template('secim.html')

@app.route('/oyun/<islem_turu>')
def oyun(islem_turu):
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    
    ayarlar = {
        'topla': {'islem_sembolu': '➕', 'oyun_basligi': 'Toplama', 'islem_isareti': '+', 'body_class': 'topla_body'},
        'cikar': {'islem_sembolu': '➖', 'oyun_basligi': 'Çıkarma', 'islem_isareti': '-', 'body_class': 'cikar_body'},
        'carpma': {'islem_sembolu': '✖️', 'oyun_basligi': 'Çarpma', 'islem_isareti': '×', 'body_class': 'carpma_body'},
        'bolme': {'islem_sembolu': '➗', 'oyun_basligi': 'Bölme', 'islem_isareti': '÷', 'body_class': 'bolme_body'}
    }
    
    if islem_turu not in ayarlar:
        return "Geçersiz işlem türü", 400
        
    ayar = ayarlar[islem_turu]
    
    # Bölme işleminde sonucun tam sayı çıkması için sayi1 çarpım olarak güncellenir
    if islem_turu == 'bolme':
        sayi1 = sayi1 * sayi2
        
    seviye_adi = f"{tip.capitalize()} Seviye"
    if tip == 'kolay':
        seviye_adi += " (1 Basamak)"
    elif tip == 'orta':
        seviye_adi += " (2-1 Basamak)"
    elif tip == 'zor':
        seviye_adi += " (2 Basamak)"
        
    return render_template('oyun.html',
                           sayi1=sayi1, sayi2=sayi2,
                           tip=tip, islem_turu=islem_turu,
                           oyun_basligi=ayar['oyun_basligi'],
                           islem_sembolu=ayar['islem_sembolu'],
                           islem_isareti=ayar['islem_isareti'],
                           body_class=ayar['body_class'],
                           seviye_adi=seviye_adi)

@app.route('/yeni-soru/<islem_turu>')
def yeni_soru_dinamik(islem_turu):
    if islem_turu not in ['topla', 'cikar', 'carpma', 'bolme']:
        return jsonify({'error': 'Geçersiz işlem türü'}), 400
        
    tip = request.args.get('tip', 'iki-basamak')
    sayi1, sayi2 = sayi_uret(tip)
    
    if islem_turu == 'bolme':
        sayi1 = sayi1 * sayi2
        
    return jsonify({
        'sayi1': sayi1,
        'sayi2': sayi2
    })


# ==================== API ROUTES ====================

@app.route('/api/cevap-kaydet', methods=['POST'])
def cevap_kaydet():
    """Kullanıcı cevabını veritabanına kaydeder"""
    data = request.json
    kullanici_adi = data.get('kullanici_adi', 'Anonim')
    islem_tipi = data.get('islem_tipi', 'bilinmiyor')
    sayi1 = data.get('sayi1', 0)
    sayi2 = data.get('sayi2', 0)
    kullanici_cevabi = data.get('kullanici_cevabi', 0)
    dogru_cevap = data.get('dogru_cevap', 0)
    zorluk = data.get('zorluk', 'bilinmiyor')
    
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        # Kullanıcı varsa ID'sini al, yoksa oluştur
        cursor.execute('SELECT id FROM kullanicilar WHERE kullanici_adi = ?', (kullanici_adi,))
        kullanici = cursor.fetchone()
        
        if kullanici:
            kullanici_id = kullanici['id']
        else:
            cursor.execute('INSERT INTO kullanicilar (kullanici_adi) VALUES (?)', (kullanici_adi,))
            conn.commit()
            kullanici_id = cursor.lastrowid
        
        # Cevabı kaydet
        dogru_mu = (kullanici_cevabi == dogru_cevap)
        cursor.execute('''
            INSERT INTO cevaplar 
            (kullanici_id, islem_tipi, sayi1, sayi2, kullanici_cevabi, dogru_cevap, dogru_mu, zorluk)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (kullanici_id, islem_tipi, sayi1, sayi2, kullanici_cevabi, dogru_cevap, dogru_mu, zorluk))
        
        conn.commit()
        conn.close()
        
        # Günlük istatistikleri güncelle
        gunluk_istatistik_guncelle(kullanici_id, dogru_mu)
        
        # 1 aydan eski verileri sil
        eski_verileri_sil()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/admin')
def admin_paneli():
    """Admin paneli ana sayfasını gösterir"""
    return render_template('admin.html')

@app.route('/api/admin/istatistikler')
def api_istatistikler():
    """Genel istatistikleri döndürür"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        # Toplam istatistikler
        cursor.execute('SELECT COUNT(*) as toplam_kullanici FROM kullanicilar')
        toplam_kullanic = cursor.fetchone()['toplam_kullanici']
        
        cursor.execute('SELECT COUNT(*) as toplam_cevap FROM cevaplar')
        toplam_cevap = cursor.fetchone()['toplam_cevap']
        
        cursor.execute('SELECT COUNT(*) as dogru_cevap FROM cevaplar WHERE dogru_mu = 1')
        dogru_cevap = cursor.fetchone()['dogru_cevap']
        
        yanlis_cevap = toplam_cevap - dogru_cevap
        basari_orani = (dogru_cevap / toplam_cevap * 100) if toplam_cevap > 0 else 0
        
        conn.close()
        return jsonify({
            'toplam_kullanici': toplam_kullanic,
            'toplam_cevap': toplam_cevap,
            'dogru_cevap': dogru_cevap,
            'yanlis_cevap': yanlis_cevap,
            'basari_orani': round(basari_orani, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/admin/kullanicilar')
def api_kullanicilar():
    """Tüm kullanıcıları ve istatistiklerini döndürür"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                k.id,
                k.kullanici_adi,
                k.olusturulma_tarihi,
                COUNT(c.id) as toplam_cevap,
                SUM(CASE WHEN c.dogru_mu = 1 THEN 1 ELSE 0 END) as dogru_cevap
            FROM kullanicilar k
            LEFT JOIN cevaplar c ON k.id = c.kullanici_id
            GROUP BY k.id
            ORDER BY toplam_cevap DESC
        ''')
        
        kullanicilar = cursor.fetchall()
        
        sonuc = []
        for k in kullanicilar:
            dogru = k['dogru_cevap'] if k['dogru_cevap'] else 0
            toplam = k['toplam_cevap']
            basari = (dogru / toplam * 100) if toplam > 0 else 0
            
            sonuc.append({
                'id': k['id'],
                'kullanici_adi': k['kullanici_adi'],
                'olusturulma_tarihi': k['olusturulma_tarihi'],
                'toplam_cevap': toplam,
                'dogru_cevap': dogru,
                'yanlis_cevap': toplam - dogru,
                'basari_orani': round(basari, 2)
            })
        
        conn.close()
        return jsonify(sonuc)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/admin/kullanici/<int:kullanici_id>')
def api_kullanici_detay(kullanici_id):
    """Belirli bir kullanıcının detaylı verilerini döndürür"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        # Kullanıcı bilgisi
        cursor.execute('SELECT * FROM kullanicilar WHERE id = ?', (kullanici_id,))
        kullanici = cursor.fetchone()
        
        if not kullanici:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
        
        # Kullanıcının cevapları
        cursor.execute('''
            SELECT * FROM cevaplar 
            WHERE kullanici_id = ? 
            ORDER BY cevap_tarihi DESC
        ''', (kullanici_id,))
        
        cevaplar = cursor.fetchall()
        
        # İstatistikler
        cursor.execute('''
            SELECT 
                islem_tipi,
                COUNT(*) as toplam,
                SUM(CASE WHEN dogru_mu = 1 THEN 1 ELSE 0 END) as dogru
            FROM cevaplar
            WHERE kullanici_id = ?
            GROUP BY islem_tipi
        ''', (kullanici_id,))
        
        islem_istatistikleri = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'kullanici': {
                'id': kullanici['id'],
                'kullanici_adi': kullanici['kullanici_adi'],
                'olusturulma_tarihi': kullanici['olusturulma_tarihi']
            },
            'son_cevaplar': [dict(c) for c in cevaplar[:20]],
            'islem_istatistikleri': [
                {
                    'islem_tipi': i['islem_tipi'],
                    'toplam': i['toplam'],
                    'dogru': i['dogru'],
                    'yanlis': i['toplam'] - i['dogru'],
                    'basari_orani': round((i['dogru'] / i['toplam'] * 100), 2) if i['toplam'] > 0 else 0
                }
                for i in islem_istatistikleri
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/admin/gunluk/<int:kullanici_id>')
def api_gunluk_istatistikler(kullanici_id):
    """Kullanıcının son 30 günün günlük istatistiklerini döndürür"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tarih, toplam_soru, dogru_soru, yanlis_soru
            FROM gunluk_istatistikler
            WHERE kullanici_id = ?
            ORDER BY tarih DESC
            LIMIT 30
        ''', (kullanici_id,))
        
        veriler = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(v) for v in veriler])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/admin/gunluk-sorular/<int:kullanici_id>/<tarih>')
def api_gunluk_sorular(kullanici_id, tarih):
    """Belirli bir günün tüm sorularını döndürür"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cevaplar 
            WHERE kullanici_id = ? AND DATE(cevap_tarihi) = ?
            ORDER BY cevap_tarihi ASC
        ''', (kullanici_id, tarih))
        
        cevaplar = cursor.fetchall()
        conn.close()
        
        if not cevaplar:
            return jsonify([])
        
        return jsonify([dict(c) for c in cevaplar])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/admin/kullanici/<int:kullanici_id>', methods=['DELETE'])
def api_kullanici_sil(kullanici_id):
    """Kullanıcıyı ve tüm verilerini siler"""
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        
        # Kullanıcının verilerini sil
        cursor.execute('DELETE FROM cevaplar WHERE kullanici_id = ?', (kullanici_id,))
        cursor.execute('DELETE FROM gunluk_istatistikler WHERE kullanici_id = ?', (kullanici_id,))
        cursor.execute('DELETE FROM kullanicilar WHERE id = ?', (kullanici_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Kullanıcı ve verisi silindi'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    print("🚀 Study sunucusu başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresine gidin")
    print("🌐 Ağdaki diğer cihazlardan erişmek için: http://[cihaz-ip]:5000")
    print("📊 Admin paneli: http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)