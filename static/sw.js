const CACHE_NAME = 'matematik-ogren-v1';
const urlsToCache = [
  '/',
  '/admin',
  '/static/css/style.css',
  '/static/css/admin.css',
  '/static/js/oyun_script.js',
  '/static/js/admin.js',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  // Sadece GET isteklerini cache'le, API isteklerini atla
  if (event.request.method !== 'GET' || event.request.url.includes('/api/') || event.request.url.includes('/yeni-soru/')) {
      return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache'de varsa döndür
        if (response) {
          return response;
        }
        
        // Yoksa ağa git
        return fetch(event.request).then(
          function(response) {
            // Geçerli bir response mu kontrol et
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Response'u kopyala çünkü response bir stream
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
