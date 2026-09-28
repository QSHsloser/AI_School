<template>
  <el-card class="content-card">
    <template #header>
      <div class="card-header">
        <span>班级管理</span>
        <el-button type="primary" @click="openAddClassDialog">添加班级</el-button>
      </div>
    </template>
    
    <div class="class-list">
      <el-table :data="classes" style="width: 100%">
        <el-table-column prop="id" label="班级ID" width="80" />
        <el-table-column prop="name" label="班级名称" />
        <el-table-column prop="course" label="课程" />
        <el-table-column prop="studentCount" label="学生人数" width="100" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewClass(scope.row)">查看</el-button>
            <el-button size="small" type="success" @click="editClass(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteClass(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>

  <!-- 添加/编辑班级弹窗 -->
  <el-dialog
    v-model="classDialogVisible"
    :title="isEditMode ? '编辑班级' : '添加班级'"
    width="500px"
  >
    <el-form :model="classForm" label-position="left" label-width="80px">
      <el-form-item label="班级名称">
        <el-input v-model="classForm.name" placeholder="请输入班级名称" />
      </el-form-item>
      <el-form-item label="课程">
        <el-input v-model="classForm.course" placeholder="请输入课程名称" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="classDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveClass">{{ isEditMode ? '保存' : '添加' }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 班级列表数据
const classes = ref([
  {
    id: 1,
    name: '初一1班',
    course: '计算机',
    studentCount: 35,
    createTime: '2025-09-01 08:00:00'
  },
  {
    id: 2,
    name: '初二2班',
    course: '数学',
    studentCount: 42,
    createTime: '2025-09-01 08:00:00'
  },
  {
    id: 3,
    name: '初三3班',
    course: '英语',
    studentCount: 28,
    createTime: '2025-09-01 08:00:00'
  }
])

// 弹窗控制
const classDialogVisible = ref(false)
const isEditMode = ref(false)

// 班级表单数据
const classForm = ref({
  id: null,
  name: '',
  course: ''
})

// 打开添加班级弹窗
const openAddClassDialog = () => {
  isEditMode.value = false
  classForm.value = {
    id: null,
    name: '',
    course: ''
  }
  classDialogVisible.value = true
}

// 打开编辑班级弹窗
const editClass = (classItem) => {
  isEditMode.value = true
  classForm.value = { ...classItem }
  classDialogVisible.value = true
}

// 查看班级详情
const viewClass = (classItem) => {
  ElMessage.info(`查看班级：${classItem.name}`)
  // 这里可以跳转到班级详情页面或显示详情弹窗
}

// 保存班级（添加或编辑）
const saveClass = () => {
  if (!classForm.value.name || !classForm.value.course) {
    ElMessage.warning('请填写完整的班级信息')
    return
  }

  if (isEditMode.value) {
    // 编辑模式：更新现有班级
    const index = classes.value.findIndex(c => c.id === classForm.value.id)
    if (index !== -1) {
      classes.value[index] = { ...classForm.value }
      ElMessage.success('班级信息更新成功')
    }
  } else {
    // 添加模式：创建新班级
    const newClass = {
      ...classForm.value,
      id: Math.max(...classes.value.map(c => c.id)) + 1,
      studentCount: 0,
      createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
    }
    classes.value.push(newClass)
    ElMessage.success('班级添加成功')
  }

  classDialogVisible.value = false
}

// 删除班级
const deleteClass = (classId) => {
  ElMessageBox.confirm('确定要删除这个班级吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = classes.value.findIndex(c => c.id === classId)
    if (index !== -1) {
      classes.value.splice(index, 1)
      ElMessage.success('班级删除成功')
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

.class-list {
  margin-top: 20px;
}
</style>