<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useTheme } from 'vuetify'

const theme = useTheme()

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
    const response = await fetch('http://localhost:5251/api/hot')
    const data = await response.json()
    const items = data.name.map((name, index) => ({
      id: id++,
      text: name,
      hot_value: data.hot_value[index],
      hash: "",
    }))
    
    for (const item of items) {
      item.hash = await chineseToNumericHash(item.text)
    }
    jsonData.value = items
  } catch (error) {
    console.error('请求数据失败：', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
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



<template>  <v-app>
    <!-- 导航栏 -->
    <v-app-bar
      elevation="0"
      color="surface"
      class="app-bar"
      height="80"
    >
      <v-container class="d-flex align-center">
        <div class="d-flex align-center">
          <v-icon size="40" color="primary" class="me-3 wobble">mdi-chart-line-variant</v-icon>
          <h1 class="text-h4 font-weight-bold gradient-text">
            社交数据洞察
          </h1>
          <v-chip 
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
        
        <div class="d-flex align-center ga-4">
          <v-btn
            icon
            @click="toggleTheme"
            color="primary"
            variant="outlined"
            class="modern-btn"
            size="large"
          >
            <v-icon>{{ theme.global.current.value.dark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
          </v-btn>
          
          <v-btn
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
        </div>
      </v-container>
    </v-app-bar>

    <!-- 主要内容 -->
    <v-main class="main-content">
      <v-container fluid class="pa-0">
        <v-row no-gutters class="fill-height">
          <!-- 热点列表侧边栏 -->
          <v-col cols="12" md="5" lg="4" class="sidebar">
            <div class="sidebar-content">
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
          <v-col cols="12" md="7" lg="8" class="content-area">
            <div class="content-wrapper">
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

