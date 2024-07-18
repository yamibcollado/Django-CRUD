from django import forms
from .models import Tarea

class tareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion','importancia']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
            'importancia': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto' }),
        }