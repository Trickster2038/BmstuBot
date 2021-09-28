from django.db import models

class PersonT(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)   
    department = models.IntegerField()
    course = models.IntegerField()
    bio = models.CharField(max_length=400) 
    is_filled = models.BooleanField()
    rating = models.IntegerField()
    accesss = models.IntegerField()

    username = models.CharField(max_length=20) 
    faculty = models.IntegerField()
    trusted = models.IntegerField()

    is_moderator = models.BooleanField()
    is_curator = models.BooleanField()

class FriendsT(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    applied = models.BooleanField()

class FacultiesT(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5)
    departments = models.IntegerField()


# Create your models here.
