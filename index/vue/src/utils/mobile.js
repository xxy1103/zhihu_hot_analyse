/**
 * 移动端工具函数库
 * 提供移动端特有的功能和优化
 */

// 检测是否为移动设备
export const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

// 检测是否为iOS设备
export const isIOS = () => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent)
}

// 检测是否为Android设备
export const isAndroid = () => {
  return /Android/.test(navigator.userAgent)
}

// 获取屏幕尺寸信息
export const getScreenInfo = () => {
  return {
    width: window.innerWidth,
    height: window.innerHeight,
    ratio: window.devicePixelRatio || 1,
    orientation: window.innerWidth > window.innerHeight ? 'landscape' : 'portrait'
  }
}

// 防抖函数 - 用于优化移动端性能
export const debounce = (func, delay) => {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(null, args), delay)
  }
}

// 节流函数 - 用于滚动事件优化
export const throttle = (func, delay) => {
  let inThrottle
  return (...args) => {
    if (!inThrottle) {
      func.apply(null, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, delay)
    }
  }
}

// 添加触摸反馈
export const addTouchFeedback = (element) => {
  if (!element) return

  element.style.transition = 'transform 0.1s ease'
  
  element.addEventListener('touchstart', () => {
    element.style.transform = 'scale(0.98)'
  }, { passive: true })
  
  element.addEventListener('touchend', () => {
    element.style.transform = 'scale(1)'
  }, { passive: true })
  
  element.addEventListener('touchcancel', () => {
    element.style.transform = 'scale(1)'
  }, { passive: true })
}

// 禁用移动端缩放
export const disableZoom = () => {
  document.addEventListener('touchmove', (e) => {
    if (e.scale !== 1) {
      e.preventDefault()
    }
  }, { passive: false })
  
  let lastTouchEnd = 0
  document.addEventListener('touchend', (e) => {
    const now = (new Date()).getTime()
    if (now - lastTouchEnd <= 300) {
      e.preventDefault()
    }
    lastTouchEnd = now
  }, false)
}

// 优化移动端滚动
export const optimizeScroll = (element) => {
  if (!element) return
  
  element.style.webkitOverflowScrolling = 'touch'
  element.style.overscrollBehavior = 'contain'
}

// 安全区域适配
export const getSafeAreaInsets = () => {
  const style = getComputedStyle(document.documentElement)
  return {
    top: style.getPropertyValue('--sat') || style.getPropertyValue('env(safe-area-inset-top)') || '0px',
    right: style.getPropertyValue('--sar') || style.getPropertyValue('env(safe-area-inset-right)') || '0px',
    bottom: style.getPropertyValue('--sab') || style.getPropertyValue('env(safe-area-inset-bottom)') || '0px',
    left: style.getPropertyValue('--sal') || style.getPropertyValue('env(safe-area-inset-left)') || '0px'
  }
}

// 处理移动端图片懒加载
export const lazyLoadImage = (img, src) => {
  if (!img || !src) return
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const image = entry.target
        image.src = src
        image.classList.remove('lazy')
        observer.unobserve(image)
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: '50px'
  })
  
  observer.observe(img)
}

// 简单的手势识别
export class GestureRecognizer {
  constructor(element, options = {}) {
    this.element = element
    this.options = {
      threshold: 50,
      timeout: 500,
      ...options
    }
    
    this.startX = 0
    this.startY = 0
    this.startTime = 0
    
    this.bindEvents()
  }
  
  bindEvents() {
    this.element.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true })
    this.element.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true })
  }
  
  handleTouchStart(e) {
    const touch = e.touches[0]
    this.startX = touch.clientX
    this.startY = touch.clientY
    this.startTime = Date.now()
  }
  
  handleTouchEnd(e) {
    const touch = e.changedTouches[0]
    const endX = touch.clientX
    const endY = touch.clientY
    const endTime = Date.now()
    
    const deltaX = endX - this.startX
    const deltaY = endY - this.startY
    const deltaTime = endTime - this.startTime
    
    if (deltaTime > this.options.timeout) return
    
    const absX = Math.abs(deltaX)
    const absY = Math.abs(deltaY)
    
    if (absX > this.options.threshold || absY > this.options.threshold) {
      if (absX > absY) {
        // 水平滑动
        if (deltaX > 0) {
          this.onSwipeRight && this.onSwipeRight()
        } else {
          this.onSwipeLeft && this.onSwipeLeft()
        }
      } else {
        // 垂直滑动
        if (deltaY > 0) {
          this.onSwipeDown && this.onSwipeDown()
        } else {
          this.onSwipeUp && this.onSwipeUp()
        }
      }
    } else {
      // 点击
      this.onTap && this.onTap()
    }
  }
  
  onSwipeLeft(callback) {
    this.onSwipeLeft = callback
    return this
  }
  
  onSwipeRight(callback) {
    this.onSwipeRight = callback
    return this
  }
  
  onSwipeUp(callback) {
    this.onSwipeUp = callback
    return this
  }
  
  onSwipeDown(callback) {
    this.onSwipeDown = callback
    return this
  }
  
  onTap(callback) {
    this.onTap = callback
    return this
  }
}

