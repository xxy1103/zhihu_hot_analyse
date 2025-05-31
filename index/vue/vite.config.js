import { fileURLToPath, URL } from 'node:url'
import os from 'os'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// 获取本机IP地址
function getNetworkIP() {
  const interfaces = os.networkInterfaces()
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address
      }
    }
  }
  return 'localhost'
}

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')
  
  // 获取API服务器地址
  const getApiTarget = () => {
    if (env.VITE_API_BASE_URL) {
      return env.VITE_API_BASE_URL
    }
    
    // 尝试多个可能的后端地址
    const possibleHosts = [
      'localhost',
      '127.0.0.1',
      getNetworkIP()
    ]
    
    // 在开发环境中，优先使用localhost
    return 'http://localhost:5251'
  }

  return {
    plugins: [
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      host: '0.0.0.0', // 允许外部访问
      port: 5174, // 指定端口
      strictPort: false, // 如果端口被占用，自动尝试下一个端口
      open: false, // 不自动打开浏览器
      cors: true, // 启用CORS
      proxy: {
        // 智能API代理
        '/api': {
          target: getApiTarget(),
          changeOrigin: true,
          secure: false,
          configure: (proxy, options) => {
            console.log(`API代理目标: ${options.target}`)
          },
          // 代理错误处理
          onError: (err, req, res) => {
            console.error('代理错误:', err.message)
            console.log('尝试的目标:', getApiTarget())
            
            // 返回错误信息而不是让请求挂起
            if (!res.headersSent) {
              res.writeHead(502, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
              })
              res.end(JSON.stringify({ 
                error: '后端服务连接失败', 
                message: '请确保后端服务正在运行',
                target: getApiTarget()
              }))
            }
          }
        }
      }
    },
    preview: {
      host: '0.0.0.0', // 预览模式也允许外部访问
      port: 4173
    }
  }
})
