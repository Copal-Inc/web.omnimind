# Documentación — Sitio Web OMNIMIND

Documentación técnica y de negocio del sitio de Omnimind, elaborada por **Copal Inc**.

| Documento | Descripción | Público |
|---|---|---|
| [`arquitectura.md`](./arquitectura.md) | Diagrama de arquitectura detallado y flujos del sistema | Técnico |
| [`documentacion-tecnica.md`](./documentacion-tecnica.md) | Componentes, APIs, despliegue, seguridad | Técnico / Cliente |
| [`cotizacion.md`](./cotizacion.md) | Costos recurrentes desglosados vs. presupuesto | Cliente |
| [`runbook-migracion-wordpress-cloudflare.md`](./runbook-migracion-wordpress-cloudflare.md) | Paso a paso para migrar el dominio de WordPress a Cloudflare | Técnico |
| [`base-conocimiento-publicar-en-el-blog.md`](./base-conocimiento-publicar-en-el-blog.md) | Guía para que Omnimind publique en el blog | Operación (Omnimind) |

## Entregables con marca Copal (.docx)

Todos los documentos se generan también como `.docx` con la identidad de Copal
(portada, logo, header/footer y paleta oficiales), más una **compilación** con
todo junto:

```bash
python3 docs/generar_docx.py
```

Genera en `docs/salida/`:
- `Omnimind — Arquitectura.docx` (con el diagrama embebido)
- `Omnimind — Documentación Técnica.docx` (con el diagrama embebido)
- `Omnimind — Cotización.docx`
- `Omnimind — Runbook Migración WordPress a Cloudflare.docx`
- `Omnimind — Base de Conocimiento (Blog).docx`
- **`Omnimind — Expediente Técnico (Compilación).docx`** — los 5 documentos en uno

> Requiere `python-docx`, `cairosvg` (logo) y `graphviz`/`dot` (diagrama).
> Reutiliza las plantillas oficiales de Copal en `../plantillas/`. El diagrama se
> renderiza con Graphviz a `docs/salida/assets/arquitectura.png`.

## Decisiones de arquitectura (resumen)

- **Hosting:** Cloudflare Pages (estático, CDN, SSL) — *lightweight* y $0.
- **Backend:** serverless (Pages Functions + Worker OAuth), sin servidor ni BD.
- **CMS:** Decap/Sveltia (Git-based) para autogestión del blog.
- **Correo:** Cloudflare Email Routing (entrante, $0) + Zoho opcional.
- **Costo real:** solo el dominio (~$204 MXN/año) — 10% del presupuesto.
