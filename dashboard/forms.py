from dataclasses import field
from random import choice
from django import forms
from .models import Notes, Homework, Todo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Notes
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

# Custom DateInput for Homework form
class DateInput(forms.DateInput):
    input_type = 'date'

# Homework
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        widgets = {
            'due': DateInput(attrs={'class': 'form-control'}),
        }

# YouTube Search
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search:")

# Todo
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

# Measurement Type Selection
class MeasurementForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

# Length Conversion
class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': 'Enter the Number'
        })
    )
    measure1 = forms.ChoiceField(label='', choices=CHOICES)
    measure2 = forms.ChoiceField(label='', choices=CHOICES)

# Mass Conversion
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
    measure1 = forms.ChoiceField(label='', choices=CHOICES)
    measure2 = forms.ChoiceField(label='', choices=CHOICES)

# User Registration
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
