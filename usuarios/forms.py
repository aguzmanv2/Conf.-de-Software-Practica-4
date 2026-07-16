from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistroForm(forms.Form):
    nombres = forms.CharField(max_length=150, label="Nombres")
    apellidos = forms.CharField(max_length=150, label="Apellidos")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar contraseña"
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")
        if password and confirmar and password != confirmar:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self):
        from django.contrib.auth.models import Group

        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data["email"],
            email=cleaned_data["email"],
            password=cleaned_data["password"],
            first_name=cleaned_data["nombres"],
            last_name=cleaned_data["apellidos"],
        )
        grupo_usuario, _ = Group.objects.get_or_create(name="Usuario")
        user.groups.add(grupo_usuario)
        return user


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Email",
        }


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "is_active"]
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Email",
            "is_active": "Activo",
        }
