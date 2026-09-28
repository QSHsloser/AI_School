<template>
  <el-container class="main-container">
    <!-- 左侧导航栏 -->
    <el-aside :width="'200px'" class="sidebar">
      <div class="logo">
        <h3>学生系统</h3>
      </div>
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        background-color="#f0f9eb"
        text-color="#2d5016"
        active-text-color="#3eaf7c"
        unique-opened
      >
        <el-menu-item index="1" @click="$router.push('/student')">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="2" @click="$router.push('/student/courses')">
          <el-icon><Reading /></el-icon>
          <span>我的课程</span>
        </el-menu-item>
        <el-menu-item index="3" @click="$router.push('/student/homework')">
          <el-icon><Notebook /></el-icon>
          <span>我的作业</span>
        </el-menu-item>
        <el-menu-item index="4" @click="$router.push('/student/scores')">
          <el-icon><Rank /></el-icon>
          <span>成绩查询</span>
        </el-menu-item>
        <el-menu-item index="5" @click="$router.push('/student/book')">
          <el-icon><Reading /></el-icon>
          <span>我的书籍</span>
        </el-menu-item>
        <el-menu-item index="6" @click="openPersonalCenter">
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
              欢迎，{{ userInfo.username || '学生用户' }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
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
        <!-- 学生仪表板内容 - 仅在根路径显示 -->
        <div v-if="$route.path === '/student'" class="dashboard-container">
          <!-- 欢迎卡片 -->
          <el-card class="welcome-card">
            <template #header>
              <div class="card-header">欢迎回来</div>
            </template>
            <div class="welcome-content">
              <p>您好，{{ userInfo.username || '学生用户' }}！祝您学习愉快！</p>
              <div class="stats">
                <el-statistic title="我的课程" :value="stats.courses" :precision="0" />
                <el-statistic title="待完成作业" :value="stats.pendingHomework" :precision="0" />
                <el-statistic title="已完成作业" :value="stats.completedHomework" :precision="0" />
              </div>
            </div>
          </el-card>

          <!-- 最近活动 -->
          <el-card class="activity-card">
            <template #header>
              <div class="card-header">最近活动</div>
            </template>
            <el-timeline>
              <el-timeline-item v-for="(item, index) in recentActivity" :key="index" :timestamp="item.time">
                {{ item.content }}
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <!-- 快速导航 -->
          <el-card class="quick-nav-card">
            <template #header>
              <div class="card-header">快速导航</div>
            </template>
            <div class="quick-nav">
              <el-button type="primary" @click="$router.push('/student/courses')">
                <el-icon><Reading /></el-icon>
                查看我的课程
              </el-button>
              <el-button type="success" @click="$router.push('/student/homework')">
                <el-icon><Notebook /></el-icon>
                查看我的作业
              </el-button>
              <el-button type="warning" @click="$router.push('/student/scores')">
                <el-icon><Rank /></el-icon>
                查询成绩
              </el-button>
            </div>
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

// 仪表板数据
const stats = ref({
  courses: 8,
  pendingHomework: 3,
  completedHomework: 12
})

// 最近活动
const recentActivity = ref([
  { time: '2025-12-18', content: '高等数学作业已发布' },
  { time: '2025-12-17', content: '英语四级课程更新了新章节' },
  { time: '2025-12-16', content: '计算机基础作业已批改完成' },
  { time: '2025-12-15', content: '您提交了大学物理实验报告' }
])

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

onMounted(() => {
  // 这里可以添加获取用户数据和统计信息的API调用
  console.log('学生首页已加载')
})
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

// 仪表板样式
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.quick-nav-card {
  .quick-nav {
    display: flex;
    gap: 20px;
    .el-button {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
  }
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

// 深色主题样式
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
          background-color: #3d3d3d !important;
        }
        
        &.is-active {
          background-color: #3eaf7c !important;
          color: #ffffff !important;
        }
      }
    }
  }
  
  .header {
    background-color: #2d2d2d;
    border-bottom-color: #444;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
  
  .content {
    background-color: #1a1a1a;
  }
  
  .el-card {
    background-color: #2d2d2d;
    border-color: #444;
    
    .el-card__header {
      border-bottom-color: #444;
    }
  }
  
  .stats .el-statistic {
    background-color: #2d2d2d !important;
    border-color: #444;
  }
  
  .el-timeline-item__timestamp {
    color: #999;
  }
}
</style>