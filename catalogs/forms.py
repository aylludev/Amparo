from django import forms
from django.forms import ModelForm
from catalogs.models import CatalogCrop, CatalogAgricultureActivity, CatalogVariety, CatalogAnimal, CatalogRace, CatalogAnimalActivity

class CropForm(ModelForm):

    class Meta:
        model = CatalogCrop
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
        }

class VarietyForm(ModelForm):

    class Meta:
        model = CatalogVariety
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
        }

class ActivityForm(ModelForm):

    class Meta:
        model = CatalogAgricultureActivity
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese una Actividad'}),
        }

class AnimalForm(ModelForm):

    class Meta:
        model = CatalogAnimal
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
        }

class RaceForm(ModelForm):

    class Meta:
        model = CatalogRace
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese una raza'}),
        }

class ActivityAForm(ModelForm):

    class Meta:
        model = CatalogAnimalActivity
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese una Actividad'}),
        }
