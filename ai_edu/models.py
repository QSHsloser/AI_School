from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class Book(models.Model):
    name = models.CharField('书名', max_length=64, primary_key=True)
    time = models.DateTimeField('编号', auto_now_add=True)


class Student(models.Model):
    id = models.IntegerField('ID', primary_key=True, auto_created=True)
    username = models.CharField('用户名', max_length=255, blank=False)
    password = models.CharField('密码', max_length=255, blank=False)
    teacher_id = models.IntegerField('教师ID', blank=False, default=0)
    
    class Meta:
        db_table = 'ai_edu_students'
        verbose_name = '学生'
        verbose_name_plural = '学生'

class Classroom(models.Model):
    class_id = models.IntegerField('ID', primary_key=True, auto_created=True)
    class_name = models.CharField('班级名称', max_length=255, blank=False)
    course = models.CharField('课程', max_length=255, blank=False)
    member = models.IntegerField('ID', max_length=4, blank=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=False)
    class Meta:
        db_table = 'ai_edu_class'
        verbose_name = '班级课程'
        verbose_name_plural = '班级课程'


class Teacher(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    teacherNum = models.CharField('教师编号', max_length=255, blank=True, null=True)
    username = models.CharField('用户名', max_length=255, blank=False)
    password = models.CharField('密码', max_length=255, blank=False)
    phone = models.IntegerField('电话', blank=True, null=True)
    hostname = models.CharField('主机名', max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'ai_edu_teachers'
        verbose_name = '教师'
        verbose_name_plural = '教师'

