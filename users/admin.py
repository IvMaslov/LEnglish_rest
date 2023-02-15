from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsersUsers

# Register your models here.
admin.site.register(UsersUsers, UserAdmin)