from django import forms
from .models import Image, PersonT
from django.utils.translation import gettext_lazy as _

COURSE_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),\
('4', '4'), ('5', '5'), ('6', '6')]

class EditForm(forms.Form):
    COURSE_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),\
    ('4', '4'), ('5', '5'), ('6', '6')]
    bio = forms.CharField(label=_("Bio"))
    course = forms.ChoiceField(choices=COURSE_CHOICES, label=_("Course"))
    # curator = forms.BooleanField(required=False, label=_("TXT.Curator_mode"))

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)