"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from ai_edu import views as BookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_book/', BookView.add_book),
    path('show_books/', BookView.show_books),
    path('register/', BookView.register),
    path('login/', BookView.login_user),
    path('get_current_user/', BookView.get_current_user),
    path('v1/', BookView.dify_chat),
    # 捕获所有路由，用于前端路由
    path('classrooms/', BookView.classrooms),
    # 教师端班级管理数据
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
