/**
 * 移动端状态管理
 * 专门为移动设备优化的轻量级状态管理解决方案
 */

import { reactive, readonly } from 'vue'

class MobileStateManager {
  constructor() {
    // 响应式状态
    this.state = reactive({
      // 设备信息
      device: {
        type: 'unknown',
        orientation: 'portrait',
        viewportWidth: window.innerWidth,
        viewportHeight: window.innerHeight,
        pixelRatio: window.devicePixelRatio || 1,
        isOnline: navigator.onLine,
        batteryLevel: null,
        memoryInfo: null
      },
      
      // 用户界面状态
      ui: {
        isDrawerOpen: false,
        isLoading: false,
        showInstallPrompt: false,
        theme: localStorage.getItem('theme') || 'light',
        fontSize: localStorage.getItem('fontSize') || 'medium',
        animationsEnabled: localStorage.getItem('animationsEnabled') !== 'false'
      },
      
      // 性能状态
      performance: {
        fps: 60,
        memoryUsage: 0,
        networkType: 'unknown',
        isLowPerformance: false,
        isDataSaveMode: localStorage.getItem('dataSaveMode') === 'true',
        isPowerSaveMode: false
      },
      
      // 用户偏好
      preferences: {
        pullToRefresh: localStorage.getItem('pullToRefresh') !== 'false',
        hapticFeedback: localStorage.getItem('hapticFeedback') !== 'false',
        autoPlayVideos: localStorage.getItem('autoPlayVideos') !== 'false',
        compactView: localStorage.getItem('compactView') === 'true'
      },
      
      // 数据状态
      data: {
        hotTopics: [],
        analysisData: null,
        lastUpdateTime: null,
        cacheSize: 0,
        offlineData: {}
      }
    })
    
    this.init()
  }

  init() {
    this.detectDevice()
    this.setupEventListeners()
    this.loadUserPreferences()
    this.initPerformanceMonitoring()
  }

  // 检测设备信息
  detectDevice() {
    const ua = navigator.userAgent
    
    if (/iPhone|iPad|iPod/i.test(ua)) {
      this.state.device.type = 'ios'
    } else if (/Android/i.test(ua)) {
      this.state.device.type = 'android'
    } else if (/Mobile/i.test(ua)) {
      this.state.device.type = 'mobile'
    } else {
      this.state.device.type = 'desktop'
    }
    
    this.updateViewportInfo()
    this.checkBatteryStatus()
    this.checkMemoryInfo()
  }

