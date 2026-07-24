# Documentación Técnica — Sitio Web OMNIMIND

| | |
|---|---|
| **Proyecto** | Omnimind — Sitio Web Corporativo |
| **Componente** | Sitio estático + CMS + correo (JAMstack sobre Cloudflare) |
| **Versión** | 1.0 |
| **Fecha** | Julio 2026 |
| **Autor / Equipo** | Copal Inc |
| **Estado** | Aprobado para implementación |
| **Confidencialidad** | CONFIDENCIAL |

---

## 1. Objetivo del documento

Describir la arquitectura, componentes, interfaces, despliegue y seguridad del
sitio web de **Omnimind**, para que sirva de referencia a desarrollo, operación y
al equipo de Omnimind que gestionará el contenido. Incluye el plan de migración
del dominio (actualmente en WordPress) y la puesta en producción sobre Cloudflare.

## 2. Alcance

**Cubre:**
- Sitio institucional estático (Astro): home, servicios, sobre-nosotras, blog,
  contacto, aviso de privacidad.
- CMS para autogestión del blog (Decap/Sveltia) con autenticación por GitHub.
- Formulario de contacto funcional (serverless).
- Correo `@dominio` (entrante por Email Routing; saliente opcional).
- Migración de dominio WordPress → Cloudflare y despliegue en Cloudflare Pages.

**Fuera de alcance:**
- Desarrollo de nuevas secciones/rediseño (patrocinado por Copal, no cotizado).
- SEO y estrategia de contenidos (patrocinado por Copal, no cotizado).
- E-commerce, portal de usuarios, o cualquier funcionalidad con base de datos.

## 3. Arquitectura del sistema

Arquitectura **JAMstack / serverless**: el sitio se pre-construye y se sirve
estático desde el CDN de Cloudflare. No hay servidor de aplicación ni base de
datos; el contenido vive versionado en Git y las funciones dinámicas (formulario,
login del CMS) corren como *serverless functions*.

**El diagrama de componentes y los flujos detallados están en
[`arquitectura.md`](./arquitectura.md).** Resumen:

- **Capa de entrega:** Cloudflare DNS + CDN + WAF + SSL → Cloudflare Pages.
- **Capa de contenido:** repositorio GitHub (código + Markdown del blog) como
  fuente de verdad; CMS que hace commits.
- **Capa serverless:** Pages Function para el formulario; Worker OAuth para el CMS.
- **Capa de correo:** Cloudflare Email Routing (entrante) + Resend/Brevo (envío
  del formulario) + Zoho/Gmail (bandeja).

### 3.1 Flujo principal (publicación de contenido)
Administradora → `/admin` (CMS) → login vía Worker OAuth → commit Markdown a
GitHub → push a `main` → build de Cloudflare Pages → deploy a edge. Un artículo
nuevo queda publicado en ~1–2 minutos, versionado en Git.

## 4. Componentes y módulos

| # | Componente | Función principal | Tecnología | Costo |
|---|---|---|---|---|
| 1 | Sitio estático | Renderiza páginas y blog | Astro v7 + MDX | $0 |
| 2 | Hosting/CDN | Sirve el sitio globalmente con SSL | Cloudflare Pages | $0 |
| 3 | CMS | Edición del blog sin código | Decap o Sveltia CMS | $0 |
| 4 | Auth del CMS | Login GitHub para editar | Worker OAuth proxy | $0 |
| 5 | Formulario | Recibe y envía las consultas | Pages Function | $0 |
| 6 | Anti-spam | Filtra bots en el formulario | Cloudflare Turnstile | $0 |
| 7 | Envío de correo | Entrega el correo del formulario | Resend o Brevo | $0 |
| 8 | Correo entrante | Reenvía `@dominio` a la bandeja | Cloudflare Email Routing | $0 |
| 9 | DNS | Resuelve el dominio | Cloudflare DNS | $0 |
| 10 | Repositorio | Fuente de verdad + respaldo | GitHub | $0 |

## 5. Interfaces y APIs

Endpoints propios (todos servidos por Cloudflare, mismo dominio):

