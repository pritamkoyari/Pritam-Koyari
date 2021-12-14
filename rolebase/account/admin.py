from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'dept', 'year', 'semester',
                    'enrollment', 'profilepic',
                    'is_cdc', 'is_teacher', 'is_student', 'status']




@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'headlines', 'details','img',
                    'dept', 'owner', 'status', 'postedtime']



