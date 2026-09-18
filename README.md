# sergiowero.github.io

Sitio personal de Sergio de Jesús Sánchez Robles. Todas las páginas comparten el mismo "shell" (diseño Dark Terminal: fondo, hoja A4, header con pestañas, idioma y tema claro/oscuro; el estado de idioma y tema se conserva entre páginas vía `localStorage`).

| Ruta | Sección | Estado |
|---|---|---|
| `/` | About me | placeholder (solo el nombre) |
| `/cv/` | Resume / CV | completo |
| `/history/` | Extended History | placeholder (solo el nombre) |
| `/blog/` | Blog | índice vacío |

- `Backups/` — las 9 variantes de diseño evaluadas (`Backups/index.html` es el selector con previews).
- `favicons/` — las 6 opciones de favicon; la elegida (`3-braces`) está en la raíz como `favicon.svg`, `favicon.ico` y `apple-touch-icon.png`.
- `tools/gen.py` — genera las variantes v2–v4 y v6–v9 desde datos compartidos, y a partir de la v3 escribe `cv/index.html` y las demás páginas del sitio (`python3 tools/gen.py`). v1 y v5 están escritas a mano.
