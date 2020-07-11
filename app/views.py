from django.shortcuts import render, redirect, reverse
from django.urls import reverse
from .forms import *

from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import *
import random
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

# def admin_index(request):
#     return render(request, 'adminpages/admin_subjects.html')
class AdminIndex(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 0:
            s = len(Curs.objects.all())
            b = s*7
            c = len(UserProfile.objects.filter(status=1))
            d = len(UserProfile.objects.filter(status=2))
            courses = Curs.objects.filter(language=a.language).order_by('type_curs')
            data = CourseData.objects.all()
            return render(request, 'adminpages/admin_subjects.html', context={'user': a, 'courses': courses, 'data':data, 's':s, 'b':b, 'c':c, 'd':d})

class AdminRating(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 0:
            search_query = request.GET.get('student_search', '')

            if search_query:
                students = UserProfile.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query), status=2).order_by('-rating')        
            else:
                students = UserProfile.objects.filter(status=2).order_by('-rating')

            paginator = Paginator(students, 50)
            page_number = request.GET.get('page', 1)

            page = paginator.get_page(page_number)
            is_paginated = page.has_other_pages()
            if page.has_previous():
                prev_url = '?page={}'.format(page.previous_page_number())
            else:
                prev_url = ''
            
            if page.has_next():
                next_url = '?page={}'.format(page.next_page_number())
            else:
                next_url = ''
            return render(request, 'adminpages/admin_rating.html', context={'user': a, 'students':page, 'is_paginated': is_paginated, 'next_url': next_url, 'prev_url': prev_url,})

class AdminTeachers(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 0:
            search_query = request.GET.get('teacher_search', '')

            if search_query:
                teachers = UserProfile.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(school__icontains=search_query) | Q(username__icontains=search_query), status=1).order_by('last_name')        
            else:
                teachers = UserProfile.objects.filter(status=1).order_by('last_name')
            paginator = Paginator(teachers, 500)
            page_number = request.GET.get('page', 1)

            page = paginator.get_page(page_number)
            is_paginated = page.has_other_pages()
            if page.has_previous():
                prev_url = '?page={}'.format(page.previous_page_number())
            else:
                prev_url = ''
            
            if page.has_next():
                next_url = '?page={}'.format(page.next_page_number())
            else:
                next_url = ''
            form_teacher = AddTeacher()
            form_password = EditPassword()
            return render(request, 'adminpages/admin_teachers.html', context={'user': a, 'form_teacher': form_teacher, 'teachers':teachers, 'form_password': form_password, 'page_objects': page, 'is_paginated': is_paginated, 'next_url': next_url, 'prev_url': prev_url})

    def post(self, request):
        if 'add_teacher'in request.POST:
            form_teacher = AddTeacher(request.POST)
            if form_teacher.is_valid():
                first_name = form_teacher.cleaned_data['first_name']
                last_name = form_teacher.cleaned_data['last_name']
                school = form_teacher.cleaned_data['school']
                username = form_teacher.cleaned_data['username']
                email = form_teacher.cleaned_data['email']
                iin = form_teacher.cleaned_data['iin']
                password = form_teacher.cleaned_data['password']
                password1 = form_teacher.cleaned_data['password1']
                patronymic = form_teacher.cleaned_data['patronymic']
                major = request.POST.get('major')
                number = request.POST.get('number')
                b = UserProfile.objects.filter(username=username).first()
                if b is not None:
                    messages.warning(request, '2')
                    return HttpResponseRedirect(reverse('admin_teachers'))
                if password != password1:
                    messages.error(request, '1')
                    return HttpResponseRedirect(reverse('admin_teachers'))
                new_teacher = UserProfile(username=username, first_name=first_name, school=school, last_name=last_name, status=1, rating=0, email=email, iin=iin, language='kz', patronymic=patronymic, major=major, phone=number)
                new_teacher.set_password(password)
                if new_teacher is not None:
                    new_teacher.save()
                    return HttpResponseRedirect(reverse('admin_teachers'))
                return HttpResponseRedirect(reverse('admin_teachers'))

