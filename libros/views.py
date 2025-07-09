from rest_framework import generics, permissions
from .models import Libro, Autor, Genero, Calificacion
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer, CalificacionSerializer

# Vistas para libros
from rest_framework.permissions import IsAuthenticated

class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]  #  protege esta vista con token


class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Vistas para autores
class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class AutorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

# Vistas para géneros
class GeneroListCreateView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class GeneroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

# Vistas para calificaciones
class CalificacionListCreateView(generics.ListCreateAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Se asigna automáticamente el usuario logueado
        serializer.save(usuario=self.request.user)

class CalificacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from libros.models import Libro, Calificacion, Genero
from django.db.models import Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recomendaciones_por_genero(request):
    genero_nombre = request.query_params.get('genero')

    if not genero_nombre:
        return Response({'error': 'Debes proporcionar un género con el parámetro ?genero='}, status=400)

    genero = Genero.objects.filter(nombre__iexact=genero_nombre).first()
    if not genero:
        return Response({'error': f'El género "{genero_nombre}" no existe.'}, status=404)

    libros = Libro.objects.filter(genero=genero)\
        .annotate(promedio=Avg('calificaciones__puntaje'))\
        .order_by('-promedio')[:5]

    resultado = [
        {
            'titulo': libro.titulo,
            'autor': libro.autor.nombre,
            'puntaje_promedio': round(libro.promedio or 0, 2)
        }
        for libro in libros
    ]

    return Response(resultado)

