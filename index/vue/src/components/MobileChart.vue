<template>
  <div class="mobile-chart-container" ref="chartContainer">
    <!-- 图表加载状态 -->
    <div v-if="loading" class="chart-loading">
      <v-progress-circular 
        indeterminate 
        size="40" 
        color="primary"
      ></v-progress-circular>
      <p class="mt-2">加载图表中...</p>
    </div>
    
    <!-- 图表错误状态 -->
    <div v-else-if="error" class="chart-error">
      <v-icon color="error" size="48">mdi-chart-line-variant</v-icon>
      <p class="mt-2">图表加载失败</p>
      <v-btn variant="outlined" size="small" @click="retryLoad">
        重试
      </v-btn>
    </div>
    
    <!-- 图表内容 -->
    <div v-else class="chart-content">
      <!-- 图表标题 -->
      <div v-if="title" class="chart-title">
        <h3>{{ title }}</h3>
        <p v-if="subtitle" class="chart-subtitle">{{ subtitle }}</p>
      </div>
      
      <!-- 图表工具栏 -->
      <div v-if="showToolbar" class="chart-toolbar">
        <v-btn-group density="compact" variant="outlined">
          <v-btn 
            v-for="period in timePeriods" 
            :key="period.value"
            :variant="selectedPeriod === period.value ? 'flat' : 'outlined'"
            size="small"
            @click="selectPeriod(period.value)"
          >
            {{ period.label }}
          </v-btn>
        </v-btn-group>
        
        <v-spacer></v-spacer>
        
        <v-btn 
          icon="mdi-refresh" 
          size="small" 
          variant="text"
          @click="refreshChart"
          :loading="refreshing"
        ></v-btn>
      </div>
      
      <!-- 响应式图表区域 -->
      <div class="chart-wrapper" :style="chartStyle">
        <canvas ref="chartCanvas" :width="canvasWidth" :height="canvasHeight"></canvas>
      </div>
      
      <!-- 图表说明 -->
      <div v-if="showLegend" class="chart-legend">
        <div 
          v-for="item in legendItems" 
          :key="item.label"
          class="legend-item"
          @click="toggleSeries(item.key)"
        >
          <span 
            class="legend-color" 
            :style="{ backgroundColor: item.color, opacity: item.visible ? 1 : 0.3 }"
          ></span>
          <span class="legend-label" :class="{ 'legend-disabled': !item.visible }">
            {{ item.label }}
          </span>
        </div>
      </div>
      
      <!-- 图表数据摘要 -->
      <div v-if="showSummary && summary" class="chart-summary">
        <div class="summary-item" v-for="item in summary" :key="item.label">
          <span class="summary-label">{{ item.label }}</span>
          <span class="summary-value">{{ item.value }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'

export default {
  name: 'MobileChart',
  props: {
    // 图表数据
    data: {
      type: Array,
      default: () => []
    },
    // 图表类型
    type: {
      type: String,
      default: 'line',
      validator: value => ['line', 'bar', 'pie', 'area'].includes(value)
    },
    // 图表标题
    title: {
      type: String,
      default: ''
    },
    // 图表副标题
    subtitle: {
      type: String,
      default: ''
    },
    // 显示工具栏
    showToolbar: {
      type: Boolean,
      default: true
    },
    // 显示图例
    showLegend: {
      type: Boolean,
      default: true
    },
    // 显示数据摘要
    showSummary: {
      type: Boolean,
      default: false
    },
    // 图表高度
    height: {
      type: [Number, String],
      default: 300
    },
    // 响应式
    responsive: {
      type: Boolean,
      default: true
    },
    // 动画
    animated: {
      type: Boolean,
      default: true
    },
    // 颜色主题
    colors: {
      type: Array,
      default: () => ['#667eea', '#f093fb', '#4ecdc4', '#ff6b6b', '#feca57']
    }
  },
  
  emits: ['chart-ready', 'period-change', 'series-toggle'],
  
  setup(props, { emit }) {
    // 响应式数据
    const chartContainer = ref(null)
    const chartCanvas = ref(null)
    const loading = ref(true)
    const error = ref(false)
    const refreshing = ref(false)
    const selectedPeriod = ref('7d')
    const chartInstance = ref(null)
    const resizeObserver = ref(null)
    
    // 时间段选项
    const timePeriods = ref([
      { label: '7天', value: '7d' },
      { label: '30天', value: '30d' },
      { label: '90天', value: '90d' },
      { label: '1年', value: '1y' }
    ])
    
    // 图例数据
    const legendItems = ref([])
    
    // 计算属性
    const chartStyle = computed(() => ({
      height: typeof props.height === 'number' ? `${props.height}px` : props.height,
      position: 'relative'
    }))
    
    const canvasWidth = computed(() => {
      return chartContainer.value?.clientWidth || 300
    })
    
    const canvasHeight = computed(() => {
      const height = typeof props.height === 'number' ? props.height : 300
      return height
    })
    
    const summary = computed(() => {
      if (!props.data || props.data.length === 0) return null
      
      // 计算数据摘要
      const values = props.data.map(item => item.value || 0)
      const total = values.reduce((sum, val) => sum + val, 0)
      const average = total / values.length
      const max = Math.max(...values)
      const min = Math.min(...values)
      
      return [
        { label: '总计', value: formatNumber(total) },
        { label: '平均', value: formatNumber(average) },
        { label: '最高', value: formatNumber(max) },
        { label: '最低', value: formatNumber(min) }
      ]
    })
    
    // 方法
    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toFixed(0)
    }
    
    const initChart = async () => {
      loading.value = true
      error.value = false
      
      try {
        await nextTick()
        
        // 模拟图表初始化（实际项目中可以集成Chart.js、ECharts等）
        await simulateChartInit()
        
        // 初始化图例
        initLegend()
        
        loading.value = false
        emit('chart-ready')
        
      } catch (err) {
        console.error('Chart initialization failed:', err)
        error.value = true
        loading.value = false
      }
    }
    
    const simulateChartInit = () => {
      return new Promise((resolve) => {
        // 模拟异步图表加载
        setTimeout(() => {
          if (chartCanvas.value) {
            const ctx = chartCanvas.value.getContext('2d')
            drawChart(ctx)
          }
          resolve()
        }, 1000)
      })
    }
    
    const drawChart = (ctx) => {
      const canvas = chartCanvas.value
      const width = canvas.width
      const height = canvas.height
      
      // 清空画布
      ctx.clearRect(0, 0, width, height)
      
      // 设置样式
      ctx.lineWidth = 2
      ctx.lineCap = 'round'
      ctx.lineJoin = 'round'
      
      if (props.type === 'line') {
        drawLineChart(ctx, width, height)
      } else if (props.type === 'bar') {
        drawBarChart(ctx, width, height)
      } else if (props.type === 'pie') {
        drawPieChart(ctx, width, height)
      }
    }
    
    const drawLineChart = (ctx, width, height) => {
      if (!props.data || props.data.length === 0) return
      
      const padding = 40
      const chartWidth = width - padding * 2
      const chartHeight = height - padding * 2
      
      const values = props.data.map(item => item.value || 0)
      const maxValue = Math.max(...values)
      const minValue = Math.min(...values)
      const range = maxValue - minValue || 1
      
      // 绘制坐标轴
      ctx.strokeStyle = '#e0e0e0'
      ctx.lineWidth = 1
      
      // Y轴
      ctx.beginPath()
      ctx.moveTo(padding, padding)
      ctx.lineTo(padding, height - padding)
      ctx.stroke()
      
      // X轴
      ctx.beginPath()
      ctx.moveTo(padding, height - padding)
      ctx.lineTo(width - padding, height - padding)
      ctx.stroke()
      
      // 绘制数据线
      ctx.strokeStyle = props.colors[0]
      ctx.lineWidth = 3
      ctx.beginPath()
      
      props.data.forEach((item, index) => {
        const x = padding + (index / (props.data.length - 1)) * chartWidth
        const y = height - padding - ((item.value - minValue) / range) * chartHeight
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.stroke()
      
      // 绘制数据点
      ctx.fillStyle = props.colors[0]
      props.data.forEach((item, index) => {
        const x = padding + (index / (props.data.length - 1)) * chartWidth
        const y = height - padding - ((item.value - minValue) / range) * chartHeight
        
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, Math.PI * 2)
        ctx.fill()
      })
    }
    
    const drawBarChart = (ctx, width, height) => {
      if (!props.data || props.data.length === 0) return
      
      const padding = 40
      const chartWidth = width - padding * 2
      const chartHeight = height - padding * 2
      
      const values = props.data.map(item => item.value || 0)
      const maxValue = Math.max(...values)
      
      const barWidth = chartWidth / props.data.length * 0.8
      const barSpacing = chartWidth / props.data.length * 0.2
      
      props.data.forEach((item, index) => {
        const x = padding + index * (chartWidth / props.data.length) + barSpacing / 2
        const barHeight = (item.value / maxValue) * chartHeight
        const y = height - padding - barHeight
        
        ctx.fillStyle = props.colors[index % props.colors.length]
        ctx.fillRect(x, y, barWidth, barHeight)
      })
    }
    
    const drawPieChart = (ctx, width, height) => {
      if (!props.data || props.data.length === 0) return
      
      const centerX = width / 2
      const centerY = height / 2
      const radius = Math.min(width, height) / 2 - 40
      
      const total = props.data.reduce((sum, item) => sum + (item.value || 0), 0)
      let currentAngle = -Math.PI / 2
      
      props.data.forEach((item, index) => {
        const sliceAngle = (item.value / total) * Math.PI * 2
        
        ctx.fillStyle = props.colors[index % props.colors.length]
        ctx.beginPath()
        ctx.moveTo(centerX, centerY)
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
        ctx.closePath()
        ctx.fill()
        
        currentAngle += sliceAngle
      })
    }
    
    const initLegend = () => {
      legendItems.value = props.data.map((item, index) => ({
        key: index,
        label: item.label || `系列 ${index + 1}`,
        color: props.colors[index % props.colors.length],
        visible: true
      }))
    }
    
    const selectPeriod = (period) => {
      selectedPeriod.value = period
      emit('period-change', period)
      refreshChart()
    }
    
    const toggleSeries = (key) => {
      const item = legendItems.value.find(item => item.key === key)
      if (item) {
        item.visible = !item.visible
        emit('series-toggle', key, item.visible)
        redrawChart()
      }
    }
    
    const refreshChart = async () => {
      refreshing.value = true
      await new Promise(resolve => setTimeout(resolve, 1000))
      redrawChart()
      refreshing.value = false
    }
    
    const redrawChart = () => {
      if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext('2d')
        drawChart(ctx)
      }
    }
    
    const retryLoad = () => {
      initChart()
    }
    
    const handleResize = () => {
      if (props.responsive && chartCanvas.value) {
        nextTick(() => {
          redrawChart()
        })
      }
    }
    
    // 生命周期
    onMounted(() => {
      initChart()
      
      if (props.responsive) {
        resizeObserver.value = new ResizeObserver(handleResize)
        resizeObserver.value.observe(chartContainer.value)
      }
    })
    
    onUnmounted(() => {
      if (resizeObserver.value) {
        resizeObserver.value.disconnect()
      }
    })
    
    // 监听数据变化
    watch(() => props.data, () => {
      redrawChart()
      initLegend()
    }, { deep: true })
    
    return {
      chartContainer,
      chartCanvas,
      loading,
      error,
      refreshing,
      selectedPeriod,
      timePeriods,
      legendItems,
      chartStyle,
      canvasWidth,
      canvasHeight,
      summary,
      selectPeriod,
      toggleSeries,
      refreshChart,
      retryLoad
    }
  }
}
</script>