class AdminProfile(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, teacher_id):
        a = request.user
        if a.status == 0:
            form_image = AddAvatar()
            form_password = EditPassword()
            teacher = UserProfile.objects.get(id__iexact=teacher_id)
            students = UserProfile.objects.filter(status=2, teacher=teacher_id)
            form_profile = EditProfile({'first_name': teacher.first_name, 'last_name': teacher.last_name, 'username':teacher.username, 'email': teacher.email, 'iin':teacher.iin, 'school':teacher.school, 'patronymic': teacher.patronymic})
            a = request.user
            return render(request, 'adminpages/admin_profile.html', context={'user': a, 'teacher':teacher, 'form_image': form_image, 'edit_profile': form_profile, 'form_password': form_password, 'students': students})

    def post(self, request, teacher_id):
        teacher = UserProfile.objects.get(id__iexact=teacher_id)
        if 'submit_avatar' in request.POST:
            form_image = AddAvatar(request.POST, request.FILES)
            if form_image.is_valid():
                image = request.FILES['image']
                teacher.avatar = image
                teacher.save()
                return HttpResponseRedirect(reverse('admin_profile', kwargs={'teacher_id': teacher_id}))
        if 'edit_profile' in request.POST:
            form_profile = EditProfile(request.POST)
            if form_profile.is_valid():
                teacher.first_name = form_profile.cleaned_data['first_name']
                teacher.last_name = form_profile.cleaned_data['last_name']
                teacher.username = form_profile.cleaned_data['username']
                teacher.school = form_profile.cleaned_data['school']
                teacher.iin = form_profile.cleaned_data['iin']
                teacher.email = form_profile.cleaned_data['email']
                teacher.patronymic = form_profile.cleaned_data['patronymic']
                teacher.major = request.POST.get('major')
                teacher.phone = request.POST.get('number')
                teacher.save()
                return HttpResponseRedirect(reverse('admin_profile', kwargs={'teacher_id': teacher_id}))
        if 'edit_password' in request.POST:
            form_password = EditPassword(request.POST)
            if form_password.is_valid():
                # password = form_password.cleaned_data['password']
                password1 = form_password.cleaned_data['password1']
                password2 = form_password.cleaned_data['password2']
                # user = authenticate(username=teacher.username, password=password)
                if teacher is not None:
                    if password1!=password2:
                        print('Password!=password1')
                        return HttpResponseRedirect(reverse('admin_profile', kwargs={'teacher_id': teacher_id}))
                    teacher.set_password(password1)
                    teacher.save()
                    print('success')
                    return HttpResponseRedirect(reverse('admin_profile', kwargs={'teacher_id': teacher_id}))
                print('user none')
                return HttpResponseRedirect(reverse('admin_profile', kwargs={'teacher_id': teacher_id}))




class AdminAddCourse(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id):
        a = request.user
        if a.status == 0:
            course = Curs.objects.get(id__iexact=course_id)
            lessons = Lessons.objects.filter(curs__id=course_id).order_by('lesson_id')
            form_title = AddCourseName({'title': course.title})
            form_image = AddCourseImage()
            form_video = AddCourseVideo()
            data = CourseData.objects.filter(curs=course).first()
            return render(request, 'adminpages/admin_add_course.html', context={'user': a, 'course': course, 'form_title': form_title, 'form_image': form_image, 'form_video':form_video, 'lessons': lessons, 'data':data})
    
    def post(self, request, course_id, *args, **kwargs):
        form_title = AddCourseName(request.POST)
        course = Curs.objects.get(id__iexact=course_id)
        lessons = Lessons.objects.filter(curs__id=course_id)
        if 'title_course' in request.POST:
            if form_title.is_valid():
                title = form_title.cleaned_data['title']
                type_curs = request.POST.get('type_curs')
                course.title = title
                course.type_curs = type_curs
                course.save()
                return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
        if 'image_course' in request.POST:
            form_image = AddCourseImage(request.POST, request.FILES)
            if form_image.is_valid():
                image = request.FILES['image']
                course.image = image
                course.save()
                return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
        if 'video_course' in request.POST:
            form_video = AddCourseVideo(request.POST, request.FILES)
            if form_video.is_valid():
                video = request.FILES['video']
                course.video = video
                course.save()
                return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
        if 'add_data_course' in request.POST:
            data = CourseData.objects.filter(curs=course).first()
            if data is None:
                data = CourseData(curs=course, developer=request.POST.get('developer'), duration=request.POST.get('duration'), certificate=request.POST.get('sert'), time=request.POST.get('time'))
                data.save()
                print('saved')
            else:
                data.developer=request.POST.get('developer')
                data.duration=request.POST.get('duration')
                data.certificate=request.POST.get('sert')
                data.time=request.POST.get('time')
                data.save()
                print('insert')
            return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
        if 'submit_new' in request.POST:
            s = request.POST.get('title_new')
            s1 = request.POST.get('number_new')
            q = Lessons.objects.filter(lesson_id=s1, curs=course).first()
            if q is not None:
                messages.error(request, str(s1), extra_tags='new_error')
                return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
            return HttpResponseRedirect(reverse('admin_create_lesson', kwargs={'course_id': course.id, 'number':s1, 'title': s}))
        if 'video_poster' in request.POST:
            s = request.FILES['new_poster']
            course.image_video = s
            course.save()
            return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
        for i in lessons:
            s = 'submit_' + str(i.id)
            if s in request.POST:
                s1 = request.POST.get('number_'+str(i.id))
                q = Lessons.objects.filter(lesson_id=s1, curs=course).first()
                if q is not None:
                    if i.lesson_id is not None:
                        if i.lesson_id != q.lesson_id:
                            if q is not None:
                                messages.error(request, str(s1), extra_tags='new_error')
                                return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
                    else:
                        if q is not None:
                            messages.error(request, str(s1), extra_tags='new_error')
                            return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))
                i.title=request.POST.get('title_'+str(i.id))
                i.lesson_id = s1
                i.save()
                return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': course.id}))

