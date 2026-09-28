from . import views
from django.urls import path
from ai_edu import views as BookView
urlpatterns = [
    path('add_book/', BookView.add_book),
    path('show_books/', BookView.show_books),
    path('get_current_user/', views.get_current_user),
    path('login/', views.login_user),
    path('register/', views.register),
    path('v1/', views.dify_chat),
    path('v1/stop/', views.dify_stop_response),
    path('v1/preview/', views.dify_file_preview),
    path('classrooms/', views.classrooms),
]