from django.contrib.auth.models import AbstractUser
from django.db import models
from words.models import UsersWords

# Create your models here.
class Users(AbstractUser):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    words = models.ManyToManyField(UsersWords)

    def __repr__(self):
        return "User with name {}".format(self.username)