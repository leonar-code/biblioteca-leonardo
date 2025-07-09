from django.urls import path
from .views import (
    AutorListCreateView, AutorDetailView,
    GeneroListCreateView, GeneroDetailView,
    LibroListCreateView, LibroDetailView,
    CalificacionListCreateView, CalificacionDetailView
)
from .views import recomendaciones_por_genero

urlpatterns = [
    path('autores/', AutorListCreateView.as_view(), name='autor-list-create'),
    path('autores/<int:pk>/', AutorDetailView.as_view(), name='autor-detail'),
    path('generos/', GeneroListCreateView.as_view(), name='genero-list-create'),
    path('generos/<int:pk>/', GeneroDetailView.as_view(), name='genero-detail'),
    path('libros/', LibroListCreateView.as_view(), name='libro-list-create'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='libro-detail'),
    path('calificaciones/', CalificacionListCreateView.as_view(), name='calificacion-list-create'),
    path('calificaciones/<int:pk>/', CalificacionDetailView.as_view(), name='calificacion-detail'),
    path('recomendaciones/', recomendaciones_por_genero, name='recomendaciones'),
]
