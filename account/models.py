from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    Gender = (
        ('Male','Male'),
        ('Female', 'Female')
    )
    username = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=Gender)
    position = models.CharField(max_length=40, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.CharField(max_length=250, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'gender', 'position', 'bio']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# class Follower(models.Model):
#     name = models.ManyToManyField()