<template>
  <el-container class="main-container">
    <!-- 左侧导航栏 -->
    <el-aside :width="'200px'" class="sidebar">
      <div class="logo">
        <h3>教师系统</h3>
      </div>
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        background-color="#f0f9eb"
        text-color="#2d5016"
        active-text-color="#3eaf7c"
        unique-opened
      >
        <el-menu-item index="1" @click="router.push('/teacher')">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="2" @click="navigateTo('class-management')">
          <el-icon><Reading /></el-icon>
          <span>班级管理</span>
        </el-menu-item>
        <el-menu-item index="3" @click="navigateTo('homework-management')">
          <el-icon><Notebook /></el-icon>
          <span>作业管理</span>
        </el-menu-item>
        <el-menu-item index="4" @click="navigateTo('score-management')">
          <el-icon><Rank /></el-icon>
          <span>成绩管理</span>
        </el-menu-item>
        <el-menu-item index="5" @click="openPersonalCenter">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航 -->
      <el-header class="header">
        <div class="home-btn">
          <el-button type="success" round @click="goToHome" :icon="House">
            返回主页
          </el-button>
        </div>
        <div class="user-info">
          <el-dropdown>
            <span class="el-dropdown-link">
              欢迎，{{ userInfo.username || '教师用户' }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="openPersonalCenter">个人中心</el-dropdown-item>
                <el-dropdown-item @click="openSettings">设置</el-dropdown-item>
                <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="content">
        <!-- 教师仪表板内容 - 仅在根路径显示 -->
        <div v-if="$route.path === '/teacher'" class="teacher-dashboard">
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
                  <div class="message-content">
                    <div v-html="msg.content.replace(/\n/g, '<br>')"></div>
                    <!-- 文件显示 -->
                    <div v-if="msg.files && msg.files.length > 0" class="message-files">
                      <div v-for="(file, fileIndex) in msg.files" :key="fileIndex" class="file-item">
                        <div class="file-info" @click="previewFile(file)">
                          <div class="file-icon"><el-icon><Document /></el-icon></div>
                          <div class="file-details">
                            <div class="file-name">{{ file.name }}</div>
                            <div class="file-size">{{ formatFileSize(file.size) }}</div>
                          </div>
                        </div>
                        <el-button v-if="file.file_id" type="primary" size="small" @click.stop="downloadFile(file)">
                          <el-icon><Download /></el-icon> 下载
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="isTyping" class="message-item ai">
                  <div class="message-content">
                    <el-skeleton :rows="1" animated />
                  </div>
                </div>
              </div>
              <!-- 输入区域 -->
              <div class="chat-input-area">
                <div class="file-upload-container">
                  <el-upload
                    class="upload-btn"
                    :file-list="fileList"
                    :auto-upload="false"
                    :on-change="handleFileChange"
                    :show-file-list="false"
                  >
                    <el-button type="primary" :icon="Upload" plain>
                      上传文件
                    </el-button>
                  </el-upload>
                  <!-- 已选择文件显示 -->
                  <div v-if="fileList.length > 0" class="selected-files">
                    <el-tag v-for="(file, index) in fileList" :key="index" closable @close="removeFile(index)" size="small">
                      {{ file.name }}
                    </el-tag>
                  </div>
                </div>
                <el-input
                  v-model="inputMessage"
                  placeholder="请输入您的问题..."
                  class="message-input"
                  @keyup.enter="sendMessage"
                />
                <div class="action-buttons">
                  <!-- 停止响应按钮 -->
                  <el-button 
                    v-if="isTyping" 
                    type="danger" 
                    @click="stopResponse" 
                    :icon="Close"
                  >
                    停止响应
                  </el-button>
                  <el-button type="primary" @click="sendMessage" :disabled="!inputMessage.trim() && fileList.length === 0 || isTyping">
                    发送
                  </el-button>
                </div>
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
        <!-- 子路由内容渲染 -->
        <router-view />
      </el-main>
    </el-container>
  </el-container>

  <!-- 个人中心弹窗 -->
  <el-dialog
    v-model="personalCenterVisible"
    title="个人中心"
    width="500px"
  >
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="info">
        <el-form label-position="left" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username" readonly />
          </el-form-item>
          <el-form-item label="账号">
            <el-input v-model="userInfo.account" readonly />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="userInfo.phone" readonly />
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="修改手机号" name="phone">
        <el-form label-position="left" label-width="120px">
          <el-form-item label="原手机号">
            <el-input v-model="phoneForm.oldPhone" type="tel" placeholder="请输入原手机号" />
          </el-form-item>
          <el-form-item label="新手机号">
            <el-input v-model="phoneForm.newPhone" type="tel" placeholder="请输入新手机号" />
          </el-form-item>
          <el-form-item label="验证码">
            <el-input v-model="phoneForm.verificationCode" placeholder="请输入验证码">
              <template #append>
                <el-button>获取验证码</el-button>
              </template>
            </el-input>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="password">
        <el-form label-position="left" label-width="120px">
          <el-form-item label="原密码">
            <el-input v-model="passwordForm.oldPassword" type="password" placeholder="请输入原密码" />
          </el-form-item>
          <el-form-item label="新密码">
            <el-input v-model="passwordForm.newPassword" type="password" placeholder="请输入新密码" />
          </el-form-item>
          <el-form-item label="确认密码">
            <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="请确认新密码" />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="personalCenterVisible = false">取消</el-button>
        <el-button type="primary" @click="activeTab === 'phone' ? updatePhone() : updatePassword()">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 设置弹窗 -->
  <el-dialog
    v-model="settingsVisible"
    title="设置"
    width="400px"
  >
    <el-form label-position="left" label-width="80px">
      <el-form-item label="主题">
        <el-radio-group v-model="theme">
          <el-radio label="light">浅色</el-radio>
          <el-radio label="dark">深色</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="通知">
        <el-checkbox v-model="notifications" label="接收系统通知" />
      </el-form-item>
      <el-form-item label="语言">
        <el-select v-model="language" placeholder="请选择语言">
          <el-option label="中文" value="zh-CN" />
          <el-option label="English" value="en-US" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="settingsVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { House, Reading, Notebook, Rank, User, ArrowDown, Setting, Upload, Close, Document, Download } from '@element-plus/icons-vue'
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElSkeleton, ElUpload } from 'element-plus'

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
    content: '+您好，我是您的助手，有什么可以帮助您的吗？\n您可以输入以下功能：\n1. 生成题目\n2. 布置作业\n3. 管理班级'
  }
])
const inputMessage = ref('')
const isTyping = ref(false)
const chatMessages = ref(null)
// 文件上传相关
const fileList = ref([])
const currentConversationId = ref('')

