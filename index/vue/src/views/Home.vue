<script setup>
import { marked } from 'marked'
import { ref, onMounted, computed } from 'vue'

const topic_classified = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    loading.value = true
    const response = await fetch('doc/hot_list_analyse.md')
    topic_classified.value = await response.text()
  } catch (error) {
    console.error('读取markdown文件出错:', error)
  } finally {
    loading.value = false
  }
})

const htmlContent = computed(() => marked(topic_classified.value))
</script>

<template>
  <div class="home-container">
    <!-- 欢迎横幅 -->
    <transition name="slide" appear>
      <v-card class="welcome-banner mb-6 glass-effect floating-card" rounded="xl" elevation="0">
        <v-card-text class="pa-6">
          <v-row align="center">
            <v-col cols="12" md="8">
              <h1 class="text-h3 font-weight-bold gradient-text mb-3">
                探索数据背后的洞察
              </h1>
              <p class="text-h6 text-medium-emphasis mb-4">
                基于先进的AI算法分析社交媒体热点趋势，为您呈现最有价值的数据洞察
              </p>
              <div class="d-flex ga-2 flex-wrap">
                <v-chip color="primary" variant="flat" prepend-icon="mdi-trending-up">实时数据</v-chip>
                <v-chip color="secondary" variant="flat" prepend-icon="mdi-robot">AI分析</v-chip>
                <v-chip color="accent" variant="flat" prepend-icon="mdi-chart-line">可视化</v-chip>
              </div>
            </v-col>
            <v-col cols="12" md="4" class="text-center">
              <v-icon 
                size="120" 
                color="primary" 
                class="rotating-icon opacity-80"
              >
                mdi-chart-bubble
              </v-icon>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </transition>

    <!-- 话题分类卡片 -->
    <transition name="slide" appear style="transition-delay: 0.1s">
      <v-card class="mb-6 glass-effect floating-card" rounded="xl" elevation="0">
        <v-card-title class="d-flex align-center pa-6">
          <v-icon start color="primary" size="32" class="wobble">mdi-tag-multiple-outline</v-icon>
          <span class="text-h5 font-weight-bold gradient-text">话题分类分析</span>
          <v-spacer></v-spacer>
          <v-chip color="info" variant="tonal" size="small" prepend-icon="mdi-update">
            实时更新
          </v-chip>
        </v-card-title>
        
        <v-divider class="mx-6"></v-divider>
        
        <v-card-text class="pa-6">
          <transition name="fade" mode="out-in">
            <div v-if="loading" class="text-center py-8">
              <v-progress-circular
                indeterminate
                color="primary"
                size="48"
                width="4"
              ></v-progress-circular>
              <p class="text-h6 mt-4 text-medium-emphasis">分析中...</p>
            </div>
            
            <div 
              v-else
              class="topic-content markdown-content fade-enter-active"
              v-html="htmlContent"
            ></div>
          </transition>
        </v-card-text>
      </v-card>
    </transition>

    <!-- 数据可视化卡片 -->
    <transition name="slide" appear style="transition-delay: 0.2s">
      <v-card class="glass-effect floating-card" rounded="xl" elevation="0">
        <v-card-title class="d-flex align-center pa-6">
          <v-icon start color="success" size="32" class="rotating-icon">mdi-chart-line-variant</v-icon>
          <span class="text-h5 font-weight-bold gradient-text">数据可视化面板</span>
          <v-spacer></v-spacer>
          <v-chip color="success" variant="tonal" size="small" prepend-icon="mdi-chart-areaspline">
            多维分析
          </v-chip>
        </v-card-title>
        
        <v-divider class="mx-6"></v-divider>
        
        <v-card-text class="pa-6">
          <v-row>
            <!-- 关注者折线图 -->
            <v-col cols="12" lg="4" class="mb-4">
              <transition name="bounce" appear style="transition-delay: 0.3s">
                <v-card variant="outlined" class="chart-card ripple glow soft-shadow" rounded="lg">
                  <v-card-subtitle class="pa-4 d-flex align-center">
                    <v-icon start color="info" size="20" class="pulse">mdi-account-group-outline</v-icon>
                    <span class="font-weight-bold">关注者趋势</span>
                    <v-spacer></v-spacer>
                    <v-chip color="info" variant="text" size="x-small">+12.5%</v-chip>                  </v-card-subtitle>
                  <v-img
                    src="/images/关注者折线图.png"
                    alt="关注者折线图"
                    class="chart-image"
                    cover
                  >
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="primary" size="32"></v-progress-circular>
                      </v-row>
                    </template>
                    <template v-slot:error>                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <div class="text-center pa-4">
                          <v-icon size="48" color="grey-lighten-1">mdi-image-broken-variant</v-icon>
                          <p class="text-caption mt-2">图片加载失败</p>
                        </div>
                      </v-row>
                    </template>
                  </v-img>
                  <v-card-actions class="pa-4">
                    <v-btn 
                      color="info" 
                      variant="text" 
                      size="small"
                      prepend-icon="mdi-eye-outline"
                    >
                      查看详情
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </transition>
            </v-col>

            <!-- 热度折线图 -->
            <v-col cols="12" lg="4" class="mb-4">
              <transition name="bounce" appear style="transition-delay: 0.4s">
                <v-card variant="outlined" class="chart-card ripple glow soft-shadow" rounded="lg">
                  <v-card-subtitle class="pa-4 d-flex align-center">
                    <v-icon start color="error" size="20" class="pulse">mdi-fire</v-icon>
                    <span class="font-weight-bold">热度趋势</span>
                    <v-spacer></v-spacer>
                    <v-chip color="error" variant="text" size="x-small">+8.3%</v-chip>                  </v-card-subtitle>
                  <v-img
                    src="/images/热度折线图.png"
                    alt="热度折线图"
                    class="chart-image"
                    cover
                  >
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="primary" size="32"></v-progress-circular>
                      </v-row>
                    </template>
                    <template v-slot:error>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <div class="text-center pa-4">
                          <v-icon size="48" color="grey-lighten-1">mdi-image-broken-variant</v-icon>
                          <p class="text-caption mt-2">图片加载失败</p>
                        </div>
                      </v-row>
                    </template>
                  </v-img>
                  <v-card-actions class="pa-4">
                    <v-btn 
                      color="error" 
                      variant="text" 
                      size="small"
                      prepend-icon="mdi-eye-outline"
                    >
                      查看详情
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </transition>
            </v-col>

            <!-- 总回答数折线图 -->
            <v-col cols="12" lg="4" class="mb-4">
              <transition name="bounce" appear style="transition-delay: 0.5s">
                <v-card variant="outlined" class="chart-card ripple glow soft-shadow" rounded="lg">
                  <v-card-subtitle class="pa-4 d-flex align-center">
                    <v-icon start color="warning" size="20" class="pulse">mdi-comment-multiple-outline</v-icon>
                    <span class="font-weight-bold">回答数趋势</span>
                    <v-spacer></v-spacer>
                    <v-chip color="warning" variant="text" size="x-small">+15.7%</v-chip>                  </v-card-subtitle>
                  <v-img
                    src="/images/总回答数折线图.png"
                    alt="总回答数折线图"
                    class="chart-image"
                    cover
                  >
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="primary" size="32"></v-progress-circular>
                      </v-row>
                    </template>
                    <template v-slot:error>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <div class="text-center pa-4">
                          <v-icon size="48" color="grey-lighten-1">mdi-image-broken-variant</v-icon>
                          <p class="text-caption mt-2">图片加载失败</p>
                        </div>
                      </v-row>
                    </template>
                  </v-img>
                  <v-card-actions class="pa-4">
                    <v-btn 
                      color="warning" 
                      variant="text" 
                      size="small"
                      prepend-icon="mdi-eye-outline"
                    >
                      查看详情
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </transition>
            </v-col>          </v-row>
        </v-card-text>
      </v-card>
    </transition>
  </div>
