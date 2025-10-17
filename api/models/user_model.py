from django.db import models
from .enum import roles_choice

# Create your models here. 

class User(models.Model):
    email = models.EmailField(unique=True, max_length=255, blank=False)
    username = models.CharField(unique=True, max_length=50,blank=False)
    password = models.CharField(max_length=255,blank=False)
    name = models.CharField(max_length=50,blank=False)
    role = models.IntegerField(choices = roles_choice.choices, default = roles_choice.GUEST)

