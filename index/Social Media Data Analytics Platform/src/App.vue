<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink , RouterView} from 'vue-router'

let id = 1
const jsonData = ref(null)




// 异步函数：将中文字符串进行 SHA-256 哈希，并转换为十进制数字字符串
async function chineseToNumericHash(text) {
  // 将字符串编码为 UTF-8
  const encoder = new TextEncoder()
  const data = encoder.encode(text)
  // 计算 SHA-256 哈希，返回 ArrayBuffer
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  // 将 Hash 数组缓冲转换为十六进制字符串
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  const hexHash = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('')
  // 使用 BigInt 将十六进制转为十进制字符串
  const numericHash = BigInt('0x' + hexHash).toString()
  return numericHash
}



async function fetchData() {
  try {
    const response = await fetch('http://localhost:5251/')
    const data = await response.json()
    // 假设 data.name 与 data.hot_value 均为数组
    const items = data.name.map((name, index) => ({
      id: id++,
      text: name,
      hot_value: data.hot_value[index],
      hash: "",
    }))
    // 计算哈希值
    for (const item of items) {
      item.hash = await chineseToNumericHash(item.text)
    }
    jsonData.value = items
  } catch (error) {
    console.error('请求数据失败：', error)
  }
}

onMounted(() => {
  fetchData()
  console.log(jsonData.value)
})


</script>



<template>
  <header>
        <h1>今日知乎热点</h1>
    </header>
    
    <div class="container">
        <aside>
            <RouterView />
        </aside>
        
        
        <main>
            <h2>Hot Search List</h2>
            <ul class="trend-list">
             
                <li v-for="list in jsonData" :key="list.id" class="trend-item">
                    <span class="rank">{{ list.id }}</span>
                    <router-link class="custom-link" :to="{ name: 'analyse', params: { userId: list.hash } }">{{ list.text }}</router-link>
                  <span class="hotness">🔥 {{ list.hot_value }}</span>
                </li>

            </ul>
        </main>
    </div>
    
</template>

