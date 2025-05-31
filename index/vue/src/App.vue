<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import { apiRequest, API_ENDPOINTS } from '@/utils/api'

const theme = useTheme()
const router = useRouter()
const drawer = ref(false)

let id = 1
const jsonData = ref(null)
const loading = ref(false)

// 格式化热度值
const formatHotValue = (value) => {
  if (value >= 10000) {
    return (value / 10000).toFixed(1) + 'w'
  }
  return value
}

// 获取排名样式类
const getRankClass = (rank) => {
  if (rank <= 3) return 'top-rank'
  if (rank <= 10) return 'high-rank'
  return 'normal-rank'
}

// 切换主题
const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}

// 移动端导航到分析页面
const navigateToAnalyse = (hash) => {
  console.log('移动端导航:', hash) // 调试日志
  console.log('当前屏幕宽度:', window.innerWidth)
  console.log('抽屉状态:', drawer.value)
  
  try {
    router.push({ name: 'analyse', params: { userId: hash } })
    drawer.value = false // 关闭移动端抽屉
    console.log('导航成功，抽屉已关闭')
  } catch (error) {
    console.error('导航失败:', error)
  }
}

// 移动端触摸优化
const handleTouchStart = (event) => {
  // 防止双击缩放
  if (event.touches.length > 1) {
    event.preventDefault()
  }
}

// 移动端抽屉开关优化
const toggleDrawer = () => {
  const prevState = drawer.value
  drawer.value = !drawer.value
  console.log('移动端抽屉状态变化:', prevState, '->', drawer.value)
  console.log('当前屏幕宽度:', window.innerWidth)
  
  // 强制刷新DOM
  if (drawer.value) {
    setTimeout(() => {
      const drawerEl = document.querySelector('.mobile-drawer')
      if (drawerEl) {
        console.log('抽屉元素找到:', drawerEl)
        drawerEl.style.pointerEvents = 'auto'
        drawerEl.style.userSelect = 'auto'
        drawerEl.style.zIndex = '1200'
      }
    }, 100)
  }
}

// 异步函数：将中文字符串进行 SHA-256 哈希，并转换为十进制数字字符串
async function chineseToNumericHash(text) {
  const encoder = new TextEncoder()
  const data = encoder.encode(text)
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  const hexHash = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('')
  const numericHash = BigInt('0x' + hexHash).toString()
  return numericHash
}

async function fetchData() {
  loading.value = true
  try {
    console.log('开始获取数据...')
    console.log('API端点:', API_ENDPOINTS.HOT_TOPICS)
    console.log('当前位置:', window.location.href)
    console.log('当前端口:', window.location.port)
    console.log('开发环境:', import.meta.env.DEV)
    
    const data = await apiRequest(API_ENDPOINTS.HOT_TOPICS)
    console.log('获取到的原始数据:', data)
    
    if (!data.name || !Array.isArray(data.name)) {
      throw new Error('数据格式不正确: name字段不存在或不是数组')
    }
    
    const items = data.name.map((name, index) => ({
      id: id++,
      text: name,
      hot_value: data.hot_value[index],
      hash: "",
    }))
    
    console.log('处理后的items:', items.length, '条')
    
    for (const item of items) {
      item.hash = await chineseToNumericHash(item.text)
    }
    jsonData.value = items
    console.log('数据设置完成，jsonData.value:', jsonData.value?.length, '条')
  } catch (error) {
    console.error('请求数据失败：', error)
    console.error('错误堆栈:', error.stack)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
  
  // 移动端触摸事件监听
  if ('ontouchstart' in window) {
    document.addEventListener('touchstart', handleTouchStart, { passive: false })
  }
  
  // 移动端视口调试
  if (window.innerWidth <= 768) {
    console.log('移动端模式激活，屏幕宽度:', window.innerWidth)
  }
})

