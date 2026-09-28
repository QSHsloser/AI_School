<script setup>
import { User, Lock } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 获取路由实例
const router = useRouter()

// 表单模型
const formModel = ref({
  username: '',
  password: '',
  repassword: '',
  user_type: 'student' // 默认学生类型
})

// 表单规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 10, message: '用户名必须是 2-10位 的字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码必须 是6-15位 的非空字符',
      trigger: 'blur'
    }
  ],
  repassword: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码必须 是6-15位 的非空字符',
      trigger: 'blur'
    },
    {
      // 自定义校验
      validator: (rule, value, callback) => {
        // 判断 value 和 当前 form 中收集的 password 是否一致
        if (value !== formModel.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback() // 就算校验成功,也需要callback
        }
      },
      trigger: 'blur'
    }
  ]
}

// 表单引用
const formRef = ref(null)

// 切换登录/注册
const isRegister = ref(false)

// 注册方法
const handleRegister = async () => {
  if (!formRef.value) return
  
  // 表单验证
  try {
    await formRef.value.validate()
  } catch (error) {
    ElMessage.error('验证失败，请检查输入')
    return
  }
  
  try {
    // 发送注册请求
    const response = await axios.post('http://localhost:8000/register/', {
      username: formModel.value.username,
      password: formModel.value.password,
      user_type: formModel.value.user_type
    })
    
    if (response.data.error_num === 0) {
      ElMessage.success(response.data.msg)
      isRegister.value = false // 注册成功后切换到登录页面
      // 清空表单
      formModel.value = {
        username: '',
        password: '',
        repassword: '',
        user_type: 'student'
      }
    } else {
      ElMessage.error(response.data.msg)
    }
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error('注册失败，请稍后重试')
  }
}

// 登录方法
const handleLogin = async () => {
  if (!formRef.value) return
  
  // 表单验证
  try {
    await formRef.value.validate()
  } catch (error) {
    ElMessage.error('验证失败，请检查输入')
    return
  }
  
  try {
    // 发送登录请求
    const response = await axios.post('http://localhost:8000/login/', {
      username: formModel.value.username,
      password: formModel.value.password,
      user_type: formModel.value.user_type
    })
    
    if (response.data.error_num === 0) {
      ElMessage.success(response.data.msg)
      // 登录成功后的处理
      console.log('登录成功，用户信息:', response.data)
      
      // 存储用户信息到本地存储
      const userInfo = {
        username: response.data.username,
        user_type: formModel.value.user_type
      }
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
      
      // 根据用户类型跳转到相应页面
      if (formModel.value.user_type === 'student') {
        router.push('/student')
      } else if (formModel.value.user_type === 'teacher') {
        router.push('/teacher')
      }
    } else {
      ElMessage.error(response.data.msg)
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('登录失败，请稍后重试')
  }
}
</script>
 
<template>
  <div class="login-page">
    <div class="form">
      <!-- 注册相关表单 -->
      <el-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        size="large"
        autocomplete="off"
        v-if="isRegister"
      >
        <el-form-item>
          <h1>注册</h1>
        </el-form-item>
        
        <!-- 用户类型选择 -->
        <el-form-item label="用户类型">
          <el-radio-group v-model="formModel.user_type">
            <el-radio label="student">学生</el-radio>
            <el-radio label="teacher">教师</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item prop="username">
          <el-input
            v-model="formModel.username"
            :prefix-icon="User"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="formModel.password"
            :prefix-icon="Lock"
            type="password"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item prop="repassword">
          <el-input
            v-model="formModel.repassword"
            :prefix-icon="Lock"
            type="password"
            placeholder="请再次输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            class="button"
            type="primary"
            auto-insert-space
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = false">
            ← 返回登录
          </el-link>
        </el-form-item>
      </el-form>
      <!-- 登陆相关表单 -->
      <el-form
        ref="formRef"
        :model="formModel"
        :rules="{
          username: rules.username,
          password: rules.password
        }"
        size="large"
        autocomplete="off"
        v-else
      >
        <el-form-item>
          <h1>登录</h1>
        </el-form-item>
        
        <!-- 用户类型选择 -->
        <el-form-item label="用户类型">
          <el-radio-group v-model="formModel.user_type">
            <el-radio label="student">学生</el-radio>
            <el-radio label="teacher">教师</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item prop="username">
          <el-input
            v-model="formModel.username"
            :prefix-icon="User"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="formModel.password"
            name="password"
            :prefix-icon="Lock"
            type="password"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item class="flex">
          <div class="flex">
            <el-checkbox>记住我</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码？</el-link>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button
            class="button"
            type="primary"
            auto-insert-space
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = true">
            注册账号 →
          </el-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
 
<style lang="scss" scoped>
.login-page {
  height: 100vh;
  background-image: url('../../assets/login_bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 0;
  }
  
  .bg {
    display: none;
  }
  
  .form {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 450px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    
    h1 {
      color: #3eaf7c;
      font-size: 32px;
      font-weight: 700;
      margin-bottom: 30px;
      text-align: center;
    }
    
    .el-form-item {
      margin-bottom: 25px;
      
      &:last-of-type {
        margin-bottom: 0;
      }
      
      .el-form-item__label {
        color: #303133;
        font-weight: 500;
        font-size: 15px;
      }
    }
    
    .el-input {
      .el-input__wrapper {
        border-radius: 8px;
        
        &:hover {
          box-shadow: 0 2px 8px rgba(62, 175, 124, 0.2);
        }
        
        &.is-focus {
          box-shadow: 0 0 0 2px rgba(62, 175, 124, 0.2);
          border-color: #3eaf7c;
        }
      }
      
      .el-input__inner {
        font-size: 16px;
        padding: 12px 16px;
      }
    }
    
    .button {
      width: 100%;
      background-color: #3eaf7c;
      border: none;
      border-radius: 8px;
      padding: 14px;
      font-size: 18px;
      font-weight: 600;
      transition: all 0.3s ease;
      
      &:hover {
        background-color: #369e6d;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(62, 175, 124, 0.3);
      }
      
      &:active {
        transform: translateY(0);
      }
    }
    
    .flex {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 25px;
      
      .el-checkbox {
        color: #606266;
        
        .el-checkbox__input.is-checked .el-checkbox__inner {
          background-color: #3eaf7c;
          border-color: #3eaf7c;
        }
        
        .el-checkbox__input.is-checked+.el-checkbox__label {
          color: #3eaf7c;
        }
      }
      
      .el-link {
        color: #3eaf7c;
        
        &:hover {
          color: #369e6d;
        }
      }
    }
    
    .el-radio-group {
      display: flex;
      gap: 20px;
      
      .el-radio {
        color: #606266;
        
        .el-radio__input.is-checked .el-radio__inner {
          background-color: #3eaf7c;
          border-color: #3eaf7c;
        }
        
        .el-radio__input.is-checked+.el-radio__label {
          color: #3eaf7c;
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .login-page {
    padding: 20px;
    
    .form {
      padding: 30px 20px;
      
      h1 {
        font-size: 28px;
      }
    }
  }
}
</style>

