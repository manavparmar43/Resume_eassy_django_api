from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username']
   


admin.site.register(User, MyUserAdmin)


admin.site.register(Role)
admin.site.register(NonBuiltInUserToken)


