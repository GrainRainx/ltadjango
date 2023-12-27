from django.db import models
from django.utils import timezone

from account.models import Account


# Create your models here.
class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.BigIntegerField(verbose_name="学号")
    name = models.CharField(max_length=255, verbose_name="学生名字")
    sex = models.CharField(max_length=10, verbose_name="性别")
    birth_day = models.CharField(max_length=255, verbose_name="出生年月")
    native_place = models.CharField(max_length=255, verbose_name="籍贯")
    major = models.CharField(max_length=255, verbose_name="专业")
    clazz = models.CharField(max_length=255, verbose_name='班级')
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="用户ID")
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)