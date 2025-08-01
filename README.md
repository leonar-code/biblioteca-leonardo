# Biblioteca - Proyecto Django + PostgreSQL

Este proyecto es una API RESTful desarrollada con Django y Django REST Framework. Permite gestionar libros, autores, géneros y calificaciones, incluyendo funcionalidades de análisis y generación de reportes gráficos. También se pueden obtener recomendaciones de libros mejor valorados por género.

---

## Versiones y dependencias utilizadas
```text
Package                       Version
----------------------------- -----------
asgiref                       3.8.1
contourpy                     1.3.2
cycler                        0.12.1
Django                        5.2.3
djangorestframework           3.16.0
djangorestframework_simplejwt 5.5.0
fonttools                     4.58.4
kiwisolver                    1.4.8
matplotlib                    3.10.3
numpy                         2.3.1
packaging                     25.0
pandas                        2.3.0
pillow                        11.3.0
pip                           25.1.1
psycopg2-binary               2.9.10
PyJWT                         2.9.0
pyparsing                     3.2.3
python-dateutil               2.9.0.post0
pytz                          2025.2
seaborn                       0.13.2
six                           1.17.0
sqlparse                      0.5.3
tzdata                        2025.2
```
---

## Instalación del entorno y del proyecto

```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate   # En Windows
```

## Instalar dependencias
pip install -r requirements.txt

## Crear proyecto Django
```bash
django-admin startproject biblioteca
cd biblioteca
python manage.py startapp libros
```

## Creacion de la base de datos
Crear la base de datos en postgresql.

Desde pgAdmin o la consola de postgresql:
```sql
CREATE DATABASE biblioteca;
CREATE USER postgres WITH PASSWORD '123456';  -- 
GRANT ALL PRIVILEGES ON DATABASE biblioteca TO postgres;
```

## Configurar la conexión en Django (settings.py)
Abrí biblioteca/settings.py y buscá la sección DATABASES, tienes que reemplazarla por:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Luego, cuando hayas configurado todo, aplicar las migraciones correspondientes:
```bash
python manage.py makemigrations
python manage.py migrate
```
## Explicación general del programa

La aplicación **Biblioteca** es una API REST desarrollada por nosotros usando Django y Django REST Framework. Está orientada a la gestión de libros digitales y análisis de calificaciones por parte de los usuarios.

Funcionalidades principales:

- Registrar libros, autores y géneros literarios.  
- Permitir que cada usuario califique un libro una sola vez, con valores decimales entre **0.5 y 5.0**.  
- Consultar listados completos o filtrados por ID (libros, autores, géneros).  
- Generar recomendaciones automáticas de libros mejor calificados, por género.  
- Ejecutar scripts personalizados para crear **reportes gráficos** a partir de los datos (con pandas, matplotlib y seaborn).

---

## ¿Cómo funciona?

El flujo general de la API es el siguiente:

1. **Autenticación y registro:**  
   Los usuarios se registran mediante `POST /api/register/` y acceden con `POST /api/login/`. Se implementa autenticación con JWT (SimpleJWT), lo que permite proteger todas las rutas sensibles (como registrar libros o calificar).

2. **Operaciones CRUD:**  
   - Los usuarios autenticados pueden consultar información pública (GET libros, géneros, autores).  
   - Solo administradores pueden agregar, editar o eliminar libros/autores/géneros.

3. **Restricción lógica en calificaciones:**  
   - Un mismo usuario no puede calificar dos veces el mismo libro.  
   - Las calificaciones se almacenan con validación automática entre 0.5 y 5.0 puntos.

4. **Scripts de análisis:**  
   - Desde consola se puede ejecutar `python manage.py generar_reportes` para obtener **gráficos en PNG** sobre tendencias, top libros, etc.  
   - También se puede ejecutar `python manage.py libros_por_genero` para obtener los mejores libros de un género específico según el promedio de calificaciones.

Todo el sistema está diseñado para facilitar tanto el uso vía Postman como el análisis posterior de los datos cargados.


## Prueba de la API
En Postman

