from ast import mod
from email import message
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    userType = models.CharField(max_length=30)
    

    def __str__(self):
        return f'{self.username} - {self.userType}'

class Source(models.Model):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    publicKey = models.CharField(max_length=1000, null=True)
    privateKey= models.CharField(max_length=2000, null=True)
    def __str__(self):
        return f'{self.username} - {self.name}'

class Editor(models.Model):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.username} - {self.name}'

class NewsTip(models.Model):
    source = models.CharField(max_length=30)
    editor = models.CharField(max_length=30)
    message = models.BinaryField(max_length=None)
    def __str__(self):
        return f'{self.source} - {self.editor}'
    

