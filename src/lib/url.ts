/**
 * Rutas conscientes del `base` del sitio.
 *
 * El proyecto se sirve bajo un subdirectorio (`base: '/web.omnimind'` en
 * astro.config.mjs), así que cualquier enlace interno escrito como
 * `/contacto/` apunta fuera del sitio en producción.
 *
 * Uso:  <a href={url('/contacto/')}>…</a>
 */
const raw = import.meta.env.BASE_URL;

/** `''` cuando el sitio vive en la raíz, `/web.omnimind` cuando no. */
export const base = raw === '/' ? '' : raw.replace(/\/$/, '');

/** Antepone el `base` a una ruta interna que empieza con `/`. */
export function url(path: string): string {
  return `${base}${path}`;
}
