from django.contrib import admin
from app.models import Curs, UserProfile
# Register your models here.

class CursAdmin(admin.ModelAdmin):
    exclude = ('video', 'number_lessons', 'language',)

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'rating')

admin.site.register(Curs, CursAdmin)
admin.site.register(UserProfile, UserAdmin)