from django import forms
from django.forms import ModelForm
from catalogs.models import Crop, AgricultureActivity, Variety

class CropForm(ModelForm):

    class Meta:
        model = Crop
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
        }

class VarietyForm(ModelForm):

    class Meta:
        model = Variety
        fields = ['crop','name']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
        }
