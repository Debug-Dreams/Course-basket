from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from home.models import Course

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

class Meta:
    model = User
    fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','rollno', 'sem', 'branch']

# class FilterBySem(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['sem']
    #     year = models.CharField(max_length=30, choices = YEAR_CHOICES)
    # branch = models.CharField(max_length=30, choices = BRANCH_CHOICES)