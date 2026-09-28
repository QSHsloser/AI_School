<template>
  <div class="courses-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的课程</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索课程"
            clearable
            class="search-input"
          >
            <template #prepend>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>
      
      <!-- 课程列表 -->
      <el-table :data="filteredCourses" stripe style="width: 100%">
        <el-table-column prop="courseName" label="课程名称" width="200" />
        <el-table-column prop="teacher" label="授课教师" width="150" />
        <el-table-column prop="startDate" label="开始日期" width="150" />
        <el-table-column prop="endDate" label="结束日期" width="150" />
        <el-table-column prop="status" label="课程状态" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.status === '进行中' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="学习进度" width="150">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.progress"
              :format="percentage => `${percentage}%`"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewCourse(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="filteredCourses.length"
          :page-size="10"
        />
      </div>
    </el-card>

    <!-- 课程详情弹窗 -->
    <el-dialog
      v-model="courseDetailVisible"
      :title="selectedCourse.courseName || '课程详情'"
      width="700px"
    >
      <div v-if="selectedCourse" class="course-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="课程名称">{{ selectedCourse.courseName }}</el-descriptions-item>
          <el-descriptions-item label="授课教师">{{ selectedCourse.teacher }}</el-descriptions-item>
          <el-descriptions-item label="课程简介">{{ selectedCourse.description }}</el-descriptions-item>
          <el-descriptions-item label="开始日期">{{ selectedCourse.startDate }}</el-descriptions-item>
          <el-descriptions-item label="结束日期">{{ selectedCourse.endDate }}</el-descriptions-item>
          <el-descriptions-item label="上课时间">{{ selectedCourse.schedule }}</el-descriptions-item>
          <el-descriptions-item label="上课地点">{{ selectedCourse.location }}</el-descriptions-item>
          <el-descriptions-item label="课程状态">
            <el-tag :type="selectedCourse.status === '进行中' ? 'success' : 'warning'">
              {{ selectedCourse.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="学习进度">
            <el-progress :percentage="selectedCourse.progress" />
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="courseDetailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 搜索查询
const searchQuery = ref('')

// 课程详情弹窗
const courseDetailVisible = ref(false)
const selectedCourse = ref({})

// 模拟课程数据
const coursesData = ref([
  {
    courseId: 1,
    courseName: '数学',
    teacher: '张老师',
    startDate: '2025-09-01',
    endDate: '2026-01-15',
    status: '进行中',
    progress: 65,
    description: '初中数学是初中生的基础课程，主要包括不等式求解、三角函数等。',
    schedule: '每周一、三、五 14:00-15:40',
    location: '教学楼A301'
  },
  {
    courseId: 2,
    courseName: '英语',
    teacher: '李老师',
    startDate: '2025-09-01',
    endDate: '2026-01-15',
    status: '进行中',
    progress: 80,
    description: '初中英语课程，提升学生的英语听、说、读、写能力。',
    schedule: '每周二、四 9:00-10:40',
    location: '语音楼B203'
  },
  {
    courseId: 3,
    courseName: '计算机',
    teacher: '王老师',
    startDate: '2025-09-01',
    endDate: '2026-01-15',
    status: '进行中',
    progress: 75,
    description: '计算机基础知识，包括操作系统、办公软件等。',
    schedule: '每周一、三 9:00-10:40',
    location: '实验楼C402'
  },
  {
    courseId: 4,
    courseName: '物理',
    teacher: '赵教授',
    startDate: '2025-09-01',
    endDate: '2026-01-15',
    status: '进行中',
    progress: 50,
    description: '初中物理课程，涵盖力学、热学、电磁学等内容。',
    schedule: '每周二、四 14:00-15:40',
    location: '实验楼D501'
  },
  {
    courseId: 5,
    courseName: '思想与品德',
    teacher: '刘老师',
    startDate: '2025-09-01',
    endDate: '2026-01-15',
    status: '进行中',
    progress: 90,
    description: '思想与品德初步接触政治思想。',
    schedule: '每周五 9:00-12:00',
    location: '教学楼B201'
  }
])

// 过滤课程数据
const filteredCourses = computed(() => {
  if (!searchQuery.value) return coursesData.value
  return coursesData.value.filter(course => 
    course.courseName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    course.teacher.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 查看课程详情
const viewCourse = (course) => {
  selectedCourse.value = course
  courseDetailVisible.value = true
}
</script>

<style lang="scss" scoped>
.courses-container {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.search-input {
  width: 300px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.course-detail {
  margin-top: 20px;
}
</style>