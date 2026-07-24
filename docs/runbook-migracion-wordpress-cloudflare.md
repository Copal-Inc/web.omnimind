# Runbook — Migrar el dominio de WordPress a Cloudflare

> Guía operativa paso a paso. El dominio de Omnimind fue adquirido a través de
> **WordPress.com**; el objetivo es servir el sitio Astro desde **Cloudflare
> Pages** y gestionar DNS y correo en Cloudflare, con la mínima interrupción.

---

## 0. Primero: entender las dos opciones (no son lo mismo)

Hay dos cosas distintas que la gente confunde:

| | **Opción A — Solo cambiar DNS** | **Opción B — Transferir el registro** |
|---|---|---|
| Qué mueves | Los *nameservers* apuntan a Cloudflare | El **registro** del dominio pasa a Cloudflare Registrar |
| Dónde se paga la renovación | Sigue en WordPress.com (~$18–25 USD/año) | En Cloudflare, **a precio de costo** (~$10–12 USD/año .com) |
| Tiempo | Minutos | 5–7 días (proceso ICANN) |
| Recomendado | Para arrancar ya | **Sí, para bajar el costo anual** |

**Recomendación:** hacer primero la **Opción A** (para publicar el sitio nuevo
cuanto antes) y luego la **Opción B** (para reducir el costo de renovación).
Ambas terminan con Cloudflare gestionando el DNS.

> ⚠️ **Requisito para transferir (Opción B):** el dominio debe tener **más de 60
> días** desde su registro o última transferencia (regla de ICANN). Si se compró
> hace poco en WordPress.com, esperar a cumplir los 60 días; mientras tanto,
> operar con la Opción A.

---

## 1. Preparación (en WordPress.com)

1. Iniciar sesión en **WordPress.com → Upgrades → Domains** y seleccionar el
   dominio.
2. **Desbloquear el dominio** (Domain lock / Transfer lock → *off*).
3. **Desactivar DNSSEC** si está activo. (Si se dejan las firmas DNSSEC viejas al
   cambiar de nameservers, la resolución DNS falla).
4. Verificar que el **correo de contacto del registrante** es válido y accesible:
   ahí llegarán el **código de autorización (EPP/Auth code)** y los avisos.
5. **Anotar todos los registros DNS actuales** (A, CNAME, MX, TXT/SPF, etc.) antes
   de mover nada, para recrearlos en Cloudflare.

## 2. Opción A — Apuntar los nameservers a Cloudflare (rápido)

1. Crear cuenta en **Cloudflare** → **Add a site** → escribir el dominio → elegir
   plan **Free**.
2. Cloudflare escanea el DNS existente e importa lo que detecta. **Revisar** que
   estén todos los registros anotados en el paso 1.5 (especialmente **MX** y
   **TXT/SPF** del correo, para no romperlo).
3. Cloudflare muestra **dos nameservers** (ej. `xxx.ns.cloudflare.com`).
4. En **WordPress.com → Domains → Name Servers**: elegir *Use custom name servers*
   y pegar los dos de Cloudflare. Guardar.
5. En Cloudflare, pulsar **Check nameservers**. La propagación suele tardar
   minutos (hasta 24 h como máximo). Cloudflare envía un correo al activarse.

> A partir de aquí, **Cloudflare gestiona el DNS** aunque el registro siga en
> WordPress.com.

## 3. Conectar el dominio a Cloudflare Pages

1. En **Cloudflare Pages**, con el proyecto ya creado desde el repo
   `Copal-Inc/web.omnimind`, ir a **Custom domains → Set up a domain**.
2. Añadir el dominio raíz (`dominio.com`) y `www`. Cloudflare crea los registros
   (CNAME/flattening) automáticamente al estar el DNS en Cloudflare.
3. Esperar a que el certificado **SSL** se emita (automático, minutos).
4. Validar que el sitio Astro carga en el dominio y que el `base` ya es `/`
   (ver [documentación técnica §7.2](./documentacion-tecnica.md)).

## 4. Configurar el correo (Email Routing)

1. En **Cloudflare → Email → Email Routing**, activar el servicio: agrega los
   registros **MX** y **SPF** necesarios (reemplazan a los de WordPress/otro).
2. Crear la regla: `contacto@dominio` → **reenviar** a la bandeja real (Gmail/Zoho)
   y **verificar** esa dirección destino.
3. (Envío como `@dominio`) configurar Gmail *"Enviar como"* con un relay SMTP
   gratuito, o dar de alta el buzón en **Zoho Mail**. Ver escenarios en la
   [cotización](./cotizacion.md).
4. Publicar **DMARC** (`_dmarc` TXT) recomendado.

## 5. Opción B — Transferir el registro a Cloudflare Registrar (ahorro)

> Hacer esto **después** de que el DNS ya vive en Cloudflare (Opción A) y de
> cumplir los 60 días.

1. En **WordPress.com**: confirmar dominio desbloqueado y solicitar el
   **código de autorización (EPP/Auth code)**.
2. En **Cloudflare → Registrar → Transfer Domains**: seleccionar el dominio,
   ingresar el código EPP y **pagar 1 año** (ICANN suma un año a la vigencia;
   a precio de costo, sin sobreprecio).
3. Aprobar el correo de confirmación de transferencia. El proceso tarda **5–7
   días**. El sitio y el correo **no se interrumpen** porque el DNS ya está en
   Cloudflare.
4. Al completarse, activar **Auto-renew** y, si se desea, **DNSSEC** en Cloudflare.

## 6. Verificación final (checklist)

- [ ] `https://dominio.com` y `https://www.dominio.com` cargan el sitio Astro con SSL.
- [ ] El blog publica al hacer commit desde el CMS (`/admin`).
- [ ] El formulario `/api/contacto` envía y la consulta llega a la bandeja.
- [ ] `contacto@dominio` recibe y reenvía correctamente.
- [ ] SPF/DKIM/DMARC verdes (probar con un correo de prueba).
- [ ] (Opción B) Registro del dominio ya figura en Cloudflare con auto-renovación.
- [ ] Retirado el deploy de GitHub Pages para evitar despliegues duplicados.

## 7. Rollback

Mientras el registro siga en WordPress.com (Opción A), revertir es tan simple como
**volver a poner los nameservers de WordPress.com**. Por eso conviene **no
transferir el registro (Opción B) hasta validar** que todo funciona en Cloudflare.
