<template>
  <div class="student-scores">
    <el-card class="scores-card">
      <template #header>
        <div class="card-header">
          <span>成绩查询</span>
          <el-select v-model="semesterFilter" placeholder="筛选学期" style="width: 150px;">
            <el-option label="全部" value="" />
            <el-option label="2025-2026第一学期" value="2025-2026-1" />
            <el-option label="2024-2025第二学期" value="2024-2025-2" />
            <el-option label="2024-2025第一学期" value="2024-2025-1" />
          </el-select>
        </div>
      </template>
      
      <div style="margin-bottom: 20px;">
        <el-statistic title="平均成绩" :value="averageScore" suffix="分" />
        <el-statistic title="总学分" :value="totalCredit" suffix="学分" style="margin-left: 30px;" />
      </div>
      
      <el-table :data="scoresData" border style="width: 100%">
        <el-table-column prop="id" label="课程ID" width="80" />
        <el-table-column prop="course" label="课程名称" width="200" />
        <el-table-column prop="teacher" label="授课老师" width="120" />
        <el-table-column prop="credit" label="学分" width="80" align="center" />
        <el-table-column prop="semester" label="学期" width="150" />
        <el-table-column prop="score" label="分数" width="100" align="center" />
        <el-table-column prop="grade" label="等级" width="80" align="center">
          <template #default="scope">
            <el-tag :type="getGradeType(scope.row.grade)">
              {{ scope.row.grade }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewDetail(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div style="margin-top: 20px; text-align: center;">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="scoresData.length"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 学期筛选
const semesterFilter = ref('')

// 分页数据
const currentPage = ref(1)
const pageSize = ref(10)

// 成绩数据（模拟数据）
const scoresData = ref([
  { id: 1, course: '数学', teacher: '张老师', credit: 4, semester: '2025-2026第一学期', score: 85, grade: 'B+' },
  { id: 2, course: '英语', teacher: '李老师', credit: 4, semester: '2025-2026第一学期', score: 92, grade: 'A' },
  { id: 3, course: '语文', teacher: '王老师', credit: 3, semester: '2025-2026第一学期', score: 78, grade: 'C+' },
  { id: 4, course: '语文', teacher: '赵老师', credit: 3, semester: '2024-2025第二学期', score: 95, grade: 'A+' },
  { id: 5, course: '数学', teacher: '刘老师', credit: 3, semester: '2024-2025第二学期', score: 88, grade: 'B+' },
  { id: 6, course: '英语', teacher: '陈老师', credit: 3, semester: '2024-2025第二学期', score: 82, grade: 'B' },
  { id: 7, course: '物理', teacher: '孙老师', credit: 3, semester: '2024-2025第一学期', score: 75, grade: 'C+' },
])

// 计算平均成绩
const averageScore = computed(() => {
  if (scoresData.value.length === 0) return 0
  const sum = scoresData.value.reduce((acc, curr) => acc + curr.score, 0)
  return (sum / scoresData.value.length).toFixed(1)
})

// 计算总学分
const totalCredit = computed(() => {
  return scoresData.value.reduce((acc, curr) => acc + curr.credit, 0)
})

// 获取等级对应的标签类型
const getGradeType = (grade) => {
  const gradeMap = {
    'A+': 'success',
    'A': 'success',
    'A-': 'success',
    'B+': 'warning',
    'B': 'warning',
    'B-': 'warning',
    'C+': 'info',
    'C': 'info',
    'C-': 'info',
    'D+': 'danger',
    'D': 'danger',
    'F': 'danger'
  }
  return gradeMap[grade] || 'info'
}

// 查看详情
const viewDetail = (score) => {
  ElMessage.success(`查看课程详情：${score.course}`)
  // 这里可以添加实际的查看详情逻辑
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  console.log(`每页 ${val} 条`)
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  console.log(`当前页: ${val}`)
}
</script>

<style scoped>
.student-scores {
  padding: 20px;
}

.scores-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
</style>