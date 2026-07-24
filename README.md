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
