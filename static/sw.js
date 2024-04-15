// https://medium.com/@firt/service-workers-replacing-appcache-a-sledgehammer-to-crack-a-nut-5db6f473cc9b

var CACHE_NAME = 'mobile-identity-cache-v2';
var urlsToCache = [
  '/client',
  '/static/jsrsasign-all-min.js',
  '/static/qr-code-styling.js'
];
self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
// self.addEventListener('fetch', event => {
//   event.respondWith(
//     caches.match(event.request).then(cachedResponse => {
//         const networkFetch = fetch(event.request).then(response => {
//           // update the cache with a clone of the network response
//           const responseClone = response.clone()
//           caches.open(CACHE_NAME).then(cache => {
//             cache.put(event.request, responseClone)
//           })
//           return response
//         }).catch(function (reason) {
//           console.error('ServiceWorker fetch failed: ', reason)
//         })
//         // prioritize cached response over network
//         return cachedResponse || networkFetch
//       }
//     )
//   )
// })