Para Registrar:
```http
POST http://127.0.0.1:8000/api/usuarios/register/
```
Debe pasarse el JSON en el body:
```json
{
  "username": "leonardoprueba",
  "email": "leoo@gmail.com",
  "password": "1234567"
}
``` 
![Image](https://github.com/user-attachments/assets/f941e1c1-3569-4c1c-b8c1-f2a33ca9926e)


Para Iniciar Sesion:
```http
POST http://127.0.0.1:8000/api/usuarios/login/
```
Debe pasarse las credenciales en el JSON en el body:
```json
{
  "username": "leonardoprueba",
  "password": "1234567"
}
```
![Image](https://github.com/user-attachments/assets/8a4315ef-f494-4640-9795-8525a6a59acd)


Si las credenciales son correctas se genera un token para autenticar las demas funciones.

## Prueba Api Libros
### Listar todos los libros
```http
GET http://127.0.0.1:8000/api/libros/
```
Se debe pasar el token generado en el login.
![Image](https://github.com/user-attachments/assets/0cc80e05-d438-4818-9376-34ebde680c03)


Codigo para listar todos los libros:
```python
def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)
```

### Obtener libro por ID
```http
GET http://127.0.0.1:8000/api/libros/3/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/fd05d39d-ec71-420e-8112-b917b6dc2ff5)

Codigo para obtener libro por ID:

```python
def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)
```

### Insertar Libro
```http
POST http://127.0.0.1:8000/api/libros/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/6c6c4dbd-9e44-4475-93fe-6a92e070474a)

Codigo para Insertar Libro:

```python
def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Actualizar Libro
```http
PUT http://127.0.0.1:8000/api/libros/9/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/6b14f026-fa1e-4317-98ed-55d16de1dcf1)

Codigo para Actualizar Libro:

```python
def put(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Eliminar Libro
```http
DELETE http://127.0.0.1:8000/api/libros/9/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/be2b0e2f-2fee-4fdf-a4d4-313490985339)

Codigo para Eliminar Libro:

```python
def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

## Análisis y Visualización de Datos
El proyecto incluye un script para generar reportes gráficos basados en los datos de libros, calificaciones, etc.

## Ubicación del script
El archivo está ubicado en:
```bash
libros/management/commands/generar_reportes.py
```

Podés ejecutarlo con:
```
python manage.py generar_reportes
```

Esto generará las imágenes .png dentro de una carpeta reportes_png/ ubicada en la raíz del proyecto.

### Gráficos generados y su interpretación
## 1. Distribución general de puntajes
Archivo: reporte1_puntajes.png
Explicación:
Podemos observar la distribucion de puntajes. 

![Image](https://github.com/user-attachments/assets/0adb0b4b-2340-4134-b23e-96b0886dd8c1)

## 2. Top 10 libros mejor calificados - Puntaje promedio
Archivo: reporte2_libros_top.png


![Image](https://github.com/user-attachments/assets/3f1748f4-af47-49b8-a3e0-ffaf03ba302e)

## 3. Puntaje promedio por año de publicacion
Archivo: reporte8_promedio_anio.png


![Image](https://github.com/user-attachments/assets/ec0c92f6-3a47-476b-a073-735461c146ba)


## Recomendaciones por género
La aplicación incluye un comando de consola que muestra los libros mejor valorados dentro de un género determinado, ordenados por su puntaje promedio.

## Ubicación del script
```bash
libros/management/commands/libros_por_genero.py
```
## ¿Cómo se ejecuta?
Desde la terminal:
```bash
python manage.py libros_por_genero "Nombre del Género" --top 10
```
Ejemplo:
```bash
python manage.py libros_por_genero "Fantasia" --top 5

```
Esto imprimirá los títulos con mayor promedio de calificación en el género Fantasia.

![Image](https://github.com/user-attachments/assets/f16ae64e-0e14-4352-81f7-8a0777c013cd)

## ¿Qué hace el script?
Recibe el nombre del género y un parámetro opcional --top (cantidad de resultados).

Verifica que el género exista; si no, muestra un mensaje de error.

Calcula el promedio de calificaciones de cada libro en ese género.

Ordena los libros de mayor a menor promedio.

Muestra los primeros N libros (por defecto 10) en consola con su puntaje medio y autor.

## Licencia

Este proyecto está licenciado bajo los términos de la [Licencia MIT](./LICENSE).

## Licencia de Terceros
```text
Name                           Version      License
 Django                         5.2.3        BSD License
 PyJWT                          2.9.0        MIT License
 asgiref                        3.8.1        BSD License
 contourpy                      1.3.2        BSD License
 cycler                         0.12.1       BSD License
 djangorestframework            3.16.0       BSD License
 djangorestframework_simplejwt  5.5.0        MIT License
 fonttools                      4.58.4       MIT
 kiwisolver                     1.4.8        BSD License
 matplotlib                     3.10.3       Python Software Foundation License
 numpy                          2.3.1        BSD License
 packaging                      25.0         Apache Software License; BSD License
 pandas                         2.3.0        BSD License
 pillow                         11.3.0       UNKNOWN
 psycopg2-binary                2.9.10       GNU Library or Lesser General Public License (LGPL)
 pyparsing                      3.2.3        MIT License
 python-dateutil                2.9.0.post0  Apache Software License; BSD License
 pytz                           2025.2       MIT License
 seaborn                        0.13.2       BSD License
 six                            1.17.0       MIT License
 sqlparse                       0.5.3        BSD License
 tzdata                         2025.2       Apache Software License
```




## Autor
Proyecto desarrollado por **Leonardo Candia**  
Contacto: leocandia47@gmail.com  
GitHub: [leonar-code](https://github.com/leonar-code)
