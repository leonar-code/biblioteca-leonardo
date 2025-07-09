from django.core.management.base import BaseCommand
from libros.models import Libro, Genero
from django.db.models import Avg
import argparse

class Command(BaseCommand):
    help = 'Muestra los libros mejor valorados de un género específico (por nombre).'

    def add_arguments(self, parser):
        parser.add_argument('genero', type=str, help='Nombre del género (por ejemplo: Fantasía)')
        parser.add_argument('--top', type=int, default=10, help='Cantidad de libros a mostrar (opcional)')

    def handle(self, *args, **kwargs):
        genero_nombre = kwargs['genero']
        top_n = kwargs['top']

        genero = Genero.objects.filter(nombre__iexact=genero_nombre).first()

        if not genero:
            self.stdout.write(self.style.ERROR(f'❌ El género "{genero_nombre}" no existe.'))
            return

        libros = Libro.objects.filter(genero=genero)\
            .annotate(promedio=Avg('calificaciones__puntaje'))\
            .order_by('-promedio')[:top_n]

        if not libros:
            self.stdout.write(self.style.WARNING(f'⚠️ No hay libros calificados en el género "{genero_nombre}".'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n📚 Libros mejor valorados en el género "{genero_nombre}":\n'))
        for idx, libro in enumerate(libros, start=1):
            promedio = round(libro.promedio or 0, 2)
            self.stdout.write(f"{idx}. {libro.titulo} — {libro.autor.nombre} ({promedio}⭐)")
