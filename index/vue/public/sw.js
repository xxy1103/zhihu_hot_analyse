const CACHE_NAME = 'social-media-analytics-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/src/main.js',
  '/src/App.vue',
  '/src/css/main.css',
  '/manifest.json'
];

// 安装事件
self.addEventListener('install', event => {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.log('Cache install failed:', err))
  );
});

// 激活事件
self.addEventListener('activate', event => {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// 获取事件 - 网络优先策略
self.addEventListener('fetch', event => {
  // 跳过非GET请求
  if (event.request.method !== 'GET') return;
  
  // 跳过Chrome扩展请求
  if (event.request.url.startsWith('chrome-extension://')) return;
  
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 如果网络请求成功，更新缓存
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseClone);
            });
        }
        return response;
      })
      .catch(() => {
        // 网络失败时，从缓存中获取
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            // 如果缓存中也没有，返回离线页面
            if (event.request.destination === 'document') {
              return caches.match('/index.html');
            }
          });
      })
  );
});

// 推送通知事件
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : '新的热点数据更新',
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: '查看详情',
        icon: '/icon-192x192.png'
      },
      {
        action: 'close',
        title: '关闭',
        icon: '/icon-192x192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('数据分析平台', options)
  );
});

// 通知点击事件
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/analyse')
    );
  }
});

// 后台同步
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // 在后台同步数据
  return fetch('/api/sync')
    .then(response => response.json())
    .then(data => {
      console.log('Background sync completed:', data);
    })
    .catch(err => {
      console.log('Background sync failed:', err);
    });
}
