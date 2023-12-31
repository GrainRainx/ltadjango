# Generated by Django 3.2.16 on 2023-12-13 06:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_alter_account_customer_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.BigIntegerField(verbose_name='学号')),
                ('name', models.CharField(max_length=255, verbose_name='学生名字')),
                ('sex', models.CharField(max_length=10, verbose_name='性别')),
                ('birth_day', models.CharField(max_length=255, verbose_name='出生年月')),
                ('native_place', models.CharField(max_length=255, verbose_name='籍贯')),
                ('major', models.CharField(max_length=255, verbose_name='专业')),
                ('clazz', models.CharField(max_length=255, verbose_name='班级')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改日期')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account', verbose_name='用户ID')),
            ],
        ),
    ]
