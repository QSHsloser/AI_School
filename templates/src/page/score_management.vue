<template>
  <el-card class="content-card">
    <template #header>
      <div class="card-header">
        <span>成绩管理</span>
        <el-button type="primary" @click="openAddScoreDialog">添加成绩</el-button>
      </div>
    </template>
    
    <div class="score-list">
      <el-table :data="scores" style="width: 100%">
        <el-table-column prop="id" label="成绩ID" width="80" />
        <el-table-column prop="studentName" label="学生姓名" />
        <el-table-column prop="studentId" label="学号" width="120" />
        <el-table-column prop="course" label="课程" />
        <el-table-column prop="className" label="班级" />
        <el-table-column prop="score" label="分数" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.score >= 60 ? 'success' : 'danger'">
              {{ scope.row.score }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="examDate" label="考试日期" width="150" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewScore(scope.row)">查看</el-button>
            <el-button size="small" type="success" @click="editScore(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteScore(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>

  <!-- 添加/编辑成绩弹窗 -->
  <el-dialog
    v-model="scoreDialogVisible"
    :title="isEditMode ? '编辑成绩' : '添加成绩'"
    width="500px"
  >
    <el-form :model="scoreForm" label-position="left" label-width="80px">
      <el-form-item label="学生姓名">
        <el-input v-model="scoreForm.studentName" placeholder="请输入学生姓名" />
      </el-form-item>
      <el-form-item label="学号">
        <el-input v-model="scoreForm.studentId" placeholder="请输入学号" />
      </el-form-item>
      <el-form-item label="所属课程">
        <el-input v-model="scoreForm.course" placeholder="请输入课程名称" />
      </el-form-item>
      <el-form-item label="所属班级">
        <el-input v-model="scoreForm.className" placeholder="请输入班级名称" />
      </el-form-item>
      <el-form-item label="分数">
        <el-input-number v-model="scoreForm.score" :min="0" :max="100" :step="1" placeholder="请输入分数" style="width: 100%" />
      </el-form-item>
      <el-form-item label="考试日期">
        <el-date-picker
          v-model="scoreForm.examDate"
          type="date"
          placeholder="选择考试日期"
          style="width: 100%"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="scoreDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveScore">{{ isEditMode ? '保存' : '添加' }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 成绩列表数据
const scores = ref([
  {
    id: 1,
    studentName: '张三',
    studentId: '20250101',
    course: '数学',
    className: '初一2班',
    score: 85,
    examDate: '2025-12-15',
    createTime: '2025-12-16 10:00:00'
  },
  {
    id: 2,
    studentName: '李四',
    studentId: '20250102',
    course: '计算机',
    className: '初二1班',
    score: 92,
    examDate: '2025-12-18',
    createTime: '2025-12-19 09:00:00'
  },
  {
    id: 3,
    studentName: '王五',
    studentId: '20250103',
    course: '英语',
    className: '初三3班',
    score: 78,
    examDate: '2025-12-20',
    createTime: '2025-12-21 14:30:00'
  },
  {
    id: 4,
    studentName: '赵六',
    studentId: '20250104',
    course: '数学',
    className: '初一2班',
    score: 58,
    examDate: '2025-12-15',
    createTime: '2025-12-16 10:00:00'
  }
])

// 弹窗控制
const scoreDialogVisible = ref(false)
const isEditMode = ref(false)

// 成绩表单数据
const scoreForm = ref({
  id: null,
  studentName: '',
  studentId: '',
  course: '',
  className: '',
  score: 0,
  examDate: null
})

// 打开添加成绩弹窗
const openAddScoreDialog = () => {
  isEditMode.value = false
  scoreForm.value = {
    id: null,
    studentName: '',
    studentId: '',
    course: '',
    className: '',
    score: 0,
    examDate: null
  }
  scoreDialogVisible.value = true
}

// 打开编辑成绩弹窗
const editScore = (scoreItem) => {
  isEditMode.value = true
  scoreForm.value = { ...scoreItem }
  scoreDialogVisible.value = true
}

// 查看成绩详情
const viewScore = (scoreItem) => {
  ElMessage.info(`查看${scoreItem.studentName}的${scoreItem.course}成绩：${scoreItem.score}`)
  // 这里可以跳转到成绩详情页面或显示详情弹窗
}

// 保存成绩（添加或编辑）
const saveScore = () => {
  if (!scoreForm.value.studentName || !scoreForm.value.studentId || !scoreForm.value.course || !scoreForm.value.className || !scoreForm.value.examDate || scoreForm.value.score === null) {
    ElMessage.warning('请填写完整的成绩信息')
    return
  }

  if (scoreForm.value.score < 0 || scoreForm.value.score > 100) {
    ElMessage.warning('分数必须在0-100之间')
    return
  }

  if (isEditMode.value) {
    // 编辑模式：更新现有成绩
    const index = scores.value.findIndex(s => s.id === scoreForm.value.id)
    if (index !== -1) {
      scores.value[index] = { ...scoreForm.value }
      ElMessage.success('成绩信息更新成功')
    }
  } else {
    // 添加模式：创建新成绩
    const newScore = {
      ...scoreForm.value,
      id: Math.max(...scores.value.map(s => s.id)) + 1,
      createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
    }
    scores.value.push(newScore)
    ElMessage.success('成绩添加成功')
  }

  scoreDialogVisible.value = false
}

// 删除成绩
const deleteScore = (scoreId) => {
  ElMessageBox.confirm('确定要删除这条成绩记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = scores.value.findIndex(s => s.id === scoreId)
    if (index !== -1) {
      scores.value.splice(index, 1)
      ElMessage.success('成绩记录删除成功')
    }
  }).catch(() => {
    ElMessage.info('取消删除')
  })
}
</script>

<style lang="scss" scoped>
.content-card {
  margin-bottom: 20px;
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
  }
}

.score-list {
  margin-top: 20px;
}
</style>