// API配置文件
// 自动检测后端服务器地址

/**
 * 获取API基础URL
 * 优先级：环境变量 > 代理模式 > 动态检测 > 默认值
 */
function getApiBaseUrl() {
  // 1. 检查环境变量
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  
  // 2. 检查是否应该使用代理模式
  // 如果前端服务器运行在5174端口，说明是通过Vite服务器访问的，应该使用代理
  const currentPort = window.location.port
  if (currentPort === '5174' || currentPort === '5175' || import.meta.env.DEV) {
    return '' // 使用相对路径，让Vite代理处理
  }
  
  // 3. 生产环境：动态检测当前主机
  const currentHost = window.location.hostname
  const currentProtocol = window.location.protocol
  
  // 如果是localhost或127.0.0.1，保持原样
  if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
    return `${currentProtocol}//localhost:5251`
  }
  
  // 如果是其他IP地址，假设后端在同一主机的5251端口
  return `${currentProtocol}//${currentHost}:5251`
}

/**
 * 获取完整的API URL
 * @param {string} endpoint - API端点
 * @returns {string} 完整的API URL
 */
export function getApiUrl(endpoint) {
  const baseUrl = getApiBaseUrl()
  // 确保endpoint以/开头
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  
  // 如果是开发环境且baseUrl为空，直接返回endpoint（相对路径）
  if (import.meta.env.DEV && !baseUrl) {
    return normalizedEndpoint
  }
  
  return `${baseUrl}${normalizedEndpoint}`
}

/**
 * 通用的API请求方法
 * @param {string} endpoint - API端点
 * @param {RequestInit} options - fetch选项
 * @returns {Promise<any>} API响应
 */
export async function apiRequest(endpoint, options = {}) {
  const url = getApiUrl(endpoint)
  
  try {
    console.log(`API请求: ${url}`)
    console.log(`环境: ${import.meta.env.DEV ? '开发' : '生产'}`)
    console.log(`基础URL: ${getApiBaseUrl()}`)
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log(`API响应成功: ${url}`, data)
    return data
  } catch (error) {
    console.error(`API请求失败: ${url}`, error)
    throw error
  }
}

// 导出基础URL获取函数
export { getApiBaseUrl }

// 常用API端点
export const API_ENDPOINTS = {
  HOT_TOPICS: '/api/hot',
  HOT_TOPIC_DETAIL: (id) => `/api/hot?id=${id}`
}
