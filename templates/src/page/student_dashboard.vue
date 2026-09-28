<template>
  <div class="dashboard-container">
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
        <el-button type="warning" @click="$router.push('/student/score')">
          <el-icon><Rank /></el-icon>
          查询成绩
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Reading, Notebook, Rank } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 用户信息
const userInfo = ref({
  username: localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')).username : '',
})

// 统计数据
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

onMounted(() => {
  // 这里可以添加获取用户数据和统计信息的API调用
  console.log('学生首页已加载')
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.welcome-card {
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
</style>