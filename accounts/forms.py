from django import forms
from django.forms import ModelForm
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = CustomUser
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'phone'
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Ingrese sus nombres',}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Ingrese sus apellidos',}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': 'Ingrese su email',}
            ),
            'username': forms.TextInput(
                attrs={'placeholder': 'Ingrese su username',}
            ),
            'password': forms.PasswordInput(
                render_value=True,
                attrs={'placeholder': 'Ingrese una contraseña',}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Ingrese numero de telefono',}
            ),
        }

        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Correo elctrónico',
            'username':'Nombre de Usuario',
            'password':'Contraseña',
            'phone':'Telefono',

        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data['password']

        # 🔹 Encripta la contraseña si el usuario es nuevo
        if user.pk is None:
            user.password = make_password(pwd)

        if commit:
            user.save()

            # 🔹 Asignar el grupo por defecto después de guardar
            vendor_group, created = Group.objects.get_or_create(name="vendor")
            user.groups.add(vendor_group)  

        return user
    

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = CustomUser
        fields = 'first_name', 'last_name', 'email', 'username', 'password'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                                            attrs={
                                                'placeholder': 'Ingrese su password',
                                            }
                                            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = CustomUser.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
