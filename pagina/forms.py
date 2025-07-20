from django import forms
from .models import Atleta

class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'idade', 'peso', 'genero', 'total_kg', 'categoria']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome do atleta'}),
            'idade': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Idade'}),
            'peso': forms.NumberInput(attrs={'min': 0, 'step': 0.1, 'placeholder': 'Peso corporal (kg)'}),
            'genero': forms.Select(choices=Atleta.GENERO_CHOICES),
            'total_kg': forms.NumberInput(attrs={'min': 0, 'step': 0.1, 'placeholder': 'Total levantado (kg)'}),
            'categoria': forms.Select(choices=Atleta.CATEGORIA_CHOICES),
        }
