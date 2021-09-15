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

# ============================================
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

class FacultyT(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5)
    departments = models.IntegerField()


# Create your models here.