class AdminAddLesson(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id, lesson_id):
        a = request.user
        if a.status == 0:
            course = Curs.objects.filter(id=course_id).first()
            lessons = Lessons.objects.filter(curs__id=course_id).order_by('lesson_id')
            les = Lessons.objects.get(id__iexact=lesson_id)
            hints = Hint.objects.filter(lesson=les)
            videos = Video_lessons.objects.filter(lesson=les)
            tests = Test.objects.filter(lesson=les)
            form_text = AddLessonText({'text': les.text})
            form_text_teacher = AddLessonTextTeacher({'text1': les.text_teacher})
            form_hint = AddLessonHint()
            form_video = AddLessonVideo()
            form_test = AddLessonTest()
            context={'user': a,
            'lessons': lessons, 
            'lesson_id': lesson_id,
            'form_text': form_text,
            'form_text_teacher': form_text_teacher,
            'les':les,
            'form_hint': form_hint, 
            'hints':hints,
            'form_video': form_video,
            'videos': videos,
            'form_test': form_test,
            'tests': tests,
            'course': course
            }
            return render(request, 'adminpages/admin_add_lesson.html', context=context)

    def post(self, request, course_id, lesson_id):
        lesson = Lessons.objects.get(id__iexact=lesson_id)
        if 'submit_text' in request.POST:
            form_text = AddLessonText(request.POST)
            if form_text.is_valid():
                text = form_text.cleaned_data['text']
                lesson.text = text
                lesson.save()
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))
        if 'submit_text_teacher' in request.POST:
            form_text_teacher = AddLessonTextTeacher(request.POST)
            if form_text_teacher.is_valid():
                text = form_text_teacher.cleaned_data['text1']
                lesson.text_teacher = text
                lesson.save()
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))
        if 'submit_hint' in request.POST:
            form_hint = AddLessonHint(request.POST)
            if form_hint.is_valid():
                text = form_hint.cleaned_data['text_hint']
                hint = Hint(text=text, lesson=lesson)
                hint.save()
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))
        if 'submit_video' in request.POST:
            form_video = AddLessonVideo(request.POST, request.FILES)
            if form_video.is_valid():
                video = request.FILES['video']
                video_lesson = Video_lessons(video=video, lesson=lesson, title=request.POST.get('title_video'))
                video_lesson.save()
                if video_lesson.id is not None:
                    messages.success(request, '1', extra_tags='add_video_success')
                else:
                    messages.error(request, '2', extra_tags='add_error')
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))
        if 'submit_test' in request.POST:
            form_test = AddLessonTest(request.POST)
            if form_test.is_valid():
                test_lesson = Test(name=form_test.cleaned_data['name_test'], ask=form_test.cleaned_data['ask_test'], answer1=form_test.cleaned_data['answer_1'], answer2=form_test.cleaned_data['answer_2'], answer3=form_test.cleaned_data['answer_3'], answer4=form_test.cleaned_data['answer_4'], answer5=form_test.cleaned_data['answer_5'], correct_answer=form_test.cleaned_data['correct_answer'], lesson=lesson)
                test_lesson.save()
                if test_lesson.id is not None:
                    messages.success(request, '1', extra_tags='add_test_success')
                else:
                    messages.error(request, '2',  extra_tags='add_error')
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))
        videos = Video_lessons.objects.filter(lesson=lesson)
        for i in videos:
            s = 'add_poster_'+str(i.id)
            if s in request.POST:
                m = request.FILES['poster_video_'+str(i.id)]
                i.image_video=m
                i.save()
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))
        for i in videos:
            s = 'update_image_'+str(i.id)
            if s in request.POST:
                m = request.POST.get('title_update_'+str(i.id))
                i.title=m
                i.save()
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))


        tests = Test.objects.filter(lesson=lesson)
        for i in tests:
            s = 'update_test_'+str(i.id)
            if s in request.POST:
                i.name = request.POST.get('name_'+str(i.id))
                i.ask = request.POST.get('ask_'+str(i.id))
                i.answer1 = request.POST.get('answer1_'+str(i.id))
                i.answer2 = request.POST.get('answer2_'+str(i.id))
                i.answer3 = request.POST.get('answer3_'+str(i.id))
                i.answer4 = request.POST.get('answer4_'+str(i.id))
                i.answer5 = request.POST.get('answer5_'+str(i.id))
                i.correct_answer = request.POST.get('trueVariant_'+str(i.id))
                i.save()
                messages.success(request, '1', extra_tags='update_test_success')
                return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.status == 0:
                return redirect(reverse('admin_index'))
            if user.status == 1:
                return redirect(reverse('teacher_index'))
            if user.status == 2:
                return redirect(reverse('student_index'))
        form = LoginForm()
        return render(request, 'login.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.status == 0:
                    return redirect(reverse('admin_index'))
                if user.status == 1:
                    return redirect(reverse('teacher_index'))
                if user.status == 2:
                    return redirect(reverse('student_index'))
            else:
                messages.error(request, 'Логин или пароль неправильный')
                return HttpResponseRedirect(reverse('login_path'))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login_path'))

class LanguageKZ(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        a = request.user
        a.language = 'kz'
        a.save()
        if a.status == 0:
            return redirect(reverse('admin_index'))
        if a.status ==1:
            return redirect(reverse('teacher_index'))
        if a.status ==2:
            return redirect(reverse('student_index'))

class LanguageRU(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        a = request.user
        a.language = 'ru'
        a.save()
        if a.status == 0:
            return redirect(reverse('admin_index'))
        if a.status ==1:
            return redirect(reverse('teacher_index'))
        if a.status ==2:
            return redirect(reverse('student_index'))

class AdminDeleteUser(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, user_id):
        a = request.user
        if a.status == 0:
            user = UserProfile.objects.get(id__iexact=user_id)
            user.delete()
            return HttpResponseRedirect(reverse('admin_teachers'))
        if a.status == 1:
            user = UserProfile.objects.get(id__iexact=user_id, status=2)
            user.delete()
            return HttpResponseRedirect(reverse('teacher_students'))


class CreateCourse(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 0:
            if a.language == 'ru':
                b = 'Новый курс'
            else:
                b = 'Жаңа курс'
            new_course = Curs(title=b, number_lessons=0, language=a.language)
            new_course.save()
            return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': new_course.id}))

class CreateLesson(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id, number, title):
        a = request.user
        if a.status == 0:
            course = Curs.objects.filter(id=course_id).first()
            new_lesson = Lessons(curs=course, lesson_id=number, title=title)
            new_lesson.save()
            return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': course_id, 'lesson_id': new_lesson.id}))

class DeleteLesson(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, lesson_id):
        a = request.user
        if a.status == 0:
            lesson = Lessons.objects.get(id__iexact=lesson_id)
            c_id = lesson.curs.id
            lesson.delete()
            return HttpResponseRedirect(reverse('admin_add_course', kwargs={'course_id': c_id}))

class DeleteHint(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, hint_id):
        aa = request.user
        if aa.status == 0:
            hint = Hint.objects.get(id__iexact=hint_id)
            a = hint.lesson.curs.id
            b = hint.lesson.id
            hint.delete()
            return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': a, 'lesson_id': b}))

class DeleteTest(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, test_id):
        aa = request.user
        if aa.status == 0:
            test = Test.objects.get(id__iexact=test_id)
            a = test.lesson.curs.id
            b = test.lesson.id
            test.delete()
            return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': a, 'lesson_id': b}))

class DeleteVideo(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, video_id):
        a = request.user
        if a.status==0:
            video = Video_lessons.objects.get(id__iexact=video_id)
            b = video.lesson.curs.id
            c = video.lesson.id
            video.delete()
            return HttpResponseRedirect(reverse('admin_add_lesson', kwargs={'course_id': b, 'lesson_id': c}))


class UnfollowStudent(LoginRequiredMixin, View):
    def get(self, request, curs_stud_id):
        a = request.user
        if a.status==1:
            student = Curs_Students.objects.filter(id=curs_stud_id, teacher=a.id ).first()
            student.block = 0
            student.save()
            return HttpResponseRedirect(reverse('teacher_students'))


# Teachers Page


class TeacherIndex(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 1:
            courses = Curs.objects.filter(language=a.language).order_by('type_curs')
            data = CourseData.objects.all()
            return render(request, 'teachpages/teacher_subjects.html', context={'user': a, 'courses': courses, 'data':data})

class TeacherCourse(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id):
        a = request.user
        if a.status == 1:
            students = UserProfile.objects.filter(status=2, teacher=a.id)
            course = Curs.objects.get(id__iexact=course_id)
            lessons = Lessons.objects.filter(curs=course).order_by('lesson_id')
            curs_students = Curs_Students.objects.filter(curs=course, block=1, teacher=a.id)
            data = CourseData.objects.filter(curs=course).first()
            return render(request, 'teachpages/teacher_course.html', context={'user': a, 'course': course, 'lessons': lessons, 'students': students, 'curs_students': curs_students, 'data': data})
    
    def post(self, request, course_id):
        a = request.user
        students = UserProfile.objects.filter(status=2, teacher=a.id)
        course = Curs.objects.get(id__iexact=course_id)
        lessons = Lessons.objects.filter(curs=course)
        if 'addstudent' in request.POST:
            for i in students:
                completed = request.POST.get(str(i.id))
                if completed is not None:
                    print(completed)
                    b = Curs_Students.objects.filter(curs__id=course_id, student__id=i.id).first()
                    if not b:
                        b = Curs_Students(curs=course, student=i, number_lesson=1, teacher=a.id, test_status=0, block=1)
                        b.save()
                    else:
                        b.block = 1
                        b.save()
                    c = TeacherCourses.objects.filter(teacher_id=a.id, curs=course).first()
                    if not c:
                        c = TeacherCourses(teacher_id=a.id, curs=course)
                        c.save()
                else:
                    b = Curs_Students.objects.filter(curs__id=course_id, student__id=i.id).first()
                    if b is not None:
                        b.block = 0
                        b.save()
            return HttpResponseRedirect(reverse('teacher_course', kwargs={'course_id': course.id}))
        for i in range(1,len(lessons)+1):
            s = 'submit_' + str(i)
            if s in request.POST:
                curs_students = Curs_Students.objects.filter(curs=course)
                for j in curs_students:
                    hometask = request.POST.get(str(j.id))
                    if hometask is not None:
                        student = UserProfile.objects.get(id__iexact=j.student.id)
                        j.number_lesson +=1
                        j.test_status = 0
                        student.rating +=5
                        student.save()
                        a.rating +=5
                        a.save()
                        j.save()
                return HttpResponseRedirect(reverse('teacher_course', kwargs={'course_id': course.id}))

class TeacherRating(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 1:
            students = UserProfile.objects.filter(status=2, teacher=a.id).order_by('-rating')[:50]
            return render(request, 'teachpages/teacher_rating.html', context={'user': a, 'students':students})


class TeacherProfile(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        teacher = request.user
        if teacher.status == 1:
            form_image = AddAvatar()
            form_password = EditPassword()
            form_profile = EditProfile1({'first_name': teacher.first_name, 'last_name': teacher.last_name, 'email': teacher.email, 'school':teacher.school, 'patronymic':teacher.patronymic})
            return render(request, 'teachpages/teacher_profile.html', context={'user': teacher, 'form_image': form_image, 'edit_profile': form_profile, 'form_password': form_password})

    def post(self, request):
        teacher = request.user
        if 'submit_avatar' in request.POST:
            form_image = AddAvatar(request.POST, request.FILES)
            if form_image.is_valid():
                image = request.FILES['image']
                teacher.avatar = image
                teacher.save()
                return HttpResponseRedirect(reverse('teacher_profile'))
        if 'edit_profile' in request.POST:
            form_profile = EditProfile1(request.POST)
            if form_profile.is_valid():
                teacher.first_name = form_profile.cleaned_data['first_name']
                teacher.last_name = form_profile.cleaned_data['last_name']
                teacher.school = form_profile.cleaned_data['school']
                teacher.email = form_profile.cleaned_data['email']
                teacher.patronymic = form_profile.cleaned_data['patronymic']
                teacher.major = request.POST.get('major')
                teacher.phone = request.POST.get('number')
                teacher.save()
                return HttpResponseRedirect(reverse('teacher_profile'))
        if 'edit_password' in request.POST:
            form_password = EditPassword(request.POST)
            if form_password.is_valid():
                # password = form_password.cleaned_data['password']
                password1 = form_password.cleaned_data['password1']
                password2 = form_password.cleaned_data['password2']
                # user = authenticate(username=teacher.username, password=password)
                if teacher is not None:
                    if password1!=password2:
                        print('Password!=password1')
                        return HttpResponseRedirect(reverse('teacher_profile'))
                    teacher.set_password(password1)
                    teacher.save()
                    print('success')
                    user = authenticate(username=teacher.username, password=password1)
                    login(request, user)
                    return HttpResponseRedirect(reverse('teacher_profile'))
                print('user none')
                return HttpResponseRedirect(reverse('teacher_profile'))

class TeacherStudents(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 1:
            students = UserProfile.objects.filter(teacher=a.id)
            courses = TeacherCourses.objects.filter(teacher_id=a.id)
            course_students = Curs_Students.objects.filter(teacher=a.id, block=1)
            form_teacher = AddTeacher()
            return render(request, 'teachpages/teacher_students.html', context={'user': a, 'form_teacher': form_teacher, 'students': students, 'courses':courses, 'course_students':course_students})

    def post(self, request):
        a = request.user
        if 'add_student'in request.POST:
            form_teacher = AddTeacher(request.POST)
            if form_teacher.is_valid():
                first_name = form_teacher.cleaned_data['first_name']
                last_name = form_teacher.cleaned_data['last_name']
                school = form_teacher.cleaned_data['school']
                username = form_teacher.cleaned_data['username']
                email = form_teacher.cleaned_data['email']
                iin = form_teacher.cleaned_data['iin']
                password = form_teacher.cleaned_data['password']
                password1 = form_teacher.cleaned_data['password1']
                patronymic = form_teacher.cleaned_data['patronymic']
                layer = request.POST.get('layer_number')
                number = request.POST.get('number')
                b = UserProfile.objects.filter(username=username).first()
                if b is not None:
                    messages.warning(request, '2')
                    return HttpResponseRedirect(reverse('teacher_students'))
                if password != password1:
                    messages.error(request, '1')
                    return HttpResponseRedirect(reverse('teacher_students'))
                new_teacher = UserProfile(username=username, first_name=first_name, school=school, last_name=last_name, status=2, rating=0, teacher=a.id, email=email, iin=iin, language=a.language, patronymic=patronymic, phone=number, layer=layer)
                new_teacher.set_password(password)
                if new_teacher is not None:
                    new_teacher.save()
                    return HttpResponseRedirect(reverse('teacher_students'))
                return HttpResponseRedirect(reverse('teacher_students'))


class TeacherStudentProfile(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, student_id):
        a = request.user
        if a.status == 1 or a.status == 0:
            form_image = AddAvatar()
            form_password = EditPassword()
            teacher = UserProfile.objects.get(id__iexact=student_id)
            list_sert = Sertificate.objects.filter(student=teacher)
            form_profile = EditProfile({'first_name': teacher.first_name, 'last_name': teacher.last_name, 'username':teacher.username, 'email': teacher.email, 'iin':teacher.iin, 'school':teacher.school, 'patronymic': teacher.patronymic})
            curs_student = Curs_Students.objects.filter(student=teacher)
            tests_student = Test_Student.objects.filter(student=teacher)
            if a.status == 1:
                return render(request, 'teachpages/teacher_student_profile.html', context={'user': a, 'teacher':teacher, 'form_image': form_image, 'edit_profile': form_profile, 'form_password': form_password, 'tests_student':tests_student, 'curs_student':curs_student, 'list_sert':list_sert})
            if a.status == 0:
                return render(request, 'adminpages/admin_student_profile.html', context={'user': a, 'teacher':teacher, 'form_image': form_image, 'edit_profile': form_profile, 'form_password': form_password, 'tests_student':tests_student, 'curs_student':curs_student, 'list_sert':list_sert})

    def post(self, request, student_id):
        teacher = UserProfile.objects.get(id__iexact=student_id)
        if 'submit_avatar' in request.POST:
            form_image = AddAvatar(request.POST, request.FILES)
            if form_image.is_valid():
                image = request.FILES['image']
                teacher.avatar = image
                teacher.save()
                return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))
        if 'edit_profile' in request.POST:
            form_profile = EditProfile(request.POST)
            if form_profile.is_valid():
                teacher.first_name = form_profile.cleaned_data['first_name']
                teacher.last_name = form_profile.cleaned_data['last_name']
                teacher.username = form_profile.cleaned_data['username']
                teacher.school = form_profile.cleaned_data['school']
                teacher.iin = form_profile.cleaned_data['iin']
                teacher.email = form_profile.cleaned_data['email']
                teacher.patronymic = form_profile.cleaned_data['patronymic']
                teacher.phone = request.POST.get('number')
                teacher.layer = request.POST.get('layer_number')
                teacher.save()
                return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))
        if 'edit_password' in request.POST:
            form_password = EditPassword(request.POST)
            if form_password.is_valid():
                # password = form_password.cleaned_data['password']
                password1 = form_password.cleaned_data['password1']
                password2 = form_password.cleaned_data['password2']
                if teacher is not None:
                    if password1!=password2:
                        print('Password!=password1')
                        return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))
                    teacher.set_password(password1)
                    teacher.save()
                    print('success')
                    return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))
                print('user none')
                return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))
        if 'submit_points' in request.POST:
            points = request.POST.get('points')
            curs = request.POST.get('addCourseName')
            image = request.FILES['sert_img']
            if int(points) > 20:
                messages.error(request, "ERROR", extra_tags='new_error')
                return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))
            sert = Sertificate.objects.filter(student=teacher, curs=curs).first()
            if sert is None:
                sert = Sertificate(student=teacher, point=points, curs=curs, image=image)
                teacher.points += int(points)
                teacher.save()
                sert.save()
            else:
                teacher.points -=sert.point
                sert.point = int(points)
                teacher.points += int(sert.point)
                sert.image = image
                teacher.save()
                sert.save()
            messages.error(request, "SUCCESS", extra_tags='success')
            return HttpResponseRedirect(reverse('teacher_student_profile', kwargs={'student_id': student_id}))

