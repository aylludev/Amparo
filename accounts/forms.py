from django import forms
from django.forms import ModelForm
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

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
        data = {}
        try:
            u = super(UserForm, self).save(commit=False)  # ✅ Correcto
            pwd = self.cleaned_data['password']

            # Si el usuario es nuevo, encripta la contraseña
            if u.pk is None:
                u.password = make_password(pwd)
            else:
                user = CustomUser.objects.get(pk=u.pk)
                if user.password != pwd:  # Si cambió la contraseña, la encripta
                    u.password = make_password(pwd)

            if commit:
                u.save()

            # Manejo de grupos si existen en el formulario
            if 'groups' in self.cleaned_data:
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)

            return u  # ✅ Devuelve el usuario creado/modificado

        except Exception as e:
            data['error'] = str(e)
            return data  # ✅ Devuelve error en caso de fallo

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
