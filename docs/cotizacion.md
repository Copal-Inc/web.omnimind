# Cotización — Infraestructura y Operación del Sitio OMNIMIND

| | |
|---|---|
| **Proyecto** | Omnimind — Sitio Web Corporativo |
| **Alcance de esta cotización** | Servicios recurrentes de hosting, CMS, formulario y correo |
| **Versión** | 1.0 |
| **Fecha** | Julio 2026 |
| **Emisor** | Copal Inc |
| **Vigencia** | 15 días naturales |
| **Confidencialidad** | CONFIDENCIAL |

> **Tipo de cambio referencial:** 1 USD = $18.50 MXN (se actualiza al formalizar).
> **Presupuesto del cliente:** $2,000 MXN/año.
> **Nota:** el **desarrollo del sitio** y el **SEO** son **patrocinados por Copal**
> y **no se cobran** (aparecen como $0). Esta cotización cubre únicamente los
> servicios recurrentes de operación.

---

## 1. Descripción

Copal propone operar el sitio de Omnimind sobre una arquitectura **estática y
serverless en Cloudflare**, que permite a Omnimind:

- **Gestionar el sitio y publicar en el blog** por su cuenta, sin tocar código
  (CMS visual).
- Recibir consultas por un **formulario de contacto** funcional.
- Contar con **correo propio `@dominio`**.

El diseño prioriza ser *lightweight* y económico: casi todos los componentes caen
en el **tier gratuito** de Cloudflare, por lo que el **único costo recurrente
real es el dominio**.

## 2. Alcance de servicios (qué incluye)

| Servicio | Incluido | Modelo de costo |
|---|---|---|
| Desarrollo del sitio (Astro) | ✅ | **Patrocinado por Copal — $0** |
| SEO y sitemap | ✅ | **Patrocinado por Copal — $0** |
| Migración de dominio y puesta en producción | ✅ | **Patrocinado por Copal — $0** |
| Hosting + CDN + SSL | ✅ | Cloudflare Pages — $0 |
| CMS para el blog | ✅ | Decap/Sveltia — $0 |
| Formulario de contacto (serverless) | ✅ | Pages Function + Resend + Turnstile — $0 |
| Correo entrante `@dominio` | ✅ | Cloudflare Email Routing — $0 |
| **Dominio** (renovación anual) | ✅ | **Costo recurrente — ver §3** |
| Correo saliente profesional (opcional) | ⭐ | Zoho Mail — ver §4 |

## 3. Infraestructura (costo anual)

| Servicio | Descripción | Plan | USD/año | MXN/año |
|---|---|---|---|---|
| Cloudflare Pages | Hosting estático + CDN + SSL + ancho de banda ilimitado | Free | $0 | $0 |
| Cloudflare Workers | Proxy OAuth del CMS + función del formulario | Free | $0 | $0 |
| Cloudflare Email Routing | Correo entrante `@dominio` → reenvío | Free | $0 | $0 |
| Cloudflare Turnstile | Anti-spam del formulario | Free | $0 | $0 |
| Cloudflare DNS + WAF | Resolución y protección | Free | $0 | $0 |
| Resend / Brevo | Envío del correo del formulario | Free | $0 | $0 |
| GitHub | Repositorio (código + contenido + respaldo) | Free | $0 | $0 |
| **Dominio (.com)** | **Renovación anual vía Cloudflare Registrar (a costo)** | — | **~$11** | **~$204** |
| **TOTAL RECURRENTE (base)** | | | **~$11** | **≈ $204 MXN/año** |

> El dominio hoy se renueva en WordPress.com (~$22 USD ≈ $407 MXN/año). Al
> **transferirlo a Cloudflare Registrar** (a precio de costo) baja a ~$11 USD.
> Si el dominio es `.mx`/`.com.mx`, la renovación es mayor (~$30–40 USD/año), aún
> dentro del presupuesto.

## 4. Correo — dos escenarios

Cloudflare Email Routing **recibe** correo gratis, pero **no envía**. Para
responder *como* `@dominio` hay dos caminos:

| | **Escenario A — Recomendado (arranque)** | **Escenario B — Buzón profesional** |
|---|---|---|
| Recibir | Cloudflare Email Routing (gratis) | Cloudflare Email Routing (gratis) |
| Enviar como `@dominio` | Gmail "Enviar como" + relay SMTP gratuito (Brevo/SMTP2GO) | Zoho Mail (buzón real con IMAP) |
| Cliente de correo | El Gmail actual de Omnimind | App/web de Zoho, Outlook, etc. |
| Límite | ~300 correos/día (relay free) | Sin ese límite |
| Costo | **$0** | **Zoho Lite ~$12 USD (~$222 MXN) / buzón / año** |

**Recomendación:** iniciar con el **Escenario A** ($0). Migrar a Zoho solo si
Omnimind quiere buzones independientes con IMAP. Zoho también tiene un **tier
gratuito** (5 buzones, solo webmail) como punto intermedio a $0.

## 5. Resumen ejecutivo de costos

| Escenario | Concepto | MXN/año |
|---|---|---|
| **A (recomendado)** | Dominio + todo Cloudflare + correo bidireccional gratis | **≈ $204** |
| **B** | Escenario A + 1 buzón Zoho Mail Lite | **≈ $426** |
| **B (2 buzones)** | Escenario A + 2 buzones Zoho Mail Lite | **≈ $648** |

| Comparativo vs. presupuesto | MXN |
|---|---|
| Presupuesto anual del cliente | $2,000 |
| Costo recomendado (Escenario A) | ≈ $204 |
| **Margen disponible** | **≈ $1,796 (90%)** |

> Con el escenario recomendado se usa **~10% del presupuesto**. El margen restante
> cubre holgadamente: renovación de un dominio `.mx`, hasta ~5 buzones Zoho de
> pago, o un futuro upgrade puntual, sin exceder los $2,000 MXN/año.

## 6. Condiciones generales

- Los costos de **desarrollo, SEO y migración** son patrocinados por Copal y no se
  facturan.
- Los servicios de infraestructura se contratan **a nombre de Omnimind**
  (dominio, Cloudflare, correo), quedando bajo su propiedad y control.
- Los precios en tier gratuito están sujetos a las políticas de cada proveedor;
  si un proveedor modificara su tier, Copal propondrá una alternativa equivalente.
- El tipo de cambio y el precio del dominio se confirman al momento de formalizar.
- Esta cotización tiene vigencia de **15 días naturales**.

---

### Firmas y aprobaciones

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Elaboró | Copal Inc | | |
| Revisó | | | |
| Aprobó | Omnimind | | |
