# Visión del producto: Blog de robótica

## Propósito

Crear un espacio digital sencillo para compartir conocimiento y experiencias sobre robótica. El blog debe permitir que cualquier visitante encuentre los artículos recientes, lea cada publicación con comodidad y conozca a la persona que escribe.

## Público y necesidades

- **Lectores:** personas interesadas en la robótica que quieren acceder al contenido de forma clara desde un móvil o un ordenador, sin tener que crear una cuenta.
- **Editor:** la persona autora, que necesita publicar y mantener artículos y su presentación sin modificar código ni plantillas.

## Experiencia deseada

La portada presenta el blog y facilita descubrir las publicaciones recientes. Cada artículo ofrece un espacio propio, ordenado y legible, mientras que la sección «Sobre mí» da contexto sobre su autor. La navegación debe ser predecible y funcionar sin depender de JavaScript.

Una API REST complementa la web: permite consultar publicaciones públicas y
que el editor cree borradores mediante un token asociado a su cuenta de Django.

La interfaz prioriza el texto: jerarquía visual clara, tipografía cómoda, contraste suficiente y adaptación a distintos tamaños de pantalla. El contenido inicial sirve como ejemplo y puede sustituirse desde las herramientas de edición.

## Principios

1. **Lectura primero:** evitar elementos que distraigan del contenido y facilitar la lectura prolongada.
2. **Acceso directo:** permitir recorrer portada, artículos y presentación mediante enlaces claros, sin registro de lectores.
3. **Edición sencilla:** ofrecer al editor una gestión de contenido conocida mediante el panel administrativo estándar de Django.
4. **Contenido fiable:** mostrar públicamente solo artículos publicados y responder con una página 404 cuando un artículo no exista.
5. **Accesibilidad y adaptación:** usar estructura semántica, navegación por teclado y un diseño usable en pantallas pequeñas y grandes.

## Límites de la primera versión

La primera versión se centra en la portada, la lectura de artículos, la presentación del autor y la gestión editorial básica. No contempla cuentas públicas, comentarios, suscripciones, búsqueda ni flujos editoriales avanzados.

## Resultado esperado

Un visitante puede descubrir y leer una publicación y encontrar información sobre su autor; el editor puede mantener el contenido desde Django Admin. La experiencia funciona tanto en móvil como en escritorio y mantiene el foco en la robótica y la lectura.
