from django.db import models
from django.contrib.auth.models import User

# Modelo de autor del libro (nombre y nacionalidad)
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Género literario (drama, ciencia ficción, etc.)
class Genero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo principal del libro
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    url_libro = models.URLField()  # solo se guarda el link al PDF

    def __str__(self):
        return self.titulo

# Calificaciones del libro (1 a 5) por usuario
class Calificacion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')
    puntaje = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        # Para evitar que un usuario califique el mismo libro más de una vez
        unique_together = ('libro', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.titulo} ({self.puntaje})"
