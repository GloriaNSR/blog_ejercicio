# Alcance del producto: Blog de robótica

## Objetivo

Entregar un blog en español centrado en la lectura de artículos sobre robótica y en la presentación de su autor. El sitio debe servir a visitantes sin requerir registro y permitir que el editor mantenga el contenido sin modificar código ni plantillas.

## Incluido en la primera versión

### Experiencia pública

- **Portada:** mostrar el nombre del blog y los artículos publicados más recientes, ordenados del más nuevo al más antiguo. Cada entrada incluye título, imágen, fecha, extracto y enlace al artículo. Si no hay publicaciones, se muestra un mensaje informativo.
- **Artículo:** ofrecer una página individual con título, imágen, fecha de publicación, autoría y contenido con párrafos y subtítulos. Las rutas de artículos inexistentes responden con una página 404 original (y a ser posible, graciosa).
- **Sobre mí:** presentar un texto breve sobre el autor que el editor pueda actualizar.
- **Navegación:** incluir enlaces claros entre la portada y «Sobre mí», además de una forma de volver a la portada desde cada artículo.
- **Contenido inicial:** proporcionar ejemplos relacionados con robótica que puedan editarse o eliminarse.

### Gestión editorial

- Utilizar Django Admin para crear, editar y retirar artículos y actualizar la presentación del autor.
- Mantener los artículos no publicados fuera de las páginas públicas.
- Restringir la gestión al editor autenticado; no habrá registro ni cuentas para visitantes.

### Requisitos transversales

- Renderizar las páginas en el servidor con Django y persistir el contenido mediante modelos y migraciones.
- Usar SQLite para el desarrollo inicial.
- Diseñar una interfaz adaptable a móviles y ordenadores, legible y accesible mediante HTML semántico, estructura de encabezados coherente, enlaces descriptivos y navegación por teclado.
- Permitir la navegación básica sin JavaScript.

## Fuera de alcance

- Registro, inicio de sesión o perfiles para lectores.
- Comentarios, reacciones u otras funciones sociales.
- Suscripciones, boletines o notificaciones.
- Búsqueda de artículos.
- Flujos editoriales avanzados, programación de publicaciones o gestión de múltiples roles.
- Selección y configuración de una base de datos de producción o del entorno de despliegue.

## Límites y supuestos

- La primera versión contempla una presentación principal del autor y un editor del sitio.
- Django Admin es la única interfaz de gestión editorial incluida.
- El contenido de ejemplo es provisional y puede sustituirse desde el panel administrativo.
- El dominio, la identidad visual y el contenido definitivo se definirán fuera de este alcance.