// 监听抽屉状态变化
watch(drawer, (newVal) => {
  console.log('抽屉状态变化:', newVal)
  if (newVal && window.innerWidth <= 768) {
    // 确保移动端抽屉可见和可交互
    setTimeout(() => {
      const drawerElements = [
        '.mobile-drawer',
        '.mobile-drawer .v-navigation-drawer',
        '.mobile-drawer .v-navigation-drawer__content',
        '.mobile-drawer .sidebar-content'
      ]
      
      drawerElements.forEach(selector => {
        const element = document.querySelector(selector)
        if (element) {
          element.style.pointerEvents = 'auto'
          element.style.userSelect = 'auto'
          element.style.opacity = '1'
          element.style.visibility = 'visible'
          console.log('强制设置元素样式:', selector)
        }
      })
    }, 50)
  }
})
</script>

<style scoped>
/* 全局移动端修复 */
.v-application {
  overflow-x: hidden !important;
}

.v-overlay-container {
  z-index: 1100 !important;
}

.v-overlay--active {
  z-index: 1199 !important;
}

.v-navigation-drawer--temporary {
  z-index: 1200 !important;
  pointer-events: auto !important;
}

.v-navigation-drawer--temporary .v-navigation-drawer__content {
  pointer-events: auto !important;
  user-select: auto !important;
  -webkit-user-select: auto !important;
}

/* 强制移动端抽屉可见 */
@media (max-width: 768px) {
  .v-navigation-drawer--temporary {
    pointer-events: auto !important;
    user-select: auto !important;
    -webkit-user-select: auto !important;
    opacity: 1 !important;
    visibility: visible !important;
  }
  
  .v-navigation-drawer--temporary.v-navigation-drawer--active {
    opacity: 1 !important;
    visibility: visible !important;
    transform: translateX(0) !important;
  }
}

.app-bar {
  backdrop-filter: blur(20px) !important;
  background: rgba(255, 255, 255, 0.9) !important;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.main-content {
  background: linear-gradient(135deg, 
    rgba(248, 251, 255, 0.95) 0%, 
    rgba(227, 242, 253, 0.9) 30%,
    rgba(240, 248, 255, 0.95) 70%,
    rgba(248, 251, 255, 1) 100%);
  min-height: 100vh;
}

.sidebar {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(102, 126, 234, 0.08);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.06);
}

.sidebar-content {
  padding: 2rem;
  height: 100vh;
  overflow-y: auto;
}

.section-header {
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 1.5rem 0;
  margin: -1rem 0 1.5rem 0;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.trend-list {
  background: transparent !important;
}

.trend-item {
  margin-bottom: 0.75rem;
  border-radius: 20px !important;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(102, 126, 234, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

.trend-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.05), transparent);
  transition: left 0.6s ease;
}

.trend-item:hover::before {
  left: 100%;
}

.trend-item:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.15);
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(102, 126, 234, 0.2);
}

.trend-item.rank-1:hover {
  box-shadow: 0 16px 40px rgba(255, 193, 7, 0.25);
  border-color: rgba(255, 193, 7, 0.3);
}

.trend-item.rank-2:hover {
  box-shadow: 0 16px 40px rgba(108, 117, 125, 0.25);
  border-color: rgba(108, 117, 125, 0.3);
}

.trend-item.rank-3:hover {
  box-shadow: 0 16px 40px rgba(205, 127, 50, 0.25);
  border-color: rgba(205, 127, 50, 0.3);
}

