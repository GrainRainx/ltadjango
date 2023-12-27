from django.db import models
from django.utils import timezone


# Create your models here.
class Account(models.Model):
    Area_level = (
        (0, 'student'),
        (1, 'teacher'),
        (2, 'manager'),
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40, null=False, verbose_name="用户名", unique=True)  # 账号
    password = models.CharField(max_length=512, null=False, verbose_name="密码")  # 密码
    customer_type = models.IntegerField(default=0, choices=Area_level, verbose_name="账号类型")  # 类型
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)
