from django import forms
from django.forms import ModelForm
from erp.models import Farm 

class FarmForm(ModelForm):

    class Meta:
        model = Farm
        fields = ['name', 'department', 'municipality', 'address', 'area']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'department': forms.Select(attrs={'id': 'department-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'municipality': forms.Select(attrs={'id': 'municipality-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'address': forms.TextInput(attrs={'class': 'form-control',}),
            'area': forms.NumberInput(attrs={'class': 'form-control',}),
        }
