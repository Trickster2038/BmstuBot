from django.db import models

class Friendship(models.Model):
    id = models.AutoField(primary_key=True)
    side1 = models.IntegerField()
    side2 = models.IntegerField()
    accepted = models.BooleanField()

class People(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=20)

class Auth(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    passhash = models.CharField(max_length=20)   

# ============================================
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)   
    department = models.IntegerField()
    course = models.IntegerField()
    faculty = models.IntegerField()
    username = models.CharField(max_length=20) 
    is_moderator = models.BooleanField()
    is_curator = models.BooleanField()

# Create your models here.
