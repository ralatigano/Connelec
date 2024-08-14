from django import forms
# cambio esto para probar un modelo de usuario con una relación OneToOneField con User
from .models import registro  # , User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import datetime


class RegistroForm(forms.ModelForm):
    usuario = forms.CharField(max_length=50)
    fecha = forms.DateField(initial=datetime.date.today)
    hora = forms.TimeField(initial=datetime.datetime.now().time())
    tipo = forms.IntegerField()

    class Meta:
        model = registro
        fields = ['usuario', 'fecha', 'hora', 'tipo']
        help_text = {k: "" for k in fields}


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
