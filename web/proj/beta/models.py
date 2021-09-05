from django.db import models

class Friendship(models.Model):
    id = models.AutoField(primary_key=True)
    side1 = models.IntegerField()
    side2 = models.IntegerField()
    accepted = models.BooleanField()

class Auth(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    passhash = models.CharField(max_length=20)    

# Create your models here.
