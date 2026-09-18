# sergiowero.github.io

Sitio personal de Sergio de Jesús Sánchez Robles. Se construye con [Astro](https://astro.build) y se publica en GitHub Pages con GitHub Actions en cada push a `main`.

| Ruta | Sección | Origen |
|---|---|---|
| `/cv/` | Resume / CV | estático (`public/cv/index.html`, generado por `tools/gen.py`) |
| `/` | About me | estático (placeholder con el nombre) |
| `/history/` | Extended History | estático (placeholder con el nombre) |
| `/blog/` | Blog | Astro: índice, páginas por tag (`/blog/tags/<tag>/`) y entradas (`/blog/<en|es>/<slug>/`) |

Todas las páginas comparten el mismo cascarón (diseño "Dark Terminal"): fondo, hoja A4, encabezado con pestañas, ES/EN y claro/oscuro. El idioma y el tema se guardan en `localStorage` y se conservan entre páginas.

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

## Desarrollo local

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # genera dist/
python3 tools/gen.py   # regenera las páginas estáticas (CV, About, History, Backups) y src/shell/
```

- `public/Backups/` — las 9 variantes de diseño evaluadas (`public/Backups/index.html` es el selector).
- `public/favicons/` — las 6 opciones de favicon; la elegida está en `public/` como `favicon.svg`, `favicon.ico` y `apple-touch-icon.png`.
- `src/shell/` — CSS, head, header y scripts del cascarón, exportados por `tools/gen.py` y usados por `src/layouts/Shell.astro`. No editar a mano.
