<template>
  <div v-if="!question" class="loading-container glass-effect">
    <v-progress-circular
      indeterminate
      color="primary"
      size="64"
      width="6"
    ></v-progress-circular>
    <p class="text-h6 mt-6 gradient-text">数据分析中...</p>
    <p class="text-body-2 text-medium-emphasis mt-2">正在获取最新的热点数据</p>
  </div>

  <div v-else class="analyse-container">
    <!-- 话题标题卡片 -->
    <transition name="slide" appear>
      <v-card class="topic-card mb-6 glass-effect floating-card" rounded="xl" elevation="0">
        <v-card-text class="pa-6">
          <div class="d-flex align-center mb-6">
            <v-icon color="primary" size="36" class="me-4 pulse">mdi-trending-up</v-icon>
            <div class="flex-grow-1">
              <h1 class="text-h4 font-weight-bold topic-title mb-2">{{ question }}</h1>
              <div class="d-flex align-center flex-wrap ga-2">
                <v-chip color="primary" variant="tonal" size="small" prepend-icon="mdi-eye">
                  {{ formatNumber(view) }} 浏览
                </v-chip>
                <v-chip color="error" variant="tonal" size="small" prepend-icon="mdi-fire">
                  热度 {{ formatNumber(hot_value) }}
                </v-chip>
                <v-chip color="success" variant="tonal" size="small" prepend-icon="mdi-account-heart">
                  {{ formatNumber(followers) }} 关注
                </v-chip>
              </div>
            </div>
          </div>
          
          <!-- 统计数据卡片 -->
          <v-row class="stats-row mb-6">
            <v-col cols="6" md="3">
              <v-card class="stat-card interactive-card soft-shadow" rounded="lg" elevation="0">
                <v-card-text class="text-center pa-4">
                  <v-icon color="info" size="32" class="mb-3 pulse">mdi-eye-outline</v-icon>
                  <div class="text-h5 font-weight-bold mb-1">{{ formatNumber(view) }}</div>
                  <div class="text-caption text-medium-emphasis">浏览量</div>
                  <v-progress-linear 
                    model-value="75" 
                    color="info" 
                    height="4" 
                    rounded 
                    class="mt-2"
                  ></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            
            <v-col cols="6" md="3">
              <v-card class="stat-card interactive-card soft-shadow" rounded="lg" elevation="0">
                <v-card-text class="text-center pa-4">
                  <v-icon color="error" size="32" class="mb-3 pulse">mdi-fire</v-icon>
                  <div class="text-h5 font-weight-bold mb-1">{{ formatNumber(hot_value) }}</div>
                  <div class="text-caption text-medium-emphasis">热度</div>
                  <v-progress-linear 
                    model-value="90" 
                    color="error" 
                    height="4" 
                    rounded 
                    class="mt-2"
                  ></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            
            <v-col cols="6" md="3">
              <v-card class="stat-card interactive-card soft-shadow" rounded="lg" elevation="0">
                <v-card-text class="text-center pa-4">
                  <v-icon color="success" size="32" class="mb-3 pulse">mdi-account-heart-outline</v-icon>
                  <div class="text-h5 font-weight-bold mb-1">{{ formatNumber(followers) }}</div>
                  <div class="text-caption text-medium-emphasis">关注者</div>
                  <v-progress-linear 
                    model-value="65" 
                    color="success" 
                    height="4" 
                    rounded 
                    class="mt-2"
                  ></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            
            <v-col cols="6" md="3">
              <v-card class="stat-card interactive-card soft-shadow" rounded="lg" elevation="0">
                <v-card-text class="text-center pa-4">
                  <v-icon color="warning" size="32" class="mb-3 pulse">mdi-comment-multiple-outline</v-icon>
                  <div class="text-h5 font-weight-bold mb-1">{{ formatNumber(answers_count) }}</div>
                  <div class="text-caption text-medium-emphasis">回答数</div>
                  <v-progress-linear 
                    model-value="80" 
                    color="warning" 
                    height="4" 
                    rounded 
                    class="mt-2"
                  ></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- 原文链接和描述 -->
          <div class="d-flex flex-column ga-4">
            <v-btn
              :href="link"
              target="_blank"
              color="primary"
              variant="elevated"
              prepend-icon="mdi-open-in-new"
              class="modern-btn align-self-start"
              size="large"
            >
              查看原文报道
            </v-btn>

            <div class="topic-description">
              <h3 class="text-h6 font-weight-bold mb-3 d-flex align-center">
                <v-icon class="me-2" color="accent">mdi-text-box-outline</v-icon>
                话题描述
              </h3>
              <p class="text-body-1">{{ detail }}</p>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </transition>

    <!-- AI分析摘要 -->
    <transition name="slide" appear style="transition-delay: 0.1s">
      <v-card class="summary-card mb-6 glass-effect floating-card" rounded="xl" elevation="0">
        <v-card-title class="d-flex align-center pa-6">
          <v-icon color="secondary" size="32" class="me-3 rotating-icon">mdi-robot-outline</v-icon>
          <span class="text-h5 font-weight-bold gradient-text">AI智能分析</span>
          <v-spacer></v-spacer>
          <v-chip color="secondary" variant="tonal" size="small" prepend-icon="mdi-brain">
            深度洞察
          </v-chip>
        </v-card-title>
        
        <v-divider class="mx-6"></v-divider>
        
        <v-card-text class="pa-6">
          <div class="markdown-content" v-html="htmlContent"></div>
        </v-card-text>
      </v-card>
    </transition>

    <!-- 热门回答 -->
    <transition name="slide" appear style="transition-delay: 0.2s">
      <v-card class="answers-card glass-effect floating-card" rounded="xl" elevation="0">
        <v-card-title class="d-flex align-center pa-6">
          <v-icon color="accent" size="32" class="me-3 wobble">mdi-star-outline</v-icon>
          <span class="text-h5 font-weight-bold gradient-text">热门回答精选</span>
          <v-spacer></v-spacer>
          <v-chip color="accent" variant="tonal" size="small" prepend-icon="mdi-thumb-up-outline">
            高质量内容
          </v-chip>
        </v-card-title>
        
        <v-divider class="mx-6"></v-divider>
        
        <v-card-text class="pa-6">
          <v-row>
            <v-col
              v-for="(answer, index) in validAnswers"
              :key="index"
              cols="12"
              class="answer-col"
            >
              <transition name="bounce" appear :style="`transition-delay: ${0.1 * index}s`">
                <v-card class="answer-card interactive-card medium-shadow" rounded="lg" elevation="0">
                  <v-card-title class="d-flex align-center justify-space-between pa-5">
                    <div class="d-flex align-center">
                      <v-avatar 
                        color="primary" 
                        size="48" 
                        class="me-4"
                        :class="`rank-${index + 1}-avatar`"
                      >
                        <v-icon color="white" size="24">mdi-account</v-icon>
                      </v-avatar>
                      <div>
                        <div class="font-weight-bold text-h6">{{ answer.name }}</div>
                        <div class="text-caption text-medium-emphasis d-flex align-center">
                          <v-icon size="14" class="me-1">mdi-shield-check</v-icon>
                          认证用户
                        </div>
                      </div>
                    </div>
                    
                    <v-chip
                      :color="index === 0 ? 'error' : index === 1 ? 'warning' : 'success'"
                      variant="flat"
                      size="default"
                      prepend-icon="mdi-thumb-up"
                      class="font-weight-bold"
                    >
                      {{ formatNumber(answer.like) }} 赞
                    </v-chip>
                  </v-card-title>
                  
                  <v-card-text class="pa-5">
                    <div class="answer-content">
                      <p v-for="(para, i) in answer.content" :key="i" class="mb-4">
                        {{ para }}
                      </p>
                    </div>
                    
                    <div class="d-flex justify-space-between align-center mt-4">
                      <div class="d-flex ga-2">
                        <v-btn 
                          variant="text" 
                          size="small" 
                          prepend-icon="mdi-thumb-up-outline"
                          color="primary"
                        >
                          点赞
                        </v-btn>
                        <v-btn 
                          variant="text" 
                          size="small" 
                          prepend-icon="mdi-comment-outline"
                          color="primary"
                        >
                          评论
                        </v-btn>
                        <v-btn 
                          variant="text" 
                          size="small" 
                          prepend-icon="mdi-share-outline"
                          color="primary"
                        >
                          分享
                        </v-btn>
                      </div>
                      
                      <v-chip 
                        variant="text" 
                        size="small" 
                        color="primary"
                        prepend-icon="mdi-trophy"
                      >
                        第{{ index + 1 }}名
                      </v-chip>
                    </div>
                  </v-card-text>
                </v-card>
              </transition>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'

