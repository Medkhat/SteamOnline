from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class UserProfile(AbstractUser):
    STATUS_ADMIN = 0
    STATUS_TEACHER = 1
    STATUS_STUDENT = 2

    STATUS_CHOICES = (
        (STATUS_ADMIN, _('admin')),
        (STATUS_TEACHER, _('teacher')),
        (STATUS_STUDENT, _('student')),
    )

    patronymic = models.CharField(max_length=30)
    iin = models.BigIntegerField(null=True)
    phone = models.BigIntegerField(null=True)
    school = models.CharField(max_length=250)
    rating = models.IntegerField(null=True)
    points = models.SmallIntegerField(default=0, null=True)
    avatar = models.ImageField(upload_to='image/avatar/', default='image/avatar/default.png', null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, null=True)
    major = models.CharField(max_length=60, null=True)
    teacher = models.IntegerField(null=True)
    language = models.CharField(null=True, max_length=2)
    layer = models.SmallIntegerField(null=True, default=0)

    def __str__(self):
        return self.first_name

    def admin_teacher_profile(self):
        return reverse('admin_profile', kwargs={'teacher_id': self.id})

    def teacher_student_profile(self):
        return reverse('teacher_student_profile', kwargs={'student_id': self.id})
    
    def admin_student_profile(self):
        return reverse('admin_student_profile', kwargs={'student_id': self.id})

    def user_delete(self):
        return reverse('admin_delete_user', kwargs={'user_id': self.id})



class Curs(models.Model):
    title = models.CharField(blank=True, max_length=100)
    video = models.FileField(upload_to='videos/curs/', default='default.mp4', null=True)
    image = models.ImageField(upload_to='image/curs/' ,default='image/curs/default.png', null=True)
    number_lessons = models.SmallIntegerField(blank=True, null=True)
    image_video = models.ImageField(upload_to='image/curs_video/', null=True)
    language = models.CharField(null=True, max_length=2)
    type_curs = models.SmallIntegerField(null=True, default=5)


    def course_detail(self):
        return reverse('admin_add_course', kwargs={'course_id': self.id})
    
    def course_detail_teacher(self):
        return reverse('teacher_course', kwargs={'course_id': self.id})

    def course_before_student(self):
        return reverse('student_course_before', kwargs={'course_id': self.id})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курс'

    

    

class Lessons(models.Model):
    lesson_id = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=120, null=True)
    text = models.TextField(null=True)
    text_teacher = models.TextField(null=True)
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE)

    def lesson_detail(self):
        return reverse('admin_add_lesson', kwargs={'course_id': self.curs.id, 'lesson_id': self.id})

    def lesson_delete(self):
        return reverse('admin_delete_lesson', kwargs={'lesson_id': self.id})

    def course_after_student(self):
        return reverse('student_course_after', kwargs={'course_id': self.curs.id, 'lesson_id': self.id})

    def teacher_lesson(self):
        return reverse('teacher_lesson', kwargs={'course_id': self.curs.id, 'lesson_id': self.id})


class Hint(models.Model):
    text = models.TextField()
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)

    def hint_delete(self):
        return reverse('admin_delete_hint', kwargs={'hint_id': self.id})

class Test(models.Model):
    ANSWER_1 = 1
    ANSWER_2 = 2
    ANSWER_3 = 3
    ANSWER_4 = 4
    ANSWER_5 = 5

    ANSWER_CHOICES = (
        (ANSWER_1, _('1-ші жауап дұрыс')),
        (ANSWER_2, _('2-ші жауап дұрыс')),
        (ANSWER_3, _('3-ші жауап дұрыс')),
        (ANSWER_4, _('4-ші жауап дұрыс')),
        (ANSWER_5, _('5-ші жауап дұрыс')),
    )

    name = models.CharField(max_length=300, blank=True)
    ask = models.TextField()
    answer1 = models.CharField(max_length=550)
    answer2 = models.CharField(max_length=550)
    answer3 = models.CharField(max_length=550)
    answer4 = models.CharField(max_length=550)
    answer5 = models.CharField(max_length=550)
    correct_answer = models.SmallIntegerField(choices=ANSWER_CHOICES)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)

    def test_delete(self):
        return reverse('admin_delete_test', kwargs={'test_id': self.id})

class Video_lessons(models.Model):
    title = models.CharField(max_length=120, null=True)
    video = models.FileField(upload_to='videos/lessons', default='default.mp4', null=True)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    image_video = models.ImageField(upload_to='image/lesson_video/', null=True)

    def video_delete(self):
        return reverse('admin_delete_video', kwargs={'video_id': self.id})

class Curs_Students(models.Model):
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    number_lesson = models.SmallIntegerField(blank=True)
    teacher = models.SmallIntegerField(null=True)
    test_status = models.SmallIntegerField(null=True)
    block = models.SmallIntegerField(null=True)

    def course_after_student(self):
        lessons = Lessons.objects.filter(curs__id=self.curs.id).order_by('lesson_id')
        if len(lessons) == 0:
            return reverse('student_course_before', kwargs={'course_id': self.curs.id})
        if self.number_lesson-1<len(lessons):
            a = lessons[self.number_lesson-1].id
        else:
            a = lessons[len(lessons)-1].id
        return reverse('student_course_after', kwargs={'course_id': self.curs.id, 'lesson_id': a})
    
    
    def unfollow_stud(self):
        return reverse('teacher_unfollow_stud', kwargs={'curs_stud_id': self.id})

class Test_Student(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE)
    name_test = models.CharField(max_length=100)
    points = models.SmallIntegerField()
    all_points = models.SmallIntegerField()
    lesson = models.SmallIntegerField()
    status = models.SmallIntegerField(default=0)

class TeacherCourses(models.Model):
    teacher_id = models.SmallIntegerField(null=True)
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE)

class CourseData(models.Model):
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE)
    developer = models.CharField(null=True, max_length=600)
    duration = models.CharField(null=True, max_length=100)
    certificate = models.CharField(null=True, max_length=100)
    time = models.CharField(null=True, max_length=100)


class Sertificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    point =  models.SmallIntegerField()
    curs = models.CharField(max_length=200)
    image = models.ImageField(upload_to='image/sertificate/' ,default='image/sertificate/default.png', null=True)