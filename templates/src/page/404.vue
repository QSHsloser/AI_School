<template>
  <div class="error-container">
    <div class="error-content">
      <div class="error-number">404</div>
      <div class="error-title">页面不存在</div>
      <div class="error-subtitle">很抱歉，您访问的页面可能已被删除或暂时不可用</div>
      <div class="error-actions">
        <el-button type="primary" size="large" @click="goHome">返回首页</el-button>
        <el-button size="large" @click="goBack">返回上一页</el-button>
      </div>
      <div class="error-image">
        <el-icon :size="120" color="rgba(255, 255, 255, 0.3)">
          <DocumentRemove />
        </el-icon>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DocumentRemove } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 返回首页
const goHome = () => {
  router.push('/')
}

// 返回上一页
const goBack = () => {
  router.back()
}
</script>

<style scoped>
.error-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e6f7f0 0%, #c3e6d4 100%);
  overflow: hidden;
}

.error-content {
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 60px 40px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  animation: fadeIn 0.8s ease-in-out;
}

.error-number {
  font-size: 120px;
  font-weight: 900;
  background: linear-gradient(135deg, #3eaf7c 0%, #2d9c68 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 20px;
  animation: bounceIn 1s ease-in-out;
}

.error-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin-bottom: 15px;
}

.error-subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 40px;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.error-actions .el-button {
  padding: 12px 30px;
  font-size: 16px;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.error-actions .el-button--primary {
  background: #3eaf7c;
  border: none;
}

.error-actions .el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(62, 175, 124, 0.3);
}

.error-actions .el-button:not(.el-button--primary):hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.error-image {
  margin-top: 20px;
  opacity: 0.8;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .error-number {
    font-size: 80px;
  }
  
  .error-title {
    font-size: 24px;
  }
  
  .error-subtitle {
    font-size: 14px;
  }
  
  .error-content {
    padding: 40px 20px;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .error-actions .el-button {
    width: 100%;
    max-width: 200px;
  }
}
</style>