from .models import Atleta

def atletas_list(request):
    if request.user.is_authenticated:
        atletas = Atleta.objects.all()
    else:
        atletas = []
    return {'atletas_menu': atletas}
