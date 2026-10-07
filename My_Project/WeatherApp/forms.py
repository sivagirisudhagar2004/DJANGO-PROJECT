from django.forms import ModelForm,TextInput
from .models import *
from django import forms


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name':forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':" Enter city name",'autocomplete':'off'})}