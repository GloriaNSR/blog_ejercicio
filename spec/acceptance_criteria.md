# Criterios de aceptación: Blog de robótica

Estos criterios describen resultados observables para la primera versión. Se basan en el alcance actual de `scope.md`; las imágenes se consideran parte de la experiencia cuando un artículo tiene una imagen asociada.

## CA-01: Portada y artículos recientes

- Al solicitar `/`, se muestra la portada con el nombre del blog.
- La portada muestra únicamente artículos publicados y los ordena del más nuevo al más antiguo.
- Cada artículo de la lista muestra su título, fecha, extracto y enlace al detalle; si tiene imagen asociada, también la muestra.
- Cuando un artículo se retira o deja de estar publicado, deja de aparecer en la portada.
- Al activar el enlace de un artículo, se abre la página correspondiente a su slug.
- Si no hay artículos publicados, se muestra un mensaje informativo en lugar de una lista vacía sin explicación.
- Un artículo en borrador no aparece en la portada, aunque su slug sea conocido por un visitante anónimo.

## CA-02: Lectura de un artículo

- La página de un artículo muestra su título, fecha de publicación, autoría y contenido.
- Si el artículo tiene una imagen asociada, esta se muestra en su página.
- Los párrafos y subtítulos del contenido se presentan con una estructura legible y coherente.
- Una ruta con un slug inexistente responde con HTTP 404 y muestra una página de error propia del sitio, no una página de éxito ni un error genérico del servidor.

## CA-03: Presentación del autor

- Existe una página `/sobre-mi/` identificable como «Sobre mí» que presenta el texto del autor.
- La página muestra el texto actualizado desde la gestión editorial, sin requerir cambios en las plantillas.

## CA-04: Navegación

- La navegación principal incluye enlaces descriptivos a la portada y a «Sobre mí».
- Desde la página de un artículo se puede volver a la portada mediante un enlace visible y comprensible.
- Los enlaces de navegación funcionan con teclado y sin JavaScript.

## CA-05: Gestión editorial y acceso

- Un editor autorizado puede crear, editar y retirar artículos desde Django Admin, incluida la imagen asociada cuando corresponda.
- Un editor autorizado puede actualizar el texto de «Sobre mí» desde Django Admin.
- Los cambios guardados en el panel se reflejan en las páginas públicas.
- Una persona anónima no puede acceder a las operaciones de gestión ni modificar contenido.
- No existe un flujo público para registrarse o crear una cuenta de lector.

## CA-06: Adaptabilidad y accesibilidad

- Las páginas de portada, artículo y «Sobre mí» se pueden utilizar en pantallas pequeñas y grandes sin desplazamiento horizontal innecesario.
- El contenido utiliza HTML semántico y una jerarquía de encabezados coherente.
- El texto y los controles mantienen contraste y legibilidad suficientes; los enlaces se distinguen y describen su destino.
- La navegación y los controles disponibles se pueden utilizar con teclado.

## CA-07: Renderizado y persistencia

- Las páginas públicas se renderizan en el servidor con Django y el contenido se conserva mediante los modelos y migraciones del proyecto.
- La navegación y lectura principales siguen funcionando con JavaScript desactivado.
