#!/usr/bin/env python3
"""
generar_docx.py — Genera TODOS los documentos de Omnimind en Word (.docx) con la
marca Copal, reutilizando las plantillas oficiales de Copal, y produce además una
compilación (expediente único con todos los documentos).

Salida (docs/salida/):
    1. Omnimind — Arquitectura.docx
    2. Omnimind — Documentación Técnica.docx
    3. Omnimind — Cotización.docx
    4. Omnimind — Runbook Migración WordPress a Cloudflare.docx
    5. Omnimind — Base de Conocimiento (Blog).docx
    6. Omnimind — Expediente Técnico (Compilación).docx   ← todos juntos

El diagrama de arquitectura se renderiza con Graphviz (dot) y se embebe como imagen.

Requiere: python-docx, cairosvg (logo), graphviz/dot (diagrama).
Plantillas en ../plantillas/ relativo a la raíz del repo.
"""
import os
import sys
import subprocess

HERE       = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(HERE)
PLANTILLAS = os.path.normpath(os.path.join(REPO_ROOT, "..", "plantillas"))
OUT_DIR    = os.path.join(HERE, "salida")
ASSETS     = os.path.join(OUT_DIR, "assets")

if not os.path.isdir(PLANTILLAS):
    sys.exit(f"[error] No se encontró la carpeta de plantillas: {PLANTILLAS}")

sys.path.insert(0, PLANTILLAS)
import build_documentacion_tecnica as C  # noqa: E402  (helpers de estilo Copal)

Cm, Pt = C.Cm, C.Pt
AL = C.WD_ALIGN_PARAGRAPH
CONF = C.CONF_LEVEL


# ═══════════════════════════════════════════════════════════════════════════════
# Diagrama de arquitectura (Graphviz → PNG)
# ═══════════════════════════════════════════════════════════════════════════════
DOT = r'''
digraph omnimind {
  rankdir=TB;
  graph [fontname="Calibri", fontsize=12, splines=true, nodesep=0.35, ranksep=0.6, bgcolor="white", pad=0.3];
  node  [fontname="Calibri", fontsize=10, shape=box, style="rounded,filled", color="#3A7A52", fillcolor="white", penwidth=1.2, margin="0.14,0.09"];
  edge  [fontname="Calibri", fontsize=8, color="#5B6470", penwidth=1.0];

  subgraph cluster_users {
    label="Personas"; labeljust="l"; style="rounded,filled"; fillcolor="#F2F3F4"; color="#9BA0A8"; fontcolor="#0F141B"; fontsize=11;
    visit [label="Visitante\n(navegador)"];
    admin [label="Administradora\nOmnimind"];
    lead  [label="Prospecto\n(formulario)"];
  }

  subgraph cluster_cf {
    label="Cloudflare — 1 cuenta (plan Free)"; labeljust="l"; style="rounded,filled"; fillcolor="#E4F3E8"; color="#3A7A52"; fontcolor="#0F141B"; fontsize=11;
    dns       [label="DNS\n(nameservers)"];
    cdn       [label="CDN + WAF + SSL"];
    pages     [label="Pages\nSitio Astro estático"];
    fnForm    [label="Pages Function\nPOST /api/contacto"];
    fnAuth    [label="Worker OAuth\n/oauth · /callback"];
    turnstile [label="Turnstile\n(anti-spam)"];
    email     [label="Email Routing\ncontacto@dominio"];
  }

  subgraph cluster_gh {
    label="GitHub — Copal-Inc/web.omnimind"; labeljust="l"; style="rounded,filled"; fillcolor="#E8E2D5"; color="#7A4A2E"; fontcolor="#0F141B"; fontsize=11;
    repo     [label="Repositorio\ncódigo + Markdown"];
    oauthApp [label="GitHub OAuth App"];
  }

  subgraph cluster_cms {
    label="CMS (/admin)"; labeljust="l"; style="rounded,filled"; fillcolor="#EAF2FF"; color="#3A7A52"; fontcolor="#0F141B"; fontsize=11;
    decap [label="Decap / Sveltia\n(SPA en navegador)"];
  }

  subgraph cluster_ext {
    label="Servicios externos (Free)"; labeljust="l"; style="rounded,filled"; fillcolor="#F3E8E4"; color="#7A4A2E"; fontcolor="#0F141B"; fontsize=11;
    resend [label="Resend / Brevo\n(envío de correo)"];
    gmail  [label="Bandeja Omnimind\n(Gmail / Zoho)"];
  }

  // Navegación pública
  visit -> cdn [label="HTTPS"];
  cdn -> pages;
  dns -> cdn [label="resuelve", style=dashed];

  // Formulario
  lead -> turnstile [label="envía"];
  turnstile -> fnForm [label="token válido"];
  fnForm -> resend [label="API"];
  resend -> gmail [label="correo consulta"];

  // Edición del blog
  admin -> decap [label="/admin"];
  decap -> fnAuth [label="login OAuth", dir=both];
  fnAuth -> oauthApp [label="token", dir=both];
  decap -> repo [label="commit MD + imágenes"];

  // CI/CD
  repo -> pages [label="push a main"];
  pages -> cdn [label="deploy a edge"];

  // Correo entrante
  visit -> email [label="correo entrante", style=dashed];
  email -> gmail [label="reenvía"];
}
'''