// 文件上传处理
const handleFileChange = (uploadFile, uploadFiles) => {
  fileList.value = uploadFiles
}

// 移除文件
const removeFile = (index) => {
  fileList.value.splice(index, 1)
}

// 发送消息
const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if ((!message && fileList.value.length === 0) || isTyping.value) return
  
  // 准备用户消息
  const userMsg = {
    type: 'user',
    content: message
  }
  
  // 如果有文件，添加到消息中
  if (fileList.value.length > 0) {
    userMsg.files = fileList.value.map(file => ({ name: file.name, size: file.size }))
  }
  
  // 添加用户消息
  messages.value.push(userMsg)
  
  inputMessage.value = ''
  isTyping.value = true
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  try {
    let response
    
    // 根据是否有文件选择不同的请求方式
    if (fileList.value.length > 0) {
      // 有文件，使用FormData和multipart/form-data
      const formData = new FormData()
      formData.append('message', message)
      formData.append('user_type', 'teacher')
      formData.append('username', userInfo.value.username || 'test_teacher')
      
      // 添加文件 - 只上传第一个文件，因为Dify API只允许单次上传一个文件
      if (fileList.value.length > 0) {
        formData.append('file', fileList.value[0].raw)
      }
      
      response = await fetch('http://127.0.0.1:8000/v1/', {
        method: 'POST',
        body: formData
      })
      
      // 清空文件列表
      fileList.value = []
    } else {
      // 没有文件，使用JSON请求
      response = await fetch('http://127.0.0.1:8000/v1/', {
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
    }
    
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
              // 保存会话ID
              if (data.conversation_id) {
                currentConversationId.value = data.conversation_id
              }
              
              // 先处理文件信息 - 无论是否有answer或done字段，都要处理files字段
              if (data.files && data.files.length > 0) {
                console.log('Dify API返回的files字段结构:', JSON.stringify(data.files, null, 2));
                // 转换文件结构以匹配前端期望的格式
                const formattedFiles = data.files.map((file, index) => {
                  const fileId = file.id || file.file_id || '';
                  console.log(`处理第${index+1}个文件，原始文件数据:`, JSON.stringify(file, null, 2));
                  console.log(`提取到的file_id:`, fileId);
                  return {
                    name: file.name || `file_${fileId || Date.now()}`,
                    size: file.size || file.file_size || 0,  // 处理不同的size字段名
                    file_id: fileId,  // 处理不同的file_id字段名
                    mime_type: file.mime_type || file.content_type || 'application/octet-stream'
                  };
                });
                console.log('格式化后的文件数据:', JSON.stringify(formattedFiles, null, 2));
                
                if (tempMessageIndex !== -1) {
                  messages.value[tempMessageIndex].files = formattedFiles
                } else {
                  tempMessageIndex = messages.value.length
                  messages.value.push({
                    type: 'ai',
                    content: data.answer || '',
                    files: formattedFiles
                  })
                }
              }
              
              // 处理回答内容
              if (data.answer) {
                aiMessage += data.answer
                if (tempMessageIndex === -1) {
                  tempMessageIndex = messages.value.length
                  // 格式化文件数据（如果有）
                  let formattedFiles = []
                  if (data.files && data.files.length > 0) {
                    formattedFiles = data.files.map((file, index) => {
                      const fileId = file.id || file.file_id || '';
                      return {
                        name: file.name || `file_${fileId || Date.now()}`,
                        size: file.size || file.file_size || 0,
                        file_id: fileId,
                        mime_type: file.mime_type || file.content_type || 'application/octet-stream'
                      };
                    });
                  }
                  messages.value.push({
                    type: 'ai',
                    content: data.answer,
                    files: formattedFiles
                  })
                } else {
                  messages.value[tempMessageIndex].content = aiMessage
                }
                // 滚动到底部
                await nextTick()
                scrollToBottom()
              }
              
              // 处理错误
              if (data.error) {
                ElMessage.error(`错误: ${data.error}`)
                aiMessage = `抱歉，出现错误: ${data.error}`
              }
              
              // 对话完成
              if (data.done) {
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

// 停止响应
const stopResponse = async () => {
  if (!currentConversationId.value) {
    ElMessage.warning('没有正在进行的对话')
    return
  }
  
  try {
    await fetch('http://127.0.0.1:8000/v1/stop/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        conversation_id: currentConversationId.value,
        user_type: 'teacher'
      })
    })
    
    isTyping.value = false
    ElMessage.success('已停止响应')
  } catch (error) {
    ElMessage.error(`停止响应失败: ${error.message}`)
  }
}

// 预览文件
const previewFile = (file) => {
  if (file.file_id) {
    console.log('Previewing file:', file);
    window.open(`http://127.0.0.1:8000/v1/preview/?file_id=${file.file_id}&user_type=teacher&as_attachment=false`, '_blank')
  } else {
    console.error('File ID not found:', file);
    ElMessage.warning('文件ID不存在，无法预览')
  }
}

// 下载文件
const downloadFile = (file) => {
  if (file.file_id) {
    console.log('Downloading file:', file);
    window.open(`http://127.0.0.1:8000/v1/preview/?file_id=${file.file_id}&user_type=teacher&as_attachment=true`, '_self')
  } else {
    console.error('File ID not found:', file);
    ElMessage.warning('文件ID不存在，无法下载')
  }
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let index = 0
  let fileSize = size
  while (fileSize >= 1024 && index < units.length - 1) {
    fileSize /= 1024
    index++
  }
  return `${fileSize.toFixed(2)} ${units[index]}`
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight
  }
}

