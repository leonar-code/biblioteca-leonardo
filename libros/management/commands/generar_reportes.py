from django.core.management.base import BaseCommand
from libros.models import Libro, Calificacion, Genero, Autor
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.functions import ExtractYear
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Command(BaseCommand):
    help = 'Genera reportes gráficos y los guarda en reportes_png/'

    def handle(self, *args, **kwargs):
        carpeta = 'reportes_png'
        os.makedirs(carpeta, exist_ok=True)

        # 1. Distribución general de puntajes
        puntajes = Calificacion.objects.values_list('puntaje', flat=True)
        plt.figure(figsize=(8,5))
        sns.histplot(puntajes, bins=5, kde=False)
        plt.title('Distribución de puntajes')
        plt.xlabel('Puntaje')
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte1_puntajes.png'))
        plt.close()

        # 2. Top 10 libros mejor calificados
        top_libros = Libro.objects.annotate(promedio=Avg('calificaciones__puntaje'))\
                                  .order_by('-promedio')[:10]
        titulos = [libro.titulo for libro in top_libros]
        promedios = [round(libro.promedio or 0, 2) for libro in top_libros]
        plt.figure(figsize=(10,5))
        sns.barplot(x=promedios, y=titulos, palette='viridis', hue=None)
        plt.title('Top 10 libros mejor calificados')
        plt.xlabel('Puntaje promedio')
        plt.ylabel('Libro')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte2_libros_top.png'))
        plt.close()

        # 3. Puntaje promedio por género
        generos = Genero.objects.annotate(promedio=Avg('libros__calificaciones__puntaje'))
        nombres_genero = [g.nombre for g in generos]
        promedios_genero = [round(g.promedio or 0, 2) for g in generos]
        plt.figure(figsize=(8,5))
        sns.barplot(x=promedios_genero, y=nombres_genero, palette='coolwarm', hue=None)
        plt.title('Puntaje promedio por género')
        plt.xlabel('Puntaje promedio')
        plt.ylabel('Género')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte3_genero_promedio.png'))
        plt.close()

        # 4. Autores con más libros
        autores = Autor.objects.annotate(cantidad=Count('libros')).order_by('-cantidad')[:10]
        nombres_autores = [a.nombre for a in autores]
        cantidades = [a.cantidad for a in autores]
        plt.figure(figsize=(10,5))
        sns.barplot(x=cantidades, y=nombres_autores, palette='magma', hue=None)
        plt.title('Autores con más libros registrados')
        plt.xlabel('Cantidad de libros')
        plt.ylabel('Autor')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte4_autores_mas_libros.png'))
        plt.close()

        # 5. Libros con más calificaciones
        libros_calificados = Libro.objects.annotate(total=Count('calificaciones')).order_by('-total')[:10]
        titulos_calif = [l.titulo for l in libros_calificados]
        total_calif = [l.total for l in libros_calificados]
        plt.figure(figsize=(10,5))
        sns.barplot(x=total_calif, y=titulos_calif, palette='cividis', hue=None)
        plt.title('Libros con más calificaciones')
        plt.xlabel('Cantidad de calificaciones')
        plt.ylabel('Libro')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte5_libros_mas_calificaciones.png'))
        plt.close()

        # Reporte 7: Usuarios con puntaje promedio más alto
        promedios_usuarios = Calificacion.objects.values('usuario__username')\
                                .annotate(promedio=Avg('puntaje'))\
                                .order_by('-promedio')[:10]
        nombres_usuarios = [u['usuario__username'] for u in promedios_usuarios]
        promedios = [round(u['promedio'], 2) for u in promedios_usuarios]

        plt.figure(figsize=(10, 6))
        sns.barplot(x=promedios, y=nombres_usuarios, palette='crest', hue=None)
        plt.title('Usuarios con Puntaje Promedio Más Alto')
        plt.xlabel('Puntaje Promedio')
        plt.ylabel('Usuario')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte7_usuarios_promedio.png'))
        plt.close()

        # Reporte 8: Puntaje promedio por año de publicación
        promedio_por_anio = Calificacion.objects.annotate(
            anio=ExtractYear('libro__fecha_lanzamiento')
        ).values('anio').annotate(
            promedio=Avg('puntaje')
        ).order_by('anio')

        anios = [r['anio'] for r in promedio_por_anio]
        promedios = [round(r['promedio'], 2) for r in promedio_por_anio]

        plt.figure(figsize=(10, 6))
        sns.lineplot(x=anios, y=promedios, marker='o', color='darkblue')
        plt.title('Puntaje Promedio por Año de Publicación')
        plt.xlabel('Año')
        plt.ylabel('Puntaje Promedio')
        plt.tight_layout()
        plt.savefig(os.path.join(carpeta, 'reporte8_promedio_anio.png'))
        plt.close()

        self.stdout.write(self.style.SUCCESS('✅ Reportes generados correctamente en reportes_png/'))