def render_diagram():
    """Renderiza el diagrama con Graphviz. Devuelve la ruta del PNG o None."""
    os.makedirs(ASSETS, exist_ok=True)
    dot_path = os.path.join(ASSETS, "arquitectura.dot")
    png_path = os.path.join(ASSETS, "arquitectura.png")
    with open(dot_path, "w", encoding="utf-8") as fh:
        fh.write(DOT)
    try:
        subprocess.run(["dot", "-Tpng", "-Gdpi=150", dot_path, "-o", png_path],
                       check=True, capture_output=True)
        return png_path
    except Exception as e:
        print(f"[aviso] No se pudo renderizar el diagrama ({e}); se omite la imagen.")
        return None


def add_diagram(doc, png, caption="Figura 1. Arquitectura del sitio Omnimind sobre Cloudflare."):
    if png and os.path.exists(png):
        p = doc.add_paragraph(); p.alignment = AL.CENTER
        p.add_run().add_picture(png, width=Cm(16))
        cap = doc.add_paragraph(); cap.alignment = AL.CENTER
        C._run(cap, caption, italic=True, size=Pt(8), color=C.MUTED)
    else:
        C.note(doc, "Nota: Insertar aquí el diagrama de arquitectura (ver docs/arquitectura.md).")


# ═══════════════════════════════════════════════════════════════════════════════
# Utilidades de documento
# ═══════════════════════════════════════════════════════════════════════════════
def new_doc(header_title, code):
    doc = C.Document()
    C.set_margins(doc)
    C.build_header(doc, header_title, code, "1.0", "Julio 2026", CONF)
    C.build_footer(doc, CONF)
    return doc


def bullets(doc, items):
    for t in items:
        C.bullet(doc, t)


# ═══════════════════════════════════════════════════════════════════════════════
# SECCIONES (contenido sin portada; reutilizable en docs individuales y expediente)
# ═══════════════════════════════════════════════════════════════════════════════
def sec_arquitectura(doc, png):
    C.h1(doc, "1. Principio Rector")
    C.body(doc, "El sitio de Omnimind es un sitio estático (JAMstack) generado con Astro. No existe "
                "base de datos ni servidor de aplicación siempre encendido: el HTML se pre-construye "
                "y se sirve desde el CDN. Todo lo que parece 'backend' (publicar en el blog, recibir "
                "el formulario, el correo) se resuelve con funciones serverless y servicios "
                "gestionados, casi todos en el tier gratuito de Cloudflare.")
    bullets(doc, ["Costo ≈ solo el dominio. Hosting, funciones, correo entrante y CDN son $0.",
                  "Sin superficie de servidor que mantener (sin parches de SO, sin BD, sin contenedores).",
                  "Una sola consola (Cloudflare) para DNS, hosting, correo y seguridad."])

    C.h1(doc, "2. Diagrama de Arquitectura")
    add_diagram(doc, png)

    C.h1(doc, "3. Flujos Principales")
    C.h2(doc, "3.1 Visita al sitio (lectura)")
    C.body(doc, "El navegador pide el dominio; Cloudflare DNS resuelve y el CDN entrega el HTML "
                "pre-construido desde el edge más cercano, con SSL y WAF. Cero cómputo por request.")
    C.h2(doc, "3.2 Publicar en el blog (Omnimind edita)")
    C.body(doc, "La administradora entra a /admin (CMS), inicia sesión con GitHub vía el Worker OAuth, "
                "escribe el artículo y al guardar el CMS hace commit del Markdown al repositorio. El "
                "push a main dispara el build de Cloudflare Pages y el artículo queda en línea en "
                "~1–2 min. El repositorio de GitHub es la única fuente de verdad; el historial de Git "
                "es el respaldo.")
    C.h2(doc, "3.3 Formulario de contacto (prospecto)")
    C.body(doc, "Turnstile valida que no es un bot; el navegador hace POST /api/contacto a una Pages "
                "Function que valida los campos y llama a Resend/Brevo para enviar el correo a la "
                "bandeja de Omnimind.")
    C.h2(doc, "3.4 Correo entrante y saliente")
    C.body(doc, "Entrante: Cloudflare Email Routing captura contacto@dominio y lo reenvía a la bandeja "
                "real (gratis). Saliente (opcional): Cloudflare no envía correo; para responder como "
                "@dominio se usa Gmail 'Enviar como' vía relay SMTP, o un buzón Zoho Mail.")

    C.h1(doc, "4. Por Qué Esta Arquitectura")
    C.add_table(doc,
        headers=["Necesidad del cliente", "Solución elegida", "Descartada", "Motivo"],
        rows=[
            ["Gestionar el sitio sin código", "Decap/Sveltia (Git-based)", "WordPress, Strapi", "Sin servidor ni BD; $0"],
            ["Subir artículos al blog", "Commits Markdown + rebuild", "CMS con BD", "Versionado en Git; respaldo gratis"],
            ["Hosting lightweight y barato", "Cloudflare Pages", "VPS, Vercel Pro", "Estático, CDN, ancho de banda ilimitado, $0"],
            ["Correo propio @dominio", "Email Routing (+ Zoho opc.)", "Google Workspace", "Recibir es gratis"],
            ["Formulario funcional", "Pages Function + Resend + Turnstile", "Backend propio", "Serverless, sin infra fija, $0"],
            ["Presupuesto ≤ $2,000 MXN/año", "Todo Cloudflare tier Free", "Netlify/Vercel de pago", "Único costo = dominio"],
        ],
        col_widths=[Cm(4.2), Cm(4.2), Cm(3.2), Cm(4.2)],
        left_align_cols={0, 1, 2, 3})

    C.h1(doc, "5. Estado Actual vs. Destino")
    bullets(doc, ["Hoy: despliega en GitHub Pages bajo subdirectorio (base '/web.omnimind'); Decap en modo test-repo (sin persistencia).",
                  "Destino: Cloudflare Pages en dominio raíz (base '/'); Decap/Sveltia con OAuth real, formulario conectado y correo enrutado.",
                  "La migración es de configuración, no de reescritura: el código Astro se conserva casi íntegro."])