// 移动端性能监控
export const performanceMonitor = {
  // 监控滚动性能
  monitorScroll(element) {
    let ticking = false
    
    const updateScrollPosition = () => {
      // 这里可以添加滚动位置相关的逻辑
      ticking = false
    }
    
    const requestScrollUpdate = () => {
      if (!ticking) {
        requestAnimationFrame(updateScrollPosition)
        ticking = true
      }
    }
    
    element.addEventListener('scroll', requestScrollUpdate, { passive: true })
  },
  
  // 监控触摸性能
  monitorTouch() {
    let touchCount = 0
    
    document.addEventListener('touchstart', () => {
      touchCount++
      if (touchCount % 100 === 0) {
        console.log(`Touch events: ${touchCount}`)
      }
    }, { passive: true })
  }
}

// 移动端振动反馈
export const vibrate = (pattern = 50) => {
  if ('vibrate' in navigator) {
    navigator.vibrate(pattern)
  }
}

// 移动端网络状态检测
export const getNetworkInfo = () => {
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection
  
  if (connection) {
    return {
      effectiveType: connection.effectiveType,
      downlink: connection.downlink,
      rtt: connection.rtt,
      saveData: connection.saveData
    }
  }
  
  return {
    effectiveType: 'unknown',
    downlink: 0,
    rtt: 0,
    saveData: false
  }
}

// 移动端电池状态（如果支持）
export const getBatteryInfo = async () => {
  if ('getBattery' in navigator) {
    try {
      const battery = await navigator.getBattery()
      return {
        level: Math.round(battery.level * 100),
        charging: battery.charging,
        chargingTime: battery.chargingTime,
        dischargingTime: battery.dischargingTime
      }
    } catch (error) {
      console.warn('Battery API not supported')
      return null
    }
  }
  return null
}

// 移动端内存信息
export const getMemoryInfo = () => {
  if ('memory' in performance) {
    return {
      usedJSHeapSize: performance.memory.usedJSHeapSize,
      totalJSHeapSize: performance.memory.totalJSHeapSize,
      jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
    }
  }
  return null
}

// 格式化文件大小
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 移动端下拉刷新
export class PullToRefresh {
  constructor(element, onRefresh, options = {}) {
    this.element = element
    this.onRefresh = onRefresh
    this.options = {
      threshold: 80,
      maxDistance: 120,
      ...options
    }
    
    this.startY = 0
    this.currentY = 0
    this.isRefreshing = false
    this.isPulling = false
    
    this.bindEvents()
  }
  
  bindEvents() {
    this.element.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true })
    this.element.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false })
    this.element.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true })
  }
  
  handleTouchStart(e) {
    if (this.element.scrollTop === 0) {
      this.startY = e.touches[0].clientY
      this.isPulling = true
    }
  }
  
  handleTouchMove(e) {
    if (!this.isPulling || this.isRefreshing) return
    
    this.currentY = e.touches[0].clientY
    const distance = this.currentY - this.startY
    
    if (distance > 0 && distance <= this.options.maxDistance) {
      e.preventDefault()
      const progress = Math.min(distance / this.options.threshold, 1)
      this.updateUI(progress, distance)
    }
  }
  
  handleTouchEnd() {
    if (!this.isPulling || this.isRefreshing) return
    
    const distance = this.currentY - this.startY
    
    if (distance >= this.options.threshold) {
      this.startRefresh()
    } else {
      this.resetUI()
    }
    
    this.isPulling = false
  }
  
  updateUI(progress, distance) {
    // 这里可以自定义刷新UI的更新逻辑
    console.log(`Pull progress: ${(progress * 100).toFixed(0)}%`)
  }
  
  startRefresh() {
    this.isRefreshing = true
    this.onRefresh().finally(() => {
      this.isRefreshing = false
      this.resetUI()
    })
  }
  
  resetUI() {
    // 重置UI状态
    console.log('Reset refresh UI')
  }
}

export default {
  isMobile,
  isIOS,
  isAndroid,
  getScreenInfo,
  debounce,
  throttle,
  addTouchFeedback,
  disableZoom,
  optimizeScroll,
  getSafeAreaInsets,
  lazyLoadImage,
  GestureRecognizer,
  performanceMonitor,
  vibrate,
  getNetworkInfo,
  getBatteryInfo,
  getMemoryInfo,
  formatFileSize,
  PullToRefresh
}
