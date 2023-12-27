from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from utils.check_login import check_login
from account.models import Account
from .models import TeacherInfo
from student.models import StudentInfo
from manager.models import Curriculum, SchoolTimeTable, ClazzStudents, StudentCurriculumScore
from utils.rendom_char import get_random_str


@check_login
def teacher_info(request):
    user_id = request.session.get('user_id')
    req_typ = request.GET.get('typ')

    if request.method == 'GET':
        if not req_typ:  # 请求方法是GET且没有指定req_typ 返回个人信息
            if not TeacherInfo.objects.filter(user_id=user_id).exists():
                # 信息不存在
                return render(request, 'teacher_info.html',
                              context={'teacher_id': '未设置', 'name': '未设置', 'sex': '未设置',
                                       'birth_day': '未设置'})
            info = TeacherInfo.objects.get(user_id=user_id)  # 信息存在 获取并返回
            return render(request, 'teacher_info.html', context=info.__dict__)
        elif req_typ.upper() == 'update'.upper():
            context = {'typ': 'update', }
            if TeacherInfo.objects.filter(user_id=user_id).exists():
                context['tid'] = TeacherInfo.objects.get(user_id=user_id).id  # 添加教师ID到上下文
            return render(request, 'teacher_info.html', context=context)
        elif req_typ.upper() == 'change_password'.upper():  # 显示修改密码
            return render(request, 'teacher_info.html', context={'typ': 'change_password'})
    elif request.method == 'POST':
        params = request.POST.dict()
        if params.get('req_typ') == 'info':
            if not params.get('name') or not params.get('sex') or not params.get('birth_day'):
                return render(request, 'teacher_info.html', context={'typ': 'update', 'message': '提交的数据不完整'})
            # 保存并更新教师信息
            TeacherInfo(name=params['name'], sex=params['sex'], birth_day=params['birth_day'],
                        teacher_id=params.get('teacher_id', get_random_str(14, True)),  # 若未提供teacher_id 生成一个随机字符串
                        user_id=Account.objects.get(id=user_id)).save()

            return redirect('/teacher_info/')
        elif params.get('req_typ') == 'password':  # 修改密码
            password = params.get('password')
            password_again = params.get('password-again')
            if password_again != password:
                return render(request, 'teacher_info.html',
                              context={'typ': 'change_password', 'message': '两次输入的密码不一致'})
            account = Account.objects.get(id=user_id)
            account.password = make_password(password)
            account.save()
            return render(request, 'teacher_info.html', context={'typ': 'change_password', 'message': '修改密码完成'})


@check_login
def teacher_time_table(request):
    user_id = request.session.get('user_id')

    if not TeacherInfo.objects.filter(user_id=user_id).exists():
        return redirect('teacher_info')

    teacher = TeacherInfo.objects.get(user_id=user_id)

    def get_stt():
        tmp = {
            '1': {'1': [], '2': [], '3': [], '4': [], '5': []},  # key是第几节课，后面的字典是周几
            '2': {'1': [], '2': [], '3': [], '4': [], '5': []},
            '3': {'1': [], '2': [], '3': [], '4': [], '5': []},
            '4': {'1': [], '2': [], '3': [], '4': [], '5': []},
        }
        for stt in SchoolTimeTable.objects.filter(curriculum__teacher_id=teacher.id).order_by('clazz_week'):
            # 遍历与教师ID相关联的SchoolTimeTable实例
            tmp[str(stt.clazz_time)][str(stt.clazz_week)].append(stt)
        return tmp

    return render(request, 'teacher_info.html', context={'time_table': get_stt(), 'typ': 'curriculum'})


@check_login
def teacher_input_score(request):
    if request.method == 'POST':
        data = request.POST.dict()
        if not StudentCurriculumScore.objects.filter(student_id__student_id=data['student_id'],
                                                     curriculum_id=data['curriculum_id']).exists():
            # 检查是否存在学生成绩信息 匹配学生的ID和课程ID 不存在就新建
            scs = StudentCurriculumScore(student_id=StudentInfo.objects.get(student_id=data['student_id']),
                                         curriculum_id=Curriculum.objects.get(id=data['curriculum_id']))
        else:
            scs = StudentCurriculumScore.objects.get(student_id__student_id=data['student_id'],
                                                     curriculum_id=data['curriculum_id'])
        scs.score = data['score']  # 已存在 直接获取
        scs.save()
    user_id = request.session.get('user_id')  # 获取当前用户ID
    if not TeacherInfo.objects.filter(user_id=user_id).exists():
        return redirect('teacher_info')

    teacher = TeacherInfo.objects.get(user_id=user_id)  # 获取教师信息
    clazz_and_curriculum_ids = []  # 初始化表 存储班级ID和课程ID的组合

    for stt in SchoolTimeTable.objects.filter(curriculum__teacher_id=teacher.id):
        # 遍历所有的时间表 获取班级ID和课程ID 添加到列表中
        _clazz_id = stt.clazz_id.id
        _curr_id = stt.curriculum.id
        if (_clazz_id, _curr_id) not in clazz_and_curriculum_ids:
            clazz_and_curriculum_ids.append((_clazz_id, _curr_id))

    all_students = []  # 存储学生信息
    all_scores = []  # 存储成绩
    all_curriculums = []  # 存储课程信息
    for ci in clazz_and_curriculum_ids:
        # 遍历获取每个班级和课程的组合
        # 获取每个班级的所有学生并将其添加到all_students列表。
        cs = ClazzStudents.objects.filter(clazz_id=ci[0])
        all_students += cs
        for _c in cs:
            # 对于每个学生，检查是否有对应课程的成绩。
            # 如果有成绩，添加到all_scores列表；如果没有，添加一个占位符'-'。
            # 将相关课程信息添加到all_curriculums列表。
            _score = StudentCurriculumScore.objects.filter(student_id=_c.student_id.id, curriculum_id=ci[1])
            if _score:
                all_scores.append(str(_score[0].score))
            else:
                all_scores.append('-')
            all_curriculums.append(Curriculum.objects.get(id=ci[1]))
    return render(request, 'teacher_info.html',
                  context={'students': zip(all_students, all_scores, all_curriculums),
                           'typ': 'score'})
