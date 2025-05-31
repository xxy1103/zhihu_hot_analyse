<script setup>
import { marked } from 'marked'
import { ref, onMounted, computed } from 'vue'

const topic_classified = ref('')
const loading = ref(true)

// 图片预览相关状态
const imageDialog = ref(false)
const selectedImage = ref({
  src: '',
  alt: '',
  title: ''
})

// 打开图片预览
const openImagePreview = (src, alt, title) => {
  selectedImage.value = {
    src,
    alt,
    title
  }
  imageDialog.value = true
}

// 关闭图片预览
const closeImagePreview = () => {
  imageDialog.value = false
  selectedImage.value = {
    src: '',
    alt: '',
    title: ''
  }
}

// 下载图片
const downloadImage = () => {
  const link = document.createElement('a')
  link.href = selectedImage.value.src
  link.download = selectedImage.value.alt + '.png'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

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
        <v-card-text class="pa-8">
          <v-row align="center">
            <v-col cols="12" md="8">
              <h1 class="text-h3 font-weight-bold gradient-text mb-4">
                🚀 欢迎使用社交数据洞察平台
              </h1>
              <p class="text-h6 mb-4" style="color: #64748b; line-height: 1.6;">
                实时追踪知乎热点，深度分析社交媒体趋势，为您提供数据驱动的洞察分析
              </p>
              <div class="d-flex ga-3 flex-wrap">
                <v-chip color="primary" variant="tonal" prepend-icon="mdi-trending-up">
                  实时数据
                </v-chip>
                <v-chip color="secondary" variant="tonal" prepend-icon="mdi-chart-line">
                  趋势分析
                </v-chip>
                <v-chip color="accent" variant="tonal" prepend-icon="mdi-robot">
                  AI总结
                </v-chip>
              </div>
            </v-col>
            <v-col cols="12" md="4" class="text-center">
              <v-avatar size="120" class="elevation-8">
                <v-icon size="60" color="primary">mdi-chart-bubble</v-icon>
              </v-avatar>
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
          <v-chip color="success" variant="outlined" size="small" prepend-icon="mdi-check-circle">
            已更新
          </v-chip>
        </v-card-title>
        
        <v-divider class="mx-6" style="border-color: rgba(102, 126, 234, 0.1);"></v-divider>
        
        <v-card-text class="pa-6">
          <transition name="fade" mode="out-in">
            <div v-if="loading" class="text-center py-8">
              <v-progress-circular
                indeterminate
                color="primary"
                size="48"
                class="mb-4"
              ></v-progress-circular>
              <p class="text-body-1">正在加载话题分析...</p>
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
          <v-chip color="info" variant="outlined" size="small" prepend-icon="mdi-clock-outline">
            实时更新
          </v-chip>
        </v-card-title>
        
        <v-divider class="mx-6" style="border-color: rgba(102, 126, 234, 0.1);"></v-divider>
        
        <v-card-text class="pa-6">
          <v-row>
            <!-- 关注者折线图 -->
            <v-col cols="12" lg="4" class="mb-4">
              <transition name="bounce" appear style="transition-delay: 0.3s">
                <v-card variant="outlined" class="chart-card ripple glow soft-shadow gradient-border" rounded="lg">
                  <v-card-subtitle class="pa-4 d-flex align-center">
                    <v-icon start color="info" size="20" class="pulse">mdi-account-group-outline</v-icon>
                    <span class="font-weight-bold">关注者趋势</span>
                    <v-spacer></v-spacer>
                    <v-chip color="info" variant="text" size="x-small">+12.5%</v-chip>                  </v-card-subtitle>                  <v-img
                    src="/images/关注者折线图.png"
                    alt="关注者折线图"
                    class="chart-image clickable-image"
                    cover
                    @click="openImagePreview('/images/关注者折线图.png', '关注者折线图', '关注者趋势分析')"
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
                      color="info" 
                      variant="text" 
                      size="small"
                      prepend-icon="mdi-eye-outline"
                      class="modern-btn"
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
                <v-card variant="outlined" class="chart-card ripple glow soft-shadow gradient-border" rounded="lg">
                  <v-card-subtitle class="pa-4 d-flex align-center">
                    <v-icon start color="error" size="20" class="pulse">mdi-fire</v-icon>
                    <span class="font-weight-bold">热度趋势</span>
                    <v-spacer></v-spacer>
                    <v-chip color="error" variant="text" size="x-small">+8.3%</v-chip>                  </v-card-subtitle>                  <v-img
                    src="/images/热度折线图.png"
                    alt="热度折线图"
                    class="chart-image clickable-image"
                    cover
                    @click="openImagePreview('/images/热度折线图.png', '热度折线图', '热度趋势分析')"
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
                      class="modern-btn"
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
                <v-card variant="outlined" class="chart-card ripple glow soft-shadow gradient-border" rounded="lg">
                  <v-card-subtitle class="pa-4 d-flex align-center">
                    <v-icon start color="warning" size="20" class="pulse">mdi-comment-multiple-outline</v-icon>
                    <span class="font-weight-bold">回答数趋势</span>
                    <v-spacer></v-spacer>
                    <v-chip color="warning" variant="text" size="x-small">+15.7%</v-chip>                  </v-card-subtitle>                  <v-img
                    src="/images/总回答数折线图.png"
                    alt="总回答数折线图"
                    class="chart-image clickable-image"
                    cover
                    @click="openImagePreview('/images/总回答数折线图.png', '总回答数折线图', '回答数趋势分析')"
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
                      class="modern-btn"
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

    <!-- 图片预览对话框 -->
    <v-dialog 
      v-model="imageDialog" 
      max-width="90%" 
      max-height="90%"
      class="image-preview-dialog"
    >
      <v-card class="image-preview-card" rounded="xl">
        <v-card-title class="d-flex align-center pa-4">
          <v-icon start color="primary" class="mr-2">mdi-chart-line</v-icon>
          <span class="text-h6 font-weight-bold">{{ selectedImage.title }}</span>
          <v-spacer></v-spacer>
          <v-btn 
            icon="mdi-close" 
            variant="text" 
            @click="closeImagePreview"
          ></v-btn>
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="pa-4">
          <div class="image-container">
            <v-img
              :src="selectedImage.src"
              :alt="selectedImage.alt"
              class="preview-image"
              contain
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
                </v-row>
              </template>
              <template v-slot:error>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <div class="text-center">
                    <v-icon size="64" color="grey-lighten-1">mdi-image-broken-variant</v-icon>
                    <p class="text-body-1 mt-2">图片加载失败</p>
                  </div>
                </v-row>
              </template>
            </v-img>
          </div>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn 
            color="primary" 
            variant="tonal" 
            prepend-icon="mdi-download"
            @click="downloadImage"
          >
            下载图片
          </v-btn>
          <v-btn 
            color="secondary" 
            variant="text" 
            @click="closeImagePreview"
          >
            关闭
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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

/* 可点击图片样式 */
.clickable-image {
  cursor: pointer;
  position: relative;
}

.clickable-image::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(102, 126, 234, 0);
  transition: all 0.3s ease;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clickable-image:hover::after {
  background: rgba(102, 126, 234, 0.1);
}

.clickable-image::before {
  content: '🔍';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 2;
  pointer-events: none;
  color: #667eea;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.clickable-image:hover::before {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1.1);
}

/* 图片预览对话框样式 */
.image-preview-dialog .v-overlay__content {
  max-width: 95vw !important;
  max-height: 95vh !important;
}

.image-preview-card {
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.image-container {
  max-height: 70vh;
  overflow: hidden;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}

.preview-image {
  max-height: 70vh;
  width: 100%;
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
  .home-container {
    padding: 0 !important;
    margin: 0 !important;
  }
  
  .welcome-banner {
    margin: 16px !important;
    border-radius: 16px !important;
  }
  
  .welcome-banner .v-card-text {
    padding: 20px !important;
  }
  
  .welcome-banner .text-h3 {
    font-size: 1.5rem !important;
    line-height: 1.3 !important;
    margin-bottom: 16px !important;
  }
  
  .welcome-banner .text-h6 {
    font-size: 1rem !important;
    line-height: 1.5 !important;
    margin-bottom: 16px !important;
  }
  
  .welcome-banner .v-row {
    flex-direction: column-reverse !important;
  }
  
  .welcome-banner .v-col {
    text-align: center !important;
  }
  
  .welcome-banner .v-avatar {
    width: 80px !important;
    height: 80px !important;
    margin-bottom: 16px !important;
  }
  
  .welcome-banner .v-avatar .v-icon {
    font-size: 40px !important;
  }
  
  .welcome-banner .v-chip {
    height: 24px !important;
    font-size: 11px !important;
    margin: 2px !important;
  }
}

/* 移动端话题分类卡片优化 */
@media (max-width: 768px) {
  .topic-classification-card {
    margin: 16px !important;
    border-radius: 16px !important;
  }
  
  .topic-classification-card .v-card-title {
    padding: 16px !important;
    font-size: 1.1rem !important;
  }
  
  .topic-classification-card .v-card-title .v-icon {
    font-size: 20px !important;
    margin-right: 8px !important;
  }
  
  .topic-classification-card .v-card-text {
    padding: 16px !important;
  }
  
  .topic-classification-card .v-divider {
    margin: 0 16px !important;
  }
}

/* 移动端图表卡片优化 */
@media (max-width: 768px) {
  .chart-section {
    margin: 16px !important;
    border-radius: 16px !important;
  }
  
  .chart-section .v-card-title {
    padding: 16px !important;
    font-size: 1.1rem !important;
  }
  
  .chart-section .v-card-text {
    padding: 16px !important;
  }
  
  .chart-card {
    margin-bottom: 16px !important;
    border-radius: 12px !important;
    border-width: 1px !important;
  }
  
  .chart-card .v-card-subtitle {
    padding: 12px !important;
    font-size: 12px !important;
  }
  
  .chart-card .v-card-subtitle .v-icon {
    font-size: 16px !important;
  }
  
  .chart-card .v-card-actions {
    padding: 12px !important;
  }
  
  .chart-card .v-btn {
    height: 32px !important;
    font-size: 12px !important;
    padding: 0 12px !important;
  }
  
  .chart-image {
    max-height: 180px !important;
    object-fit: cover !important;
  }
  
  .clickable-image {
    cursor: pointer !important;
    -webkit-tap-highlight-color: transparent !important;
    touch-action: manipulation !important;
  }
  
  .clickable-image:active {
    transform: scale(0.98) !important;
    transition: transform 0.1s ease !important;
  }
}

/* 移动端Markdown内容优化 */
@media (max-width: 768px) {
  .markdown-content {
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 0 !important;
  }
  
  .markdown-content h1 {
    font-size: 1.3rem !important;
    margin: 16px 0 12px 0 !important;
    line-height: 1.3 !important;
  }
  
  .markdown-content h2 {
    font-size: 1.2rem !important;
    margin: 14px 0 10px 0 !important;
    line-height: 1.3 !important;
  }
  
  .markdown-content h3 {
    font-size: 1.1rem !important;
    margin: 12px 0 8px 0 !important;
    line-height: 1.3 !important;
  }
  
  .markdown-content p {
    margin: 8px 0 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
  }
  
  .markdown-content ul, 
  .markdown-content ol {
    padding-left: 20px !important;
    margin: 8px 0 !important;
  }
  
  .markdown-content li {
    margin: 4px 0 !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
  }
  
  .markdown-content blockquote {
    border-left: 3px solid #667eea !important;
    padding: 8px 12px !important;
    margin: 12px 0 !important;
    background: rgba(102, 126, 234, 0.05) !important;
    border-radius: 0 8px 8px 0 !important;
    font-style: italic !important;
  }
  
  .markdown-content code {
    background: rgba(102, 126, 234, 0.1) !important;
    padding: 2px 4px !important;
    border-radius: 4px !important;
    font-size: 12px !important;
    font-family: 'Fira Code', monospace !important;
  }
  
  .markdown-content pre {
    background: rgba(102, 126, 234, 0.05) !important;
    padding: 12px !important;
    border-radius: 8px !important;
    overflow-x: auto !important;
    font-size: 12px !important;
    line-height: 1.4 !important;
    font-family: 'Fira Code', monospace !important;
  }
  
  .markdown-content img {
    max-width: 100% !important;
    height: auto !important;
    border-radius: 8px !important;
    margin: 12px 0 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  }
  
  .markdown-content table {
    width: 100% !important;
    font-size: 12px !important;
    border-collapse: collapse !important;
    margin: 12px 0 !important;
    overflow-x: auto !important;
    display: block !important;
    white-space: nowrap !important;
  }
  
  .markdown-content th,
  .markdown-content td {
    padding: 6px 8px !important;
    border: 1px solid rgba(102, 126, 234, 0.2) !important;
    text-align: left !important;
  }
  
  .markdown-content th {
    background: rgba(102, 126, 234, 0.1) !important;
    font-weight: 600 !important;
  }
  
  .markdown-content a {
    color: #667eea !important;
    text-decoration: none !important;
    border-bottom: 1px solid rgba(102, 126, 234, 0.3) !important;
    transition: all 0.2s ease !important;
  }
  
  .markdown-content a:hover {
    color: #5a67d8 !important;
    border-bottom-color: #5a67d8 !important;
  }
}

/* 移动端图片预览对话框优化 */
@media (max-width: 768px) {
  .v-dialog .v-card {
    margin: 16px !important;
    border-radius: 16px !important;
    max-height: 85vh !important;
    overflow-y: auto !important;
  }
  
  .v-dialog .v-card-title {
    padding: 16px !important;
    font-size: 1.1rem !important;
  }
  
  .v-dialog .v-card-text {
    padding: 16px !important;
  }
  
  .v-dialog .v-card-actions {
    padding: 16px !important;
    justify-content: center !important;
  }
  
  .v-dialog .v-btn {
    height: 40px !important;
    border-radius: 20px !important;
    min-width: 120px !important;
  }
  
  .v-dialog img {
    max-width: 100% !important;
    height: auto !important;
    border-radius: 8px !important;
  }
}

/* 移动端加载状态优化 */
@media (max-width: 768px) {
  .loading-state {
    padding: 40px 20px !important;
    text-align: center !important;
  }
  
  .loading-state .v-progress-circular {
    width: 48px !important;
    height: 48px !important;
  }
  
  .loading-state .text-h6 {
    font-size: 1.1rem !important;
    margin-top: 16px !important;
  }
  
  .loading-state .text-body-2 {
    font-size: 14px !important;
    margin-top: 8px !important;
  }
}

/* 移动端动画优化 */
@media (max-width: 768px) {
  .floating-card {
    transform: none !important;
  }
  
  .floating-card:hover {
    transform: none !important;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.1) !important;
  }
  
  .chart-card.ripple::before {
    display: none !important;
  }
  
  .chart-card.glow::after {
    display: none !important;
  }
  
  .gradient-border {
    border-width: 1px !important;
  }
  
  /* 简化动画效果 */
  .v-icon.pulse {
    animation: none !important;
  }
  
  .bounce-enter-active,
  .bounce-leave-active {
    transition: none !important;
  }
  
  .slide-enter-active,
  .slide-leave-active {
    transition: opacity 0.3s ease !important;
  }
}

/* 超小屏幕优化 */
@media (max-width: 375px) {
  .welcome-banner,
  .topic-classification-card,
  .chart-section {
    margin: 12px !important;
  }
  
  .welcome-banner .v-card-text,
  .topic-classification-card .v-card-text,
  .chart-section .v-card-text {
    padding: 16px !important;
  }
  
  .welcome-banner .text-h3 {
    font-size: 1.3rem !important;
  }
  
  .welcome-banner .text-h6 {
    font-size: 0.95rem !important;
  }
  
  .chart-image {
    max-height: 150px !important;
  }
  
  .markdown-content {
    font-size: 13px !important;
  }
  
  .markdown-content h1 {
    font-size: 1.2rem !important;
  }
  
  .markdown-content h2 {
    font-size: 1.1rem !important;
  }
  
  .markdown-content h3 {
    font-size: 1rem !important;
  }
}

/* 横屏模式优化 */
@media (max-width: 768px) and (orientation: landscape) {
  .welcome-banner {
    margin: 12px !important;
  }
  
  .welcome-banner .v-card-text {
    padding: 16px !important;
  }
  
  .welcome-banner .text-h3 {
    font-size: 1.4rem !important;
  }
  
  .chart-image {
    max-height: 140px !important;
  }
  
  .v-dialog .v-card {
    max-height: 90vh !important;
  }
}

/* 移动端暗色主题优化 */
.v-theme--dark {
  @media (max-width: 768px) {
    .markdown-content blockquote {
      background: rgba(102, 126, 234, 0.1) !important;
      border-left-color: #818cf8 !important;
    }
    
    .markdown-content code {
      background: rgba(102, 126, 234, 0.15) !important;
    }
    
    .markdown-content pre {
      background: rgba(102, 126, 234, 0.1) !important;
    }
    
    .markdown-content th,
    .markdown-content td {
      border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    .markdown-content th {
      background: rgba(102, 126, 234, 0.15) !important;
    }
    
    .markdown-content a {
      color: #818cf8 !important;
      border-bottom-color: rgba(129, 140, 248, 0.3) !important;
    }
    
    .markdown-content a:hover {
      color: #a5b4fc !important;
      border-bottom-color: #a5b4fc !important;
    }
    
    .gradient-border {
      background: linear-gradient(rgba(30, 41, 59, 1), rgba(30, 41, 59, 1)) padding-box,
                  linear-gradient(135deg, #818cf8, #a78bfa) border-box !important;
    }
  }
}
</style>
