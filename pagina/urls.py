from django.urls import path
from . import views

urlpatterns = [
    path('', views.ranking, name='ranking'),  # Página inicial agora mostra só os scoreboards
    path('cadastrar/', views.cadastrar_atleta, name='cadastrar'),
]
