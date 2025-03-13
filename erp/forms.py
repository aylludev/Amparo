from django import forms
from django.forms import ModelForm
from erp.models import Animal, Crop, Farm, Activity, Worker

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

class CropForm(ModelForm):

    class Meta:
        model = Crop
        fields = ['name', 'variety', 'type', 'status', 'area', 'planting_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'variety': forms.TextInput(attrs={'id': 'department-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'type': forms.Select(attrs={'class': 'select2 form-control', 'style': 'width: 100%'}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'area': forms.NumberInput(attrs={'class': 'form-control',}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control',}),
        }

class AnimalForm(ModelForm):

    class Meta:
        model = Animal
        fields = ['name', 'raza', 'type', 'status', 'age', 'birthday_date', 'observations']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'raza': forms.TextInput(attrs={'id': 'department-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'type': forms.Select(attrs={'class': 'select2 form-control', 'style': 'width: 100%'}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'age': forms.NumberInput(attrs={'class': 'form-control',}),
            'birthday_date': forms.DateInput(attrs={'class': 'form-control',}),
            'observations': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
        }

class WorkerForm(ModelForm):

    class Meta:
        model = Worker
        fields = ['name', 'phone', 'salary', 'hired_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'hired_date': forms.DateInput(attrs={'class': 'form-control',}),
        }

class ActivityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Activity
        fields = 'name', 'description', 'type', 'date', 'status', 'workers'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Actividades', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Descripcion de la actividad', 'class':'form-control'}),
            'type': forms.TextInput(attrs={'placeholder': 'Ej: Siembra, Retape, Fumigacion...','class':'form-control',}),
            'date': forms.DateInput(attrs={'class':'form-control',}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'workers': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }
