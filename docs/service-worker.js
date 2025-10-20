const CACHE_NAME = 'enviro-app-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/style.css',
  '/script.js',
  '/health_education.png',
  '/agroecology.html',
  '/agropastoral.html',
  '/climate_solutions.html',
  '/pollution_solutions.html',
  '/water_energy_solutions.html',
  '/health_education.html',
  '/agroecology.css',
  '/agropastoral.css',
  '/climate_solutions.css',
  '/pollution_solutions.css',
  '/water_energy_solutions.css',
  '/health_education.css'
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
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
