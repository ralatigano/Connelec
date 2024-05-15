from django import forms
from .models import registro, User
import datetime

class RegistroForm(forms.ModelForm):
    usuario = forms.CharField(max_length=50)
    fecha = forms.DateField(initial=datetime.date.today)
    hora = forms.TimeField(initial=datetime.datetime.now().time())
    tipo = forms.IntegerField()
    
    class Meta:
        model = registro
        fields = ['usuario', 'fecha', 'hora', 'tipo']
        help_text = {k:"" for k in fields}

