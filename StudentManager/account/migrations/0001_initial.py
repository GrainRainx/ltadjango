# Generated by Django 3.2.16 on 2023-12-12 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=40, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=512, verbose_name='密码')),
                ('customer_type', models.IntegerField(choices=[(0, 'student'), (1, 'teacher'), (2, 'manager')], default=0, verbose_name='账号类型')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改日期')),
            ],
        ),
    ]
