<template>
  <div 
    ref="containerRef"
    class="mobile-gesture-container"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <slot></slot>
    
    <!-- 下拉刷新指示器 -->
    <div 
      v-if="enablePullRefresh && pullDistance > 0"
      class="pull-refresh-indicator"
      :style="{ transform: `translateY(${Math.min(pullDistance, maxPullDistance)}px)` }"
    >
      <div class="refresh-content">
        <v-progress-circular
          v-if="isRefreshing"
          indeterminate
          size="24"
          width="3"
          color="primary"
        ></v-progress-circular>
        <v-icon 
          v-else
          :style="{ transform: pullDistance >= refreshThreshold ? 'rotate(180deg)' : 'rotate(0deg)' }"
          class="refresh-arrow"
          color="primary"
        >
          mdi-arrow-down
        </v-icon>
        <span class="refresh-text">
          {{ getRefreshText() }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  enableSwipe: {
    type: Boolean,
    default: true
  },
  enablePullRefresh: {
    type: Boolean,
    default: false
  },
  swipeThreshold: {
    type: Number,
    default: 50
  },
  refreshThreshold: {
    type: Number,
    default: 80
  },
  maxPullDistance: {
    type: Number,
    default: 120
  }
})

const emit = defineEmits([
  'swipe-left',
  'swipe-right', 
  'swipe-up',
  'swipe-down',
  'tap',
  'long-press',
  'refresh'
])

const containerRef = ref(null)
const startX = ref(0)
const startY = ref(0)
const currentX = ref(0)
const currentY = ref(0)
const startTime = ref(0)
const pullDistance = ref(0)
const isRefreshing = ref(false)
const longPressTimer = ref(null)

const handleTouchStart = (e) => {
  const touch = e.touches[0]
  startX.value = currentX.value = touch.clientX
  startY.value = currentY.value = touch.clientY
  startTime.value = Date.now()
  
  // 长按检测
  longPressTimer.value = setTimeout(() => {
    emit('long-press', { x: currentX.value, y: currentY.value })
  }, 800)
  
  // 重置下拉距离
  if (!isRefreshing.value) {
    pullDistance.value = 0
  }
}

const handleTouchMove = (e) => {
  const touch = e.touches[0]
  currentX.value = touch.clientX
  currentY.value = touch.clientY
  
  // 清除长按定时器
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value)
    longPressTimer.value = null
  }
  
  // 下拉刷新逻辑
  if (props.enablePullRefresh && !isRefreshing.value) {
    const deltaY = currentY.value - startY.value
    const container = containerRef.value
    
    if (deltaY > 0 && container && container.scrollTop === 0) {
      e.preventDefault()
      pullDistance.value = Math.min(deltaY * 0.5, props.maxPullDistance)
    }
  }
}

const handleTouchEnd = (e) => {
  const endTime = Date.now()
  const deltaTime = endTime - startTime.value
  const deltaX = currentX.value - startX.value
  const deltaY = currentY.value - startY.value
  const absX = Math.abs(deltaX)
  const absY = Math.abs(deltaY)
  
  // 清除长按定时器
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value)
    longPressTimer.value = null
  }
  
  // 下拉刷新检测
  if (props.enablePullRefresh && pullDistance.value >= props.refreshThreshold && !isRefreshing.value) {
    startRefresh()
    return
  }
  
  // 重置下拉距离
  if (!isRefreshing.value) {
    pullDistance.value = 0
  }
  
  // 滑动手势检测
  if (props.enableSwipe && deltaTime < 500) {
    if (absX > props.swipeThreshold || absY > props.swipeThreshold) {
      if (absX > absY) {
        // 水平滑动
        if (deltaX > 0) {
          emit('swipe-right', { distance: absX, duration: deltaTime })
        } else {
          emit('swipe-left', { distance: absX, duration: deltaTime })
        }
      } else {
        // 垂直滑动
        if (deltaY > 0) {
          emit('swipe-down', { distance: absY, duration: deltaTime })
        } else {
          emit('swipe-up', { distance: absY, duration: deltaTime })
        }
      }
      return
    }
  }
  
  // 点击检测
  if (absX < 10 && absY < 10 && deltaTime < 300) {
    emit('tap', { x: currentX.value, y: currentY.value })
  }
}

const startRefresh = () => {
  isRefreshing.value = true
  pullDistance.value = props.refreshThreshold
  
  emit('refresh', () => {
    // 刷新完成回调
    isRefreshing.value = false
    pullDistance.value = 0
  })
}

const getRefreshText = () => {
  if (isRefreshing.value) {
    return '正在刷新...'
  } else if (pullDistance.value >= props.refreshThreshold) {
    return '释放立即刷新'
  } else {
    return '下拉可以刷新'
  }
}

onMounted(() => {
  // 禁用默认的触摸行为
  if (containerRef.value) {
    containerRef.value.style.touchAction = 'pan-y'
  }
})

onUnmounted(() => {
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value)
  }
})
</script>

<style scoped>
.mobile-gesture-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

.pull-refresh-indicator {
  position: absolute;
  top: -60px;
  left: 0;
  right: 0;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: transform 0.3s ease;
}

.refresh-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.refresh-arrow {
  transition: transform 0.3s ease;
}

.refresh-text {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

/* 暗色主题适配 */
.v-theme--dark .pull-refresh-indicator {
  background: rgba(30, 41, 59, 0.95);
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.v-theme--dark .refresh-text {
  color: #cbd5e1;
}

@media (max-width: 768px) {
  .pull-refresh-indicator {
    height: 50px;
    top: -50px;
  }
  
  .refresh-text {
    font-size: 11px;
  }
}
</style>