def sec_tecnica(doc, png):
    C.h1(doc, "1. Objetivo del Documento")
    C.body(doc, "Describir la arquitectura, componentes, interfaces, despliegue y seguridad del sitio "
                "web de Omnimind, como referencia para desarrollo, operación y para el equipo de "
                "Omnimind que gestionará el contenido. Incluye el plan de migración del dominio "
                "(actualmente en WordPress) y la puesta en producción sobre Cloudflare.")

    C.h1(doc, "2. Alcance")
    C.body(doc, "Cubre:")
    bullets(doc, ["Sitio institucional estático (Astro): home, servicios, sobre-nosotras, blog, contacto, aviso de privacidad.",
                  "CMS para autogestión del blog (Decap/Sveltia) con autenticación por GitHub.",
                  "Formulario de contacto funcional (serverless).",
                  "Correo @dominio (entrante por Email Routing; saliente opcional).",
                  "Migración de dominio WordPress → Cloudflare y despliegue en Cloudflare Pages."])
    C.body(doc, "Fuera de alcance:")
    bullets(doc, ["Desarrollo de nuevas secciones o rediseño (patrocinado por Copal, no cotizado).",
                  "SEO y estrategia de contenidos (patrocinado por Copal, no cotizado).",
                  "E-commerce, portal de usuarios o cualquier funcionalidad con base de datos."])

    C.h1(doc, "3. Arquitectura del Sistema")
    C.body(doc, "Arquitectura JAMstack / serverless: el sitio se pre-construye y se sirve estático "
                "desde el CDN de Cloudflare. No hay servidor de aplicación ni base de datos; el "
                "contenido vive versionado en Git y las funciones dinámicas corren como funciones "
                "serverless.")
    add_diagram(doc, png)
    C.h2(doc, "3.1 Flujo Principal (publicación de contenido)")
    C.body(doc, "Administradora → /admin (CMS) → login vía Worker OAuth → commit Markdown a GitHub → "
                "push a main → build de Cloudflare Pages → deploy a edge. Un artículo nuevo queda "
                "publicado en ~1–2 minutos, versionado en Git.")

    C.h1(doc, "4. Componentes y Módulos")
    C.add_table(doc,
        headers=["#", "Componente", "Función principal", "Tecnología", "Costo"],
        rows=[
            ["1", "Sitio estático", "Renderiza páginas y blog", "Astro v7 + MDX", "$0"],
            ["2", "Hosting/CDN", "Sirve el sitio con SSL", "Cloudflare Pages", "$0"],
            ["3", "CMS", "Edición del blog sin código", "Decap / Sveltia", "$0"],
            ["4", "Auth del CMS", "Login GitHub para editar", "Worker OAuth proxy", "$0"],
            ["5", "Formulario", "Recibe y envía consultas", "Pages Function", "$0"],
            ["6", "Anti-spam", "Filtra bots en el formulario", "Cloudflare Turnstile", "$0"],
            ["7", "Envío de correo", "Entrega el correo del formulario", "Resend / Brevo", "$0"],
            ["8", "Correo entrante", "Reenvía @dominio a la bandeja", "Email Routing", "$0"],
            ["9", "DNS", "Resuelve el dominio", "Cloudflare DNS", "$0"],
            ["10", "Repositorio", "Fuente de verdad + respaldo", "GitHub", "$0"],
        ],
        col_widths=[Cm(0.8), Cm(3.2), Cm(5.0), Cm(3.5), Cm(1.5)],
        left_align_cols={1, 2, 3})

    C.h1(doc, "5. Interfaces y APIs")
    C.add_table(doc,
        headers=["#", "Endpoint", "Método", "Descripción", "Auth"],
        rows=[
            ["1", "/api/contacto", "POST", "Recibe el formulario, valida Turnstile y envía correo", "Turnstile token"],
            ["2", "/oauth", "GET", "Inicia el login del CMS con GitHub", "—"],
            ["3", "/callback", "GET", "Recibe el código OAuth y emite el token al CMS", "GitHub OAuth"],
            ["4", "/admin/", "GET", "SPA del CMS (Decap/Sveltia)", "Sesión GitHub"],
            ["5", "/rss.xml", "GET", "Feed del blog", "—"],
        ],
        col_widths=[Cm(0.8), Cm(3.0), Cm(1.6), Cm(6.2), Cm(2.4)],
        left_align_cols={1, 3, 4})
    C.note(doc, "Integraciones externas: GitHub API (commits del CMS) y Resend/Brevo API (envío del formulario).")

    C.h1(doc, "6. Dependencias")
    C.add_table(doc,
        headers=["#", "Paquete / Servicio", "Propósito", "Licencia / Plan"],
        rows=[
            ["1", "astro ^7", "Framework del sitio", "MIT"],
            ["2", "@astrojs/mdx", "Artículos en Markdown/MDX", "MIT"],
            ["3", "@astrojs/sitemap", "Sitemap para SEO", "MIT"],
            ["4", "@astrojs/rss", "Feed RSS del blog", "MIT"],
            ["5", "sharp", "Optimización de imágenes", "Apache-2.0"],
            ["6", "Decap / Sveltia CMS", "CMS del blog", "MIT"],
            ["7", "Cloudflare (Pages/Workers/Email/Turnstile)", "Hosting, serverless, correo, anti-spam", "Free"],
            ["8", "Resend / Brevo", "Envío transaccional del formulario", "Free"],
        ],
        col_widths=[Cm(0.8), Cm(4.6), Cm(6.0), Cm(2.6)],
        left_align_cols={1, 2, 3})

    C.h1(doc, "7. Despliegue e Infraestructura")
    C.h2(doc, "7.1 Requisitos de Entorno (variables)")
    C.add_table(doc,
        headers=["Variable", "Descripción", "Dónde", "Req."],
        rows=[
            ["GITHUB_OAUTH_CLIENT_ID", "ID de la OAuth App del CMS", "Worker OAuth", "Sí"],
            ["GITHUB_OAUTH_CLIENT_SECRET", "Secret de la OAuth App", "Worker (secreto)", "Sí"],
            ["RESEND_API_KEY", "Clave para enviar el correo del formulario", "Pages Fn (secreto)", "Sí"],
            ["TURNSTILE_SECRET_KEY", "Verificación anti-spam", "Pages Fn (secreto)", "Sí"],
            ["CONTACT_TO_EMAIL", "Bandeja destino de las consultas", "Pages Fn", "Sí"],
        ],
        col_widths=[Cm(4.4), Cm(5.4), Cm(2.8), Cm(1.4)],
        left_align_cols={0, 1, 2})
    C.h2(doc, "7.2 Proceso de Despliegue")
    bullets(doc, ["Conectar el repo a Cloudflare Pages (build: pnpm build, salida: dist/, Node 22).",
                  "Ajustar astro.config.mjs: base '/' y site con el dominio real (hoy usa /web.omnimind).",
                  "Configurar variables/secretos en Pages y en el Worker OAuth.",
                  "Crear la GitHub OAuth App y desplegar el Worker OAuth proxy.",
                  "Migrar el dominio a Cloudflare y apuntar Pages al dominio raíz (ver runbook).",
                  "Activar Email Routing (contacto@dominio → bandeja) y registros SPF/DKIM.",
                  "Retirar el workflow de GitHub Pages; Cloudflare Pages despliega en cada push a main."])
    C.note(doc, "CI/CD: integración Git de Cloudflare Pages. Cada push a main reconstruye y publica.")

    C.h1(doc, "8. Consideraciones de Seguridad")
    bullets(doc, ["Autenticación del CMS: OAuth con GitHub; el client_secret vive solo en el Worker.",
                  "Secretos: claves de API y OAuth como secrets de Cloudflare, fuera del repositorio.",
                  "Anti-spam: Turnstile + validación en la Pages Function + WAF de Cloudflare.",
                  "Correo: SPF y DKIM obligatorios (Cloudflare los exige desde julio 2025); DMARC recomendado.",
                  "Transporte: HTTPS forzado y certificado gestionado por Cloudflare.",
                  "Superficie mínima: sin servidor ni base de datos que endurecer o parchear."])

    C.h1(doc, "9. Historial de Revisiones")
    C.add_table(doc,
        headers=["Versión", "Fecha", "Autor", "Descripción del Cambio"],
        rows=[["1.0", "Julio 2026", "Copal Inc", "Versión inicial: arquitectura, migración y despliegue."]],
        col_widths=[Cm(1.5), Cm(2.5), Cm(3.0), Cm(7.5)],
        left_align_cols={2, 3})


