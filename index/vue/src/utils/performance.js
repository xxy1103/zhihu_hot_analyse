/**
 * 移动端性能监控工具
 * 用于监控和优化移动设备上的应用性能
 */

class MobilePerformanceMonitor {
  constructor() {
    this.metrics = {
      fps: [],
      memory: [],
      network: [],
      battery: null,
      loadTime: null,
      renderTime: null
    };
    
    this.observers = [];
    this.isMonitoring = false;
    
    this.init();
  }

  init() {
    this.setupPerformanceObserver();
    this.monitorFPS();
    this.monitorMemory();
    this.monitorNetwork();
    this.monitorBattery();
    this.setupPageVisibilityHandler();
  }

  // 设置性能观察器
  setupPerformanceObserver() {
    if ('PerformanceObserver' in window) {
      // 监控导航计时
      const navObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          if (entry.entryType === 'navigation') {
            this.metrics.loadTime = {
              domContentLoaded: entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart,
              loadComplete: entry.loadEventEnd - entry.loadEventStart,
              firstPaint: entry.responseEnd - entry.requestStart,
              timestamp: Date.now()
            };
          }
        });
      });
      
      try {
        navObserver.observe({ entryTypes: ['navigation'] });
        this.observers.push(navObserver);
      } catch (e) {
        console.warn('Navigation timing not supported');
      }

      // 监控资源加载
      const resourceObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const slowResources = entries.filter(entry => entry.duration > 1000);
        if (slowResources.length > 0) {
          console.warn('Slow resources detected:', slowResources);
        }
      });
      
      try {
        resourceObserver.observe({ entryTypes: ['resource'] });
        this.observers.push(resourceObserver);
      } catch (e) {
        console.warn('Resource timing not supported');
      }
    }
  }

  // 监控FPS
  monitorFPS() {
    let lastTime = performance.now();
    let frameCount = 0;
    
    const measureFPS = (currentTime) => {
      frameCount++;
      
      if (currentTime >= lastTime + 1000) {
        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
        this.metrics.fps.push({
          value: fps,
          timestamp: Date.now()
        });
        
        // 保持最近50个FPS记录
        if (this.metrics.fps.length > 50) {
          this.metrics.fps.shift();
        }
        
        // 如果FPS过低，发出警告
        if (fps < 30) {
          console.warn(`Low FPS detected: ${fps}`);
          this.onLowPerformance('fps', fps);
        }
        
        frameCount = 0;
        lastTime = currentTime;
      }
      
      if (this.isMonitoring) {
        requestAnimationFrame(measureFPS);
      }
    };
    
    this.isMonitoring = true;
    requestAnimationFrame(measureFPS);
  }

  // 监控内存使用
  monitorMemory() {
    if ('memory' in performance) {
      setInterval(() => {
        const memory = {
          used: Math.round(performance.memory.usedJSHeapSize / 1048576), // MB
          total: Math.round(performance.memory.totalJSHeapSize / 1048576), // MB
          limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576), // MB
          timestamp: Date.now()
        };
        
        this.metrics.memory.push(memory);
        
        // 保持最近20个内存记录
        if (this.metrics.memory.length > 20) {
          this.metrics.memory.shift();
        }
        
        // 检查内存使用是否过高
        const usagePercent = (memory.used / memory.limit) * 100;
        if (usagePercent > 80) {
          console.warn(`High memory usage: ${usagePercent.toFixed(1)}%`);
          this.onLowPerformance('memory', usagePercent);
        }
      }, 5000);
    }
  }

  // 监控网络状态
  monitorNetwork() {
    if ('connection' in navigator) {
      const updateNetworkInfo = () => {
        const connection = navigator.connection;
        const networkInfo = {
          effectiveType: connection.effectiveType,
          downlink: connection.downlink,
          rtt: connection.rtt,
          saveData: connection.saveData,
          timestamp: Date.now()
        };
        
        this.metrics.network.push(networkInfo);
        
        // 保持最近10个网络记录
        if (this.metrics.network.length > 10) {
          this.metrics.network.shift();
        }
        
        // 检查网络质量
        if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
          console.warn('Slow network detected:', connection.effectiveType);
          this.onLowPerformance('network', connection.effectiveType);
        }
      };
      
      // 初始检查
      updateNetworkInfo();
      
      // 监听网络变化
      navigator.connection.addEventListener('change', updateNetworkInfo);
    }
  }

  // 监控电池状态
  async monitorBattery() {
    if ('getBattery' in navigator) {
      try {
        const battery = await navigator.getBattery();
        
        const updateBatteryInfo = () => {
          this.metrics.battery = {
            level: Math.round(battery.level * 100),
            charging: battery.charging,
            chargingTime: battery.chargingTime,
            dischargingTime: battery.dischargingTime,
            timestamp: Date.now()
          };
          
          // 低电量警告
          if (battery.level < 0.2 && !battery.charging) {
            console.warn('Low battery detected:', this.metrics.battery.level + '%');
            this.onLowPerformance('battery', this.metrics.battery.level);
          }
        };
        
        // 初始检查
        updateBatteryInfo();
        
        // 监听电池状态变化
        battery.addEventListener('levelchange', updateBatteryInfo);
        battery.addEventListener('chargingchange', updateBatteryInfo);
      } catch (e) {
        console.warn('Battery API not supported');
      }
    }
  }

  // 页面可见性处理
  setupPageVisibilityHandler() {
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // 页面隐藏时暂停监控
        this.pauseMonitoring();
      } else {
        // 页面显示时恢复监控
        this.resumeMonitoring();
      }
    });
  }

  // 暂停监控
  pauseMonitoring() {
    this.isMonitoring = false;
    console.log('Performance monitoring paused');
  }

  // 恢复监控
  resumeMonitoring() {
    if (!this.isMonitoring) {
      this.isMonitoring = true;
      this.monitorFPS();
      console.log('Performance monitoring resumed');
    }
  }

  // 性能问题回调
  onLowPerformance(type, value) {
    // 触发自定义事件
    const event = new CustomEvent('lowPerformance', {
      detail: { type, value, timestamp: Date.now() }
    });
    window.dispatchEvent(event);
    
    // 可以在这里实现性能优化策略
    this.applyPerformanceOptimization(type, value);
  }

  // 应用性能优化
  applyPerformanceOptimization(type, value) {
    switch (type) {
      case 'fps':
        // 降低动画质量
        document.documentElement.style.setProperty('--animation-duration', '0.1s');
        break;
        
      case 'memory':
        // 清理缓存
        this.clearCache();
        break;
        
      case 'network':
        // 启用数据节省模式
        this.enableDataSaveMode();
        break;
        
      case 'battery':
        // 启用省电模式
        this.enablePowerSaveMode();
        break;
    }
  }

  // 清理缓存
  clearCache() {
    // 清理图片缓存
    const images = document.querySelectorAll('img[data-lazy]');
    images.forEach(img => {
      if (!img.classList.contains('visible')) {
        img.src = '';
      }
    });
    
    console.log('Cache cleared for performance optimization');
  }

  // 启用数据节省模式
  enableDataSaveMode() {
    document.body.classList.add('data-save-mode');
    
    // 禁用自动播放
    const videos = document.querySelectorAll('video[autoplay]');
    videos.forEach(video => {
      video.removeAttribute('autoplay');
    });
    
    console.log('Data save mode enabled');
  }

  // 启用省电模式
  enablePowerSaveMode() {
    document.body.classList.add('power-save-mode');
    
    // 降低刷新率
    this.isMonitoring = false;
    setTimeout(() => {
      this.isMonitoring = true;
      this.monitorFPS();
    }, 2000);
    
    console.log('Power save mode enabled');
  }

  // 获取性能报告
  getPerformanceReport() {
    const avgFPS = this.metrics.fps.length > 0 
      ? this.metrics.fps.reduce((sum, item) => sum + item.value, 0) / this.metrics.fps.length 
      : 0;
      
    const latestMemory = this.metrics.memory[this.metrics.memory.length - 1];
    const latestNetwork = this.metrics.network[this.metrics.network.length - 1];
    
    return {
      averageFPS: Math.round(avgFPS),
      currentMemory: latestMemory,
      currentNetwork: latestNetwork,
      battery: this.metrics.battery,
      loadTime: this.metrics.loadTime,
      timestamp: Date.now()
    };
  }

  // 销毁监控器
  destroy() {
    this.isMonitoring = false;
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
    console.log('Performance monitor destroyed');
  }
}

// 导出性能监控器
export default MobilePerformanceMonitor;

// 创建全局实例
export const performanceMonitor = new MobilePerformanceMonitor();
