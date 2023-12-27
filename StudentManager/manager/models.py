from django.db import models
from django.utils import timezone
from student.models import StudentInfo
from teacher.models import TeacherInfo


# Create your models here.
class Major(models.Model):
    # 专业
    id = models.BigAutoField(primary_key=True)
    major_code = models.CharField(max_length=32, verbose_name='专业代码', unique=True)
    name = models.CharField(max_length=32, verbose_name='专业名', unique=True)
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)


class Clazz(models.Model):
    # 班级
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='班级名')
    major_id = models.ForeignKey(Major, on_delete=models.CASCADE)
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)

class Meta:
    unique_together = ('name', 'major_id',)


class ClazzStudents(models.Model):
    # 班级学生表
    id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    clazz_id = models.ForeignKey(Clazz, on_delete=models.CASCADE)
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)

    class Meta:
        unique_together = ('student_id', 'clazz_id',)


class Curriculum(models.Model):
    # 课程信息
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='课程名')
    teacher_id = models.ForeignKey(TeacherInfo, on_delete=models.CASCADE)  # 老师信息
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)

    class Meta:
        unique_together = ('name', 'teacher_id',)


class SchoolTimeTable(models.Model):
    # 课表
    time = (  # 一共4节课，上午2节，下午2节(大课)
        (1, '8:00~9:40'),
        (2, '10:00~11:40'),
        (3, '14:00~15:40'),
        (4, '15:50~17:50'),
    )

    daytime = (
        (1, '周一'),
        (2, '周二'),
        (3, '周三'),
        (4, '周四'),
        (5, '周五'),
    )

    id = models.BigAutoField(primary_key=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)  # 课程信息
    clazz_week = models.CharField(max_length=32, verbose_name='周几的课', choices=time)  # 上课时间，周几
    clazz_time = models.CharField(max_length=32, verbose_name='上课时间', choices=daytime)  # 上课时间，时间
    clazz_id = models.ForeignKey(Clazz, on_delete=models.CASCADE)  # 班级信息
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)

    class Meta:
        unique_together = ('clazz_week', 'clazz_time', 'clazz_id')


class StudentCurriculumScore(models.Model):
    """
    学生成绩表
    """
    id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=1, max_digits=10)
    create_time = models.DateTimeField('保存日期', default=timezone.now)
    update_time = models.DateTimeField('修改日期', default=timezone.now)

    class Meta:
        unique_together = ('student_id', 'curriculum_id')