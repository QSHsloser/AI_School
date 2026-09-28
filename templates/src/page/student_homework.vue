<template>
  <div class="homework-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的作业</span>
          <div class="filter-controls">
            <el-select v-model="statusFilter" placeholder="筛选状态" clearable style="width: 150px; margin-right: 10px;">
              <el-option label="全部" value="" />
              <el-option label="待完成" value="pending" />
              <el-option label="已提交" value="submitted" />
              <el-option label="已批改" value="graded" />
              <el-option label="已过期" value="expired" />
            </el-select>
            <el-input
              v-model="searchQuery"
              placeholder="搜索作业"
              clearable
              class="search-input"
            >
              <template #prepend>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </template>
      
      <!-- 作业列表 -->
      <el-table :data="filteredHomework" stripe style="width: 100%">
        <el-table-column prop="homeworkName" label="作业名称" width="200" />
        <el-table-column prop="courseName" label="所属课程" width="150" />
        <el-table-column prop="teacher" label="布置教师" width="120" />
        <el-table-column prop="publishDate" label="发布日期" width="150" />
        <el-table-column prop="deadline" label="截止日期" width="150" />
        <el-table-column prop="status" label="作业状态" width="120">
          <template #default="scope">
            <el-tag
              :type="getStatusType(scope.row.status)"
            >
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="score" label="分数" width="100">
          <template #default="scope">
            {{ scope.row.status === 'graded' ? scope.row.score : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewHomework(scope.row)">
              查看详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="success" 
              size="small" 
              @click="submitHomework(scope.row)"
            >
              提交作业
            </el-button>
            <el-button
              v-if="scope.row.status === 'submitted' || scope.row.status === 'graded'"
              type="info" 
              size="small" 
              @click="viewSubmission(scope.row)"
            >
              查看提交
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="filteredHomework.length"
          :page-size="10"
        />
      </div>
    </el-card>

    <!-- 作业详情弹窗 -->
    <el-dialog
      v-model="homeworkDetailVisible"
      :title="selectedHomework.homeworkName || '作业详情'"
      width="700px"
    >
      <div v-if="selectedHomework" class="homework-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="作业名称">{{ selectedHomework.homeworkName }}</el-descriptions-item>
          <el-descriptions-item label="所属课程">{{ selectedHomework.courseName }}</el-descriptions-item>
          <el-descriptions-item label="布置教师">{{ selectedHomework.teacher }}</el-descriptions-item>
          <el-descriptions-item label="发布日期">{{ selectedHomework.publishDate }}</el-descriptions-item>
          <el-descriptions-item label="截止日期">{{ selectedHomework.deadline }}</el-descriptions-item>
          <el-descriptions-item label="作业状态">
            <el-tag :type="getStatusType(selectedHomework.status)">
              {{ getStatusText(selectedHomework.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="作业要求" :span="3">{{ selectedHomework.requirements }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedHomework.status === 'graded'" label="分数">{{ selectedHomework.score }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedHomework.status === 'graded'" label="教师评语" :span="3">
            {{ selectedHomework.feedback || '暂无评语' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="homeworkDetailVisible = false">关闭</el-button>
          <el-button
            v-if="selectedHomework.status === 'pending'"
            type="success"
            @click="submitHomework(selectedHomework)"
          >
            提交作业
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 提交作业弹窗 -->
    <el-dialog
      v-model="submitDialogVisible"
      :title="`提交作业：${submittingHomework.homeworkName || ''}`"
      width="600px"
    >
      <div class="submit-form">
        <el-form label-position="top" label-width="80px">
          <el-form-item label="作业要求">
            <el-input
              v-model="submittingHomework.requirements"
              type="textarea"
              :rows="4"
              readonly
              placeholder="作业要求"
            />
          </el-form-item>
          <el-form-item label="作业文件">
            <el-upload
              ref="uploadRef"
              :action="'#'"
              :on-change="handleFileChange"
              :auto-upload="false"
              :file-list="uploadFiles"
              accept=".pdf,.doc,.docx,.txt,.zip"
              multiple
            >
              <el-button type="primary">
                <el-icon><Upload /></el-icon>
                选择文件
              </el-button>
              <template #tip>
                <div class="el-upload__tip">
                  支持上传 PDF、Word、TXT、ZIP 文件，单个文件不超过 10MB
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item label="作业说明">
            <el-input
              v-model="submissionNote"
              type="textarea"
              :rows="3"
              placeholder="请输入作业说明（可选）"
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="submitDialogVisible = false; resetUpload()">取消</el-button>
          <el-button type="primary" @click="confirmSubmission" :disabled="!uploadFiles.length">
            确认提交
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看提交弹窗 -->
    <el-dialog
      v-model="submissionDetailVisible"
      :title="`已提交作业：${viewingSubmission.homeworkName || ''}`"
      width="600px"
    >
      <div v-if="viewingSubmission" class="submission-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="提交日期">{{ viewingSubmission.submissionDate }}</el-descriptions-item>
          <el-descriptions-item label="提交文件">
            <div v-if="viewingSubmission.submittedFiles && viewingSubmission.submittedFiles.length">
              <el-link
                v-for="(file, index) in viewingSubmission.submittedFiles"
                :key="index"
                type="primary"
                :underline="false"
              >
                <el-icon><Document /></el-icon>
                {{ file.name }}
              </el-link>
            </div>
            <span v-else>无提交文件</span>
          </el-descriptions-item>
          <el-descriptions-item label="作业说明">{{ viewingSubmission.submissionNote || '无说明' }}</el-descriptions-item>
          <el-descriptions-item v-if="viewingSubmission.status === 'graded'" label="分数">{{ viewingSubmission.score }}</el-descriptions-item>
          <el-descriptions-item v-if="viewingSubmission.status === 'graded'" label="教师评语">{{ viewingSubmission.feedback || '暂无评语' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="submissionDetailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search, Upload, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

// 搜索和过滤
const searchQuery = ref('')
const statusFilter = ref('')

// 弹窗控制
const homeworkDetailVisible = ref(false)
const submitDialogVisible = ref(false)
const submissionDetailVisible = ref(false)

// 选中的作业
const selectedHomework = ref({})
const submittingHomework = ref({})
const viewingSubmission = ref({})

// 上传相关
const uploadRef = ref(null)
const uploadFiles = ref([])
const submissionNote = ref('')

// 模拟作业数据
const homeworkData = ref([
  {
    homeworkId: 1,
    homeworkName: '初中数学作业',
    courseName: '初中数学',
    teacher: '张老师',
    publishDate: '2025-12-10',
    deadline: '2025-12-20',
    status: 'pending',
    requirements: '完成教材第5章的习题1-10题，要求写出详细的解题步骤。',
    score: null,
    feedback: null,
    submissionDate: null,
    submittedFiles: [],
    submissionNote: null
  },
  {
    homeworkId: 2,
    homeworkName: '初中英语作文',
    courseName: '初中英语',
    teacher: '李老师',
    publishDate: '2025-12-08',
    deadline: '2025-12-18',
    status: 'submitted',
    requirements: '写一篇关于"My Dream"的英语作文，字数不少于100字。',
    score: null,
    feedback: null,
    submissionDate: '2025-12-15',
    submittedFiles: [{ name: 'My Dream.docx' }],
    submissionNote: '这是我的英语作文，请老师批改。'
  },
  {
    homeworkId: 3,
    homeworkName: '计算机基础实验报告',
    courseName: '计算机',
    teacher: '王老师',
    publishDate: '2025-12-05',
    deadline: '2025-12-15',
    status: 'graded',
    requirements: '完成Excel数据处理实验，提交实验报告。',
    score: 95,
    feedback: '实验报告撰写规范，数据处理正确，优秀！',
    submissionDate: '2025-12-14',
    submittedFiles: [{ name: 'Excel实验报告.pdf' }],
    submissionNote: '实验报告已完成，请老师查看。'
  },
  {
    homeworkId: 4,
    homeworkName: '初中物理实验报告',
    courseName: '初中物理',
    teacher: '赵教授',
    publishDate: '2025-11-30',
    deadline: '2025-12-10',
    status: 'graded',
    requirements: '完成力学实验，提交实验数据和分析报告。',
    score: 88,
    feedback: '实验数据准确，分析合理，但结论部分可以更深入。',
    submissionDate: '2025-12-08',
    submittedFiles: [{ name: '力学实验报告.pdf' }],
    submissionNote: '实验报告已完成，请老师批改。'
  },
  {
    homeworkId: 5,
    homeworkName: '思想与品德课后作业',
    courseName: '思想与品德',
    teacher: '刘老师',
    publishDate: '2025-11-25',
    deadline: '2025-12-05',
    status: 'expired',
    requirements: '完成教材第2章的习题5-15题，要求写出详细的解题步骤。',
    score: null,
    feedback: null,
    submissionDate: null,
    submittedFiles: [],
    submissionNote: null
  }
])

// 过滤后的作业列表
const filteredHomework = computed(() => {
  return homeworkData.value.filter(homework => {
    const matchesSearch = !searchQuery.value || 
      homework.homeworkName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      homework.courseName.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesStatus = !statusFilter.value || homework.status === statusFilter.value;
    return matchesSearch && matchesStatus;
  });
});

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    pending: 'warning',
    submitted: 'primary',
    graded: 'success',
    expired: 'danger'
  };
  return statusMap[status] || 'info';
};

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待完成',
    submitted: '已提交',
    graded: '已批改',
    expired: '已过期'
  };
  return statusMap[status] || '未知状态';
};

// 查看作业详情
const viewHomework = (homework) => {
  selectedHomework.value = homework;
  homeworkDetailVisible.value = true;
};

// 提交作业
const submitHomework = (homework) => {
  submittingHomework.value = homework;
  uploadFiles.value = [];
  submissionNote.value = '';
  submitDialogVisible.value = true;
};

// 查看提交详情
const viewSubmission = (homework) => {
  viewingSubmission.value = homework;
  submissionDetailVisible.value = true;
};

// 文件变化处理
const handleFileChange = (file, files) => {
  uploadFiles.value = files;
};

// 重置上传
const resetUpload = () => {
  uploadFiles.value = [];
  submissionNote.value = '';
  if (uploadRef.value) {
    uploadRef.value.clearFiles();
  }
};

// 确认提交
const confirmSubmission = () => {
  // 这里可以添加提交作业的API调用
  ElMessage.success('作业提交成功！');
  
  // 更新本地数据
  const index = homeworkData.value.findIndex(hw => hw.homeworkId === submittingHomework.value.homeworkId);
  if (index !== -1) {
    homeworkData.value[index].status = 'submitted';
    homeworkData.value[index].submissionDate = new Date().toISOString().split('T')[0];
    homeworkData.value[index].submittedFiles = uploadFiles.value.map(file => ({ name: file.name }));
    homeworkData.value[index].submissionNote = submissionNote.value;
  }
  
  // 关闭弹窗并重置
  submitDialogVisible.value = false;
  resetUpload();
  homeworkDetailVisible.value = false;
};
</script>

<style lang="scss" scoped>
.homework-container {
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

.filter-controls {
  display: flex;
  align-items: center;
}

.search-input {
  width: 250px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.homework-detail,
.submission-detail {
  margin-top: 20px;
}

.submit-form {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>