def sec_cotizacion(doc):
    C.h1(doc, "1. Descripción")
    C.body(doc, "Copal propone operar el sitio de Omnimind sobre una arquitectura estática y serverless "
                "en Cloudflare, que permite a Omnimind gestionar el sitio y el blog sin tocar código, "
                "recibir consultas por un formulario funcional y contar con correo propio @dominio. El "
                "diseño es lightweight y económico: casi todo cae en el tier gratuito de Cloudflare, "
                "por lo que el único costo recurrente real es el dominio.")
    C.note(doc, "TC referencial 1 USD = $18.50 MXN. Presupuesto del cliente: $2,000 MXN/año. "
                "Desarrollo y SEO patrocinados por Copal ($0).")

    C.h1(doc, "2. Alcance de Servicios")
    C.add_table(doc,
        headers=["Servicio", "Incluido", "Modelo de costo"],
        rows=[
            ["Desarrollo del sitio (Astro)", "Sí", "**Patrocinado por Copal — $0**"],
            ["SEO y sitemap", "Sí", "**Patrocinado por Copal — $0**"],
            ["Migración de dominio y puesta en producción", "Sí", "**Patrocinado por Copal — $0**"],
            ["Hosting + CDN + SSL", "Sí", "Cloudflare Pages — $0"],
            ["CMS para el blog", "Sí", "Decap/Sveltia — $0"],
            ["Formulario de contacto (serverless)", "Sí", "Pages Fn + Resend + Turnstile — $0"],
            ["Correo entrante @dominio", "Sí", "Email Routing — $0"],
            ["Dominio (renovación anual)", "Sí", "**Costo recurrente — ver 3**"],
            ["Correo saliente profesional (opcional)", "Opcional", "Zoho Mail — ver 4"],
        ],
        col_widths=[Cm(6.5), Cm(2.2), Cm(7.5)],
        left_align_cols={0, 2})

    C.h1(doc, "3. Infraestructura (costo anual)")
    C.add_table(doc,
        headers=["Servicio", "Plan", "USD/año", "MXN/año"],
        rows=[
            ["Cloudflare Pages (hosting + CDN + SSL)", "Free", "$0", "$0"],
            ["Cloudflare Workers (OAuth CMS + formulario)", "Free", "$0", "$0"],
            ["Cloudflare Email Routing (correo entrante)", "Free", "$0", "$0"],
            ["Cloudflare Turnstile (anti-spam)", "Free", "$0", "$0"],
            ["Cloudflare DNS + WAF", "Free", "$0", "$0"],
            ["Resend / Brevo (envío del formulario)", "Free", "$0", "$0"],
            ["GitHub (repositorio + respaldo)", "Free", "$0", "$0"],
            ["Dominio .com (vía Cloudflare Registrar, a costo)", "—", "~$11", "~$204"],
            ["**TOTAL RECURRENTE (base)**", "", "**~$11**", "**~$204**"],
        ],
        col_widths=[Cm(9.0), Cm(2.2), Cm(2.5), Cm(2.5)],
        left_align_cols={0})
    C.note(doc, "El dominio hoy se renueva en WordPress.com (~$22 USD ≈ $407 MXN). Transferirlo a "
                "Cloudflare Registrar lo baja a ~$11 USD. Un .mx/.com.mx sería ~$30–40 USD/año.")

    C.h1(doc, "4. Correo — Dos Escenarios")
    C.body(doc, "Cloudflare Email Routing recibe correo gratis, pero no envía. Para responder como "
                "@dominio hay dos caminos:")
    C.add_table(doc,
        headers=["Aspecto", "A — Recomendado (arranque)", "B — Buzón profesional"],
        rows=[
            ["Recibir", "Email Routing (gratis)", "Email Routing (gratis)"],
            ["Enviar como @dominio", "Gmail 'Enviar como' + relay SMTP gratuito", "Zoho Mail (buzón real, IMAP)"],
            ["Límite de envío", "~300 correos/día", "Sin ese límite"],
            ["Costo", "**$0**", "**~$222 MXN / buzón / año**"],
        ],
        col_widths=[Cm(3.5), Cm(6.0), Cm(5.5)],
        left_align_cols={0, 1, 2})
    C.note(doc, "Recomendación: iniciar con el Escenario A ($0). Zoho también tiene tier gratuito "
                "(5 buzones, solo webmail) como punto intermedio a $0.")

    C.h1(doc, "5. Resumen Ejecutivo de Costos")
    C.add_table(doc,
        headers=["Escenario", "Concepto", "MXN/año"],
        rows=[
            ["A (recomendado)", "Dominio + Cloudflare + correo bidireccional gratis", "**~$204**"],
            ["B", "Escenario A + 1 buzón Zoho Mail Lite", "~$426"],
            ["B (2 buzones)", "Escenario A + 2 buzones Zoho Mail Lite", "~$648"],
        ],
        col_widths=[Cm(3.5), Cm(8.5), Cm(3.0)],
        left_align_cols={0, 1})
    C.add_table(doc,
        headers=["Comparativo vs. presupuesto", "MXN"],
        rows=[
            ["Presupuesto anual del cliente", "$2,000"],
            ["Costo recomendado (Escenario A)", "~$204"],
            ["**Margen disponible**", "**~$1,796 (90%)**"],
        ],
        col_widths=[Cm(11.5), Cm(3.5)],
        left_align_cols={0})

    C.h1(doc, "6. Condiciones Generales")
    bullets(doc, ["Desarrollo, SEO y migración son patrocinados por Copal y no se facturan.",
                  "La infraestructura se contrata a nombre de Omnimind (dominio, Cloudflare, correo), bajo su propiedad y control.",
                  "Los tiers gratuitos están sujetos a las políticas de cada proveedor; ante cambios, Copal propondrá una alternativa equivalente.",
                  "El tipo de cambio y el precio del dominio se confirman al formalizar.",
                  "Esta cotización tiene vigencia de 15 días naturales."])


