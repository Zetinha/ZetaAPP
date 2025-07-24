from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib import messages
from .forms import AtribuirConquistaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Atleta, calculate_gl_points, Conquista
from .forms import AtletaForm, FotoPerfilForm
from .forms import ConquistaForm
from .conquistas import CONQUISTAS_DISPONIVEIS



# Página de login com autenticação real
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if 'next' in request.GET:
        messages.info(request, "Você precisa estar logado para acessar essa página.")

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or 'ranking'
            return redirect(next_url)
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, 'pagina/login.html', {'form': form})


# Página de logout
def logout_view(request):
    logout(request)
    return redirect('ranking')


@login_required
def perfil_atleta(request, atleta_id):
    atleta = get_object_or_404(Atleta, id=atleta_id)

    if request.user != atleta.user and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar o perfil de outro atleta.")
        return redirect('ranking')

    # Atualização do destaque
    if request.method == 'POST':
        # Foto de perfil
        if 'foto' in request.FILES:
            form = FotoPerfilForm(request.POST, request.FILES, instance=atleta)
            if form.is_valid():
                form.save()
                messages.success(request, "Foto atualizada com sucesso.")
                return redirect('perfil_atleta', atleta_id=atleta.id)

        # Conquista destaque
        elif 'conquista_destaque' in request.POST:
            conquista_id = request.POST.get('conquista_destaque')
            if conquista_id:
                conquista = Conquista.objects.filter(id=conquista_id).first()
                if conquista and conquista in atleta.conquistas.all():
                    atleta.conquista_destaque = conquista
                else:
                    atleta.conquista_destaque = None
            else:
                atleta.conquista_destaque = None
            atleta.save()
            messages.success(request, "Conquista de destaque atualizada com sucesso.")
            return redirect('perfil_atleta', atleta_id=atleta.id)

    else:
        form = FotoPerfilForm(instance=atleta)

    return render(request, 'pagina/perfil_atleta.html', {
        'atleta': atleta,
        'form_foto': form
    })



# Cadastro de atleta
@login_required
def cadastrar_atleta(request):
    if request.method == 'POST':
        form = AtletaForm(request.POST)
        if form.is_valid():
            atleta = form.save(commit=False)

            username = atleta.nome.lower().replace(" ", "")  # ou outro identificador
            password = get_random_string(8)
            user = User.objects.create_user(username=username, password=password)
            atleta.user = user    

            atleta.ipf_gl_points = calculate_gl_points(
                bodyweight=float(atleta.peso),
                result=float(atleta.total_kg),
                category=atleta.categoria
            )
            atleta.save()

            messages.success(request, f"Usuário criado: {username} | Senha: {password}")

            return redirect('ranking')
    else:
        form = AtletaForm()
    return render(request, 'pagina/formulario.html', {'form': form})



# Editar atleta
@login_required
def editar_atleta(request, atleta_id):
    atleta = get_object_or_404(Atleta, id=atleta_id)

    if request.user != atleta.user and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para editar esse perfil.")
        return redirect('ranking')

    if request.method == 'POST':
        form = AtletaForm(request.POST, instance=atleta)
        if form.is_valid():
            atleta = form.save(commit=False)
            atleta.ipf_gl_points = calculate_gl_points(
                bodyweight=float(atleta.peso),
                result=float(atleta.total_kg),
                category=atleta.categoria
            )
            atleta.save()
            return redirect('ranking')
    else:
        form = AtletaForm(instance=atleta)

    return render(request, 'pagina/formulario.html', {'form': form, 'edicao': True})


# Ranking de atletas
def ranking(request):
    ranking_masculino = Atleta.objects.filter(genero='M').order_by('-ipf_gl_points')[:5]
    ranking_feminino = Atleta.objects.filter(genero='F').order_by('-ipf_gl_points')[:5]

    context = {
        'ranking_masculino': ranking_masculino,
        'ranking_feminino': ranking_feminino,
    }
    return render(request, 'pagina/ranking.html', context)


@login_required
def listar_atletas(request):
    atletas = Atleta.objects.all()
    return render(request, 'pagina/listar_atletas.html', {'atletas': atletas})


@login_required
def editar_atleta_redirect(request):
    atleta_id = request.GET.get('atleta_id')
    if atleta_id:
        return redirect('editar_atleta', atleta_id=atleta_id)
    return redirect('listar_atletas')

@staff_member_required
def nova_conquista(request):
    if request.method == 'POST':
        form = ConquistaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conquista cadastrada com sucesso.")
            return redirect('nova_conquista')
    else:
        form = ConquistaForm()
    return render(request, 'pagina/nova_conquista.html', {'form': form})

@staff_member_required
def atribuir_conquistas(request):
    atletas = Atleta.objects.all()
    conquistas = Conquista.objects.all()
    conquistas_disponiveis = CONQUISTAS_DISPONIVEIS

    if request.method == 'POST':
        for atleta in atletas:
            conquistas_ids = request.POST.getlist(f'atleta_{atleta.id}')
            atleta.conquistas.set(conquistas_ids)
        return redirect('atribuir_conquistas')

    return render(request, 'pagina/atribuir_conquistas.html', {
        'atletas': atletas,
        'conquistas': conquistas,
        'conquistas_disponiveis': conquistas_disponiveis,
    })

def lista_conquistas(request):
    conquistas = CONQUISTAS_DISPONIVEIS
    return render(request, 'pagina/lista_conquistas.html', {'conquistas': conquistas})

@staff_member_required
def atribuir_conquista_individual(request):
    if request.method == 'POST':
        form = AtribuirConquistaForm(request.POST)
        if form.is_valid():
            atleta = form.cleaned_data['atleta']
            conquista = form.cleaned_data['conquista']
            atleta.conquistas.add(conquista)
            messages.success(request, f"Conquista '{conquista}' atribuída a {atleta.nome}.")
            return redirect('atribuir_conquista_individual')
    else:
        form = AtribuirConquistaForm()

    return render(request, 'pagina/atribuir_conquista_individual.html', {'form': form})