.rank-badge {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  margin-right: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.rank-badge.top-rank {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #b45309;
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
  animation: pulse 2s infinite;
}

.rank-badge.high-rank {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.rank-badge.normal-rank {
  background: linear-gradient(135deg, #e2e8f0, #f1f5f9);
  color: #64748b;
  box-shadow: 0 4px 12px rgba(100, 116, 139, 0.2);
}

.trend-title {
  font-weight: 600;
  line-height: 1.5;
  color: #1e293b;
  letter-spacing: -0.01em;
}

.content-area {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
}

.content-wrapper {
  padding: 2rem;
  height: 100vh;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 响应式设计 */
@media (max-width: 960px) {
  .sidebar-content {
    padding: 1rem;
  }
  
  .content-wrapper {
    padding: 1rem;
  }
  
  .trend-item {
    border-radius: 16px !important;
  }
  
  .rank-badge {
    width: 32px;
    height: 32px;
    margin-right: 12px;
    font-size: 12px;
  }
}

/* 移动端特定样式 - 全面重写 */
@media (max-width: 768px) {
  .app-bar {
    position: fixed !important;
    z-index: 1001 !important;
  }
  
  .main-content {
    padding-top: 56px !important;
  }
  
  /* 移动端抽屉样式 - 强制覆盖 */
  .mobile-drawer {
    z-index: 1200 !important;
  }
  
  .mobile-drawer .v-overlay__scrim {
    background-color: rgba(0, 0, 0, 0.6) !important;
    opacity: 1 !important;
    z-index: 1199 !important;
  }
  
  .mobile-drawer .v-navigation-drawer {
    z-index: 1201 !important;
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(20px) !important;
    border: none !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    pointer-events: auto !important;
    user-select: auto !important;
  }
  
  .mobile-drawer .v-navigation-drawer__content {
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(20px) !important;
    border-right: none !important;
    box-shadow: none !important;
    height: 100vh !important;
    width: 100% !important;
    overflow: visible !important;
    pointer-events: auto !important;
    user-select: auto !important;
    position: relative !important;
    z-index: 1 !important;
  }
  
  .mobile-drawer .sidebar-content {
    padding: 16px !important;
    height: 100vh !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    overscroll-behavior: contain !important;
    position: relative !important;
    z-index: 2 !important;
    pointer-events: auto !important;
    user-select: auto !important;
    background: transparent !important;
  }
  
  .mobile-drawer .section-header {
    position: sticky !important;
    top: 0 !important;
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(20px) !important;
    padding: 16px 0 !important;
    margin: -16px 0 16px 0 !important;
    border-radius: 12px !important;
    z-index: 10 !important;
    border: 1px solid rgba(102, 126, 234, 0.1) !important;
    pointer-events: auto !important;
  }
  
  .mobile-drawer .trend-list {
    background: transparent !important;
    padding: 0 !important;
    pointer-events: auto !important;
  }
  
  .mobile-drawer .trend-item {
    margin-bottom: 12px !important;
    border-radius: 12px !important;
    min-height: 64px !important;
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(102, 126, 234, 0.15) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    cursor: pointer !important;
    user-select: none !important;
    -webkit-tap-highlight-color: rgba(102, 126, 234, 0.2) !important;
    touch-action: manipulation !important;
    pointer-events: auto !important;
    transition: all 0.2s ease !important;
    position: relative !important;
    z-index: 1 !important;
  }
  
  .mobile-drawer .trend-item:hover,
  .mobile-drawer .trend-item:focus,
  .mobile-drawer .trend-item:active {
    background: rgba(102, 126, 234, 0.1) !important;
    border-color: rgba(102, 126, 234, 0.3) !important;
    transform: scale(0.98) !important;
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2) !important;
  }
  
  .mobile-drawer .trend-item .v-list-item__content {
    pointer-events: auto !important;
  }
  
  .mobile-drawer .trend-title {
    font-size: 14px !important;
    line-height: 1.4 !important;
    color: #1e293b !important;
    font-weight: 600 !important;
    pointer-events: auto !important;
  }
  
  .mobile-drawer .rank-badge {
    width: 28px !important;
    height: 28px !important;
    font-size: 11px !important;
    margin-right: 8px !important;
    pointer-events: auto !important;
  }
  
  .mobile-drawer .v-chip {
    pointer-events: auto !important;
  }
  
  .content-wrapper {
    padding: 16px !important;
    height: calc(100vh - 56px) !important;
    overflow-y: auto !important;
  }
  
  /* 移动端安全滚动 */
  .mobile-scroll {
    -webkit-overflow-scrolling: touch !important;
    overscroll-behavior: contain !important;
  }
  
  /* 移动端触摸优化 */
  .trend-item {
    -webkit-tap-highlight-color: transparent !important;
    touch-action: manipulation !important;
  }
  
  .trend-item:active {
    transform: scale(0.98) !important;
    transition: transform 0.1s ease !important;
  }
  
  /* 移动端状态优化 */
  .v-progress-linear {
    height: 3px !important;
  }
  
  .v-chip--size-x-small {
    height: 20px !important;
    font-size: 10px !important;
  }
}

/* 极窄屏幕优化 (小于400px) */
@media (max-width: 400px) {
  .mobile-drawer .sidebar-content {
    padding: 12px !important;
  }
  
  .mobile-drawer .section-header {
    padding: 12px 0 !important;
    margin: -12px 0 12px 0 !important;
  }
  
  .mobile-drawer .trend-item {
    min-height: 56px !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
  }
  
  .mobile-drawer .trend-title {
    font-size: 13px !important;
    line-height: 1.3 !important;
  }
  
  .mobile-drawer .rank-badge {
    width: 24px !important;
    height: 24px !important;
    font-size: 10px !important;
    margin-right: 6px !important;
  }
  
  .content-wrapper {
    padding: 12px !important;
  }
  
  .v-chip--size-x-small {
    height: 18px !important;
    font-size: 9px !important;
    padding: 0 6px !important;
  }
  
  .gradient-text {
    font-size: 1.1rem !important;
  }
  
  .v-app-bar .v-container {
    padding: 8px 12px !important;
  }
}

/* 超窄屏幕优化 (小于360px) */
@media (max-width: 360px) {
  .mobile-drawer .trend-title {
    font-size: 12px !important;
    line-height: 1.2 !important;
  }
  
  .mobile-drawer .rank-badge {
    width: 22px !important;
    height: 22px !important;
    font-size: 9px !important;
  }
  
  .gradient-text {
    font-size: 1rem !important;
  }
}

/* 深色主题适配 */
.v-theme--dark .app-bar {
  background: rgba(30, 41, 59, 0.9) !important;
  border-bottom-color: rgba(102, 126, 234, 0.2) !important;
}

.v-theme--dark .sidebar {
  background: rgba(30, 41, 59, 0.85);
  border-right-color: rgba(102, 126, 234, 0.15);
}

/* 深色主题移动端抽屉 */
.v-theme--dark .mobile-drawer .v-navigation-drawer {
  background: rgba(30, 41, 59, 0.98) !important;
}

.v-theme--dark .mobile-drawer .v-navigation-drawer__content {
  background: rgba(30, 41, 59, 0.98) !important;
}

.v-theme--dark .mobile-drawer .sidebar-content {
  background: transparent !important;
}

.v-theme--dark .mobile-drawer .section-header {
  background: rgba(30, 41, 59, 0.98) !important;
  border-color: rgba(102, 126, 234, 0.2) !important;
}

.v-theme--dark .mobile-drawer .trend-item {
  background: rgba(51, 65, 85, 0.95) !important;
  border-color: rgba(102, 126, 234, 0.2) !important;
  color: #e2e8f0 !important;
}

.v-theme--dark .mobile-drawer .trend-item:hover,
.v-theme--dark .mobile-drawer .trend-item:focus,
.v-theme--dark .mobile-drawer .trend-item:active {
  background: rgba(102, 126, 234, 0.15) !important;
  border-color: rgba(102, 126, 234, 0.4) !important;
}

.v-theme--dark .mobile-drawer .trend-title {
  color: #e2e8f0 !important;
}

.v-theme--dark .trend-item {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(102, 126, 234, 0.15);
  color: #e2e8f0;
}

.v-theme--dark .trend-item:hover {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(102, 126, 234, 0.3);
}

.v-theme--dark .content-area {
  background: rgba(15, 23, 42, 0.5);
}

.v-theme--dark .section-header {
  background: rgba(30, 41, 59, 0.95);
}

.v-theme--dark .trend-title {
  color: #e2e8f0;
}

/* 按钮美化 */
.v-btn {
  border-radius: 12px !important;
  text-transform: none !important;
  font-weight: 600 !important;
  letter-spacing: 0.01em !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.v-btn:hover {
  transform: translateY(-2px) !important;
}

.v-btn--variant-outlined {
  border-width: 2px !important;
}

/* 芯片美化 */
.v-chip {
  border-radius: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.01em !important;
}

/* 进度条美化 */
.v-progress-linear {
  border-radius: 8px !important;
  overflow: hidden !important;
}

.v-progress-linear__determinate {
  background: linear-gradient(90deg, #667eea, #764ba2) !important;
}

/* 图标动画 */
.v-icon {
  transition: all 0.3s ease !important;
}

.trend-item:hover .v-icon {
  transform: scale(1.1);
}
</style>



<template>
  <v-app>    <!-- 移动端导航抽屉 -->
    <v-navigation-drawer
      v-model="drawer"
      temporary
      location="left"
      :width="$vuetify.display.width < 400 ? Math.max($vuetify.display.width - 40, 280) : 320"
      class="mobile-drawer"
      :scrim="true"
      elevation="24"
      :touchless="false"
      :disable-resize-watcher="false"
      :disable-route-watcher="false"
      :expand-on-hover="false"
      :floating="false"
      :mini-variant="false"
      :permanent="false"
      :rail="false"
      :absolute="false"
      style="z-index: 1200 !important;"
    >      <div class="sidebar-content mobile-scroll">
        <div class="section-header glass-effect">
          <h2 class="text-h6 font-weight-bold mb-4">
            <v-icon class="me-2 pulse" color="error" size="24">mdi-fire</v-icon>
            今日知乎热点
            <v-chip 
              class="ml-2" 
              color="success" 
              variant="flat" 
              size="x-small"
            >
              实时
            </v-chip>
          </h2>
        </div>

        <v-progress-linear
          v-if="loading"
          indeterminate
          color="primary"
          class="mb-4"
          height="4"
          rounded
        ></v-progress-linear>

        <v-list class="trend-list" v-if="jsonData">
          <v-list-item
            v-for="(item, index) in jsonData"
            :key="item.id"
            class="trend-item floating-card"
            :class="`rank-${index + 1}`"
            @click="navigateToAnalyse(item.hash)"
          >
            <template v-slot:prepend>
              <div class="rank-badge" :class="getRankClass(index + 1)">
                {{ index + 1 }}
              </div>
            </template>

            <v-list-item-title class="trend-title">
              {{ item.text }}
            </v-list-item-title>

            <template v-slot:append>
              <v-chip
                color="error"
                variant="tonal"
                size="x-small"
                prepend-icon="mdi-fire"
                class="font-weight-bold"
              >
                {{ formatHotValue(item.hot_value) }}
              </v-chip>
            </template>
          </v-list-item>
        </v-list>
      </div>
    </v-navigation-drawer>

    <!-- 导航栏 -->
    <v-app-bar
      elevation="0"
      color="surface"
      class="app-bar"
      :height="$vuetify.display.mobile ? 56 : 80"
    >
      <v-container class="d-flex align-center" :class="{ 'pa-4': $vuetify.display.mobile }">        <!-- 移动端菜单按钮 -->
        <v-btn
          v-if="$vuetify.display.mobile"
          icon
          @click="toggleDrawer"
          color="primary"
          variant="text"
          class="me-2"
          :ripple="false"
        >
          <v-icon>mdi-menu</v-icon>
        </v-btn>
        
        <div class="d-flex align-center">
          <v-icon 
            :size="$vuetify.display.mobile ? 28 : 40" 
            color="primary" 
            class="me-2 wobble"
          >
            mdi-chart-line-variant
          </v-icon>
          <h1 
            :class="$vuetify.display.mobile ? 'text-h6' : 'text-h4'"
            class="font-weight-bold gradient-text"
          >
            {{ $vuetify.display.mobile ? '数据洞察' : '社交数据洞察' }}
          </h1>
          <v-chip 
            v-if="!$vuetify.display.mobile"
            class="ml-3" 
            color="accent" 
            variant="outlined" 
            size="small"
            prepend-icon="mdi-beta"
          >
            Beta
          </v-chip>
        </div>
        
        <v-spacer></v-spacer>
        
        <div class="d-flex align-center" :class="$vuetify.display.mobile ? 'ga-2' : 'ga-4'">
          <v-btn
            icon
            @click="toggleTheme"
            color="primary"
            variant="outlined"
            class="modern-btn"
            :size="$vuetify.display.mobile ? 'default' : 'large'"
          >
            <v-icon :size="$vuetify.display.mobile ? 20 : 24">
              {{ theme.global.current.value.dark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}
            </v-icon>
          </v-btn>
          
          <v-btn
            v-if="!$vuetify.display.mobile"
            color="primary"
            variant="elevated"
            prepend-icon="mdi-refresh"
            @click="fetchData"
            :loading="loading"
            class="modern-btn"
            size="large"
          >
            刷新数据
          </v-btn>
          
          <v-btn
            v-else
            icon
            color="primary"
            variant="outlined"
            @click="fetchData"
            :loading="loading"
            class="modern-btn"
          >
            <v-icon size="20">mdi-refresh</v-icon>
          </v-btn>
        </div>
      </v-container>
    </v-app-bar>    <!-- 主要内容 -->
    <v-main class="main-content">
      <v-container fluid class="pa-0">
        <v-row no-gutters class="fill-height">
          <!-- 桌面端热点列表侧边栏 -->
          <v-col 
            v-if="!$vuetify.display.mobile" 
            cols="12" 
            md="5" 
            lg="4" 
            class="sidebar"
          >
            <div class="sidebar-content mobile-scroll">
              <div class="section-header glass-effect">
                <h2 class="text-h5 font-weight-bold mb-4">
                  <v-icon class="me-2 pulse" color="error" size="28">mdi-fire</v-icon>
                  今日知乎热点
                  <v-chip 
                    class="ml-2" 
                    color="success" 
                    variant="flat" 
                    size="x-small"
                  >
                    实时
                  </v-chip>
                </h2>
              </div>

              <v-progress-linear
                v-if="loading"
                indeterminate
                color="primary"
                class="mb-4"
                height="4"
                rounded
              ></v-progress-linear>

              <v-list class="trend-list" v-if="jsonData">
                <v-list-item
                  v-for="(item, index) in jsonData"
                  :key="item.id"
                  class="trend-item floating-card"
                  :class="`rank-${index + 1}`"
                  @click="$router.push({ name: 'analyse', params: { userId: item.hash } })"
                >
                  <template v-slot:prepend>
                    <div class="rank-badge" :class="getRankClass(index + 1)">
                      {{ index + 1 }}
                    </div>
                  </template>

                  <v-list-item-title class="trend-title">
                    {{ item.text }}
                  </v-list-item-title>

                  <template v-slot:append>
                    <v-chip
                      color="error"
                      variant="tonal"
                      size="small"
                      prepend-icon="mdi-fire"
                      class="font-weight-bold"
                    >
                      {{ formatHotValue(item.hot_value) }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>

              <v-empty-state
                v-if="!loading && !jsonData"
                icon="mdi-database-off-outline"
                title="暂无数据"
                text="请检查网络连接或稍后重试"
                class="glass-effect"
              >
                <template v-slot:actions>
                  <v-btn
                    color="primary"
                    variant="elevated"
                    @click="fetchData"
                    class="modern-btn"
                    prepend-icon="mdi-refresh"
                  >
                    重新加载
                  </v-btn>
                </template>
              </v-empty-state>
            </div>
          </v-col>

          <!-- 详情内容区域 -->
          <v-col 
            cols="12" 
            :md="$vuetify.display.mobile ? 12 : 7" 
            :lg="$vuetify.display.mobile ? 12 : 8" 
            class="content-area"
          >
            <div class="content-wrapper mobile-scroll">
              <RouterView v-slot="{ Component }">
                <transition name="fade-slide" mode="out-in">
                  <component :is="Component" />
                </transition>
              </RouterView>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