const route = useRoute()
const userId = ref(route.params.userId)
const topic_classified = ref('')

// 响应式数据
const object = ref({})
const hot_value = ref(0)
const followers = ref(0)
const answers_count = ref(0)
const view = ref(0)
const question = ref('')
const link = ref('')
const detail = ref('')
const answer1 = ref('')
const answer1_like = ref(0)
const answer2 = ref('')
const answer2_like = ref(0)
const answer3 = ref('')
const answer3_like = ref(0)

// 格式化数字
const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toLocaleString()
}

// 读取文档
const fetchDocument = async (id) => {
  try {
    const response = await fetch('/doc/' + id + '.md')
    topic_classified.value = await response.text()
  } catch (error) {
    console.error('读取文档文件出错:', error)
  }
}

// 获取数据
const fetchData = async () => {
  try {
    const response = await fetch(`http://localhost:5251/?id=${userId.value}`)
    const data = await response.json()
    
    view.value = data['被浏览量'] || 0
    hot_value.value = data['热度'] || 0
    followers.value = data['关注者'] || 0
    answers_count.value = data['总回答数'] || 0
    question.value = data['标题'] || ''
    link.value = data['链接'] || ''
    detail.value = data['描述'] || ''
    object.value = data
    answer1.value = data['回答1'] || ''
    answer1_like.value = data['回答1点赞数'] || 0
    answer2.value = data['回答2'] || ''
    answer2_like.value = data['回答2点赞数'] || 0
    answer3.value = data['回答3'] || ''
    answer3_like.value = data['回答3点赞数'] || 0
  } catch (error) {
    console.error('请求数据出错:', error)
  }
}

