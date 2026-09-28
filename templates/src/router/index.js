import { createRouter, createWebHistory } from 'vue-router'
import NotFound from '../page/404.vue'
import { ElMessage } from 'element-plus'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../page/Home.vue'),
      meta : {
        title : '首页'
      }
    },
    {
      path: '/bv',
      name: 'BookTest',
      component: () => import('../page/BookView.vue'),
      meta : {
        title : '图书查阅'
      }
    },
    {
      path: '/t',
      name: 'T',
      component: () => import('../page/Main.vue'),
      meta : {
        title : '测试'
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../page/login.vue'),
      meta : {
        title : '登录页面'
      }
    },
    // 学生端多级路由
    {
      path: '/student',
      name: 'Student',
      component: () => import('../page/student_main.vue'),
      meta: { requiresAuth: true, allowedUserType: 'student' },
      children: [
        {
          path: 'courses',
          name: 'StudentCourses',
          component: () => import('../page/student_courses.vue'),
          meta: { requiresAuth: true, allowedUserType: 'student' },
        },
        {
          path: 'homework',
          name: 'StudentHomework',
          component: () => import('../page/student_homework.vue'),
          meta: { requiresAuth: true, allowedUserType: 'student' },
        },
        {
          path: 'scores',
          name: 'StudentScores',
          component: () => import('../page/student_scores.vue'),
          meta: { requiresAuth: true, allowedUserType: 'student' },
        },
        {
          path: 'book',
          name: 'StudentBook',
          component: () => import('../page/BookView.vue'),
          meta: { requiresAuth: true, allowedUserType: 'student' },
        },
        // 可以添加更多学生子路由
      ]
    },
    // 教师端多级路由
    {
      path: '/teacher',
      name: 'Teacher',
      component: () => import('../page/teacher_main.vue'),
      meta: { requiresAuth: true, allowedUserType: 'teacher' },
      children: [

        // 可以添加更多教师子路由
        {
          path: 'class-management',
          name: 'ClassManagement',
          component: () => import('../page/class_management.vue'),
          meta: { requiresAuth: true, allowedUserType: 'teacher' },
        },
        {
          path: 'homework-management',
          name: 'HomeworkManagement',
          component: () => import('../page/homework_management.vue'),
          meta: { requiresAuth: true, allowedUserType: 'teacher' },
        },
        {
          path: 'score-management',
          name: 'ScoreManagement',
          component: () => import('../page/score_management.vue'),
          meta: { requiresAuth: true, allowedUserType: 'teacher' },
        },
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound,
    },
  ],
})

// 路由守卫，实现登录验证和用户类型隔离
router.beforeEach((to, from, next) => {
  // 检查路由是否需要登录
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查本地存储中是否有用户信息
    const userInfoStr = localStorage.getItem('userInfo');
    if (userInfoStr) {
      const userInfo = JSON.parse(userInfoStr);
      
      // 检查路由是否有特定的用户类型要求
      const allowedUserType = to.matched.some(record => record.meta.allowedUserType);
      if (allowedUserType) {
        // 检查用户类型是否匹配
        const routeUserType = to.matched.find(record => record.meta.allowedUserType)?.meta.allowedUserType;
        if (userInfo.user_type === routeUserType) {
          // 用户类型匹配，继续导航
          next();
        } else {
          // 用户类型不匹配，重定向到首页并显示提示
          if (userInfo.user_type === 'student') {
            ElMessage.warning('当前登录为学生，不能进入教师页面');
          } else if (userInfo.user_type === 'teacher') {
            ElMessage.warning('当前登录为教师，不能进入学生页面');
          }
          next({ path: '/' }); // 重定向到首页
        }
      } else {
        // 没有特定用户类型要求，继续导航
        next();
      }
    } else {
      // 未登录，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 保存当前路由，以便登录后返回
      });
    }
  } else {
    // 不需要登录的路由，直接导航
    next();
  }
});

export default router
