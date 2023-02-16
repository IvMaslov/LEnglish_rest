from django.db import models
from django.contrib.auth.models import AbstractUser
from words.models import UsersWords

class UsersUsers(AbstractUser):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

class UsersUsersWords(models.Model):
    users = models.ForeignKey(UsersUsers, models.DO_NOTHING)
    userswords = models.ForeignKey(UsersWords, on_delete=models.CASCADE)