// 计算属性
const htmlContent = computed(() => marked(topic_classified.value))

const answers = computed(() => [
  {
    name: "高赞回答1",
    like: answer1_like.value,
    content: Array.isArray(answer1.value) ? answer1.value : answer1.value ? [answer1.value] : []
  },
  {
    name: "高赞回答2", 
    like: answer2_like.value,
    content: Array.isArray(answer2.value) ? answer2.value : answer2.value ? [answer2.value] : []
  },
  {
    name: "高赞回答3",
    like: answer3_like.value,
    content: Array.isArray(answer3.value) ? answer3.value : answer3.value ? [answer3.value] : []
  }
])

const validAnswers = computed(() => {
  return answers.value.filter(answer => answer.content.length > 0)
})

// 生命周期
onMounted(() => {
  fetchDocument(userId.value)
  fetchData()
})

// 监听路由变化
watch(() => route.params.userId, (newId) => {
  userId.value = newId
  fetchDocument(newId)
  fetchData()
})
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  border-radius: 20px;
  margin: 2rem;
  padding: 3rem;
  text-align: center;
}

.analyse-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.topic-card {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.04) 0%, 
    rgba(118, 75, 162, 0.04) 50%,
    rgba(78, 205, 196, 0.04) 100%) !important;
  border: 1px solid rgba(102, 126, 234, 0.12) !important;
  position: relative;
  overflow: hidden;
}

.topic-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.05), transparent);
  transition: left 0.8s ease;
}

.topic-card:hover::before {
  left: 100%;
}

.topic-title {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.3;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.stats-row {
  margin-top: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(102, 126, 234, 0.08) !important;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
}

.stat-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.stat-card:hover::after {
  transform: scaleX(1);
}

.stat-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.2) !important;
  background: rgba(255, 255, 255, 0.95) !important;
  border-color: rgba(102, 126, 234, 0.2) !important;
}

.topic-description {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9));
  border-radius: 16px;
  padding: 2rem;
  border-left: 4px solid #667eea;
  line-height: 1.8;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.summary-card {
  background: linear-gradient(135deg, 
    rgba(118, 75, 162, 0.04) 0%, 
    rgba(78, 205, 196, 0.04) 100%) !important;
  border: 1px solid rgba(118, 75, 162, 0.12) !important;
}

.answers-card {
  background: linear-gradient(135deg, 
    rgba(78, 205, 196, 0.04) 0%, 
    rgba(6, 255, 165, 0.04) 100%) !important;
  border: 1px solid rgba(78, 205, 196, 0.12) !important;
}

.answer-col {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.answer-card {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(78, 205, 196, 0.1) !important;
  position: relative;
  overflow: hidden;
}

.answer-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.03), transparent);
  transition: left 0.6s ease;
}

.answer-card:hover::before {
  left: 100%;
}

.answer-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 50px rgba(78, 205, 196, 0.15) !important;
  background: rgba(255, 255, 255, 0.95) !important;
  border-color: rgba(78, 205, 196, 0.2) !important;
}

.rank-1-avatar {
  background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
}

.rank-2-avatar {
  background: linear-gradient(135deg, #feca57, #ff9ff3) !important;
  box-shadow: 0 6px 20px rgba(254, 202, 87, 0.3);
}

.rank-3-avatar {
  background: linear-gradient(135deg, #06ffa5, #4ecdc4) !important;
  box-shadow: 0 6px 20px rgba(6, 255, 165, 0.3);
}

.answer-content {
  line-height: 1.8;
  font-size: 1rem;
  color: #475569;
}

.answer-content p {
  text-align: justify;
  text-indent: 2em;
  margin-bottom: 1.5rem;
  transition: color 0.3s ease;
}

.answer-card:hover .answer-content p {
  color: #334155;
}

.markdown-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9));
  border-radius: 16px;
  padding: 2rem;
  line-height: 1.8;
  border: 1px solid rgba(118, 75, 162, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  margin-bottom: 1.5rem;
  margin-top: 2rem;
  letter-spacing: -0.01em;
}

