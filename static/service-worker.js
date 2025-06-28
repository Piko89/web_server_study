const CACHE_NAME = 'matematik-app-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/topla_script.js',
  '/static/js/cikar_script.js',
  '/static/js/carpma_script.js',
  '/static/js/bolme_script.js',
  '/manifest.json'
];

// Service Worker kurulumu
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching files');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('Service Worker: Installed successfully');
        return self.skipWaiting();
      })
  );
});

// Service Worker aktifleştirme
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker: Activated');
      return self.clients.claim();
    })
  );
});

// Offline için fetch olaylarını yakalama
self.addEventListener('fetch', event => {
  console.log('Service Worker: Fetching', event.request.url);
  
  // Sadece GET isteklerini önbelleğe al
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Önbellekte varsa önbellekten döndür
        if (response) {
          console.log('Service Worker: Found in cache', event.request.url);
          return response;
        }

        // Önbellekte yoksa ağdan getir
        return fetch(event.request)
          .then(response => {
            // Geçerli bir response değilse cache'e ekleme
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Response'u klonla (stream olduğu için)
            const responseToCache = response.clone();

            // Yeni dosyaları cache'e ekle
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // Ağ bağlantısı yoksa ve cache'de de yoksa
            // Offline sayfası göster (opsiyonel)
            if (event.request.destination === 'document') {
              return caches.match('/');
            }
          });
      })
  );
});

// Yeni soru API'leri için offline destek
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Yeni soru istekleri için offline yanıt
  if (url.pathname === '/yeni-soru' || url.pathname === '/yeni-soru-bolme') {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          // Offline durumda rastgele sayılar üret
          const tip = url.searchParams.get('tip') || 'kolay';
          let sayi1, sayi2;
          
          if (tip === 'kolay') {
            sayi1 = Math.floor(Math.random() * 9) + 1;
            sayi2 = Math.floor(Math.random() * 9) + 1;
          } else if (tip === 'orta') {
            sayi1 = Math.floor(Math.random() * 90) + 10;
            sayi2 = Math.floor(Math.random() * 9) + 1;
          } else { // zor
            sayi1 = Math.floor(Math.random() * 90) + 10;
            sayi2 = Math.floor(Math.random() * 90) + 10;
          }
          
          // Büyük olanı birinci sıraya al
          if (sayi1 < sayi2) {
            [sayi1, sayi2] = [sayi2, sayi1];
          }
          
          // Bölme için sayi1'i sayi2 ile çarp
          if (url.pathname === '/yeni-soru-bolme') {
            sayi1 = sayi1 * sayi2;
          }
          
          const responseData = {
            sayi1: sayi1,
            sayi2: sayi2
          };
          
          return new Response(JSON.stringify(responseData), {
            headers: { 'Content-Type': 'application/json' }
          });
        })
    );
  }
});
