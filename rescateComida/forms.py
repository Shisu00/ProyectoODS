from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Producto, Categoria
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Usuario
import re


from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña',
        help_text='Mínimo 8 caracteres, debe incluir al menos una mayúscula y un carácter especial'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar contraseña'
    )
    
    tipo_usuario = forms.ChoiceField(
        choices=Usuario.TIPO_USUARIO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select', 
        }),
        label='Tipo de Usuario'
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'comuna']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección (opcional)'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comuna (opcional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].widget = forms.HiddenInput()
            self.fields['password_confirm'].widget = forms.HiddenInput()
            del self.fields['password']
            del self.fields['password_confirm']
        
        if not self.instance:
            self.fields['tipo_usuario'].initial = 'cliente'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance:
            if Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Este nombre de usuario ya está en uso')
        else:
            if Usuario.objects.filter(username=username).exists():
                raise forms.ValidationError('Este nombre de usuario ya está en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance:
            if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado')
        else:
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        password = self.cleaned_data.get('password')
        if password:
            usuario.set_password(password)
        usuario.tipo_usuario = self.cleaned_data['tipo_usuario']
        
        if commit:
            usuario.save()
        return usuario

class RegistroFormCliente(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña',
        help_text='Mínimo 8 caracteres, debe incluir al menos una mayúscula y un carácter especial'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar contraseña'
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'comuna']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección (opcional)'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comuna (opcional)'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('El nombre de usuario solo puede contener letras y números, sin caracteres especiales.')
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial.')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email  

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            if not re.match(r'^\+569\d{8}$', telefono):
                raise ValidationError('El teléfono debe comenzar con +569 seguido de 8 dígitos.')
        return telefono

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z]+$', first_name):
            raise ValidationError('El nombre solo debe contener letras.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z]+$', last_name):
            raise ValidationError('El apellido solo debe contener letras.')
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            usuario.set_password(password)
        usuario.tipo_usuario = 'cliente' 
        if commit:
            usuario.save()
        return usuario

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o Correo',
            'autofocus': True
        }),
        label='Usuario o Correo'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'unidad_medida', 'fecha_vencimiento', 'id_categoria', 'estado', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad'
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'id_categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
