from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class EditProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ('user', 'location')

class BusinessForm(forms.ModelForm):
  class Meta:
    model = Business
    exclude = ('owner', 'hood')

class HoodForm(forms.ModelForm):
    class Meta:
        model = Hood
        exclude = ('admin',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'hood')