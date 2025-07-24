from django.db import models
import math
from django.contrib.auth.models import User

class Conquista(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo

class Atleta(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    CATEGORIA_CHOICES = [
        ("mens_classic", "Masculino Clássico-RAW"),
        ("womens_classic", "Feminino Clássico-RAW"),
    ]

    PESO_CHOICES = [
        ('52', '52 kg'),
        ('57', '57 kg'),
        ('63', '63 kg'),
        ('69', '69 kg'),
        ('76', '76 kg'),
        ('84', '84 kg'),
        ('84+', '84+ kg'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()
    peso = models.CharField(max_length=10)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    total_kg = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    ipf_gl_points = models.FloatField(null=True, blank=True)  # será calculado e salvo
    foto = models.ImageField(upload_to='fotos_atletas/', null=True, blank=True)
    conquistas = models.ManyToManyField('Conquista', blank=True)
    conquista_destaque = models.ForeignKey(
        'Conquista',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='destaques')

    def __str__(self):
        nomes = self.nome.strip().split()
        if self.conquista_destaque:
            if len(nomes) >= 2:
                primeiro = nomes[0]
                ultimo = nomes[-1]
                return f"{primeiro} “{self.conquista_destaque.titulo}” {ultimo}"
            else:
                return f"{self.nome} “{self.conquista_destaque.titulo}”"
        return self.nome





GL_COEFFICIENTS = {
    "mens_equipped": (1236.25115, 1449.21864, 0.01644),
    "mens_classic": (1199.72839, 1025.18162, 0.00921),
    "mens_equipped_bench": (381.22073, 733.79378, 0.02398),
    "mens_classic_bench": (320.98041, 281.40258, 0.01008),
    "womens_equipped": (758.63878, 949.31382, 0.02435),
    "womens_classic": (610.32796, 1045.59282, 0.03048),
    "womens_equipped_bench": (221.82209, 357.00377, 0.02937),
    "womens_classic_bench": (142.40398, 442.52671, 0.04724),
}

def calculate_gl_points(bodyweight: float, result: float, category: str) -> float:
    if category not in GL_COEFFICIENTS:
        raise ValueError(f"Categoria '{category}' não reconhecida.")

    A, B, C = GL_COEFFICIENTS[category]
    denominator = A - B * math.exp(-C * bodyweight)
    points = (result * 100) / denominator
    return round(points, 2)