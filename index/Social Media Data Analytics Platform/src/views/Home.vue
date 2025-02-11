<script setup>
import { marked } from 'marked'
import { ref,onMounted, computed } from 'vue'

const topic_classified = ref('')

onMounted(async () => {
  try {
    const response = await fetch('doc/hot_list_analyse.md') // txt 文件放在 public 目录下
    topic_classified.value = await response.text()
  } catch (error) {
    console.error('读取txt文件出错:', error)
  }
})

const htmlContent = computed(() => marked(topic_classified.value))

</script>

<template>
<h3>话题分类</h3>
            <div class="topic_classified" v-html="htmlContent"></div>
            <h3>数据可视化</h3>
            <img src="@/image/关注者折线图.png" alt="示例图片" style="width:80%; height:auto;" />
            <img src="@/image/热度折线图.png" alt="示例图片" style="width:80%; height:auto;" />
            <img src="@/image/总回答数折线图.png" alt="示例图片" style="width:80%; height:auto;" />
            <ul class="side-content">
            </ul>
</template>