// 弹窗控制
const personalCenterVisible = ref(false)
const settingsVisible = ref(false)

// 修改手机号和密码的表单数据
const phoneForm = ref({
  oldPhone: '',
  newPhone: '',
  verificationCode: ''
})

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 个人中心标签页
const activeTab = ref('info')

// 设置表单数据
const theme = ref(localStorage.getItem('theme') || 'light')
const notifications = ref(localStorage.getItem('notifications') !== 'false')
const language = ref(localStorage.getItem('language') || 'zh-CN')

// 初始化主题
const initTheme = () => {
  if (theme.value === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 切换主题
const toggleTheme = (newTheme) => {
  theme.value = newTheme
  if (newTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('theme', newTheme)
}

// 初始化时设置主题
initTheme()

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 打开个人中心
const openPersonalCenter = () => {
  personalCenterVisible.value = true
}

// 打开设置
const openSettings = () => {
  settingsVisible.value = true
}

// 退出登录
const logout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    localStorage.removeItem('userInfo')
    router.push('/')
    ElMessage.success('退出登录成功')
  }).catch(() => {
    ElMessage.info('取消退出')
  })
}

// 修改手机号
const updatePhone = () => {
  // 这里可以添加手机号验证和更新逻辑
  ElMessage.success('手机号修改成功')
  personalCenterVisible.value = false
  phoneForm.value = {
    oldPhone: '',
    newPhone: '',
    verificationCode: ''
  }
}

