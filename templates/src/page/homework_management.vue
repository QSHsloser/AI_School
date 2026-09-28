<template>
  <el-card class="content-card">
    <template #header>
      <div class="card-header">
        <span>作业管理</span>
        <el-button type="primary" @click="openAddHomeworkDialog">添加作业</el-button>
      </div>
    </template>
    
    <div class="homework-list">
      <el-table :data="homeworks" style="width: 100%">
        <el-table-column prop="id" label="作业ID" width="80" />
        <el-table-column prop="title" label="作业标题" />
        <el-table-column prop="course" label="课程" />
        <el-table-column prop="className" label="班级" />
        <el-table-column prop="deadline" label="截止时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已发布' ? 'success' : scope.row.status === '已截止' ? 'danger' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewHomework(scope.row)">查看</el-button>
            <el-button size="small" type="success" @click="editHomework(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteHomework(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>

  <!-- 添加/编辑作业弹窗 -->
  <el-dialog
    v-model="homeworkDialogVisible"
    :title="isEditMode ? '编辑作业' : '添加作业'"
    width="500px"
  >
    <el-form :model="homeworkForm" label-position="left" label-width="80px">
      <el-form-item label="作业标题">
        <el-input v-model="homeworkForm.title" placeholder="请输入作业标题" />
      </el-form-item>
      <el-form-item label="所属课程">
        <el-input v-model="homeworkForm.course" placeholder="请输入课程名称" />
      </el-form-item>
      <el-form-item label="所属班级">
        <el-input v-model="homeworkForm.className" placeholder="请输入班级名称" />
      </el-form-item>
      <el-form-item label="截止时间">
        <el-date-picker
          v-model="homeworkForm.deadline"
          type="datetime"
          placeholder="选择截止时间"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="作业状态">
        <el-select v-model="homeworkForm.status" placeholder="选择状态">
          <el-option label="未发布" value="未发布" />
          <el-option label="已发布" value="已发布" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="homeworkDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveHomework">{{ isEditMode ? '保存' : '添加' }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 作业列表数据
const homeworks = ref([
  {
    id: 1,
    title: '初中数学第一章习题',
    course: '数学',
    className: '初二2班',
    deadline: '2025-12-25 23:59:59',
    createTime: '2025-12-18 14:30:00',
    status: '已发布'
  },
  {
    id: 2,
    title: 'Python编程作业',
    course: '计算机',
    className: '初一1班',
    deadline: '2025-12-20 23:59:59',
    createTime: '2025-12-15 10:00:00',
    status: '已截止'
  },
  {
    id: 3,
    title: '英语作文练习',
    course: '英语',
    className: '初三3班',
    deadline: '2025-12-28 23:59:59',
    createTime: '2025-12-19 09:00:00',
    status: '未发布'
  }
])

// 弹窗控制
const homeworkDialogVisible = ref(false)
const isEditMode = ref(false)

// 作业表单数据
const homeworkForm = ref({
  id: null,
  title: '',
  course: '',
  className: '',
  deadline: null,
  status: '未发布'
})

// 打开添加作业弹窗
const openAddHomeworkDialog = () => {
  isEditMode.value = false
  homeworkForm.value = {
    id: null,
    title: '',
    course: '',
    className: '',
    deadline: null,
    status: '未发布'
  }
  homeworkDialogVisible.value = true
}

// 打开编辑作业弹窗
const editHomework = (homeworkItem) => {
  isEditMode.value = true
  homeworkForm.value = { ...homeworkItem }
  homeworkDialogVisible.value = true
}

// 查看作业详情
const viewHomework = (homeworkItem) => {
  ElMessage.info(`查看作业：${homeworkItem.title}`)
  // 这里可以跳转到作业详情页面或显示详情弹窗
}

// 保存作业（添加或编辑）
const saveHomework = () => {
  if (!homeworkForm.value.title || !homeworkForm.value.course || !homeworkForm.value.className || !homeworkForm.value.deadline) {
    ElMessage.warning('请填写完整的作业信息')
    return
  }

  if (isEditMode.value) {
    // 编辑模式：更新现有作业
    const index = homeworks.value.findIndex(h => h.id === homeworkForm.value.id)
    if (index !== -1) {
      homeworks.value[index] = { ...homeworkForm.value }
      ElMessage.success('作业信息更新成功')
    }
  } else {
    // 添加模式：创建新作业
    const newHomework = {
      ...homeworkForm.value,
      id: Math.max(...homeworks.value.map(h => h.id)) + 1,
      createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
    }
    homeworks.value.push(newHomework)
    ElMessage.success('作业添加成功')
  }

  homeworkDialogVisible.value = false
}

// 删除作业
const deleteHomework = (homeworkId) => {
  ElMessageBox.confirm('确定要删除这个作业吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = homeworks.value.findIndex(h => h.id === homeworkId)
    if (index !== -1) {
      homeworks.value.splice(index, 1)
      ElMessage.success('作业删除成功')
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

.homework-list {
  margin-top: 20px;
}
</style>