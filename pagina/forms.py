from django import forms
from .models import Atleta, Conquista
from django.contrib.admin.views.decorators import staff_member_required


class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'idade', 'peso', 'genero', 'total_kg', 'categoria', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome do atleta'}),
            'idade': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Idade'}),
            'genero': forms.Select(choices=Atleta.GENERO_CHOICES),
            'total_kg': forms.NumberInput(attrs={'min': 0, 'step': 0.1, 'placeholder': 'Total levantado (kg)'}),
            'categoria': forms.Select(choices=Atleta.CATEGORIA_CHOICES),
        }
class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['foto']


class ConquistaForm(forms.ModelForm):
    class Meta:
        model = Conquista
        fields = ['titulo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Juggernaut'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Ex: Atingiu 600kg de total', 'rows': 3}),
        }

class AtribuirConquistaForm(forms.Form):
    atleta = forms.ModelChoiceField(queryset=Atleta.objects.all(), label="Atleta")
    conquista = forms.ModelChoiceField(queryset=Conquista.objects.all(), label="Conquista")