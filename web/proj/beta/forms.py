from django import forms

COURSE_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),\
('4', '4'), ('5', '5'), ('6', '6')]

class NameForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    surname = forms.CharField(label='Surname', max_length=100)
    course = forms.ChoiceField(widget=forms.RadioSelect, choices=COURSE_CHOICES)