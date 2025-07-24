from django.urls import path
from django.shortcuts import redirect
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import listar_atletas, editar_atleta_redirect, logout_view
from pagina.views import login_view


urlpatterns = [
    path('', lambda request: redirect('ranking', permanent=False)),  # página inicial
    path('cadastrar/', views.cadastrar_atleta, name='cadastrar'),
    path('ranking/', views.ranking, name='ranking'),

    # Perfil individual do atleta
    path('atleta/<int:atleta_id>/', views.perfil_atleta, name='perfil_atleta'),

    # Edição/listagem
    path('alterar/', listar_atletas, name='listar_atletas'),
    path('editar/<int:atleta_id>/', views.editar_atleta, name='editar_atleta'),
    path('editar-atleta/', editar_atleta_redirect, name='editar_atleta_redirect'),

    # Login/logout
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #admin
    path('atribuir_conquista/', views.atribuir_conquista_individual, name='atribuir_conquista_individual'),
    path('conquistas/', views.lista_conquistas, name='lista_conquistas'),


]