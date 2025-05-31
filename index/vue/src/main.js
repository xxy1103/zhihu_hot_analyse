import './css/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// 移动端工具
import { isMobile, disableZoom, optimizeScroll } from './utils/mobile.js'
// 移动端性能监控
import { performanceMonitor } from './utils/performance.js'
// 移动端错误处理
import { mobileErrorHandler } from './utils/errorHandler.js'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#667eea',
          secondary: '#f093fb',
          accent: '#4ecdc4',
          error: '#ff6b6b',
          warning: '#feca57',
          info: '#48cae4',
          success: '#06ffa5',
          surface: '#ffffff',
          background: '#f8fbff',
          'surface-variant': '#f1f5f9',
          'on-surface-variant': '#64748b',
          'primary-container': '#e0e7ff',
          'secondary-container': '#fce7f3',
          'accent-container': '#ccf7f0',
        }
      },
      dark: {
        colors: {
          primary: '#818cf8',
          secondary: '#a78bfa',
          accent: '#22d3ee',
          error: '#f87171',
          warning: '#fbbf24',
          info: '#60a5fa',
          success: '#34d399',
          surface: '#1e293b',
          background: '#0f172a',
          'surface-variant': '#334155',
          'on-surface-variant': '#94a3b8',
          'primary-container': '#312e81',
          'secondary-container': '#581c87',
          'accent-container': '#155e75',
        }
      }
    }
  }
})

const app = createApp(App)

app.use(router)
app.use(vuetify)

// 移动端优化初始化
if (isMobile()) {
  console.log('Mobile device detected, applying optimizations...')
  
  // 禁用双击缩放（可选）
  // disableZoom()
  
  // 优化滚动性能
  document.addEventListener('DOMContentLoaded', () => {
    const scrollElements = document.querySelectorAll('.mobile-scroll')
    scrollElements.forEach(element => {
      optimizeScroll(element)
    })
  })
  
  // 添加移动端特定的CSS类
  document.documentElement.classList.add('mobile-device')
  
  // 防止iOS Safari地址栏影响视口高度
  const setViewportHeight = () => {
    const vh = window.innerHeight * 0.01
    document.documentElement.style.setProperty('--vh', `${vh}px`)
  }
  
  setViewportHeight()
  window.addEventListener('resize', setViewportHeight)
  window.addEventListener('orientationchange', setViewportHeight)
  
  // 性能监控事件监听
  window.addEventListener('lowPerformance', (event) => {
    console.warn('Low performance detected:', event.detail)
    
    // 可以在这里添加性能警告的UI提示
    if (event.detail.type === 'fps' && event.detail.value < 20) {
      // FPS过低时的处理
      document.body.classList.add('low-performance-mode')
    }
  })
  
  // 错误处理事件监听
  window.addEventListener('mobileError', (event) => {
    console.error('Mobile error captured:', event.detail)
    
    // 可以在这里添加错误上报逻辑
    // reportErrorToAnalytics(event.detail)
  })
}

// 全局性能监控（所有设备）
document.addEventListener('DOMContentLoaded', () => {
  console.log('Performance monitoring started')
  
  // 页面加载完成后生成性能报告
  window.addEventListener('load', () => {
    setTimeout(() => {
      const report = performanceMonitor.getPerformanceReport()
      console.log('Performance Report:', report)
    }, 2000)
  })
})

// PWA 安装提示
window.addEventListener('beforeinstallprompt', (e) => {
  // 阻止Chrome 67及更早版本自动显示安装提示
  e.preventDefault()
  
  // 存储事件，以便稍后触发
  window.deferredPrompt = e
  
  console.log('PWA install prompt available')
  
  // 可以在这里显示自定义的安装按钮
  const installButton = document.createElement('button')
  installButton.textContent = '安装应用'
  installButton.className = 'pwa-install-button'
  installButton.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 12px 24px;
    background: #1976d2;
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    cursor: pointer;
    z-index: 1000;
  `
  
  installButton.addEventListener('click', async () => {
    if (window.deferredPrompt) {
      window.deferredPrompt.prompt()
      const { outcome } = await window.deferredPrompt.userChoice
      console.log(`PWA install outcome: ${outcome}`)
      window.deferredPrompt = null
      installButton.remove()
    }
  })
  
  document.body.appendChild(installButton)
  
  // 5秒后自动隐藏按钮
  setTimeout(() => {
    if (installButton.parentNode) {
      installButton.style.opacity = '0'
      setTimeout(() => {
        if (installButton.parentNode) {
          installButton.remove()
        }
      }, 300)
    }
  }, 5000)
})

app.mount('#app')