def sec_runbook(doc):
    C.h1(doc, "0. Dos Opciones (no son lo mismo)")
    C.body(doc, "Cambiar el DNS (apuntar nameservers a Cloudflare) es distinto de transferir el "
                "registro del dominio a Cloudflare Registrar.")
    C.add_table(doc,
        headers=["", "A — Solo cambiar DNS", "B — Transferir el registro"],
        rows=[
            ["Qué mueves", "Nameservers a Cloudflare", "El registro a Cloudflare Registrar"],
            ["Renovación", "Sigue en WordPress.com (~$18–25 USD)", "En Cloudflare, a costo (~$11 USD .com)"],
            ["Tiempo", "Minutos", "5–7 días (proceso ICANN)"],
            ["Recomendado", "Para arrancar ya", "Sí, para bajar el costo anual"],
        ],
        col_widths=[Cm(3.0), Cm(6.0), Cm(6.0)],
        left_align_cols={0, 1, 2})
    C.note(doc, "Recomendación: primero Opción A (publicar ya), luego Opción B (bajar costo). "
                "Requisito de la Opción B: dominio con >60 días desde su registro (regla ICANN).")

    C.h1(doc, "1. Preparación (en WordPress.com)")
    bullets(doc, ["Iniciar sesión en WordPress.com → Upgrades → Domains y seleccionar el dominio.",
                  "Desbloquear el dominio (Transfer lock → off).",
                  "Desactivar DNSSEC si está activo (evita fallas de resolución al cambiar nameservers).",
                  "Verificar que el correo del registrante es válido: ahí llega el código EPP.",
                  "Anotar todos los registros DNS actuales (A, CNAME, MX, TXT/SPF) antes de mover nada."])

    C.h1(doc, "2. Opción A — Apuntar Nameservers a Cloudflare")
    bullets(doc, ["Crear cuenta en Cloudflare → Add a site → escribir el dominio → plan Free.",
                  "Revisar que Cloudflare importó todos los registros (sobre todo MX y TXT/SPF del correo).",
                  "Copiar los dos nameservers que muestra Cloudflare.",
                  "En WordPress.com → Domains → Name Servers: usar custom name servers y pegar los de Cloudflare.",
                  "En Cloudflare, pulsar 'Check nameservers' (propaga en minutos, hasta 24 h)."])

    C.h1(doc, "3. Conectar el Dominio a Cloudflare Pages")
    bullets(doc, ["En Cloudflare Pages → Custom domains → Set up a domain.",
                  "Añadir el dominio raíz y www; Cloudflare crea los registros automáticamente.",
                  "Esperar la emisión del certificado SSL (automático).",
                  "Validar que el sitio Astro carga y que el base ya es '/'."])

    C.h1(doc, "4. Configurar el Correo (Email Routing)")
    bullets(doc, ["En Cloudflare → Email → Email Routing: activar (agrega MX y SPF).",
                  "Crear la regla contacto@dominio → reenviar a la bandeja real y verificarla.",
                  "Para enviar como @dominio: Gmail 'Enviar como' + relay SMTP, o buzón Zoho.",
                  "Publicar DMARC (_dmarc TXT) recomendado."])

    C.h1(doc, "5. Opción B — Transferir el Registro (ahorro)")
    bullets(doc, ["Hacerlo después de que el DNS ya vive en Cloudflare y de cumplir los 60 días.",
                  "En WordPress.com: confirmar dominio desbloqueado y solicitar el código EPP.",
                  "En Cloudflare → Registrar → Transfer Domains: ingresar el EPP y pagar 1 año (a costo).",
                  "Aprobar el correo de confirmación; el proceso tarda 5–7 días sin interrumpir el sitio.",
                  "Al completarse, activar Auto-renew y, si se desea, DNSSEC."])

    C.h1(doc, "6. Verificación Final (checklist)")
    bullets(doc, ["Sitio carga en dominio raíz y www con SSL.",
                  "El blog publica al hacer commit desde el CMS.",
                  "El formulario /api/contacto envía y la consulta llega a la bandeja.",
                  "contacto@dominio recibe y reenvía correctamente.",
                  "SPF/DKIM/DMARC verdes.",
                  "(Opción B) Registro en Cloudflare con auto-renovación.",
                  "Retirado el deploy de GitHub Pages."])

    C.h1(doc, "7. Rollback")
    C.body(doc, "Mientras el registro siga en WordPress.com (Opción A), revertir es tan simple como "
                "volver a poner los nameservers de WordPress.com. Por eso conviene no transferir el "
                "registro (Opción B) hasta validar que todo funciona en Cloudflare.")


