<template>
  <div class="teacher-dashboard">
    <!-- 人工智能对话区域 -->
    <el-card class="chat-card">
      <template #header>
        <div class="card-header">
          <span>智能助手</span>
        </div>
      </template>
      <div class="chat-container">
        <!-- 对话消息列表 -->
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(msg, index) in messages" :key="index" :class="['message-item', msg.type]">
            <div class="message-content">{{ msg.content }}</div>
          </div>
          <div v-if="isTyping" class="message-item ai">
            <div class="message-content">
              <el-skeleton :rows="1" animated />
            </div>
          </div>
        </div>
        <!-- 输入区域 -->
        <div class="chat-input-area">
          <el-input
            v-model="inputMessage"
            placeholder="请输入您的问题..."
            class="message-input"
            @keyup.enter="sendMessage"
          />
          <el-button type="primary" @click="sendMessage" :disabled="!inputMessage.trim() || isTyping">
            发送
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 欢迎卡片 -->
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <span>欢迎使用教师系统</span>
        </div>
      </template>
      <div class="welcome-content">
        <p>这是教师端的主页，您可以在这里管理您的课程、作业和学生成绩。</p>
        <div class="stats">
          <el-statistic title="教授课程" :value="5" suffix="门" />
          <el-statistic title="待批改作业" :value="25" suffix="份" />
          <el-statistic title="学生人数" :value="120" suffix="人" />
        </div>
      </div>
    </el-card>

    <!-- 最近动态 -->
    <el-card class="activity-card">
      <template #header>
        <div class="card-header">
          <span>最近动态</span>
          <el-button type="primary" size="small">查看全部</el-button>
        </div>
      </template>
      <el-timeline>
        <el-timeline-item timestamp="2025-12-18 14:30" placement="top">
          发布了新作业《高等数学期末复习题》
        </el-timeline-item>
        <el-timeline-item timestamp="2025-12-17 10:00" placement="top">
          批改了学生提交的英语作业
        </el-timeline-item>
        <el-timeline-item timestamp="2025-12-16 16:45" placement="top">
          上传了新的教学视频《编程基础》
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { House, Reading, Notebook, Rank, User, ArrowDown, Setting } from '@element-plus/icons-vue'
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElSkeleton } from 'element-plus'

const router = useRouter()

// 用户信息
const userInfo = ref({
  username: localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')).username : '',
  phone: '138****8888', // 示例手机号
  account: localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')).username : ''
})

// 对话功能
const messages = ref([
  {
    type: 'ai',
    content: '您好，我是智能助手，有什么可以帮助您的吗？'
  }
])
const inputMessage = ref('')
const isTyping = ref(false)
const chatMessages = ref(null)

// 发送消息
const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if (!message || isTyping.value) return
  
  // 添加用户消息
  messages.value.push({
    type: 'user',
    content: message
  })
  
  inputMessage.value = ''
  isTyping.value = true
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  try {
    // 调用后端API
    const response = await fetch('http://127.0.0.1:8000/v1/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        user_type: 'teacher',
        username: userInfo.value.username || 'test_teacher'
      })
    })
    
    if (!response.ok) {
      throw new Error('请求失败')
    }
    
    // 处理流式响应
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let aiMessage = ''
    let tempMessageIndex = -1
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')
      
      for (const line of lines) {
        if (line.trim()) {
          try {
            const data = JSON.parse(line)
            if (data.done) {
              // 对话完成
              break
            } else if (data.answer) {
              // 更新AI回复
              aiMessage += data.answer
              if (tempMessageIndex === -1) {
                tempMessageIndex = messages.value.length
                messages.value.push({
                  type: 'ai',
                  content: data.answer
                })
              } else {
                messages.value[tempMessageIndex].content = aiMessage
              }
              // 滚动到底部
              await nextTick()
              scrollToBottom()
            } else if (data.error) {
              ElMessage.error(`错误: ${data.error}`)
              aiMessage = `抱歉，出现错误: ${data.error}`
              break
            }
          } catch (e) {
            // JSON解析错误，忽略
            continue
          }
        }
      }
    }
    
    // 如果没有接收到完整消息，添加默认回复
    if (aiMessage === '') {
      messages.value.push({
        type: 'ai',
        content: '抱歉，我暂时无法回答您的问题，请稍后再试。'
      })
    }
    
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
    messages.value.push({
      type: 'ai',
      content: '抱歉，与服务器连接失败，请稍后再试。'
    })
  } finally {
    isTyping.value = false
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight
  }
}
</script>

<style lang="scss" scoped>
.teacher-dashboard {
  .chat-card {
    margin-bottom: 20px;
    .chat-container {
      display: flex;
      flex-direction: column;
      height: 400px;
    }
    
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 15px;
      margin-bottom: 15px;
      border-radius: 4px;
      background-color: #fafafa;
      
      .message-item {
        margin-bottom: 10px;
        display: flex;
        
        &.user {
          justify-content: flex-end;
          .message-content {
            background-color: #3eaf7c;
            color: white;
            border-radius: 15px 15px 0 15px;
            max-width: 70%;
          }
        }
        
        &.ai {
          justify-content: flex-start;
          .message-content {
            background-color: white;
            color: #333;
            border-radius: 15px 15px 15px 0;
            max-width: 70%;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          }
        }
        
        .message-content {
          padding: 10px 15px;
          word-wrap: break-word;
          line-height: 1.5;
        }
      }
    }
    
    .chat-input-area {
      display: flex;
      gap: 10px;
      align-items: flex-end;
      
      .message-input {
        flex: 1;
      }
    }
  }

  .welcome-card {
    margin-bottom: 20px;
    .welcome-content {
      p {
        margin-bottom: 20px;
        font-size: 16px;
        color: #606266;
      }
      .stats {
        display: flex;
        gap: 20px;
        .el-statistic {
          background-color: #ffffff;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
          flex: 1;
          text-align: center;
        }
      }
    }
  }

  .activity-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>