# Bitácora robótica

Blog en español para compartir artículos sobre robótica. La web está construida
con Django y presenta el contenido en un diseño adaptable, centrado en la
lectura y utilizable desde móviles y ordenadores.

## Qué incluye

- **Portada:** muestra los artículos publicados más recientes.
- **Artículos:** cada publicación tiene su propia página con título, fecha,
  autor, texto y, opcionalmente, una imagen.
- **Sobre mí:** página de presentación del autor, editable desde el panel.
- **Administración:** Django Admin permite crear y editar artículos, controlar
  si están publicados y actualizar la presentación del autor.
- **API REST:** permite consultar artículos publicados y crear borradores con
  un token de una cuenta autorizada del panel.
- **Almacenamiento local:** SQLite guarda los datos y las imágenes se guardan
  en la carpeta `src/media/`.

Los visitantes pueden leer el blog sin registrarse. Solo el editor necesita una
cuenta para entrar en el panel administrativo. El proyecto no incluye
comentarios, registro público de lectores, suscripciones ni buscador.

## Requisitos

- Python **3.12 o posterior** y `pip` (requisito de la versión de Django
  indicada en `requirements.txt`).
- Windows, macOS o Linux.
- Conexión a Internet durante la instalación de las dependencias.

Las dependencias del proyecto están definidas en `requirements.txt` e incluyen
Django, Django REST Framework y Pillow (para gestionar imágenes).

## Instalación y ejecución local

Abre una terminal en la carpeta del proyecto. Los comandos siguientes suponen
que el repositorio está en `blog_ejercicio`; si tu carpeta tiene otro nombre,
ajusta la ruta.

### Windows (PowerShell)

La primera vez, abre una terminal en la carpeta del proyecto y ejecuta:

```powershell
cd C:\ruta\a\blog_ejercicio
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd src
python manage.py migrate
```

Si PowerShell impide activar el entorno por la política de ejecución, puedes
usar la terminal **Símbolo del sistema (cmd)** en su lugar:

```cmd
cd C:\ruta\a\blog_ejercicio
py -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
cd src
python manage.py migrate
```

Después de esa configuración, cada vez que quieras iniciar el blog desde
Visual Studio Code, abre una terminal en la carpeta principal del proyecto y
ejecuta:

```powershell
.\.venv\Scripts\python.exe .\src\manage.py runserver
```

Deja la terminal abierta mientras uses el blog y visita
<http://127.0.0.1:8000/>. Para detenerlo, pulsa `Ctrl+C` en la terminal.

### macOS o Linux

```bash
cd /ruta/a/blog_ejercicio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd src
python manage.py migrate
```

Después de la configuración inicial, inicia el servidor desde `src/` con
`python manage.py runserver`.

Al iniciar correctamente, Django mostrará en la terminal una dirección local.
Abre estas páginas en el navegador:

- Blog: <http://127.0.0.1:8000/>
- Presentación: <http://127.0.0.1:8000/sobre-mi/>
- Administración: <http://127.0.0.1:8000/admin/>

Para detener el servidor, vuelve a la terminal y pulsa `Ctrl+C`. Para salir del
entorno virtual, ejecuta `deactivate`.

## Crear la cuenta del editor

La migración crea las tablas, pero no crea automáticamente una cuenta para el
panel. Crea el superusuario una sola vez por cada base de datos. En Windows,
abre una terminal en la carpeta principal del proyecto y ejecuta:

```powershell
.\.venv\Scripts\python.exe .\src\manage.py createsuperuser
```

En macOS o Linux, activa el entorno virtual y ejecuta `python manage.py
createsuperuser` desde la carpeta `src/`.

Sigue las instrucciones para elegir un nombre de usuario y contraseña. Al
escribir la contraseña no verás los caracteres en la terminal; es normal.
Después inicia el servidor e inicia sesión en
<http://127.0.0.1:8000/admin/> con esas credenciales.

## Cargar el contenido de ejemplo

El repositorio incluye un fixture con las noticias y la presentación del autor.
En una base de datos nueva, después de ejecutar las migraciones, ve a `src/` y
ejecuta:

```bash
python manage.py loaddata blog_data
```

El fixture usa los archivos de imagen incluidos en `src/media/`. No lo cargues
si ya tienes noticias o una presentación guardadas en esa base de datos.