// 修改密码
const updatePassword = () => {
  // 这里可以添加密码验证和更新逻辑
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  ElMessage.success('密码修改成功')
  personalCenterVisible.value = false
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}

// 导航菜单跳转
const navigateTo = (path) => {
  router.push(`/teacher/${path}`)
}

// 保存设置
const saveSettings = () => {
  // 保存设置到本地存储
  localStorage.setItem('theme', theme.value)
  localStorage.setItem('notifications', notifications.value)
  localStorage.setItem('language', language.value)
  
  // 应用主题设置
  toggleTheme(theme.value)
  
  ElMessage.success('设置保存成功')
  settingsVisible.value = false
}
</script>

<style lang="scss" scoped>
.main-container {
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background-color: #f0f9eb;
  border-right: 1px solid #d9f7be;
  .logo {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #d9f7be;
    h3 {
      margin: 0;
      color: #2d5016;
      font-weight: 600;
    }
  }
}

.header {
  background-color: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  .user-info {
    display: flex;
    align-items: center;
  }
  .home-btn {
    display: flex;
    align-items: center;
  }
}

.content {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

/* 教师仪表板样式 */
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
          
          .message-files {
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
          }
          
          .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 6px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            border-left: 3px solid #3eaf7c;
          }
          
          .file-info {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            flex: 1;
          }
          
          .file-icon {
            color: #3eaf7c;
            font-size: 18px;
          }
          
          .file-details {
            display: flex;
            flex-direction: column;
            justify-content: center;
          }
          
          .file-name {
            font-weight: 500;
            font-size: 14px;
            color: #333;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 300px;
          }
          
          .file-size {
            font-size: 12px;
            color: #909399;
          }
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