.markdown-content :deep(h1) {
  font-size: 1.75rem;
}

.markdown-content :deep(h2) {
  font-size: 1.5rem;
}

.markdown-content :deep(h3) {
  font-size: 1.25rem;
}

.markdown-content :deep(p) {
  margin-bottom: 1.5rem;
  text-align: justify;
  color: #475569;
  line-height: 1.8;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 2rem;
  margin-bottom: 1.5rem;
}

.markdown-content :deep(li) {
  margin-bottom: 0.75rem;
  color: #64748b;
  line-height: 1.7;
}

.markdown-content :deep(code) {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  color: #667eea;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.9em;
  font-weight: 600;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  padding: 1.5rem;
  border-radius: 0 12px 12px 0;
  margin: 2rem 0;
  font-style: italic;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.08);
}

.markdown-content :deep(pre) {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  padding: 1.5rem;
  border-radius: 12px;
  overflow-x: auto;
  margin: 2rem 0;
  border: 1px solid rgba(102, 126, 234, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 深色主题适配 */
.v-theme--dark .topic-card {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.08) 0%, 
    rgba(118, 75, 162, 0.08) 100%) !important;
  border-color: rgba(102, 126, 234, 0.2) !important;
}

.v-theme--dark .stat-card {
  background: rgba(30, 41, 59, 0.85) !important;
  border-color: rgba(102, 126, 234, 0.2) !important;
}

.v-theme--dark .answer-card {
  background: rgba(30, 41, 59, 0.85) !important;
  border-color: rgba(78, 205, 196, 0.2) !important;
}

.v-theme--dark .topic-description,
.v-theme--dark .markdown-content {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(51, 65, 85, 0.9));
  border-color: rgba(148, 163, 184, 0.2);
}

.v-theme--dark .answer-content p {
  color: #cbd5e1;
}

.v-theme--dark .answer-card:hover .answer-content p {
  color: #e2e8f0;
}

.v-theme--dark .markdown-content :deep(p) {
  color: #cbd5e1;
}

.v-theme--dark .markdown-content :deep(li) {
  color: #94a3b8;
}

/* 动画增强 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.topic-card {
  animation: fadeInUp 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.summary-card {
  animation: slideInLeft 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
  animation-delay: 0.1s;
  animation-fill-mode: both;
}

.answers-card {
  animation: fadeInUp 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
  animation-delay: 0.2s;
  animation-fill-mode: both;
}

/* 进度条美化 */
.v-progress-linear {
  border-radius: 8px !important;
  overflow: hidden !important;
}

.v-progress-linear__determinate {
  border-radius: 8px !important;
}

/* 响应式设计优化 */
@media (max-width: 768px) {
  .analyse-container {
    padding: 0 0.5rem;
  }
  
  .topic-title {
    font-size: 1.5rem !important;
    line-height: 1.4;
  }
  
  .answer-content p {
    text-indent: 1em;
    font-size: 0.95rem;
  }
  
  .topic-description,
  .markdown-content {
    padding: 1.5rem;
  }
  
  .stat-card .text-h5 {
    font-size: 1.25rem !important;
  }
}

@media (max-width: 480px) {
  .topic-card .pa-6,
  .summary-card .pa-6,
  .answers-card .pa-6 {
    padding: 1rem !important;
  }
  
  .answer-card .pa-5 {
    padding: 1rem !important;
  }
  
  .stat-card .pa-4 {
    padding: 0.75rem !important;
  }
}

/* 按钮和交互元素美化 */
.v-btn.modern-btn {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25) !important;
}

.v-btn.modern-btn:hover {
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35) !important;
}

/* 芯片美化 */
.v-chip {
  font-weight: 600 !important;
  letter-spacing: 0.01em !important;
}

.v-chip--variant-tonal {
  backdrop-filter: blur(10px);
}

/* 图标动画增强 */
.v-icon.pulse {
  animation: pulse 2s infinite ease-in-out;
}

.v-icon.wobble {
  animation: wobble 3s ease-in-out infinite;
}

.v-icon.rotating-icon {
  animation: rotate 10s linear infinite;
}

/* 卡片边框发光效果 */
.floating-card {
  position: relative;
}

.floating-card::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #667eea, #764ba2, #4ecdc4, #06ffa5);
  border-radius: inherit;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.floating-card:hover::after {
  opacity: 0.1;
}
</style>