## Añadir un artículo

1. Inicia el servidor y entra en el panel administrativo con tu cuenta.
2. Abre **Articles** y selecciona **Add article**.
3. Completa el título, el contenido, el autor y la fecha. El `slug` es el
   identificador usado en la URL; normalmente puede generarse a partir del
   título. El extracto y la imagen son opcionales.
4. Marca **Is published** para que el artículo aparezca en el blog público.
   Los artículos no publicados no son visibles para los visitantes.
5. Guarda los cambios. El artículo aparecerá en la portada y tendrá una página
   propia bajo `/articulos/<slug>/`.

En el campo de contenido, separa los párrafos con una línea en blanco y empieza
una línea con `## ` para crear un subtítulo.

Para cambiar la presentación del autor, abre **Presentación del autor** en el
panel y edita su contenido.

## API REST

Las lecturas de la API son públicas y solo muestran artículos publicados:

- `GET http://127.0.0.1:8000/api/articulos/` — lista de artículos publicados.
- `GET http://127.0.0.1:8000/api/articulos/1/` — detalle publicado por ID.

Si ya tenías el proyecto instalado antes de añadir la API, aplica la migración
del almacén de tokens una vez:

```powershell
.\.venv\Scripts\python.exe .\src\manage.py migrate
```

Consulta la lista con `curl.exe` desde PowerShell:

```powershell
curl.exe http://127.0.0.1:8000/api/articulos/
```

Para crear un borrador, genera un token para una cuenta con acceso al Django
Admin. En Windows, desde la carpeta principal del proyecto, ejecuta:

```powershell
.\.venv\Scripts\python.exe .\src\manage.py drf_create_token tu_usuario_admin
```

El comando muestra el token. Guárdalo de forma privada y asígnalo a una
variable de entorno en PowerShell:

```powershell
$env:BLOG_API_TOKEN = "pega_aqui_el_token"
```

Usa `curl.exe` desde PowerShell para crear un borrador; `titulo` y `cuerpo`
son obligatorios y el borrador no aparecerá en las lecturas públicas hasta
que se publique desde Django Admin:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/articulos/ -H "Authorization: Token $env:BLOG_API_TOKEN" -H "Content-Type: application/json" --data-raw '{"titulo":"Nuevo borrador","cuerpo":"Texto del artículo."}'
```

La respuesta incluye `id`, `titulo`, `cuerpo` y `estado`. Al crear, el estado
siempre es `borrador`, por ejemplo:

```json
{
  "id": 3,
  "titulo": "Nuevo borrador",
  "cuerpo": "Texto del artículo.",
  "estado": "borrador"
}
```

Las noticias creadas mediante la API pueden revisarse y publicarse en Django
Admin.

## Estructura del proyecto

```text
blog_ejercicio/
├── README.md
├── requirements.txt
└── src/
    ├── manage.py
    ├── db.sqlite3
    ├── config/          # Configuración y rutas del proyecto Django
    └── blog/            # Modelos, vistas, plantillas, estilos y administración
```

La base de datos SQLite y los archivos multimedia locales se encuentran dentro
de `src/`. No borres `src/db.sqlite3` si quieres conservar el contenido creado.

## Solución de problemas

- **`python` no se reconoce:** instala Python y asegúrate de incluirlo en el
  `PATH`. En Windows también puedes probar `py` en lugar de `python`.
- **No se encuentra Django:** activa el entorno virtual y ejecuta
  `python -m pip install -r requirements.txt` desde la carpeta del proyecto.
- **La página no carga:** comprueba que `python manage.py runserver` sigue
  ejecutándose en la terminal y que estás usando la dirección indicada.
- **El puerto 8000 está ocupado:** inicia el servidor en otro puerto, por
  ejemplo con `python manage.py runserver 8001`, y visita
  <http://127.0.0.1:8001/>.
- **No puedes entrar en `/admin/`:** crea una cuenta con
  `python manage.py createsuperuser` desde `src/`.

## Nota de seguridad

`runserver` está pensado para desarrollo local, no para publicar el sitio en
Internet. Antes de un despliegue real hay que configurar, entre otras cosas,
una clave secreta segura, `DEBUG = False`, los hosts permitidos, HTTPS y un
servidor de producción adecuado. No compartas las credenciales del panel.
