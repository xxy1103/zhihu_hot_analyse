<template>
  <div class="content">
    <div class="question-meta">
      <span>{{view}}次浏览</span>
      <span>•</span>
      <span>{{ followers }} 关注</span>
      <span>•</span>
      <span>{{ answers_count }}个回答</span>
    </div>
  </div>
  <h1 class="question-title">{{ question }}</h1>
  <a :href="link" class="original-link" target="_blank" rel="noopener noreferrer">查看原文报道 →</a>
  <div class="question-detail">
    {{ detail }}
  </div>
  <h2>AI热评总结</h2>
  <div class="topic_classified" v-html="htmlContent"></div>
  <!-- 使用 v-for 渲染 answers -->
  <div class="right-panel" id="answers-container">
    <div v-for="(answer, index) in answers" :key="index" class="answer-box">
      <div class="user-info">
        <div>
          <span class="user-name">{{ answer.name }}</span>
          <span class="like">回答点赞数：{{ answer.like }}</span>
        </div>
      </div>
      <div class="answer-content">
        <p v-for="(para, i) in answer.content" :key="i">{{ para }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'

export default {
  setup() {
    const route = useRoute()
    const userId = ref(route.params.userId)
    const topic_classified = ref('')

    const fetchDocument = async (id) => {
      try {
        const response = await fetch('/doc/' + id + '.md')
        topic_classified.value = await response.text()
      } catch (error) {
        console.error('读取txt文件出错:', error)
      }
    }

    // 将 JSON 数据请求封装为一个函数
    const fetchData = () => {
      fetch(`http://localhost:5251/?id=${userId.value}`)
        .then(response => response.json())
        .then(data => {
          console.log(data)
          view.value = data['被浏览量']
          hot_value.value = data['热度']
          followers.value = data['关注者']
          answers_count.value = data['总回答数']
          question.value = data['标题']
          link.value = data['链接']
          detail.value = data['描述']
          object.value = data
          answer1.value = data['回答1']
          console.log(answer1.value)
          answer1_like.value = data['回答1点赞数']
          answer2.value = data['回答2']
          answer2_like.value = data['回答2点赞数']
          answer3.value = data['回答3']
          answer3_like.value = data['回答3点赞数']
        })
        .catch(error => {
          console.error('请求出错:', error)
        })
    }

    onMounted(() => {
      fetchDocument(userId.value)
      fetchData()
    })

    watch(() => route.params.userId, (newId) => {
      userId.value = newId
      fetchDocument(newId)
      fetchData()
    })

    const object = ref({})
    const hot_value = ref()
    const followers = ref()
    const answers_count = ref()
    const view = ref()
    const question = ref()
    const link = ref()
    const detail = ref('')
    const answer1 = ref('')
    const answer1_like = ref('')
    const answer2 = ref('')
    const answer2_like = ref('')
    const answer3 = ref('')
    const answer3_like = ref('')
    const htmlContent = computed(() => marked(topic_classified.value))

    // 将答案数组合并为 computed ，以便动态更新
    const answers = computed(() => [
      {
        name: "高赞回答1",
        like: answer1_like.value,
        content: answer1.value
      },
      {
        name: "高赞回答2",
        like: answer2_like.value,
        content: answer2.value
      },
      {
        name: "高赞回答3",
        like: answer3_like.value,
        content: answer3.value
      }
    ])

    return {
      view,
      hot_value,
      followers,
      answers_count,
      userId,
      htmlContent,
      answers,
      question,
      link,
      detail,
    }
  }
}
</script>

