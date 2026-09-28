# sergiowero.github.io

Sitio personal de Sergio de Jesús Sánchez Robles. Se construye con [Astro](https://astro.build) y se publica en GitHub Pages con GitHub Actions en cada push a `main`.

| Ruta | Sección | Origen |
|---|---|---|
| `/` | Resume / CV | estático (`public/index.html`, generado por `tools/gen.py`; `/cv/` redirige aquí) |
| `/timeline/` | Extended History | estático: línea de tiempo con panel lateral que sigue el scroll y un buscador (`tools/gen.py` → `history_entries()`) |
| `/blog/` | Blog | Astro: índice, páginas por tag (`/blog/tags/<tag>/`) y entradas (`/blog/<en|es>/<slug>/`) |
| `/about/` | About me | estático (placeholder con el nombre) |
| `/llms.txt` | Perfil para IA | estático (`tools/gen.py`), ver abajo |
| `/cv/{en,es}/source.yaml`, `/cv/template.html` | Datos y plantilla del CV para generadores externos | estático (`tools/gen.py`), ver abajo |
| `/robots.txt` | Crawlers | estático (`public/robots.txt`) |

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

### Buscar en el timeline

La barra `grep -i` arriba del timeline (se queda pegada al hacer scroll; `/` la enfoca) filtra las entradas y el filtro viaja en la URL, así que un link como `/timeline/?q=aws` abre la página ya filtrada:

- Varias palabras se combinan con **O** (`lead aws` = cualquiera de las dos); `"tech lead"` busca la frase. Sin distinguir mayúsculas ni acentos, y solo en el idioma que está en pantalla.
- Un año (`2021`) o un rango (`2009-2011`) conserva las entradas cuyo periodo lo cubre; un hijo sin fecha hereda el periodo de su padre.
- Las entradas sin coincidencia se **atenúan**: quedan solo el puesto, la empresa y las fechas, y el panel lateral las salta.
- En las que sí coinciden, los bloques que no mencionan el término se pliegan a una línea `▸ // título` (clic para abrirlo); si solo coincidió el encabezado (empresa, puesto, fecha) la entrada se muestra completa. Las coincidencias se resaltan.
- `// filters` despliega chips de tech, industria y tipo; cada chip solo agrega (o quita) su palabra al buscador. La `×` (o Esc) limpia todo.

Hasta **dos niveles**: cualquier entrada acepta `children=[…]` (en un empleo de `JOBS`, `history_children=[…]`) con dicts del mismo formato; se dibujan anidados y el panel lateral indica `↳ inside <padre>`. Guía completa en [`docs/adding-history-entries.md`](docs/adding-history-entries.md).

## Perfil para IA (`/llms.txt`)

[`/llms.txt`](https://llmstxt.org) es el perfil en Markdown para LLMs y crawlers de IA (ChatGPT, Claude, Perplexity…): el CV y el timeline completos en un solo archivo, en inglés: resumen, contacto, skills, un renglón por empleo, la historia completa de cada uno y links.

- Sale de los **mismos datos** que el CV y el timeline: `python3 tools/gen.py` lo escribe en `public/` (no editar a mano), así que basta regenerar como con cualquier cambio del CV.
- Los años de experiencia (año actual − 2010, igual que el CV) se calculan al correr `gen.py`: regenera una vez al año para que no se queden atrás.
- `public/robots.txt` deja pasar a todos los crawlers y los aleja de `/Backups/` y `/favicons/`, que repiten el CV en borradores de diseño.

## Datos del CV para generadores externos (`/cv/`)

Para armar CVs enfocados desde otro proyecto, `python3 tools/gen.py` publica el CV como datos, de los **mismos datos** que el CV, el timeline y About (no editar a mano):

- **`/cv/en/source.yaml`** y **`/cv/es/source.yaml`** — todo en un idioma por archivo: `meta`, `profile` (nombre, roles, resumen, bio), `contact`, `stats`, `skills`, `languages`, `experience`, `education`, `other`, `shipped_titles`, `toolbox` y `labels` (títulos de sección en pantalla y para ATS, meses, "Actualidad"…). Cada entrada del timeline trae todo lo largo (`summary`, `facts`, `highlights`, `sections`, `achievements`, `stack`, `links`, `children`), y los empleos y títulos además un bloque `cv` con exactamente lo que imprime el CV de una hoja.
- **`/cv/template.html`** — el CV actual como plantilla [Mustache](https://mustache.github.io): el mismo HTML y CSS (autocontenido), con etiquetas donde va el contenido. Se renderiza con **cualquier** motor Mustache (mustache.js, Stubble en C#, JMustache en Java, chevron en Python) usando un `source.yaml` como vista:
  1. Convierte cada texto a HTML: escapa `& < > "` y luego `**x**` → `<b>x</b>`, `[x](url)` → `<a href="url">x</a>` (por eso la plantilla usa `{{{triple llave}}}`).
  2. Para un CV enfocado, recorta los datos antes de renderizar (`experience`, los `cv.highlights` de cada empleo, `skills.technologies`…): cada lista pinta lo que trae, en orden.
  3. Imprime a PDF desde un navegador (A4, sin márgenes, con fondos; en Chromium `page.pdf` con `preferCSSPageSize` y `printBackground`).
  - En `<html>`: `data-theme="dark"` para el tema oscuro, `data-print="ats"` para el PDF de una columna para ATS.
  - Sin lógica a propósito (solo secciones, secciones invertidas, nombres con punto y `{{.}}`): los datos traen ya calculado lo que la página calcula con JS (duración de cada empleo en `dates.elapsed`, la barra ASCII de cada skill en `meter`), y lo que dependía del marcado (íconos de contacto, separadores de roles) va en CSS.
  - Probado: mustache.js y chevron dan el mismo HTML byte a byte, y el render se ve igual al CV publicado salvo el gris de los "Tech: …" en los puntos de Wizeline (el Markdown del YAML no lleva ese matiz).

Reglas del formato, pensadas para leerlo de forma determinista:

- Un solo documento YAML por archivo; los metadatos van en `meta:` (primer bloque), no en un segundo documento.
- Todo texto va entre comillas dobles, así ningún parser adivina tipos (`"2020-03"` y `"no"` siguen siendo texto). Las fechas son `"YYYY-MM"`; `dates.end: null` con `ongoing: true` = actualidad.
- El texto solo puede traer `**negritas**` y `[texto](url)`; `gen.py` falla si un texto choca con eso.
- Los `id` son estables e iguales en los dos idiomas: empleos y títulos usan su `slug` (el mismo ancla de `/timeline/#h-<slug>`); secciones y logros usan `<id-de-la-entrada>/<título en inglés>`. Si renombras el título de un logro o de un grupo, su `id` cambia: fíjalo con `id="…"` en su `dict` si ya lo usa un generador.
- Si PyYAML está instalado, `gen.py` vuelve a leer cada archivo y verifica que salga igual a los datos; sin PyYAML solo lo escribe.
- `meta.schema` (`cv-source/1`, `cv-template/1`) sube cuando se renombra o se quita una llave; agregar llaves no lo cambia.

## Desarrollo local

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # genera dist/
python3 tools/gen.py   # regenera las páginas estáticas (CV, About, Timeline, Backups), src/shell/ y llms.txt (requiere Python 3.12+)
```

- `public/Backups/` — las 9 variantes de diseño evaluadas (`public/Backups/index.html` es el selector).
- `public/favicons/` — las 6 opciones de favicon; la elegida está en `public/` como `favicon.svg`, `favicon.ico` y `apple-touch-icon.png`.
- `src/shell/` — CSS, head, header y scripts del cascarón, exportados por `tools/gen.py` y usados por `src/layouts/Shell.astro`. No editar a mano.
- `public/cv-export.js` — la descarga en PDF/DOCX. Este sí se edita a mano; `tools/gen.py` solo lo enlaza desde el CV junto con el JSON de datos.
