# Çarpma ve Toplama İşlemi Öğreniyorum

Bu proje, ilkokul seviyesindeki öğrencilerin çarpma ve toplama işlemlerini eğlenceli bir şekilde pekiştirmesi için hazırlanmış web tabanlı bir uygulamadır. Kullanıcılar farklı zorluk seviyelerinde rastgele oluşturulan işlemleri çözerek pratik yapabilirler.

## Özellikler

- **Çarpma ve toplama işlemleri** için ayrı oyun ekranları
- Kolay, orta ve zor olmak üzere **3 farklı seviye**
- Her yeni soru için rastgele sayı üretimi
- Doğru ve yanlış cevap sayacı
- Modern ve renkli kullanıcı arayüzü

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
├── study.py
├── readme.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── carpma_script.js
│       └── topla_script.js
└── templates/
    ├── secim.html
    ├── oyun_carpma.html
    └── oyun_topla.html
```



## Katkı ve Lisans

Bu proje eğitim amaçlıdır. Katkıda bulunmak isterseniz pull request gönderebilirsiniz.

## Teşekkür

Bu projeyi geliştirirken kodlama ve hata ayıklama süreçlerinde **yapay zekadan (GitHub Copilot)ve(Claude)** yardım alınmıştır.