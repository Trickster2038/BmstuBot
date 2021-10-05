from django.db import models
import os
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class PersonT(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)   
    department = models.IntegerField()
    course = models.IntegerField(default=1,\
        validators=[
            MaxValueValidator(6),
            MinValueValidator(1)
        ])
    bio = models.CharField(max_length=400) 
    is_filled = models.BooleanField()
    rating = models.IntegerField()
    accesss = models.IntegerField()

    username = models.CharField(max_length=20) 
    faculty = models.IntegerField()
    trusted = models.IntegerField()

    is_moderator = models.BooleanField()
    is_curator = models.BooleanField()
    def detail(self):
        trustmap = [_("not checked"), _("on check"), _("checked")]
        p = self
        p.trusted = _(trustmap[p.trusted])
        p.faculty = FacultiesT.objects.get(id=p.faculty).name
        p.department = p.faculty + str(p.department)
        return p
    def avatar_exist(self):
        p = self
        fl = (UserImage.objects.filter(user=p.id, folder="avatars")\
            .count() > 0)
        return fl
    def append_to_list(self, p_list):
        p = self
        p = p.detail()
        fl = p.avatar_exist() 
        p_list.append({"rowdata": p, 
                "avatar": fl, \
                "path_avatar": 'avatars/' + str(p.id) + '.jpg'})

class FriendsT(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    applied = models.BooleanField()

class FacultiesT(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5)
    departments = models.IntegerField()

class UserImage(models.Model):
    def photo_path(instance, filename):
        return instance.folder + "/" + str(instance.user) + ".jpg"
    user = models.IntegerField()
    image = models.ImageField(upload_to=photo_path)
    folder = models.CharField(max_length=10)
    def delete(self, *args, **kwargs):
       print("> gg")
       os.remove(os.path.join(settings.MEDIA_ROOT, self.folder + "/" + str(self.user) + ".jpg"))
       super(UserImage,self).delete(*args,**kwargs)

class Image(models.Model):
    image = models.ImageField(upload_to="default/")
    n1 = models.IntegerField()

# Create your models here.