<style scoped>
.mobile-chart-container {
  width: 100%;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 16px;
}

.chart-loading,
.chart-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #666;
}

.chart-title h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #333;
}

.chart-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0 0 16px 0;
}

.chart-toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  gap: 8px;
}

.chart-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
}

canvas {
  width: 100%;
  height: 100%;
  max-width: 100%;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.legend-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: opacity 0.2s;
}

.legend-item:hover {
  opacity: 0.8;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 8px;
  transition: opacity 0.2s;
}

.legend-label {
  font-size: 14px;
  color: #333;
  transition: color 0.2s;
}

.legend-disabled {
  color: #999;
  text-decoration: line-through;
}

.chart-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.summary-item {
  text-align: center;
}

.summary-label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.summary-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .mobile-chart-container {
    padding: 12px;
    border-radius: 8px;
  }
  
  .chart-title h3 {
    font-size: 16px;
  }
  
  .chart-toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .chart-legend {
    gap: 12px;
  }
  
  .chart-summary {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}

/* 暗色主题 */
@media (prefers-color-scheme: dark) {
  .mobile-chart-container {
    background: #1e1e1e;
    color: white;
  }
  
  .chart-title h3 {
    color: white;
  }
  
  .chart-subtitle {
    color: #ccc;
  }
  
  .legend-label {
    color: white;
  }
  
  .summary-value {
    color: white;
  }
}

/* 低性能模式 */
:global(.low-performance-mode) .mobile-chart-container {
  box-shadow: none;
  border: 1px solid #e0e0e0;
}

/* 数据节省模式 */
:global(.data-save-mode) canvas {
  image-rendering: pixelated;
}
</style>