/* 深色主题下的聊天样式 */
.dark {
  .teacher-dashboard {
    .chat-card {
      background-color: #2d2d2d;
      border-color: #444;
      
      .chat-messages {
        background-color: #3a3a3a;
        
        .message-item {
          &.user {
            .message-content {
              background-color: #3eaf7c;
              color: white;
            }
          }
          
          &.ai {
            .message-content {
              background-color: #4a4a4a;
              color: #e0e0e0;
              box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            }
          }
        }
      }
    }
  }
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

/* 深色主题样式 */
.dark {
  .main-container {
    background-color: #1a1a1a;
    color: #e0e0e0;
  }
  
  .sidebar {
    background-color: #2d2d2d;
    border-right-color: #444;
    
    .logo {
      border-bottom-color: #444;
      
      h3 {
        color: #3eaf7c;
      }
    }
    
    .el-menu {
      background-color: #2d2d2d !important;
      color: #e0e0e0 !important;
      
      .el-menu-item {
        color: #e0e0e0 !important;
        
        &:hover {
          background-color: #3a3a3a !important;
        }
        
        &.is-active {
          background-color: #3eaf7c !important;
          color: #fff !important;
        }
      }
    }
  }
  
  .header {
    background-color: #2d2d2d;
    border-bottom-color: #444;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    
    .el-button {
      background-color: #3eaf7c;
      border-color: #3eaf7c;
      
      &:hover {
        background-color: #2d8a5a;
        border-color: #2d8a5a;
      }
    }
    
    .user-info {
      .el-dropdown-link {
        color: #e0e0e0;
      }
    }
  }
  
  .content {
    background-color: #1a1a1a;
  }
  
  .welcome-card {
    background-color: #2d2d2d;
    border-color: #444;
    
    .welcome-content {
      p {
        color: #e0e0e0;
      }
      
      .stats {
        .el-statistic {
          background-color: #3a3a3a;
          color: #e0e0e0;
          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
          
          .el-statistic__label {
            color: #b0b0b0;
          }
          
          .el-statistic__value {
            color: #e0e0e0 !important;
          }
        }
      }
    }
  }
  
  .activity-card {
    background-color: #2d2d2d;
    border-color: #444;
    
    .card-header {
      color: #e0e0e0;
    }
    
    .el-timeline {
      .el-timeline-item {
        color: #e0e0e0;
        
        .el-timeline-item__timestamp {
          color: #b0b0b0;
        }
      }
    }
  }
  
  /* 弹窗样式 */
  .el-dialog {
    background-color: #2d2d2d;
    border-color: #444;
    
    .el-dialog__header {
      border-bottom-color: #444;
      
      .el-dialog__title {
        color: #e0e0e0;
      }
    }
    
    .el-tabs {
      .el-tabs__nav {
        border-bottom-color: #444;
        
        .el-tabs__item {
          color: #b0b0b0;
          
          &.is-active {
            color: #3eaf7c;
          }
        }
      }
    }
    
    .el-form {
      .el-form-item {
        .el-form-item__label {
          color: #e0e0e0;
        }
      }
    }
    
    .el-input {
      .el-input__inner {
        background-color: #3a3a3a;
        border-color: #555;
        color: #e0e0e0;
        
        &:focus {
          border-color: #3eaf7c;
        }
      }
    }
    
    .el-button {
      &.el-button--default {
        background-color: #3a3a3a;
        border-color: #555;
        color: #e0e0e0;
        
        &:hover {
          background-color: #4a4a4a;
          border-color: #666;
          color: #e0e0e0;
        }
      }
      
      &.el-button--primary {
        background-color: #3eaf7c;
        border-color: #3eaf7c;
        color: #fff;
        
        &:hover {
          background-color: #2d8a5a;
          border-color: #2d8a5a;
          color: #fff;
        }
      }
    }
  }
  
  /* 设置弹窗样式 */
  .el-radio-group {
    .el-radio {
      color: #e0e0e0;
      
      .el-radio__input {
        .el-radio__inner {
          border-color: #555;
          
          &:after {
            background-color: #3eaf7c;
          }
        }
        
        &.is-checked {
          .el-radio__inner {
            border-color: #3eaf7c;
            background-color: #3eaf7c;
          }
        }
      }
    }
  }
  
  .el-checkbox {
    color: #e0e0e0;
    
    .el-checkbox__input {
      .el-checkbox__inner {
        border-color: #555;
        background-color: #3a3a3a;
        
        &:after {
          border-color: #fff;
        }
      }
      
      &.is-checked {
        .el-checkbox__inner {
          border-color: #3eaf7c;
          background-color: #3eaf7c;
        }
      }
    }
  }
  
  .el-select {
    .el-select__wrapper {
      background-color: #3a3a3a;
      border-color: #555;
      
      &:hover {
        border-color: #666;
      }
      
      &.is-focus {
        border-color: #3eaf7c;
      }
    }
    
    .el-select__input {
      color: #e0e0e0;
    }
    
    .el-select__placeholder {
      color: #888;
    }
  }
  
  .el-dropdown-menu {
    background-color: #2d2d2d;
    border-color: #444;
    
    .el-dropdown-item {
      color: #e0e0e0;
      
      &:hover {
        background-color: #3a3a3a;
      }
      
      &.is-divided {
        border-top-color: #444;
      }
    }
  }
}
</style>