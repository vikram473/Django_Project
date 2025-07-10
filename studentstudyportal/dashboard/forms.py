from dataclasses import field
from random import choice
from tkinter.tix import Select
from tkinter.ttk import Widget
from django import forms
from .models import *
from .models import Homework
from .models import Todo
from django.contrib.auth.forms import UserCreationForm

# notes 
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'

# Homework
class HomeworkForm(forms.ModelForm):
    input_type = 'date'
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_finished' ] 
        widgets = {
            'due': forms.DateInput(
                attrs={
                    'type': 'date',  # Only date picker
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            )
        }
    
# youtube
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Searh :")
    
       
# todo      
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

# conversion 
class ConversionForm(forms.Form):
    CHOICES = [('length','Lenght'), ('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES,widget = forms.RadioSelect)
   
# conversion length 
class ConversionForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': 'Enter the Number'
        })
    )
    measure1 = forms.ChoiceField(
        label='',
        choices=CHOICES,
        widget=forms.Select()
    )
    measure2 = forms.ChoiceField(
        label='',
        choices=CHOICES,
        widget=forms.Select()
    )

# Mass Conversion Form
class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': 'Enter the Number'
        })
    )
    measure1 = forms.ChoiceField(
        label='',
        choices=CHOICES,
        widget=forms.Select()
    )
    measure2 = forms.ChoiceField(
        label='',
        choices=CHOICES,
        widget=forms.Select()
    )

# registration form
class UserRegistrationForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username','password1','password2']


