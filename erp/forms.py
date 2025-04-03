from datetime import datetime
from django import forms
from django.forms import ModelForm
from erp.models import ActivityAnimal, Animal, Crop, Equipment, Farm, Activity, Suply, Worker, Category, Cotization, CreditPayment, Product, Client, Sale

class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = ['name', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre',}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese un nombre', 'rows': 3, 'cols': 3 }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = ['name', 'cat', 'stock', 'purchase', 'pvp']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre',}),
            'cat': forms.Select(attrs={'class': 'select2', 'style': 'width: 100%'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres',}),
            'surnames': forms.TextInput(attrs={'placeholder': 'Ingrese sus apellidos',}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese su dni',}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su email',}),
            'date_birthday': forms.DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'autocomplete': 'off', 'class': 'form-control datetimepicker-input datetimepiker4', 'id': 'date_joined', 'data-target': '#date_joined', 'data-toggle': 'datetimepicker' }),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese su dirección', }),
            'gender': forms.Select(),
            'observation': forms.Textarea(attrs={'placeholder': 'Observaciones',}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class TestForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={'class': 'custom-select select2',}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'autocomplete': 'off', 'class': 'form-control datetimepicker-input', 'id': 'date_joined', 'data-target': '#date_joined', 'data-toggle': 'datetimepicker' }),
            'iva': forms.TextInput(attrs={'class': 'form-control', }),
            'subtotal': forms.TextInput(attrs={'readonly': True, 'class': 'form-control', }),
            'discountall': forms.TextInput(attrs={ 'class': 'form-control', }),
            'total': forms.TextInput(attrs={'readonly': True, 'class': 'form-control', }),
            'type_payment': forms.Select(attrs={'class': 'form-control', }),
            'down_payment': forms.TextInput(attrs={'value': 0.00, 'class': 'form-control', }),
            'observation' : forms.TextInput(attrs={'class': 'form-control'}),
        }
class CreditPaymentForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = CreditPayment
        fields = ['date','amount']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d',attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'autocomplete': 'off', 'class': 'form-control datetimepicker-input', 'id': 'date_joined', 'data-target': '#date_joined', 'data-toggle': 'datetimepicker' }),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class CotizationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()

    class Meta:
        model = Cotization
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'discountall': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'type_payment': forms.Select(attrs={
                'class': 'form-control',
            }),
            'biweekly_pay': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class FarmForm(ModelForm):

    class Meta:
        model = Farm
        fields = ['name', 'department', 'municipality', 'address', 'area']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'department': forms.Select(attrs={'id': 'department-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'municipality': forms.Select(attrs={'id': 'municipality-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'address': forms.TextInput(attrs={'class': 'form-control',}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min':'0.1'}),
        }

class CropForm(ModelForm):

    class Meta:
        model = Crop
        fields = ['name', 'variety', 'status', 'area', 'planting_date']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'variety': forms.Select(attrs={'id': 'department-select', 'class': 'select2 form-control', 'style': 'width: 100%'}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min':'0.1'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control',}),
        }

class AnimalForm(ModelForm):

    class Meta:
        model = Animal
        fields = ['name', 'raza', 'type', 'birthday_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'type': forms.Select(attrs={'class': 'select2 form-control', 'style': 'width: 100%'}),
            'raza': forms.Select(attrs={'class': 'select2 form-control', 'style': 'width: 100%'}),
            'birthday_date': forms.DateInput(attrs={'class': 'form-control',}),
        }

class WorkerForm(ModelForm):

    class Meta:
        model = Worker
        fields = ['name', 'phone', 'salary', 'hired_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'min':'0.1'}),
            'hired_date': forms.DateInput(attrs={'class': 'form-control',}),
        }

class ActivityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extraer 'user' antes de llamar a super()
        super(ActivityForm, self).__init__(*args, **kwargs)  # Llamar al constructor sin 'user'

        if user:
            # Filtrar insumos y trabajadores por usuario autenticado
            self.fields['suplies'].queryset = Suply.objects.filter(user=user)
            self.fields['workers'].queryset = Worker.objects.filter(user=user)

    class Meta:
        model = Activity
        fields = 'name', 'description', 'date', 'status', 'workers', 'cash'
        widgets = {
            'name': forms.Select(attrs={'placeholder': 'Actividades', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Descripcion de la actividad', 'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control',}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'workers': forms.SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'multiple': 'multiple' }),
            'cash': forms.NumberInput(attrs={'class': 'form-control', 'min':'0.1'})
        }

class ActivityAnimalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ActivityAnimal
        fields = 'name', 'description', 'date', 'status', 'workers', 'suplies', 'cash'
        widgets = {
            'name': forms.Select(attrs={'placeholder': 'Actividades', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Descripcion de la actividad', 'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control',}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'workers': forms.SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'multiple': 'multiple' }),
            'suplies': forms.SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'multiple': 'multiple' }),
            'cash': forms.NumberInput(attrs={'class': 'form-control', 'min':'0.1'})
        }

class SuplyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Suply
        fields = ['name', 'cat', 'stock', 'purchase']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre',}),
            'cat': forms.Select(attrs={'class': 'select2', 'style': 'width: 100%'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class EquipmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Equipment
        fields = ['name', 'desc', 'status', 'purchase', 'costph']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre', 'class':'form-control'}),
            'desc': forms.TextInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'purchase': forms.NumberInput(attrs={'class':'form-control', 'min':'0.1'}),
            'costph': forms.NumberInput(attrs={'class':'form-control', 'min':'0.1'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
