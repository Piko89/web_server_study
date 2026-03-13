# İşlemleri Öğreniyorum (Toplama, Çıkarma, Çarpma, Bölme)

Bu proje, ilkokul seviyesindeki öğrencilerin toplama, çıkarma, çarpma ve bölme işlemlerini eğlenceli bir şekilde pekiştirmesi için hazırlanmış web tabanlı bir uygulamadır. Kullanıcılar farklı zorluk seviyelerinde rastgele oluşturulan işlemleri çözerek pratik yapabilirler.

## Özellikler

- **Dinamik Oyun Ekranı**: Toplama, çıkarma, çarpma ve bölme işlemleri tek bir dinamik yapıda sunulmaktadır. (DRY Prensibi)
- **3 Farklı Zorluk Seviyesi**: Kolay, orta ve zor seviyelerde rastgele sayı üretimi. Seçilen seviyeye göre işlem aralıkları değişir.
- **PWA (Progressive Web App) Desteği**: Uygulama masaüstü ve mobil platformlara web uygulaması olarak yüklenebilir (Ana Ekrana Ekle özelliği). Çevrimdışı desteği mevcuttur (Service Worker & Manifest).
- **Gelişmiş Veritabanı (SQLite) & Hata Yönetimi**: Kullanıcı geçmişi ve tüm skorlar SQLite veritabanına güvenli şekilde kaydedilir. Gelişmiş "Error Handling" mekanizmaları ve validasyonlar ile veritabanı "lock" sorunları veya geçersiz işlemler önlenir.
- **Admin Paneli**: Toplam kullanıcı, başarı oranı, kişiselleştirilmiş grafikler ve son aktivite tablosu `/admin` sayfasında görüntülenebilir.
- **Kullanıcı Dostu & Modern Tasarım**: Öğrenmeyi keyifli hale getiren akıcı ve renkli kullanıcı arayüzü.

## Kurulum ve Çalıştırma

1. **Depoyu klonlayın:**
   ```sh
   git clone https://github.com/Piko89/web_server_study.git
   cd web_server_study
   ```

2. **Gerekli Python paketlerini yükleyin:**
   ```sh
   pip install flask
   ```

3. **Uygulamayı başlatın:**
   ```sh
   python start.py
   ```
   veya Linux/Mac için:
   ```sh
   python3 start.py
   ```

4. **Tarayıcınızda açın:**  
   [http://localhost:5000](http://localhost:5000) adresine gidin.

## Klasör Yapısı

```
web_server_study/
│
├── start.py
├── study.py            # Ana Flask backend dosyası (Veritabanı ve API rotaları burada)
├── oyun_verisi.db      # SQLite kullanıcı istatistikleri (Uygulama çalışınca oluşur)
├── readme.md
│
├── static/
│   ├── css/
│   │   ├── style.css   # Temel UI stilleri
│   │   └── admin.css   # Admin paneline özel stiller
│   ├── js/
│   │   ├── oyun_script.js # 4 işlem için ortak dinamik mantık dosyası
│   │   └── admin.js       # Admin portalı için mantık dosyası
│   ├── icons/          # PWA İkonları (192, 512 boyutlarında)
│   ├── manifest.json   # PWA Manifest veri dosyası
│   └── sw.js           # PWA Service Worker (Cache/Çevrimdışı Yönetimi)
│
└── templates/
    ├── secim.html      # Ana Menü
    ├── oyun.html       # Oyunların tümüne hizmet eden ortak tasarım şablonu
    └── admin.html      # İstatistiklerin izlendiği admin paneli
```

## Katılımcılar ve Teşekkür

Bu projenin geliştirilmesi, refactoring (kod iyileştirme) süreçleri ve hata çözümlerinde modern yapay zeka araçlarının sunduğu imkanlardan faydalanılmıştır. Bu bağlamda, kodlama süreçlerine katkılarından dolayı **GitHub Copilot**, **Claude** ve Google DeepMind tarafından geliştirilen **Antigravity** (Gemini) yapay zeka asistanlarına teşekkür ederiz. Projede insan ve yapay zeka iş birliğinin ("vibe coding") eğitici bir örneği sergilenmektedir.