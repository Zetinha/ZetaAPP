from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Atleta, calculate_gl_points
from .forms import AtletaForm

# Página de cadastro
@login_required
def cadastrar_atleta(request):
    if request.method == 'POST':
        form = AtletaForm(request.POST)
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
            # Form inválido: renderiza com erros
            return render(request, 'pagina/formulario.html', {'form': form})
    else:
        form = AtletaForm()
    return render(request, 'pagina/formulario.html', {'form': form})


# Página de ranking
def ranking(request):
    ranking_masculino = Atleta.objects.filter(genero='M').order_by('-ipf_gl_points')[:5]
    ranking_feminino = Atleta.objects.filter(genero='F').order_by('-ipf_gl_points')[:5]

    context = {
        'ranking_masculino': ranking_masculino,
        'ranking_feminino': ranking_feminino,
    }
    return render(request, 'pagina/ranking.html', context)