</template>

<style scoped>
.home-container {
  height: 100%;
  overflow-y: auto;
}

.welcome-banner {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.05) 0%, 
    rgba(118, 75, 162, 0.05) 50%,
    rgba(78, 205, 196, 0.05) 100%) !important;
  border: 1px solid rgba(102, 126, 234, 0.1) !important;
}

.chart-card {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(102, 126, 234, 0.1) !important;
  overflow: hidden;
  position: relative;
}

.chart-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.03), transparent);
  transition: left 0.6s ease;
  z-index: 1;
}

.chart-card:hover::before {
  left: 100%;
}

.chart-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.15) !important;
  border-color: rgba(102, 126, 234, 0.2) !important;
}

.chart-image {
  border-radius: 12px;
  max-height: 240px;
  transition: all 0.3s ease;
}

.chart-card:hover .chart-image {
  transform: scale(1.02);
}

.markdown-content {
  line-height: 1.8;
  font-size: 1rem;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.markdown-content h1 {
  font-size: 1.75rem;
}

.markdown-content h2 {
  font-size: 1.5rem;
}

.markdown-content h3 {
  font-size: 1.25rem;
}

.markdown-content p {
  margin-bottom: 1.5rem;
  text-align: justify;
  color: #475569;
  line-height: 1.8;
}

.markdown-content ul,
.markdown-content ol {
  padding-left: 2rem;
  margin-bottom: 1.5rem;
}

.markdown-content li {
  margin-bottom: 0.75rem;
  color: #64748b;
  line-height: 1.7;
}

.markdown-content li::marker {
  color: #667eea;
}

.markdown-content code {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  color: #667eea;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 0.9em;
  font-weight: 600;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.markdown-content pre {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  padding: 1.5rem;
  border-radius: 12px;
  overflow-x: auto;
  margin: 2rem 0;
  border: 1px solid rgba(102, 126, 234, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.markdown-content pre code {
  background: none;
  padding: 0;
  border: none;
  color: #334155;
}

.markdown-content blockquote {
  border-left: 4px solid #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: #64748b;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.markdown-content th,
.markdown-content td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.markdown-content th {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-weight: 600;
}

.markdown-content tr:nth-child(even) {
  background: rgba(102, 126, 234, 0.02);
}

.markdown-content tr:hover {
  background: rgba(102, 126, 234, 0.05);
}

/* 深色主题适配 */
.v-theme--dark .markdown-content p {
  color: #cbd5e1;
}

.v-theme--dark .markdown-content li {
  color: #94a3b8;
}

.v-theme--dark .markdown-content code {
  background: linear-gradient(135deg, #334155, #475569);
  color: #a5b4fc;
  border-color: rgba(165, 180, 252, 0.2);
}

.v-theme--dark .markdown-content pre {
  background: linear-gradient(135deg, #1e293b, #334155);
  border-color: rgba(165, 180, 252, 0.2);
}

.v-theme--dark .markdown-content pre code {
  color: #e2e8f0;
}

.v-theme--dark .markdown-content blockquote {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  color: #94a3b8;
  border-color: #818cf8;
}

.v-theme--dark .chart-card {
  border-color: rgba(148, 163, 184, 0.2) !important;
}

.v-theme--dark .chart-card:hover {
  border-color: rgba(129, 140, 248, 0.3) !important;
}

/* 动画增强 */
.chart-card .v-card-actions {
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
}

.chart-card:hover .v-card-actions {
  opacity: 1;
  transform: translateY(0);
}

/* 统计芯片样式 */
.v-chip.v-chip--variant-text {
  font-weight: 700;
  letter-spacing: 0.02em;
}

/* 渐变边框效果 */
.gradient-border {
  position: relative;
  border-radius: 12px;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #667eea, #764ba2) border-box;
  border: 2px solid transparent;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .welcome-banner .text-h3 {
    font-size: 1.75rem !important;
  }
  
  .welcome-banner .text-h6 {
    font-size: 1.1rem !important;
  }
  
  .chart-image {
    max-height: 200px;
  }
  
  .markdown-content {
    font-size: 0.95rem;
  }
}
</style>