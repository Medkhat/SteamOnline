from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Логин или email'})
    password.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите пароль'})

class AddCourseName(forms.Form):
    title = forms.CharField(max_length=100)

    title.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите название курса', 'id': 'courseTitleInput'})

class AddCourseImage(forms.Form):
    image = forms.ImageField(label='')
    
    image.widget.attrs.update({'id': 'img_upload'})

class AddCourseVideo(forms.Form):
    video = forms.FileField(label='')
    
    video.widget.attrs.update({'id': 'uploadVideo'})

class AddLessonText(forms.Form):
    text = forms.CharField(widget=SummernoteWidget(attrs={'summernote': 
    {
        'width': '100%',
        'followingToolbar': True,
    }}))

class AddLessonTextTeacher(forms.Form):
    text1 = forms.CharField(widget=SummernoteWidget(attrs={'summernote': 
    {
        'width': '100%',
        'followingToolbar': True,
    }}))

class AddLessonHint(forms.Form):
    text_hint = forms.CharField(widget=SummernoteWidget(attrs={'summernote': 
    {
        'height': '200', 
        'width': '100%',
        'toolbar': [['insert', ['link', 'hr']]],
        'followingToolbar': True,
        'codemirror': { 
            'theme': 'monokai'
        }
    }}))


class AddLessonVideo(forms.Form):
    video = forms.FileField(label='')
    
    video.widget.attrs.update({'id': 'uplVideoForLess'})

class AddLessonTest(forms.Form):
    Options = [
        ('', 'Выберите правильный вариант'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
      ]

    name_test = forms.CharField(max_length=100)
    ask_test = forms.CharField(max_length=300)
    answer_1 = forms.CharField(max_length=300)
    answer_2 = forms.CharField(max_length=300)
    answer_3 = forms.CharField(max_length=300)
    answer_4 = forms.CharField(max_length=300)
    answer_5 = forms.CharField(max_length=300)
    correct_answer = forms.ChoiceField(widget=forms.Select, choices=Options)

    name_test.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите название курса'})
    ask_test.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите вопрос теста'})
    answer_1.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите первый вариант'})
    answer_2.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите второй вариант'})
    answer_3.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите третий вариант'})
    answer_4.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите четвертый вариант'})
    answer_5.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите пятый вариант'})
    correct_answer.widget.attrs.update({'class': 'testSelect', 'placeholder': 'Введите название курса'})

class AddTeacher(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    patronymic = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    iin = forms.IntegerField(required=False)
    school = forms.CharField(max_length=50)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)


    first_name.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Имя'})
    last_name.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Фамилия'})
    patronymic.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Отчество'})
    school.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите школу'})
    username.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Придумайте логин'})
    password.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Придумайте пароль'})
    password1.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Повторите пароль'})
    email.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Почта'})
    iin.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'ИИН'})


class AddAvatar(forms.Form):
    image = forms.ImageField(label='')
    
    image.widget.attrs.update({'id': 'img_upload'})

class EditProfile(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    patronymic = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    iin = forms.IntegerField(required=False)
    school = forms.CharField(max_length=50)


    first_name.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Имя'})
    last_name.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Фамилия'})
    patronymic.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Отчество'})
    school.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Школу'})
    username.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Логин'})
    email.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Почта'})
    iin.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'ИИН'})

class EditPassword(forms.Form):
    # password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)

    # password.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Введите пароль', 'id': 'resPass1'})
    password1.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Придумайте пароль', 'id': 'resPass2'})
    password2.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Повторите пароль', 'id': 'resPass2'})



class EditProfile1(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    patronymic = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    school = forms.CharField(max_length=50)


    first_name.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Имя'})
    last_name.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Фамилия'})
    patronymic.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Отчество'})
    school.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Школу'})
    email.widget.attrs.update({'class': 'res_pass_input', 'placeholder': 'Почта'})

