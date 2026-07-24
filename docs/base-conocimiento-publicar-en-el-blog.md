# Base de Conocimiento — Cómo publicar un artículo en el blog

| | |
|---|---|
| **Código** | KB-OMNI-001 |
| **Categoría** | Operación / Gestión de contenido |
| **Versión** | 1.0 · Julio 2026 |
| **Autor** | Copal Inc |
| **Dirigido a** | Equipo de Omnimind que gestiona el blog |
| **Confidencialidad** | INTERNO |

---

## 1. Resumen ejecutivo

El blog de Omnimind se administra desde un **CMS visual** en `dominio.com/admin`,
sin necesidad de saber programar. Escribes el artículo en un editor parecido a
Word, le pones título, categoría e imagen, y al guardar **el sitio se actualiza
solo** en un par de minutos. Cada artículo queda **respaldado automáticamente** en
el historial del proyecto (Git). Esta guía explica el flujo completo.

## 2. Contexto: por qué importa

- Omnimind necesita **publicar contenido con autonomía**, sin depender de Copal
  para cada artículo.
- El blog es un canal clave de **posicionamiento y captación** (neurociencias,
  bienestar, productividad).
- El sistema elegido no tiene base de datos que se pueda "corromper": **el
  contenido vive versionado**, así que nada se pierde y todo cambio es reversible.

> "Publicar debe ser tan simple como escribir un correo — el resto lo hace la
> plataforma."

## 3. Conceptos clave

| Concepto | Definición |
|---|---|
| **CMS** | Panel visual (`/admin`) para crear y editar artículos sin código. |
| **Artículo (post)** | Cada entrada del blog. Se guarda como un archivo Markdown. |
| **Frontmatter** | Los datos del artículo (título, fecha, categoría, portada). El CMS los pide con formulario; no los escribes a mano. |
| **Borrador (draft)** | Artículo guardado pero **no visible** en el sitio hasta que lo publiques. |
| **Publicar / Deploy** | Al guardar, el sitio se reconstruye y el artículo aparece en línea en ~1–2 min. |

## 4. Desarrollo — el flujo paso a paso

### 4.1 Entrar al panel
1. Ir a `dominio.com/admin`.
2. Iniciar sesión con la cuenta de **GitHub** autorizada (Copal la configura una
   sola vez por persona).

### 4.2 Crear el artículo
1. Entrar a la colección **Blog** → **New Artículo**.
2. Llenar los campos:
   - **Título** y **Descripción** (la descripción sale en la lista y en Google).
   - **Fecha de publicación**.
   - **Categoría** (elegir de la lista: Bienestar, Neurociencias, Liderazgo…).
   - **Etiquetas** (opcional).
   - **Imagen de portada** + su **texto alternativo** (importante para
     accesibilidad y SEO). Tamaño recomendado: **1200×630 px**.
3. Escribir el **contenido** en el editor (negritas, listas, encabezados,
   imágenes).

### 4.3 Guardar como borrador o publicar
- Dejar **Borrador = activado** para seguir trabajando sin que se vea en el sitio.
- Cuando esté listo: **Borrador = desactivado** y **Publish/Guardar**.
- Esperar ~1–2 minutos y verificar en `dominio.com/blog`.

## 5. Aplicación práctica

1. **Antes de escribir:** ten listo el texto, la imagen de portada (1200×630) y la
   categoría.
2. **Escribe** el artículo en el CMS; usa encabezados para separar secciones.
3. **Revisa** en borrador; corrige typos y la descripción.
4. **Publica** y confirma en el sitio.
5. Si algo salió mal, **edita y vuelve a guardar** — se corrige en minutos.

## 6. Buenas prácticas y errores comunes

| ✓ Hacer | ✗ Evitar |
|---|---|
| Escribir una **descripción** clara (1–2 frases) | Dejar la descripción vacía |
| Subir portada de **1200×630 px** optimizada | Subir imágenes enormes (pesan y tardan) |
| Poner **texto alternativo** a la portada | Dejar el alt en blanco (daña accesibilidad/SEO) |
| Usar **una categoría** de la lista oficial | Inventar categorías nuevas cada vez |
| Guardar en **borrador** mientras trabajas | Publicar a medias y editar en vivo |

## 7. Checklist accionable

- [ ] Título y descripción listos
- [ ] Fecha de publicación correcta
- [ ] Categoría seleccionada
- [ ] Portada 1200×630 + texto alternativo
- [ ] Contenido revisado (sin typos)
- [ ] Borrador desactivado al publicar
- [ ] Verificado en `dominio.com/blog`

## 8. Referencias y recursos

- Documentación técnica del sitio: [`documentacion-tecnica.md`](./documentacion-tecnica.md)
- Arquitectura: [`arquitectura.md`](./arquitectura.md)
- Decap CMS: https://decapcms.org/docs/ · Sveltia CMS: https://github.com/sveltia/sveltia-cms
- Contacto de soporte (Copal): definir canal dedicado.
