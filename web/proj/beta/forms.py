from django import forms
from .models import Image
from django.utils.translation import gettext_lazy as _

COURSE_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),\
('4', '4'), ('5', '5'), ('6', '6')]

class NameForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=100)
    surname = forms.CharField(label=_('Surname'), max_length=100)
    course = forms.ChoiceField(label=_('Course'), widget=forms.RadioSelect, choices=COURSE_CHOICES)

# class ImageForm(forms.Form):
#     image = forms.ImageField(label=_('Image'))

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')