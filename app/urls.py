from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index, name='index'),
    path('lang=kz', index_kz, name='index_kz'),
    path('admin_page/subject', AdminIndex.as_view(), name='admin_index'),
    path('admin_page/rating', AdminRating.as_view(), name='admin_rating'),
    path('admin_page/teachers', AdminTeachers.as_view(), name='admin_teachers'),
    path('admin_page/profile/teacher/<int:teacher_id>', AdminProfile.as_view(), name='admin_profile'),
    path('admin_page/add/course/<int:course_id>', AdminAddCourse.as_view(), name='admin_add_course'),
    path('admin_page/add_course/create', CreateCourse.as_view(), name='admin_create_course'),
    path('admin_page/course/<int:course_id>/add_lesson/<int:lesson_id>', AdminAddLesson.as_view(), name='admin_add_lesson'),
    path('admin_page/add_lesson/create/<int:course_id>/number/<int:number>/title/<str:title>', CreateLesson.as_view(), name='admin_create_lesson'),
    path('admin_page/lesson/delete/<int:lesson_id>', DeleteLesson.as_view(), name='admin_delete_lesson'),
    path('admin_page/hint/delete/<int:hint_id>', DeleteHint.as_view(), name='admin_delete_hint'),
    path('admin_page/test/delete/<int:test_id>', DeleteTest.as_view(), name='admin_delete_test'),
    path('admin_page/video/delete/<int:video_id>', DeleteVideo.as_view(), name='admin_delete_video'),
    path('admin_page/delete/user/<int:user_id>', AdminDeleteUser.as_view(), name='admin_delete_user'),
    path('login', LoginView.as_view(), name='login_path'),
    path('logout', LogoutView.as_view(), name='logout_path'),
    path('admin_page/student/<int:student_id>/profile/', TeacherStudentProfile.as_view(), name='admin_student_profile'),
    # teacher urls
    path('teacher_page/subject', TeacherIndex.as_view(), name='teacher_index'),
    path('teacher_page/course_detail/<int:course_id>', TeacherCourse.as_view(), name='teacher_course'),
    path('teacher_page/rating', TeacherRating.as_view(), name='teacher_rating'),
    path('teacher_page/profile', TeacherProfile.as_view(), name='teacher_profile'),
    path('teacher_page/students', TeacherStudents.as_view(), name='teacher_students'),
    path('teacher_page/student/<int:student_id>/profile/', TeacherStudentProfile.as_view(), name='teacher_student_profile'),
    path('teacher_page/course/<int:course_id>/lesson/<int:lesson_id>', TeacherLesson.as_view(), name='teacher_lesson'),
    path('teacher_page/unfollow/student/<int:curs_stud_id>', UnfollowStudent.as_view(), name='teacher_unfollow_stud'),
    # student urls
    path('student_page/learning_page', StudentIndex.as_view(), name='student_index'),
    path('student_page/rating', StudentRating.as_view(), name='student_rating'),
    path('student_page/subject', StudentSubject.as_view(), name='student_subject'),
    path('student_page/profile/', StudentProfile.as_view(), name='student_profile'),
    path('student_page/course/<int:course_id>/before', StudentCourseBefore.as_view(), name='student_course_before'),
    path('student_page/course/<int:course_id>/lesson/<int:lesson_id>', StudentCourseAfter.as_view(), name='student_course_after'),
    # language
    path('language/kz', LanguageKZ.as_view(), name='language_kz'),
    path('language/ru', LanguageRU.as_view(), name='language_ru'),
]