  // 设置事件监听器
  setupEventListeners() {
    // 视口变化
    window.addEventListener('resize', () => {
      this.updateViewportInfo()
    })
    
    // 屏幕旋转
    window.addEventListener('orientationchange', () => {
      setTimeout(() => {
        this.updateViewportInfo()
        this.state.device.orientation = window.innerHeight > window.innerWidth ? 'portrait' : 'landscape'
      }, 100)
    })
    
    // 网络状态变化
    window.addEventListener('online', () => {
      this.state.device.isOnline = true
      this.syncOfflineData()
    })
    
    window.addEventListener('offline', () => {
      this.state.device.isOnline = false
    })
    
    // 网络类型变化
    if ('connection' in navigator) {
      navigator.connection.addEventListener('change', () => {
        this.state.performance.networkType = navigator.connection.effectiveType
        
        // 根据网络类型调整性能设置
        if (navigator.connection.effectiveType === 'slow-2g' || navigator.connection.effectiveType === '2g') {
          this.enableDataSaveMode()
        }
      })
    }
    
    // 页面可见性变化
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.state.ui.isLoading = false
      }
    })
    
    // 性能监控事件
    window.addEventListener('lowPerformance', (event) => {
      this.handleLowPerformance(event.detail)
    })
  }

  // 更新视口信息
  updateViewportInfo() {
    this.state.device.viewportWidth = window.innerWidth
    this.state.device.viewportHeight = window.innerHeight
    this.state.device.orientation = window.innerHeight > window.innerWidth ? 'portrait' : 'landscape'
  }

  // 检查电池状态
  async checkBatteryStatus() {
    if ('getBattery' in navigator) {
      try {
        const battery = await navigator.getBattery()
        this.state.device.batteryLevel = Math.round(battery.level * 100)
        
        battery.addEventListener('levelchange', () => {
          this.state.device.batteryLevel = Math.round(battery.level * 100)
          
          // 低电量时启用省电模式
          if (battery.level < 0.2 && !battery.charging) {
            this.enablePowerSaveMode()
          } else if (battery.level > 0.3 || battery.charging) {
            this.disablePowerSaveMode()
          }
        })
      } catch (e) {
        console.warn('Battery API not supported')
      }
    }
  }

  // 检查内存信息
  checkMemoryInfo() {
    if ('memory' in performance) {
      const memory = performance.memory
      this.state.device.memoryInfo = {
        used: Math.round(memory.usedJSHeapSize / 1048576),
        total: Math.round(memory.totalJSHeapSize / 1048576),
        limit: Math.round(memory.jsHeapSizeLimit / 1048576)
      }
      
      // 定期更新内存信息
      setInterval(() => {
        const currentMemory = performance.memory
        this.state.device.memoryInfo = {
          used: Math.round(currentMemory.usedJSHeapSize / 1048576),
          total: Math.round(currentMemory.totalJSHeapSize / 1048576),
          limit: Math.round(currentMemory.jsHeapSizeLimit / 1048576)
        }
        
        this.state.performance.memoryUsage = (currentMemory.usedJSHeapSize / currentMemory.jsHeapSizeLimit) * 100
      }, 10000)
    }
  }

  // 加载用户偏好
  loadUserPreferences() {
    // 从localStorage加载偏好设置
    const savedPrefs = localStorage.getItem('mobilePreferences')
    if (savedPrefs) {
      try {
        const prefs = JSON.parse(savedPrefs)
        Object.assign(this.state.preferences, prefs)
      } catch (e) {
        console.warn('Failed to load user preferences')
      }
    }
  }

  // 保存用户偏好
  saveUserPreferences() {
    localStorage.setItem('mobilePreferences', JSON.stringify(this.state.preferences))
  }

  // 初始化性能监控
  initPerformanceMonitoring() {
    let frameCount = 0
    let lastTime = performance.now()
    
    const measureFPS = (currentTime) => {
      frameCount++
      
      if (currentTime >= lastTime + 1000) {
        this.state.performance.fps = Math.round((frameCount * 1000) / (currentTime - lastTime))
        frameCount = 0
        lastTime = currentTime
        
        // 检查是否需要启用低性能模式
        if (this.state.performance.fps < 30) {
          this.state.performance.isLowPerformance = true
        } else if (this.state.performance.fps > 45) {
          this.state.performance.isLowPerformance = false
        }
      }
      
      requestAnimationFrame(measureFPS)
    }
    
    requestAnimationFrame(measureFPS)
  }

  // 处理低性能情况
  handleLowPerformance(detail) {
    this.state.performance.isLowPerformance = true
    
    switch (detail.type) {
      case 'fps':
        this.disableAnimations()
        break
      case 'memory':
        this.clearCache()
        break
      case 'network':
        this.enableDataSaveMode()
        break
      case 'battery':
        this.enablePowerSaveMode()
        break
    }
  }

  // 禁用动画
  disableAnimations() {
    this.state.ui.animationsEnabled = false
    document.body.classList.add('animations-disabled')
    localStorage.setItem('animationsEnabled', 'false')
  }

  // 启用动画
  enableAnimations() {
    this.state.ui.animationsEnabled = true
    document.body.classList.remove('animations-disabled')
    localStorage.setItem('animationsEnabled', 'true')
  }

  // 启用数据节省模式
  enableDataSaveMode() {
    this.state.performance.isDataSaveMode = true
    document.body.classList.add('data-save-mode')
    localStorage.setItem('dataSaveMode', 'true')
  }

  // 禁用数据节省模式
  disableDataSaveMode() {
    this.state.performance.isDataSaveMode = false
    document.body.classList.remove('data-save-mode')
    localStorage.setItem('dataSaveMode', 'false')
  }

  // 启用省电模式
  enablePowerSaveMode() {
    this.state.performance.isPowerSaveMode = true
    document.body.classList.add('power-save-mode')
    this.disableAnimations()
  }

  // 禁用省电模式
  disablePowerSaveMode() {
    this.state.performance.isPowerSaveMode = false
    document.body.classList.remove('power-save-mode')
    if (this.state.preferences.animationsEnabled !== false) {
      this.enableAnimations()
    }
  }

  // 清理缓存
  clearCache() {
    // 清理组件缓存
    this.state.data.hotTopics = []
    this.state.data.analysisData = null
    
    // 清理localStorage中的临时数据
    const keys = Object.keys(localStorage)
    keys.forEach(key => {
      if (key.startsWith('temp_') || key.startsWith('cache_')) {
        localStorage.removeItem(key)
      }
    })
    
    this.state.data.cacheSize = 0
    console.log('Cache cleared for performance optimization')
  }

  // 同步离线数据
  syncOfflineData() {
    if (Object.keys(this.state.data.offlineData).length > 0) {
      console.log('Syncing offline data...')
      
      // 这里可以实现离线数据同步逻辑
      // 例如：将离线收集的数据发送到服务器
      
      // 同步完成后清理离线数据
      this.state.data.offlineData = {}
    }
  }

  // 添加离线数据
  addOfflineData(key, data) {
    this.state.data.offlineData[key] = {
      data,
      timestamp: Date.now()
    }
  }

  // 设置主题
  setTheme(theme) {
    this.state.ui.theme = theme
    localStorage.setItem('theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
  }

  // 设置字体大小
  setFontSize(size) {
    this.state.ui.fontSize = size
    localStorage.setItem('fontSize', size)
    document.documentElement.setAttribute('data-font-size', size)
  }

  // 切换抽屉
  toggleDrawer() {
    this.state.ui.isDrawerOpen = !this.state.ui.isDrawerOpen
  }

  // 设置加载状态
  setLoading(loading) {
    this.state.ui.isLoading = loading
  }

  // 更新热点数据
  updateHotTopics(topics) {
    this.state.data.hotTopics = topics
    this.state.data.lastUpdateTime = Date.now()
  }

  // 更新分析数据
  updateAnalysisData(data) {
    this.state.data.analysisData = data
  }

  // 获取只读状态
  getState() {
    return readonly(this.state)
  }

  // 获取设备信息
  getDeviceInfo() {
    return readonly(this.state.device)
  }

  // 获取性能信息
  getPerformanceInfo() {
    return readonly(this.state.performance)
  }

  // 获取用户偏好
  getUserPreferences() {
    return readonly(this.state.preferences)
  }
}

// 创建全局状态管理实例
export const mobileStateManager = new MobileStateManager()

// 导出状态管理器
export default MobileStateManager
