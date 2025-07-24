from django.core.management.base import BaseCommand
from pagina.models import Conquista
from pagina.conquistas import CONQUISTAS_DISPONIVEIS  # <- seu arquivo externo

class Command(BaseCommand):
    help = "Carrega conquistas pré-definidas no banco de dados"

    def handle(self, *args, **kwargs):
        for c in CONQUISTAS_DISPONIVEIS:
            obj, created = Conquista.objects.get_or_create(
                titulo=c['titulo'],
                defaults={'descricao': c['descricao']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Conquista '{obj.titulo}' criada"))
            else:
                self.stdout.write(self.style.WARNING(f"Conquista '{obj.titulo}' já existe"))
