/**
 * 移动端错误处理和日志系统
 * 专门为移动设备优化的错误捕获和处理机制
 */

class MobileErrorHandler {
  constructor() {
    this.errors = [];
    this.maxErrors = 50;
    this.deviceInfo = this.getDeviceInfo();
    
    this.init();
  }

  init() {
    this.setupGlobalErrorHandlers();
    this.setupUnhandledRejectionHandler();
    this.setupResourceErrorHandler();
    this.setupNetworkErrorHandler();
  }

  // 获取设备信息
  getDeviceInfo() {
    const ua = navigator.userAgent;
    const info = {
      userAgent: ua,
      platform: navigator.platform,
      language: navigator.language,
      cookieEnabled: navigator.cookieEnabled,
      onLine: navigator.onLine,
      screen: {
        width: screen.width,
        height: screen.height,
        devicePixelRatio: window.devicePixelRatio || 1
      },
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      },
      timestamp: Date.now()
    };

    // 检测设备类型
    if (/iPhone|iPad|iPod/i.test(ua)) {
      info.deviceType = 'iOS';
      info.os = ua.match(/OS (\d+)_(\d+)/)?.[0] || 'Unknown iOS';
    } else if (/Android/i.test(ua)) {
      info.deviceType = 'Android';
      info.os = ua.match(/Android (\d+\.?\d*)/)?.[0] || 'Unknown Android';
    } else if (/Mobile/i.test(ua)) {
      info.deviceType = 'Mobile';
    } else {
      info.deviceType = 'Desktop';
    }

    // 检测浏览器
    if (/Chrome/i.test(ua)) {
      info.browser = 'Chrome';
    } else if (/Safari/i.test(ua)) {
      info.browser = 'Safari';
    } else if (/Firefox/i.test(ua)) {
      info.browser = 'Firefox';
    } else {
      info.browser = 'Unknown';
    }

