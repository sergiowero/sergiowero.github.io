# sergiowero.github.io

Sitio personal de Sergio de Jesús Sánchez Robles. Se construye con [Astro](https://astro.build) y se publica en GitHub Pages con GitHub Actions en cada push a `main`.

| Ruta | Sección | Origen |
|---|---|---|
| `/` | Resume / CV | estático (`public/index.html`, generado por `tools/gen.py`; `/cv/` redirige aquí) |
| `/timeline/` | Extended History | estático: línea de tiempo con panel lateral que sigue el scroll (`tools/gen.py` → `history_entries()`) |
| `/blog/` | Blog | Astro: índice, páginas por tag (`/blog/tags/<tag>/`) y entradas (`/blog/<en|es>/<slug>/`) |
| `/about/` | About me | estático (placeholder con el nombre) |

Todas las páginas comparten el mismo cascarón (diseño "Dark Terminal"): fondo, hoja A4, encabezado con pestañas, ES/EN y claro/oscuro. El idioma y el tema se guardan en `localStorage` y se conservan entre páginas.

## Descargar el CV

Los botones **PDF** y **DOCX** fijos abajo a la derecha (solo en `/`; viven fuera de la hoja para no escalarse con ella) bajan el CV en el idioma que estés viendo. Todo ocurre en el navegador — GitHub Pages solo sirve archivos estáticos. El encabezado del sitio nunca sale en la descarga: `@media print` lo oculta y el DOCX se arma desde los datos, no desde la página.

- **PDF** — abre el diálogo de impresión del navegador (Guardar como PDF) con el tema y el idioma que estén en pantalla, sin preguntar nada. Sale una hoja A4 exacta, con el texto seleccionable y legible por los filtros ATS de los reclutadores. El nombre propuesto es `Sergio-Sanchez-CV-EN.pdf` / `-ES.pdf`. El fondo oscuro se conserva gracias a `print-color-adjust: exact` en `html`.
- **DOCX** — genera el `.docx` en el navegador ([`public/cv-export.js`](public/cv-export.js) escribe el OOXML y el zip a mano, sin dependencias). Siempre en claro, porque es un documento para editar e imprimir.

El CV cabe en **una sola hoja A4 en los dos idiomas** (1123 px). Si agregas texto, verifica que siga cupiendo: el español suele ocupar ~15 % más.

## Textos en dos idiomas

Los datos del CV en `tools/gen.py` son `T(en, es)`; `T("solo esto")` sirve cuando el texto es igual en ambos. De ahí salen las dos versiones del HTML (CSS muestra una según `html[data-lang]`) y el JSON que usa el DOCX, así que **se traduce en un solo lugar**. Lo que se dibuja desde JS (fechas, panel de `/timeline/`) se redibuja con el evento `langchange`.

## Publicar una entrada del blog

1. Crea `src/content/blog/en/<slug>.md` y/o `src/content/blog/es/<slug>.md` (mismo `<slug>` = misma entrada en los dos idiomas; el botón ES/EN salta entre ellas).
2. Front matter:
   ```yaml
   ---
   title: "Título"
   description: "Una línea para el índice"
   pubDate: 2026-09-18
   tags: ["astro", "meta"]
   draft: false   # true lo oculta en producción
   ---
   ```
3. `git push` → GitHub Actions construye y despliega (≈1 min).

## Agregar entradas al timeline (`/timeline/`)

Los empleos de `JOBS` y la educación ya aparecen. Para añadir otra cosa (charla, proyecto, certificación…), agrega un dict a `EXTRA_HISTORY` en `tools/gen.py`:

```python
dict(kind="milestone", slug="mi-charla", role="Speaker", co="Nombre del evento",
     frm="2023-05",            # "YYYY-MM"; agrega to="YYYY-MM" (o to=None = presente) si es un periodo
     loc="Guadalajara, México", inds=["Community"], tech=["Unity"], pts=["Qué hice…"])
```

y corre `python3 tools/gen.py`. Las entradas se ordenan solas de la más reciente a la más antigua.

Hasta **dos niveles**: cualquier entrada acepta `children=[…]` (en un empleo de `JOBS`, `history_children=[…]`) con dicts del mismo formato; se dibujan anidados y el panel lateral indica `↳ inside <padre>`. Guía completa en [`docs/adding-history-entries.md`](docs/adding-history-entries.md).

## Desarrollo local

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # genera dist/
python3 tools/gen.py   # regenera las páginas estáticas (CV, About, Timeline, Backups) y src/shell/
```

- `public/Backups/` — las 9 variantes de diseño evaluadas (`public/Backups/index.html` es el selector).
- `public/favicons/` — las 6 opciones de favicon; la elegida está en `public/` como `favicon.svg`, `favicon.ico` y `apple-touch-icon.png`.
- `src/shell/` — CSS, head, header y scripts del cascarón, exportados por `tools/gen.py` y usados por `src/layouts/Shell.astro`. No editar a mano.
- `public/cv-export.js` — la descarga en PDF/DOCX. Este sí se edita a mano; `tools/gen.py` solo lo enlaza desde el CV junto con el JSON de datos.