def sec_kb(doc):
    C.h1(doc, "1. Resumen Ejecutivo")
    C.body(doc, "El blog de Omnimind se administra desde un CMS visual en dominio.com/admin, sin saber "
                "programar. Escribes el artículo en un editor parecido a Word, le pones título, "
                "categoría e imagen, y al guardar el sitio se actualiza solo en un par de minutos. "
                "Cada artículo queda respaldado automáticamente en el historial del proyecto (Git).")

    C.h1(doc, "2. Contexto: Por Qué Importa")
    bullets(doc, ["Omnimind necesita publicar contenido con autonomía, sin depender de Copal por cada artículo.",
                  "El blog es un canal clave de posicionamiento y captación.",
                  "El contenido vive versionado: nada se pierde y todo cambio es reversible."])

    C.h1(doc, "3. Conceptos Clave")
    C.add_table(doc,
        headers=["Concepto", "Definición"],
        rows=[
            ["**CMS**", "Panel visual (/admin) para crear y editar artículos sin código."],
            ["**Artículo (post)**", "Cada entrada del blog. Se guarda como un archivo Markdown."],
            ["**Frontmatter**", "Los datos del artículo (título, fecha, categoría, portada). El CMS los pide con formulario."],
            ["**Borrador (draft)**", "Artículo guardado pero no visible en el sitio hasta publicarlo."],
            ["**Publicar / Deploy**", "Al guardar, el sitio se reconstruye y el artículo aparece en ~1–2 min."],
        ],
        col_widths=[Cm(4.5), Cm(12.0)],
        left_align_cols={0, 1})

    C.h1(doc, "4. Desarrollo — Paso a Paso")
    C.h2(doc, "4.1 Entrar al panel")
    bullets(doc, ["Ir a dominio.com/admin.",
                  "Iniciar sesión con la cuenta de GitHub autorizada (Copal la configura una vez por persona)."])
    C.h2(doc, "4.2 Crear el artículo")
    bullets(doc, ["Colección Blog → New Artículo.",
                  "Llenar Título y Descripción (la descripción sale en la lista y en Google).",
                  "Fecha de publicación, Categoría (de la lista) y Etiquetas (opcional).",
                  "Imagen de portada (1200×630 px) + su texto alternativo.",
                  "Escribir el contenido en el editor (negritas, listas, encabezados)."])
    C.h2(doc, "4.3 Guardar o publicar")
    bullets(doc, ["Borrador activado = seguir trabajando sin que se vea en el sitio.",
                  "Listo: Borrador desactivado y Publish/Guardar.",
                  "Esperar ~1–2 min y verificar en dominio.com/blog."])

    C.h1(doc, "5. Buenas Prácticas y Errores Comunes")
    C.add_table(doc,
        headers=["✓ Hacer", "✗ Evitar"],
        rows=[
            ["Escribir una descripción clara (1–2 frases)", "Dejar la descripción vacía"],
            ["Subir portada de 1200×630 px optimizada", "Subir imágenes enormes (pesan y tardan)"],
            ["Poner texto alternativo a la portada", "Dejar el alt en blanco (daña accesibilidad/SEO)"],
            ["Usar una categoría de la lista oficial", "Inventar categorías nuevas cada vez"],
            ["Guardar en borrador mientras trabajas", "Publicar a medias y editar en vivo"],
        ],
        col_widths=[Cm(8.25), Cm(8.25)],
        left_align_cols={0, 1})

    C.h1(doc, "6. Checklist Accionable")
    bullets(doc, ["[ ] Título y descripción listos",
                  "[ ] Fecha de publicación correcta",
                  "[ ] Categoría seleccionada",
                  "[ ] Portada 1200×630 + texto alternativo",
                  "[ ] Contenido revisado (sin typos)",
                  "[ ] Borrador desactivado al publicar",
                  "[ ] Verificado en dominio.com/blog"])


