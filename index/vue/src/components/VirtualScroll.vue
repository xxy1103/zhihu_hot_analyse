<template>
  <div 
    ref="containerRef"
    class="virtual-scroll-container"
    @scroll="handleScroll"
  >
    <div 
      class="scroll-content"
      :style="{ height: totalHeight + 'px' }"
    >
      <div 
        class="visible-items"
        :style="{ transform: `translateY(${offsetY}px)` }"
      >
        <div
          v-for="item in visibleItems"
          :key="getItemKey(item)"
          class="scroll-item"
          :style="{ height: itemHeight + 'px' }"
        >
          <slot :item="item" :index="item._index"></slot>
        </div>
      </div>
    </div>
    
    <!-- 加载更多指示器 -->
    <div 
      v-if="loading"
      class="loading-indicator"
    >
      <v-progress-circular
        indeterminate
        size="24"
        width="3"
        color="primary"
      ></v-progress-circular>
      <span class="loading-text">{{ loadingText }}</span>
    </div>
    
    <!-- 没有更多数据提示 -->
    <div 
      v-if="noMore && items.length > 0"
      class="no-more-indicator"
    >
      <v-divider class="mb-2"></v-divider>
      <span class="no-more-text">{{ noMoreText }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { throttle } from '../utils/mobile.js'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
  itemHeight: {
    type: Number,
    default: 60
  },
  bufferSize: {
    type: Number,
    default: 5
  },
  threshold: {
    type: Number,
    default: 200
  },
  loading: {
    type: Boolean,
    default: false
  },
  noMore: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: '加载中...'
  },
  noMoreText: {
    type: String,
    default: '没有更多数据了'
  },
  itemKey: {
    type: [String, Function],
    default: 'id'
  }
})

const emit = defineEmits(['load-more', 'scroll'])

const containerRef = ref(null)
const scrollTop = ref(0)
const containerHeight = ref(0)

// 计算总高度
const totalHeight = computed(() => {
  return props.items.length * props.itemHeight
})

// 计算可见区域的起始和结束索引
const visibleRange = computed(() => {
  const start = Math.max(0, Math.floor(scrollTop.value / props.itemHeight) - props.bufferSize)
  const end = Math.min(
    props.items.length - 1,
    Math.ceil((scrollTop.value + containerHeight.value) / props.itemHeight) + props.bufferSize
  )
  return { start, end }
})

// 计算可见项目
const visibleItems = computed(() => {
  const { start, end } = visibleRange.value
  return props.items.slice(start, end + 1).map((item, index) => ({
    ...item,
    _index: start + index
  }))
})

// 计算偏移量
const offsetY = computed(() => {
  return visibleRange.value.start * props.itemHeight
})

// 获取项目的唯一标识
const getItemKey = (item) => {
  if (typeof props.itemKey === 'function') {
    return props.itemKey(item)
  }
  return item[props.itemKey] || item._index
}

// 节流的滚动处理函数
const handleScroll = throttle((e) => {
  const container = e.target
  scrollTop.value = container.scrollTop
  
  // 发出滚动事件
  emit('scroll', {
    scrollTop: container.scrollTop,
    scrollHeight: container.scrollHeight,
    clientHeight: container.clientHeight
  })
  
  // 检查是否需要加载更多
  if (!props.loading && !props.noMore) {
    const distanceToBottom = container.scrollHeight - container.scrollTop - container.clientHeight
    if (distanceToBottom <= props.threshold) {
      emit('load-more')
    }
  }
}, 16) // 约60fps

// 更新容器高度
const updateContainerHeight = () => {
  if (containerRef.value) {
    containerHeight.value = containerRef.value.clientHeight
  }
}

// 滚动到指定位置
const scrollTo = (position) => {
  if (containerRef.value) {
    containerRef.value.scrollTop = position
  }
}

// 滚动到指定项目
const scrollToItem = (index) => {
  const position = index * props.itemHeight
  scrollTo(position)
}

// 滚动到顶部
const scrollToTop = () => {
  scrollTo(0)
}

// 滚动到底部
const scrollToBottom = () => {
  if (containerRef.value) {
    scrollTo(containerRef.value.scrollHeight)
  }
}

// 监听窗口大小变化
const resizeObserver = ref(null)

onMounted(() => {
  updateContainerHeight()
  
  // 使用ResizeObserver监听容器大小变化
  if (window.ResizeObserver && containerRef.value) {
    resizeObserver.value = new ResizeObserver(updateContainerHeight)
    resizeObserver.value.observe(containerRef.value)
  } else {
    // 降级方案
    window.addEventListener('resize', updateContainerHeight)
  }
})

onUnmounted(() => {
  if (resizeObserver.value) {
    resizeObserver.value.disconnect()
  } else {
    window.removeEventListener('resize', updateContainerHeight)
  }
})

// 监听items变化，重置滚动位置（可选）
watch(() => props.items.length, (newLength, oldLength) => {
  // 如果是新加载的数据（长度增加），不重置滚动位置
  // 如果是重新加载的数据（长度减少或为0），重置到顶部
  if (newLength < oldLength || newLength === 0) {
    nextTick(() => {
      scrollToTop()
    })
  }
})

// 暴露方法给父组件
defineExpose({
  scrollTo,
  scrollToItem,
  scrollToTop,
  scrollToBottom,
  getScrollTop: () => scrollTop.value,
  getVisibleRange: () => visibleRange.value
})
</script>

<style scoped>
.virtual-scroll-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

.scroll-content {
  position: relative;
  width: 100%;
}

.visible-items {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.scroll-item {
  width: 100%;
  overflow: hidden;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  gap: 8px;
}

.loading-text {
  font-size: 14px;
  color: #666;
}

.no-more-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
}

.no-more-text {
  font-size: 12px;
  color: #999;
  text-align: center;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .virtual-scroll-container {
    /* 优化移动端滚动性能 */
    will-change: scroll-position;
    transform: translateZ(0);
  }
  
  .loading-indicator {
    padding: 12px;
  }
  
  .loading-text {
    font-size: 13px;
  }
  
  .no-more-text {
    font-size: 11px;
  }
}

/* 暗色主题适配 */
.v-theme--dark .loading-text {
  color: #cbd5e1;
}

.v-theme--dark .no-more-text {
  color: #94a3b8;
}
</style>
