from django import forms
from .models import ModelFile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class ImageForm(forms.ModelForm):
   class Meta:
       model = ModelFile
       fields = ('image',)