class TeacherLesson(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id, lesson_id):
        a = request.user
        if a.status == 1:
            lessons = Lessons.objects.filter(curs__id=course_id).order_by('lesson_id')
            les = Lessons.objects.get(id__iexact=lesson_id)
            hints = Hint.objects.filter(lesson=les)
            videos = Video_lessons.objects.filter(lesson=les)
            context={'user': a,
            'lessons': lessons, 
            'lesson_id': lesson_id,
            'les':les,
            'hints':hints,
            'videos': videos,
            }
            return render(request, 'teachpages/teacher_course_after.html', context=context)


# Student Views

class StudentIndex(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 2:
            courses = Curs_Students.objects.filter(student__id=a.id, block=1)
            data = CourseData.objects.all()
            return render(request, 'studpages/stud_learning_page.html', context={'user': a, 'courses':courses, 'data': data})

class StudentRating(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 2:
            students = UserProfile.objects.filter(status=2).order_by('-rating')[:50]
            return render(request, 'studpages/stud_rating.html', context={'user': a, 'students':students})

class StudentSubject(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 2:
            courses = Curs.objects.filter(language=a.language).order_by('type_curs')
            data = CourseData.objects.all()
            return render(request, 'studpages/stud_subjects.html', context={'user': a, 'courses': courses, 'data':data})

class StudentProfile(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request):
        a = request.user
        if a.status == 2:
            form_image = AddAvatar()
            form_password = EditPassword()
            curs_student = Curs_Students.objects.filter(student=a)
            tests_student = Test_Student.objects.filter(student=a)
            form_profile = EditProfile1({'first_name': a.first_name, 'last_name': a.last_name, 'email': a.email, 'school':a.school, 'patronymic': a.patronymic})
            return render(request, 'studpages/stud_profile.html', context={'user': a, 'form_image': form_image, 'edit_profile': form_profile, 'form_password': form_password, 'tests_student':tests_student, 'curs_student':curs_student})

    def post(self, request):
        a = request.user
        if 'submit_avatar' in request.POST:
            form_image = AddAvatar(request.POST, request.FILES)
            if form_image.is_valid():
                image = request.FILES['image']
                a.avatar = image
                a.save()
                return HttpResponseRedirect(reverse('student_profile'))
        if 'edit_profile' in request.POST:
            form_profile = EditProfile1(request.POST)
            if form_profile.is_valid():
                a.first_name = form_profile.cleaned_data['first_name']
                a.last_name = form_profile.cleaned_data['last_name']
                # a.username = form_profile.cleaned_data['username']
                a.school = form_profile.cleaned_data['school']
                # a.iin = form_profile.cleaned_data['iin']
                a.email = form_profile.cleaned_data['email']
                a.patronymic = form_profile.cleaned_data['patronymic']
                a.phone = request.POST.get('number')
                a.save()
                return HttpResponseRedirect(reverse('student_profile'))
        if 'edit_password' in request.POST:
            form_password = EditPassword(request.POST)
            if form_password.is_valid():
                # password = form_password.cleaned_data['password']
                password1 = form_password.cleaned_data['password1']
                password2 = form_password.cleaned_data['password2']
                # user = authenticate(username=a.username, password=password)
                if a is not None:
                    if password1!=password2:
                        print('Password!=password1')
                        return HttpResponseRedirect(reverse('student_profile'))
                    a.set_password(password1)
                    a.save()
                    print('success')
                    user = authenticate(username=a.username, password=password1)
                    login(request, user)
                    return HttpResponseRedirect(reverse('student_profile'))
                print('user none')
                return HttpResponseRedirect(reverse('student_profile'))


class StudentCourseBefore(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id):
        a = request.user
        if a.status == 2:
            course = Curs.objects.get(id__iexact=course_id)
            lessons = Lessons.objects.filter(curs__id=course_id).order_by('lesson_id')
            data = CourseData.objects.filter(curs=course).first()
            return render(request, 'studpages/stud_course_before.html', context={'user': a, 'course': course, 'lessons': lessons, 'data':data})


class StudentCourseAfter(LoginRequiredMixin, View):
    login_url = '/login'
    raise_exception = True
    def get(self, request, course_id, lesson_id):
        a = request.user
        if a.status == 2:
            course = Curs_Students.objects.filter(curs__id=course_id, student__id=a.id).first()
            lessons = Lessons.objects.filter(curs__id=course_id).order_by('lesson_id')
            les = Lessons.objects.get(id__iexact=lesson_id)
            hints = Hint.objects.filter(lesson=les)
            videos = Video_lessons.objects.filter(lesson=les)
            tests = Test.objects.filter(lesson=les).order_by('?')
            test_student = Test_Student.objects.filter(curs__id=course_id, student=a, lesson=lesson_id)
            if test_student is not None:
                s = 0
                s1 = 0
                for i in test_student:
                    s += i.points
                    s1 += i.all_points
            rd = random.sample(range(1, 6), 5)
            context={'user': a,
            'lessons': lessons, 
            'lesson_id': lesson_id,
            'les':les,
            'hints':hints,
            'videos': videos,
            'tests': tests,
            'course': course,
            'test_student': test_student,
            'rd': rd,
            'points': s,
            'all_points': s1
            }
            return render(request, 'studpages/stud_course_after.html', context=context)

    def post(self, request, course_id, lesson_id):
        a = request.user
        course = Curs.objects.filter(id=course_id).first()
        if 'submit_test' in request.POST:
            tests = Test.objects.filter(lesson__id=lesson_id)
            for i in tests:
                s = 'answer_' + str(i.id)
                answer = request.POST.get(s)
                test_student = Test_Student.objects.filter(curs=course, student=a, name_test=i.name, lesson=lesson_id).first()
                if test_student is None:
                    test_student = Test_Student(curs=course, student=a, name_test=i.name, points=0, all_points=0, lesson=lesson_id)
                    test_student.save()
                if test_student.status == 0:
                    test_student.all_points +=1
                    if int(i.correct_answer)==int(answer):
                        test_student.points +=1
                    test_student.save()
            test_student = Test_Student.objects.filter(curs=course, student=a, lesson=lesson_id)
            student = UserProfile.objects.get(id__iexact=a.id)
            # teacher = UserProfile.objects.filter(id=student.teacher).first()
            for j in test_student:
                if j.status == 0:
                    student.rating = student.rating + j.points*5
                    j.status=1
                    j.save()
            student.save()
            w = Curs_Students.objects.filter(curs=course, student=a).first()
            if w is None:
                w = Curs_Students(curs=course, student=a, teacher=a.teacher, block=1, number_lesson=1)
            w.test_status = 1
            w.save()
            return HttpResponseRedirect(reverse('student_course_after', kwargs={'course_id': course_id, 'lesson_id': lesson_id}))


def index(request):
    courses = Curs.objects.filter(language='ru').order_by('type_curs')
    a = len(Curs.objects.all())
    b = a*7
    c = len(UserProfile.objects.filter(status=1))
    d = len(UserProfile.objects.filter(status=2))
    data = CourseData.objects.all()
    context = {
        'courses': courses,
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'data': data
    }
    return render(request, 'index.html', context=context)

def index_kz(request):
    courses = Curs.objects.filter(language='kz').order_by('type_curs')
    a = len(Curs.objects.all())
    b = a*7
    c = len(UserProfile.objects.filter(status=1))
    d = len(UserProfile.objects.filter(status=2))
    data = CourseData.objects.all()
    context = {
        'courses': courses,
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'data': data
    }
    return render(request, 'index2.html', context=context)
