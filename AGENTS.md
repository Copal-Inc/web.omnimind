## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

---

## Omnimind — Decisiones de arquitectura pendientes de hosting

### Decap CMS — Backend

El hosting del sitio aún no está definido (Netlify, Vercel, propio, etc.).
Mientras tanto, configurar Decap CMS con `backend: test-repo` para que la
interfaz funcione en local sin autenticación.

En `public/admin/config.yml`, dejar la configuración real comentada:

```yaml
# backend:           # ← descomentar cuando haya hosting definido
#   name: github
#   repo: org/repo
#   branch: main

backend:
  name: test-repo   # ← solo para desarrollo local
```

Cuando se defina el hosting, reemplazar `test-repo` con el backend real.
No desarrollar el flujo de autenticación OAuth ni el proxy de auth hasta la Iteración 8.

### Formulario de contacto — Sin backend por ahora

Construir el formulario de contacto como HTML semántico completo
(campos, validación nativa, estilos), pero **sin conectar un backend real**.

Dejar el `action` como placeholder comentado con las opciones disponibles:
- Netlify Forms: agregar `netlify` al `<form>` y el atributo `data-netlify="true"`
- Formspree: `action="https://formspree.io/f/XXXXXXXX"`
- Endpoint propio: definir en Iteración 8

No invertir tiempo en backend de formularios hasta que el hosting esté decidido.

### Control de versiones — Git local

Hacer commits de Git locales a lo largo del desarrollo aunque no haya remote configurado.
El repositorio puede permanecer solo local y subirse al remote de la empresa cuando
se decida el hosting y la cuenta organizacional.

Agrupar los commits por iteración o por feature. Ejemplo:
- `feat: iteración 5 — rutas secundarias`
- `feat: iteración 6 — Decap CMS UI`
