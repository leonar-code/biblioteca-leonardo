from rest_framework import serializers
from .models import Libro, Autor, Genero, Calificacion

# Serializador básico para autores
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

# Serializador básico para géneros
class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

# Serializador completo para libros
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

# Serializador de calificaciones, sin incluir usuario (se asigna en la vista)
class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'libro', 'puntaje']

    # Validación personalizada para asegurar valores entre 1.0 y 5.0
    def validate_puntaje(self, value):
        if not 1.0 <= value <= 5.0:
            raise serializers.ValidationError("El puntaje debe estar entre 1.0 y 5.0.")
        return value