# ═══════════════════════════════════════════════════════════════════════════════
# Documentos individuales
# ═══════════════════════════════════════════════════════════════════════════════
def build_arquitectura(png):
    doc = new_doc("Arquitectura", "ARQ-OMNI-001")
    C.portada(doc, titulo="Arquitectura del Sitio",
              subtitulo="Diagrama detallado y flujos del sistema (JAMstack sobre Cloudflare)",
              proyecto="Omnimind — Sitio Web Corporativo", version="1.0", fecha="Julio 2026", autor="Copal Inc")
    sec_arquitectura(doc, png)
    C.firmas(doc)
    _save(doc, "Omnimind — Arquitectura.docx")


def build_tecnica(png):
    doc = new_doc("Documentación Técnica", "DOC-OMNI-001")
    C.portada(doc, titulo="Documentación Técnica",
              subtitulo="Sitio estático + CMS + correo (JAMstack sobre Cloudflare)",
              proyecto="Omnimind — Sitio Web Corporativo", version="1.0", fecha="Julio 2026", autor="Copal Inc")
    sec_tecnica(doc, png)
    C.firmas(doc)
    _save(doc, "Omnimind — Documentación Técnica.docx")


def build_cotizacion():
    doc = new_doc("Cotización", "COT-OMNI-001")
    C.portada(doc, titulo="Cotización — Infraestructura y Operación",
              subtitulo="Servicios recurrentes: hosting, CMS, formulario y correo",
              proyecto="Omnimind — Sitio Web Corporativo", version="1.0", fecha="Julio 2026", autor="Copal Inc")
    sec_cotizacion(doc)
    C.firmas(doc)
    _save(doc, "Omnimind — Cotización.docx")