    return info;
  }

  // 设置全局错误处理器
  setupGlobalErrorHandlers() {
    window.addEventListener('error', (event) => {
      this.handleError({
        type: 'javascript',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        error: event.error,
        stack: event.error?.stack,
        timestamp: Date.now(),
        url: window.location.href
      });
    });

    window.addEventListener('unhandledrejection', (event) => {
      this.handleError({
        type: 'promise',
        message: event.reason?.message || String(event.reason),
        promise: event.promise,
        reason: event.reason,
        stack: event.reason?.stack,
        timestamp: Date.now(),
        url: window.location.href
      });
    });
  }

  // 设置未处理的Promise拒绝处理器
  setupUnhandledRejectionHandler() {
    window.addEventListener('unhandledrejection', (event) => {
      console.error('Unhandled promise rejection:', event.reason);
      
      // 阻止默认的控制台错误输出
      event.preventDefault();
      
      this.handleError({
        type: 'unhandled-promise',
        message: `Unhandled Promise Rejection: ${event.reason}`,
        reason: event.reason,
        timestamp: Date.now(),
        url: window.location.href
      });
    });
  }

  // 设置资源错误处理器
  setupResourceErrorHandler() {
    window.addEventListener('error', (event) => {
      const target = event.target;
      
      if (target !== window && (target.tagName === 'IMG' || target.tagName === 'SCRIPT' || target.tagName === 'LINK')) {
        this.handleError({
          type: 'resource',
          message: `Failed to load ${target.tagName.toLowerCase()}: ${target.src || target.href}`,
          element: target.tagName,
          source: target.src || target.href,
          timestamp: Date.now(),
          url: window.location.href
        });
      }
    }, true);
  }

  // 设置网络错误处理器
  setupNetworkErrorHandler() {
    // 监听网络状态变化
    window.addEventListener('online', () => {
      this.logInfo('Network status: Online');
    });

    window.addEventListener('offline', () => {
      this.logError('Network status: Offline');
      this.handleError({
        type: 'network',
        message: 'Network connection lost',
        timestamp: Date.now(),
        url: window.location.href
      });
    });
  }

  // 处理错误
  handleError(errorInfo) {
    // 添加设备信息
    errorInfo.deviceInfo = this.deviceInfo;
    
    // 添加页面信息
    errorInfo.pageInfo = {
      url: window.location.href,
      title: document.title,
      referrer: document.referrer,
      timestamp: Date.now()
    };

    // 存储错误
    this.errors.push(errorInfo);
    
    // 限制错误数量
    if (this.errors.length > this.maxErrors) {
      this.errors.shift();
    }

    // 控制台输出
    console.error('Mobile Error Captured:', errorInfo);

    // 触发错误事件
    this.dispatchErrorEvent(errorInfo);

    // 根据错误类型进行特殊处理
    this.handleSpecificError(errorInfo);

    // 如果是严重错误，尝试恢复
    if (this.isCriticalError(errorInfo)) {
      this.attemptRecovery(errorInfo);
    }
  }

  // 分发错误事件
  dispatchErrorEvent(errorInfo) {
    const event = new CustomEvent('mobileError', {
      detail: errorInfo
    });
    window.dispatchEvent(event);
  }

  // 处理特定类型的错误
  handleSpecificError(errorInfo) {
    switch (errorInfo.type) {
      case 'javascript':
        this.handleJavaScriptError(errorInfo);
        break;
      case 'resource':
        this.handleResourceError(errorInfo);
        break;
      case 'network':
        this.handleNetworkError(errorInfo);
        break;
      case 'promise':
        this.handlePromiseError(errorInfo);
        break;
    }
  }

  // 处理JavaScript错误
  handleJavaScriptError(errorInfo) {
    // 如果是语法错误，显示用户友好的消息
    if (errorInfo.message.includes('SyntaxError')) {
      this.showUserMessage('页面出现了一些问题，请刷新页面重试');
    }
  }

  // 处理资源加载错误
  handleResourceError(errorInfo) {
    if (errorInfo.element === 'IMG') {
      // 图片加载失败，使用占位符
      const img = document.querySelector(`img[src="${errorInfo.source}"]`);
      if (img) {
        img.src = '/placeholder-image.png';
        img.alt = '图片加载失败';
      }
    } else if (errorInfo.element === 'SCRIPT') {
      // 脚本加载失败，显示警告
      this.showUserMessage('部分功能可能不可用，请检查网络连接');
    }
  }

  // 处理网络错误
  handleNetworkError(errorInfo) {
    this.showUserMessage('网络连接中断，请检查网络设置');
    
    // 启用离线模式
    document.body.classList.add('offline-mode');
  }

  // 处理Promise错误
  handlePromiseError(errorInfo) {
    // 记录Promise错误但不向用户显示
    console.warn('Promise error handled:', errorInfo.message);
  }

  // 判断是否为严重错误
  isCriticalError(errorInfo) {
    const criticalPatterns = [
      /Cannot read property.*of undefined/,
      /Cannot read properties.*of undefined/,
      /Maximum call stack size exceeded/,
      /Out of memory/,
      /Script error/
    ];

    return criticalPatterns.some(pattern => 
      pattern.test(errorInfo.message)
    );
  }

  // 尝试恢复
  attemptRecovery(errorInfo) {
    console.log('Attempting recovery from critical error:', errorInfo.type);

    // 清理可能损坏的状态
    try {
      // 清理localStorage中可能损坏的数据
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        try {
          JSON.parse(localStorage.getItem(key));
        } catch (e) {
          localStorage.removeItem(key);
          console.log(`Removed corrupted localStorage item: ${key}`);
        }
      });

      // 重新初始化Vue组件状态
      const event = new CustomEvent('forceRerender');
      window.dispatchEvent(event);

    } catch (e) {
      console.error('Recovery attempt failed:', e);
      
      // 最后的手段：建议用户刷新页面
      this.showUserMessage('应用遇到严重问题，建议刷新页面', {
        action: '刷新页面',
        callback: () => window.location.reload()
      });
    }
  }

  // 显示用户消息
  showUserMessage(message, options = {}) {
    // 创建移动端友好的提示
    const toast = document.createElement('div');
    toast.className = 'mobile-error-toast';
    toast.innerHTML = `
      <div class="toast-content">
        <span class="toast-message">${message}</span>
        ${options.action ? `<button class="toast-action">${options.action}</button>` : ''}
      </div>
    `;

    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
      .mobile-error-toast {
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-size: 14px;
        animation: slideUp 0.3s ease-out;
      }
      
      .toast-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .toast-action {
        background: rgba(255,255,255,0.2);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        margin-left: 12px;
        cursor: pointer;
      }
      
      @keyframes slideUp {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
    `;

    if (!document.querySelector('.mobile-error-toast-style')) {
      style.className = 'mobile-error-toast-style';
      document.head.appendChild(style);
    }

    // 添加到页面
    document.body.appendChild(toast);

    // 绑定事件
    if (options.callback) {
      const actionBtn = toast.querySelector('.toast-action');
      if (actionBtn) {
        actionBtn.onclick = options.callback;
      }
    }

    // 自动移除
    setTimeout(() => {
      if (toast.parentNode) {
        toast.style.animation = 'slideUp 0.3s ease-in reverse';
        setTimeout(() => {
          if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
          }
        }, 300);
      }
    }, options.duration || 5000);
  }

  // 记录信息日志
  logInfo(message, data = {}) {
    console.log(`[Mobile Info] ${message}`, data);
  }

  // 记录警告日志
  logWarning(message, data = {}) {
    console.warn(`[Mobile Warning] ${message}`, data);
  }

  // 记录错误日志
  logError(message, data = {}) {
    console.error(`[Mobile Error] ${message}`, data);
  }

  // 获取错误报告
  getErrorReport() {
    return {
      errors: this.errors,
      deviceInfo: this.deviceInfo,
      summary: {
        totalErrors: this.errors.length,
        errorTypes: this.getErrorTypes(),
        lastError: this.errors[this.errors.length - 1],
        timestamp: Date.now()
      }
    };
  }

  // 获取错误类型统计
  getErrorTypes() {
    const types = {};
    this.errors.forEach(error => {
      types[error.type] = (types[error.type] || 0) + 1;
    });
    return types;
  }

  // 清除错误日志
  clearErrors() {
    this.errors = [];
    console.log('Error log cleared');
  }

  // 销毁错误处理器
  destroy() {
    // 移除事件监听器会在页面卸载时自动清理
    this.clearErrors();
    console.log('Mobile error handler destroyed');
  }
}

// 导出错误处理器
export default MobileErrorHandler;

// 创建全局实例
export const mobileErrorHandler = new MobileErrorHandler();
