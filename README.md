# 🧠 OMNIMIND — Sitio Web Corporativo

Sitio web corporativo de **Omnimind**, empresa de talleres e intervenciones organizacionales enfocada en neurociencias, bienestar y productividad para equipos de alto rendimiento.

Construido con [Astro](https://astro.build/) — generador de sitios estáticos ultrarrápido.

---

## 📁 Estructura del proyecto

```
src/
├── components/        # Componentes reutilizables (Header, Footer, BaseHead)
├── content/blog/      # Artículos del blog en Markdown
├── layouts/           # Layouts: BaseLayout, BlogPost, AdminLayout
├── pages/
│   ├── index.astro             # Página principal
│   ├── sobre-nosotras.astro    # Quiénes somos
│   ├── contacto.astro          # Formulario de contacto
│   ├── aviso-de-privacidad.astro
│   ├── cms-demo.astro          # Demo del CMS para administradoras
│   ├── blog/                   # Listado y detalle de artículos
│   └── servicios/              # Empowermind, Neurowise, Wealth & Mind
├── styles/global.css  # Sistema de diseño global (tokens, tipografía, colores)
└── content.config.ts  # Schema de validación del blog
public/
├── admin/             # Decap CMS (config.yml + SPA)
└── img/               # Logos e imágenes de marca
```

---

## 🔄 Iteraciones de desarrollo

| # | Iteración | Estado |
|---|-----------|--------|
| 1 | Sistema visual global + Header + Footer | ✅ Completo |
| 2 | Hero + Servicios + CTA de cotización | ✅ Completo |
| 3 | Sobre Omnimind + Client Journey | ✅ Completo |
| 4 | Casos de éxito + Testimonios | ⏳ Pendiente (esperando contenido real) |
| 5 | Rutas secundarias (servicios, contacto, blog, aviso de privacidad) | ✅ Completo |
| 6 | Decap CMS — interfaz de administración del blog | ✅ Completo |
| 7 | Responsive + Accesibilidad + Build de producción | 🔜 Próxima |
| 8 | Deploy en **Cloudflare Pages** + CMS con OAuth real + formulario y correo | 🔜 Próxima |

> **Arquitectura y hosting definidos:** el sitio se desplegará en **Cloudflare Pages**
> (estático + serverless), con Decap/Sveltia CMS por OAuth de GitHub, formulario vía
> Pages Function y correo por Cloudflare Email Routing. Ver [`docs/`](./docs/).

---

## 🛠️ Comandos

```bash
# Instalar dependencias
pnpm install

# Servidor de desarrollo
pnpm dev

# Build de producción
pnpm build

# Preview del build
pnpm preview
```

---

## 🧩 Stack tecnológico

- **Framework:** [Astro](https://astro.build/) v7 (sitio estático / JAMstack)
- **Estilos:** CSS puro con sistema de tokens (variables CSS)
- **Blog:** Markdown / MDX con content collections
- **CMS:** [Decap CMS](https://decapcms.org/) / [Sveltia](https://github.com/sveltia/sveltia-cms) — Git-based, autenticación por OAuth de GitHub
- **Hosting:** [Cloudflare Pages](https://pages.cloudflare.com/) + Workers/Functions (serverless) + Email Routing
- **Fuentes:** Atkinson Hyperlegible (proveedor de fuentes local de Astro)

---

## 📚 Documentación

La documentación técnica y de negocio vive en [`docs/`](./docs/):

| Documento | Contenido |
|---|---|
| [`docs/arquitectura.md`](./docs/arquitectura.md) | Diagrama de arquitectura detallado y flujos |
| [`docs/documentacion-tecnica.md`](./docs/documentacion-tecnica.md) | Componentes, APIs, despliegue, seguridad |
| [`docs/cotizacion.md`](./docs/cotizacion.md) | Costos recurrentes desglosados vs. presupuesto |
| [`docs/runbook-migracion-wordpress-cloudflare.md`](./docs/runbook-migracion-wordpress-cloudflare.md) | Migrar el dominio de WordPress a Cloudflare |
| [`docs/base-conocimiento-publicar-en-el-blog.md`](./docs/base-conocimiento-publicar-en-el-blog.md) | Guía para publicar en el blog |

Los entregables al cliente (Documentación Técnica y Cotización) se generan también
como `.docx` con la marca Copal: `python3 docs/generar_docx.py` → `docs/salida/`.

---

## 📝 Notas

- El CMS demo (`/cms-demo/`) simula el flujo completo de creación de artículos sin backend. Cuando el sitio esté desplegado, se usará `/admin/` con Decap CMS conectado a GitHub.
- Los artículos del blog se almacenan como archivos `.md` en `src/content/blog/` y se validan con el schema definido en `content.config.ts`.
- El formulario de contacto está maquetado pero no tiene backend conectado aún.

---

## ✨ Sistema de movimiento

Toda la animación vive en `src/styles/motion.css` (tokens y estilos) y
`src/components/Motion.astro` (motor JS, sin dependencias). El componente
`Motion` se monta una sola vez desde `BaseLayout`.

**Interruptor global:** un script inline en `BaseHead` pone
`<html data-motion="on|off">` antes del primer pintado. Con
`prefers-reduced-motion: reduce`, o sin JS, vale `off` y el sitio queda
completamente estático y legible — ningún contenido depende de la animación
para mostrarse.

### Ganchos disponibles (atributos `data-*`)

| Atributo | Qué hace |
|---|---|
| `data-reveal="up\|down\|left\|right\|scale\|blur\|mask"` | Aparece al entrar en pantalla (IntersectionObserver) |
| `data-stagger="120"` | En un contenedor: escalona a sus hijos `data-reveal` cada N ms |
| `data-enter` + `--enter-delay` | Entrada inmediata al cargar (heros), sin esperar scroll |
| `data-count="+50"` | Cuenta desde 0 al entrar en pantalla, respetando prefijo y sufijo |
| `data-spotlight` / `data-spotlight="dark"` | Halo teal que sigue al cursor dentro del elemento |
| `data-tilt="4"` | Inclinación 3D suave hacia el cursor (grados máximos) |
| `data-magnetic="0.2"` | Botón imantado: se acerca al cursor (envolver el texto en `.btn__label`) |
| `data-parallax="0.15"` | Desplazamiento vertical según el scroll |
| `data-mouse-parallax` + `data-depth="20"` | Capas con profundidad que reaccionan al cursor |
| `.card-hover` + `.card-media` | Zoom de la imagen al pasar el cursor por la tarjeta |

### Componentes de apoyo

- **`NeuralField.astro`** — fondo de secciones oscuras: auroras de color en CSS
  + red neuronal en canvas que reacciona al cursor. El padre necesita
  `position: relative` (las `.section-dark` ya lo traen).
- **`PageHero.astro`** — encabezado unificado de páginas internas, con campo
  neuronal y entrada escalonada del texto.

### Cursor personalizado

Punto teal que sigue 1:1 (no se pierde precisión) más un anillo con inercia
que se expande sobre elementos interactivos. Solo se activa en punteros finos
y se desactiva sobre campos de formulario. Para volver al cursor del sistema,
basta con eliminar el bloque `html.cursor-active { cursor: none }` de
`motion.css`.

### Navegación

`ClientRouter` (View Transitions de Astro) funde el cambio de página en lugar
de parpadear en blanco. Cualquier script que enlace listeners debe hacerlo en
`astro:page-load`, no solo en `DOMContentLoaded`.

### Rutas

El sitio se sirve bajo un subdirectorio (`base: '/web.omnimind'`), así que los
enlaces internos deben escribirse con el helper `src/lib/url.ts`:
`<a href={url('/contacto/')}>` — nunca `href="/contacto/"`.