def build_runbook():
    doc = new_doc("Runbook — Migración", "RUN-OMNI-001")
    C.portada(doc, titulo="Runbook — Migración del Dominio",
              subtitulo="De WordPress a Cloudflare (DNS, Pages, correo, transferencia)",
              proyecto="Omnimind — Sitio Web Corporativo", version="1.0", fecha="Julio 2026", autor="Copal Inc")
    sec_runbook(doc)
    C.firmas(doc)
    _save(doc, "Omnimind — Runbook Migración WordPress a Cloudflare.docx")


def build_kb():
    doc = new_doc("Base de Conocimiento", "KB-OMNI-001")
    C.portada(doc, titulo="Cómo Publicar un Artículo en el Blog",
              subtitulo="Guía para el equipo de Omnimind que gestiona el contenido",
              proyecto="Omnimind — Sitio Web Corporativo", version="1.0", fecha="Julio 2026", autor="Copal Inc")
    sec_kb(doc)
    _save(doc, "Omnimind — Base de Conocimiento (Blog).docx")


# ═══════════════════════════════════════════════════════════════════════════════
# Compilación — Expediente único con todos los documentos
# ═══════════════════════════════════════════════════════════════════════════════
def build_expediente(png):
    doc = new_doc("Expediente Técnico", "EXP-OMNI-001")
    C.portada(doc, titulo="Expediente Técnico — Sitio Web Omnimind",
              subtitulo="Arquitectura · Documentación Técnica · Cotización · Migración · Operación",
              proyecto="Omnimind — Sitio Web Corporativo", version="1.0", fecha="Julio 2026", autor="Copal Inc")

    C.h1(doc, "Índice del Expediente")
    C.add_table(doc,
        headers=["#", "Documento", "Contenido"],
        rows=[
            ["I",   "Arquitectura", "Diagrama detallado y flujos del sistema"],
            ["II",  "Documentación Técnica", "Componentes, APIs, despliegue, seguridad"],
            ["III", "Cotización", "Costos recurrentes desglosados vs. presupuesto"],
            ["IV",  "Runbook de Migración", "Migrar el dominio de WordPress a Cloudflare"],
            ["V",   "Base de Conocimiento", "Cómo publicar en el blog"],
        ],
        col_widths=[Cm(1.2), Cm(5.5), Cm(9.8)],
        left_align_cols={1, 2})

    parts = [
        ("I. Arquitectura",           lambda d: sec_arquitectura(d, png)),
        ("II. Documentación Técnica", lambda d: sec_tecnica(d, png)),
        ("III. Cotización",           sec_cotizacion),
        ("IV. Runbook de Migración",  sec_runbook),
        ("V. Base de Conocimiento",   sec_kb),
    ]
    for title, fn in parts:
        doc.add_page_break()
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(6)
        C._run(p, title, bold=True, size=Pt(16), color=C.MED)
        fn(doc)

    C.firmas(doc)
    _save(doc, "Omnimind — Expediente Técnico (Compilación).docx")


# ═══════════════════════════════════════════════════════════════════════════════
def _save(doc, name):
    out = os.path.join(OUT_DIR, name)
    doc.save(out)
    print(f"Guardado: {name}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    png = render_diagram()
    build_arquitectura(png)
    build_tecnica(png)
    build_cotizacion()
    build_runbook()
    build_kb()
    build_expediente(png)
    print("Listo — 6 documentos en", OUT_DIR)


if __name__ == "__main__":
    main()
