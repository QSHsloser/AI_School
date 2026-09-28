<template>
  <div class="home-container">
    <!-- 头部区域 -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon class="logo-icon"><Reading /></el-icon>
          <h1 class="logo-text">AI精准教育平台</h1>
        </div>
        <nav class="nav">
          <el-menu mode="horizontal" background-color="transparent" text-color="#000" active-text-color="#3eaf7c">
            <el-menu-item index="1" @click="goToHome">首页</el-menu-item>
            <el-menu-item index="2" @click="showNotImplemented">课程介绍</el-menu-item>
            <el-menu-item index="3" @click="showNotImplemented">关于我们</el-menu-item>
            <el-menu-item index="4" @click="showNotImplemented">联系我们</el-menu-item>
            <!-- 根据登录状态动态显示 -->
            <template v-if="isLoggedIn">
              <el-menu-item index="5" @click="logout">退出登录</el-menu-item>
            </template>
            <template v-else>
              <el-menu-item index="5" @click="goToLogin">注册/登录</el-menu-item>
            </template>
          </el-menu>
        </nav>
      </div>
    </header>

    <!-- 主体内容区域 -->
    <main class="main-content">
      <div class="content-wrapper">
        <div class="text-content">
          <h2 class="title">
            <span class="highlight">智能教育</span>，成就未来
          </h2>
          <p class="subtitle">
            我们致力于提供高质量的在线教育服务，帮助学生和教师实现更好的教学体验和学习效果
          </p>
          <div class="button-group">
            <el-button
              type="primary"
              size="large"
              :icon="UserFilled"
              round
              @click="goToStudent"
            >
              学生入口
            </el-button>
            <el-button
              type="success"
              size="large"
              :icon="Avatar"
              round
              @click="goToTeacher"
            >
              教师入口
            </el-button>
          </div>
        </div>
        <div class="image-content">
          <el-card class="feature-card">
            <div class="feature-icon">
              <el-icon><Cpu /></el-icon>
            </div>
            <h3 class="feature-title">AI驱动的学习</h3>
            <p class="feature-description">个性化学习路径，智能推荐课程</p>
          </el-card>
          <el-card class="feature-card">
            <div class="feature-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <h3 class="feature-title">在线互动教学</h3>
            <p class="feature-description">实时互动课堂，提高学习效率</p>
          </el-card>
          <el-card class="feature-card">
            <div class="feature-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <h3 class="feature-title">学习数据分析</h3>
            <p class="feature-description">详细的学习报告，全面了解学习情况</p>
          </el-card>
        </div>
      </div>
    </main>

    <!-- 页脚区域 -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2025 AI精准教育平台. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Reading, UserFilled, Avatar, Cpu, 
  Monitor, DataAnalysis, ArrowDown 
} from '@element-plus/icons-vue'

const router = useRouter()

// 登录状态检测
const isLoggedIn = ref(false)

// 组件挂载时检查登录状态
onMounted(() => {
  const userInfo = localStorage.getItem('userInfo')
  isLoggedIn.value = !!userInfo
})

// 跳转到学生主页
const goToStudent = () => {
  router.push('/student')
}

// 跳转到教师主页
const goToTeacher = () => {
  router.push('/teacher')
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 显示功能未完善提示
const showNotImplemented = () => {
  ElMessage.warning('功能未完善')
}

// 跳转到登录页面
const goToLogin = () => {
  router.push('/login')
}

// 退出登录
const logout = () => {
  // 清除localStorage中的用户信息
  localStorage.removeItem('userInfo')
  // 更新登录状态
  isLoggedIn.value = false
  // 跳转到首页
  router.push('/')
  // 显示退出成功消息
  ElMessage.success('退出登录成功')
}
</script>

<style lang="scss" scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-image: url('../../assets/login_bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  overflow: hidden;
}

.home-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4); /* 添加半透明黑色遮罩 */
  z-index: 0;
}

.header, .main-content, .footer {
  position: relative;
  z-index: 1;
}

.header {
  padding: 20px 0;
  position: relative;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  .logo-icon {
    font-size: 32px;
    color: #3eaf7c;
  }
  .logo-text {
    margin: 0;
    color: #fff;
    font-size: 24px;
    font-weight: 700;
  }
}

.nav {
  .el-menu {
    border-bottom: none;
    
    .el-menu-item {
      color: rgba(255, 255, 255, 0.95) !important;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
      font-weight: 500;
      
      &:hover {
        color: #fff !important;
      }
      
      &.is-active {
        color: #3eaf7c !important;
      }
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.content-wrapper {
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.text-content {
  text-align: center;
  color: #fff;
  .title {
    font-size: 48px;
    margin-bottom: 20px;
    font-weight: 700;
    line-height: 1.2;
    .highlight {
      color: #3eaf7c;
    }
  }
  .subtitle {
    font-size: 18px;
    margin-bottom: 40px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    opacity: 0.9;
  }
  .button-group {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    .el-button {
      padding: 12px 40px;
      font-size: 18px;
      font-weight: 600;
      transition: all 0.3s ease;
      &:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
      }
    }
  }
}

.image-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  .feature-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    .feature-icon {
      font-size: 64px;
      color: #3eaf7c;
      margin-bottom: 20px;
    }
    .feature-title {
      font-size: 20px;
      margin-bottom: 15px;
      color: #303133;
      font-weight: 600;
    }
    .feature-description {
      color: #606266;
      font-size: 16px;
    }
  }
}

.footer {
  padding: 30px 20px;
  background-color: rgba(0, 0, 0, 0.2);
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    p {
      margin: 0;
      font-size: 14px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 20px;
  }
  
  .title {
    font-size: 36px !important;
  }
  
  .subtitle {
    font-size: 16px !important;
  }
  
  .button-group {
    flex-direction: column;
    align-items: center;
  }
  
  .image-content {
    grid-template-columns: 1fr;
  }
}
</style>