| # | Endpoint | Método | Descripción | Auth |
|---|---|---|---|---|
| 1 | `/api/contacto` | POST | Recibe el formulario, valida Turnstile y envía correo | Turnstile token |
| 2 | `/oauth` | GET | Inicia el login del CMS con GitHub | — |
| 3 | `/callback` | GET | Recibe el código OAuth y emite el token al CMS | GitHub OAuth |
| 4 | `/admin/` | GET | SPA del CMS (Decap/Sveltia) | Sesión GitHub |
| 5 | `/rss.xml` | GET | Feed del blog (generado por Astro) | — |

Integraciones externas: **GitHub API** (commits del CMS) y **Resend/Brevo API**
(envío del correo del formulario).

## 6. Dependencias

| # | Paquete / Servicio | Propósito | Licencia / Plan |
|---|---|---|---|
| 1 | `astro` ^7 | Framework del sitio | MIT |
| 2 | `@astrojs/mdx` | Artículos en Markdown/MDX | MIT |
| 3 | `@astrojs/sitemap` | Sitemap para SEO | MIT |
| 4 | `@astrojs/rss` | Feed RSS del blog | MIT |
| 5 | `sharp` | Optimización de imágenes | Apache-2.0 |
| 6 | Decap CMS / Sveltia CMS | CMS del blog | MIT |
| 7 | Cloudflare Pages/Workers/Email/Turnstile | Hosting, serverless, correo, anti-spam | Free tier |
| 8 | Resend o Brevo | Envío transaccional del formulario | Free tier |

## 7. Despliegue e infraestructura

### 7.1 Requisitos de entorno (variables)

| Variable | Descripción | Dónde | Requerida |
|---|---|---|---|
| `GITHUB_OAUTH_CLIENT_ID` | ID de la OAuth App del CMS | Worker OAuth | Sí |
| `GITHUB_OAUTH_CLIENT_SECRET` | Secret de la OAuth App | Worker OAuth (secreto) | Sí |
| `RESEND_API_KEY` | Clave para enviar el correo del formulario | Pages Function (secreto) | Sí |
| `TURNSTILE_SECRET_KEY` | Verificación anti-spam del formulario | Pages Function (secreto) | Sí |
| `CONTACT_TO_EMAIL` | Bandeja destino de las consultas | Pages Function | Sí |

### 7.2 Proceso de despliegue
1. Conectar el repo `Copal-Inc/web.omnimind` a **Cloudflare Pages** (build:
   `pnpm build`, salida: `dist/`, Node 22).
2. Ajustar `astro.config.mjs`: `base: '/'` y `site: 'https://<dominio-real>'`
   (hoy usa `/web.omnimind`, propio de GitHub Pages).
3. Configurar variables/secretos (§7.1) en Pages y en el Worker OAuth.
4. Crear la **GitHub OAuth App** y desplegar el Worker OAuth proxy.
5. Migrar el dominio a Cloudflare y apuntar Pages al dominio raíz
   (ver [runbook](./runbook-migracion-wordpress-cloudflare.md)).
6. Activar **Email Routing** (`contacto@dominio` → bandeja) y registros SPF/DKIM.
7. Retirar el workflow de GitHub Pages (`.github/workflows/deploy.yml`); a partir
   de aquí despliega Cloudflare Pages en cada push a `main`.

> **CI/CD:** integración Git de Cloudflare Pages. Cada `push` a `main`
> reconstruye y publica automáticamente. Sin pipeline que mantener.

## 8. Consideraciones de seguridad

- **Autenticación del CMS:** OAuth con GitHub; el `client_secret` vive solo en el
  Worker (nunca en el navegador). Solo colaboradores del repo pueden editar.
- **Secretos:** claves de API y OAuth como *secrets* de Cloudflare, fuera del
  repositorio y fuera del bundle del cliente.
- **Anti-spam / anti-abuso:** Turnstile en el formulario; validación de campos en
  la Pages Function; WAF de Cloudflare frente a todo el tráfico.
- **Correo:** SPF y DKIM obligatorios (Cloudflare exige autenticación para
  reenviar desde julio 2025); DMARC recomendado.
- **Transporte:** HTTPS forzado y certificado gestionado por Cloudflare.
- **Superficie mínima:** sin servidor ni base de datos que endurecer o parchear.

## 9. Historial de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0 | Julio 2026 | Copal Inc | Versión inicial: arquitectura, migración y despliegue. |

---

### Firmas y aprobaciones

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Elaboró | Copal Inc | | |
| Revisó | | | |
| Aprobó | Omnimind | | |
