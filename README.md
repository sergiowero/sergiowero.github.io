# sergiowero.github.io

Sitio personal de Sergio de Jesús Sánchez Robles. Se construye con [Astro](https://astro.build) y se publica en GitHub Pages con GitHub Actions en cada push a `main`.

| Ruta | Sección | Origen |
|---|---|---|
| `/` | Resume / CV | estático (`public/index.html`, generado por `tools/gen.py`; `/cv/` redirige aquí) |
| `/timeline/` | Extended History | estático: línea de tiempo con panel lateral que sigue el scroll y un buscador (`tools/gen.py` → `history_entries()`) |
| `/blog/` | Blog | Astro: índice, páginas por tag (`/blog/tags/<tag>/`) y entradas (`/blog/<en|es>/<slug>/`) |
| `/about/` | About me | estático (placeholder con el nombre) |
| `/llms.txt` | Perfil para IA | estático (`tools/gen.py`), ver abajo |
| `/cv/{en,es}/tree.json`, `/cv/tree.schema.json`, `/cv/template.html` | El timeline como árbol de records, su esquema y la plantilla del CV | estático (`tools/gen.py`), ver abajo |
| `/tailor-cv/<empresa>-<puesto>-<aaaammdd>.html` (y `.md`) | El CV adaptado a una vacante, y la vacante junto a él | estático (`tools/tailor.py`, skill `/tailor-cv`), ver abajo |
| `/robots.txt` | Crawlers | estático (`public/robots.txt`) |
| `/og/<página>.png` | Imagen de la link card de cada página | Astro, en el build (`src/pages/og/[...card].png.ts`), ver abajo |

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
   `title`, `description`, fecha y tags son también lo que muestra su link card (sin `description`, se usa el primer párrafo).
3. `git push` → GitHub Actions construye y despliega (≈1 min), con la imagen de su link card incluida.

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

## Link cards (vista previa al compartir un link)

Cada página trae su `<title>`, `description`, `canonical` y las etiquetas Open Graph y Twitter, así que un link pegado en WhatsApp, LinkedIn, Slack, X, Discord o Teams se ve como una tarjeta con título, resumen e imagen propios:

| Página | Tarjeta | Imagen |
|---|---|---|
| `/` (y `/cv/`) | nombre, roles, años de experiencia, industrias, skills, foto | `/og/cv.png` |
| `/timeline/` (y `/history/`) | periodo, empresas y proyectos de cliente | `/og/timeline.png` |
| `/about/` | bio, herramientas, foto | `/og/about.png` |
| `/blog/` | número de entradas, tags | `/og/blog.png` |
| `/blog/<en\|es>/<slug>/` | título, descripción, fecha, tiempo de lectura, tags (`og:type` `article`) | `/og/blog/<en\|es>/<slug>.png` |
| `/blog/tags/<tag>/` | entradas con ese tag | `/og/blog/tags/<tag>.png` |

- Las imágenes (1200×630, diseño "Dark Terminal") se dibujan en el build con [satori](https://github.com/vercel/satori) + [resvg](https://github.com/yisibl/resvg-js): una sola plantilla en `src/lib/og.ts`, el contenido de cada tarjeta en `src/lib/cards.ts`. No se guardan en el repo: una entrada nueva del blog tiene la suya en el siguiente deploy sin hacer nada.
- CV, Timeline y About salen de los **mismos datos** que las páginas: `python3 tools/gen.py` escribe sus etiquetas en el HTML y el contenido de sus imágenes en `src/shell/cards.json`. Los años de experiencia se cuentan al correr `gen.py`, igual que en `/llms.txt`.
- Van en inglés (el idioma que lee un crawler; ES se elige en el navegador), con `og:locale:alternate` `es_MX`. Las entradas del blog van en su idioma.
- Slack muestra además dos datos bajo la tarjeta (`twitter:label1/2`): experiencia y ubicación, empresas, tiempo de lectura y tags…
- Para verla antes de compartir: `npm run dev` y abre `http://localhost:4321/og/cv.png`. Ya publicada, los depuradores de cada red la vuelven a leer si cambió: [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/), [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/). WhatsApp y X guardan la tarjeta en caché un tiempo, así que un cambio puede tardar en verse ahí.

## Perfil para IA (`/llms.txt`)

[`/llms.txt`](https://llmstxt.org) es el perfil en Markdown para LLMs y crawlers de IA (ChatGPT, Claude, Perplexity…): el CV y el timeline completos en un solo archivo, en inglés: resumen, contacto, skills, un renglón por empleo, la historia completa de cada uno y links.

- Sale de los **mismos datos** que el CV y el timeline: `python3 tools/gen.py` lo escribe en `public/` (no editar a mano), así que basta regenerar como con cualquier cambio del CV.
- Los años de experiencia (año actual − 2010, igual que el CV) se calculan al correr `gen.py`: regenera una vez al año para que no se queden atrás.
- `public/robots.txt` deja pasar a todos los crawlers y los aleja de `/Backups/` y `/favicons/`, que repiten el CV en borradores de diseño.

## El timeline como árbol de records (`/cv/`)

Para armar CVs dinámicos desde otro programa, `python3 tools/gen.py` publica todo el timeline como un **árbol de records tipados**, de los mismos datos que el CV, el timeline y About (no editar a mano). **El timeline (`/timeline/`) se dibuja desde ese mismo árbol**, así que la página y el JSON no pueden diferir.

- **`/cv/en/tree.json`** y **`/cv/es/tree.json`** — un archivo por idioma, con los mismos `id`, la misma estructura y los mismos tags:
  - `records` — cada nodo del árbol, en orden de página. Todos tienen **las mismas llaves** (`null` o `[]` cuando no aplican). Tipos (`type`): `person` (la raíz), `job`, `project` (trabajo para un cliente dentro de un empleo), `education`, los logros `milestone`, `release`, `prototype`, `award`, `pace`, `training` (y `talk`), `topic` (un área de trabajo con título dentro de una entrada) y `highlight` (cada bullet). `category` los agrupa: position, work, education, achievement, content.
  - Cada record trae `tech` (ids del catálogo de tecnologías), `tags` (ids del vocabulario) y `tag_sources` (de dónde salió cada tag). También `context` (empleo, cliente, rol, periodo, lugar e industria heredados de sus ancestros) y `embedding_text` (un texto plano autocontenido listo para embeddings o para un prompt).
  - `tree` — la misma estructura como ids anidados; `parent`, `children` y `path` en cada record dicen lo mismo.
  - `vocabulary` — los tipos; los tags con su faceta (domain, practice, competency, outcome, industry); y las tecnologías con categoría, alias, tags implícitos, dominio autoevaluado (`proficiency`) y `usage` (en qué entradas aparece, meses, años; `exact: false` cuando parte del tiempo viene de un proyecto sin fechas).
  - `profile` — la persona: nombre, roles, resumen, bio, contacto, idiomas.
  - `resume` — el CV de una hoja como vista lista para `template.html`; sus `highlight_ids` apuntan a records.
- **`/cv/tree.schema.json`** — el spec: JSON Schema (2020-12) de cada tipo y campo, con los enums del vocabulario (un validador rechaza un tag o una tecnología que no existe).
- **`/cv/template.html`** — el CV actual como plantilla [Mustache](https://mustache.github.io), autocontenida. Se renderiza con **cualquier** motor Mustache (mustache.js, Stubble en C#, JMustache en Java, chevron en Python) usando `resume` como vista:
  1. Convierte cada texto a HTML: escapa `& < > "` y luego `**x**` → `<b>x</b>`, `[x](url)` → `<a href="url">x</a>` (por eso la plantilla usa `{{{triple llave}}}`).
  2. Para enfocar el CV, edita la vista: deja en `experience` los empleos que quieras y pon en sus `highlights` el `text` de los records `highlight` que elegiste (por tags, tech o embeddings). Cada lista pinta lo que trae, en orden.
  3. Imprime a PDF desde un navegador (A4, sin márgenes, con fondos; en Chromium `page.pdf` con `preferCSSPageSize` y `printBackground`).
  - En `<html>`: `data-theme="dark"` para el tema oscuro, `data-print="ats"` para el PDF de una columna para ATS.

### Tecnologías y tags (en `tools/gen.py`)

- **`TECH_CATALOG`** — cada tecnología: nombre, categoría (language, framework, cloud, database, engine, platform, ai-tool…), padre (`aws-lambda` → `aws`), los alias con que la escriben los datos (`"Java 11"` → `java`), el patrón que la encuentra en un texto y los tags que implica (`unity` → `game-dev`).
- **`TAGS`** — el vocabulario controlado: faceta, etiqueta en los dos idiomas, un patrón de palabras clave sobre el texto en inglés y los alias de las listas `tech=[…]` que en realidad son prácticas o competencias (`"Mentorship"` → `mentoring`, `"Outbox pattern"` → `reliable-messaging`).
- Los tags de un record salen de reglas deterministas: su stack, las tecnologías que menciona su texto, palabras clave, su tipo (`release` → `shipped`), su industria y si es remoto. A mano: `tags=["…"]` en una entrada, un grupo o un logro.
- Cada cadena de un `tech=[…]` tiene que existir en `TECH_CATALOG` o en los alias de `TAGS`: si agregas una nueva, `gen.py` se detiene y te dice cuál falta.

Reglas que un programa puede dar por hechas (`gen.py` se detiene si alguna falla):

- Los `id` son estables e iguales en los dos idiomas: las entradas usan su `slug` (el mismo ancla de `/timeline/#h-<slug>`); topics y logros usan `<entrada>/<título en inglés>` (fíjalo con `id="…"` en su `dict` si ya lo usa un generador); los highlights son posicionales (`<padre>/<n>`, o `<empleo>/cv<n>` para un bullet que solo sale en el CV).
- Cada record tiene las mismas llaves; cada `parent` lista a su hijo; `tech` y `tags` solo usan ids del vocabulario; los árboles en inglés y en español tienen la misma estructura, tech y tags.
- El texto solo trae `**negritas**` y `[texto](url)`. Las fechas son `"YYYY-MM"`; `dates.end: null` con `ongoing: true` es actualidad.
- `meta.schema` (`cv-tree/1`) sube cuando se renombra o se quita una llave; agregar llaves no lo cambia.

## CVs adaptados a una vacante (`/tailor-cv/`)

Con Claude Code, **`/tailor-cv`** seguido de la vacante (el texto, un archivo o un link) arma un CV adaptado a ella y lo deja en el repo. La skill vive en [`.claude/skills/tailor-cv/SKILL.md`](.claude/skills/tailor-cv/SKILL.md) y usa [`tools/tailor.py`](tools/tailor.py) para todo lo mecánico. Cada CV son tres archivos con el mismo nombre, `<empresa>-<puesto>-<aaaammdd>` (p. ej. `acme-senior-backend-engineer-20260929`):

| Archivo | Qué es |
|---|---|
| `tailor-cv/<nombre>.json` | el **spec**: qué muestra este CV en lugar del maestro y de qué records de `tree.json` sale cada bullet (no se publica) |
| `public/tailor-cv/<nombre>.html` | el **CV**, en `/tailor-cv/<nombre>.html` |
| `public/tailor-cv/<nombre>.md` | la **vacante** a la que responde, tal como llegó, con un front matter (empresa, puesto, fecha, idioma, link) |

- **Mismo diseño que el CV maestro**, porque lo dibuja el mismo código: `gen.cv_page()` arma `public/index.html` y cada CV adaptado, con el spec como vista (`gen.master_view()` es la del maestro). Trae el cambio ES/EN, el tema y las tres descargas (DOCX ATS, PDF ATS y PDF), con archivos que llevan la vacante en el nombre (`Sergio-Sanchez-CV-Acme-Senior-Backend-Engineer-EN.pdf`). Abre en el idioma de la vacante (`<html data-default-lang>`; si el visitante ya eligió uno, gana el suyo) y lleva `noindex` para que no aparezca en buscadores.
- **Qué cambia y qué no** (`tailor.py build` rechaza un spec que rompa una regla):
  - Siempre los **6 empleos** del maestro, en su orden; puesto, empresa, fechas, lugar e industrias son los del maestro. Contacto, stats, IA, educación e idiomas no se tocan.
  - Un empleo **con hijos** (Wizeline y sus clientes) muestra solo los clientes relevantes para la vacante (`tailored`). Si ninguno lo es (`fallback`), muestra el bullet de cada uno reescrito hacia la vacante. En los dos casos puede sumar bullets del propio empleo (rol, IA, mentoría) si son relevantes.
  - Un empleo **sin hijos** muestra solo los bullets relevantes (`tailored`). Si nada lo es (`fallback`), muestra sus bullets de siempre, uno por uno, reescritos para encajar lo mejor posible.
  - El número de bullets por empleo es libre. El **perfil** cambia un poco. Los **roles** pueden reordenarse o ser menos, pero nunca nuevos.
  - **Core skills**, chips de tecnologías y "Fortalezas" solo cambian por lo que la vacante **exige** (`jd.required`, cada uno con la frase de la vacante que lo pide) y el árbol respalda. Los niveles salen de `CORE` o de **`CORE_EXTRA`** en `tools/gen.py`, nunca del spec. `CORE_EXTRA` son niveles que tú das (1–10) a skills que el maestro no muestra como core (Unity3D, por ejemplo) para que una vacante que los exige pueda subirlos.
- **Sin mentir**: cada bullet cita sus `sources`, y `build` rechaza cualquier tecnología o número que esas fuentes no respalden. También rechaza las tecnologías que no están en ninguna parte del árbol (`UNBACKED` en `tools/tailor.py`: Kubernetes, Kafka…), que van a `jd.gaps` para que sepas qué pide la vacante que tu historia no muestra. Si sí lo tienes, agrégalo al timeline en `gen.py`.
- **Una hoja**: `build` imprime el CV a PDF con Chrome/Chromium/Edge en modo headless (`TAILOR_CHROME=<ruta>` si no lo encuentra) y exige 1 página en EN y en ES, con las fuentes reales. Dice cuánto espacio le queda a la columna de experiencia (~12 px por renglón). `python3 tools/tailor.py check public/index.html` mide el maestro.
- `python3 tools/gen.py` vuelve a dibujar todos los CVs adaptados al final de cada corrida, así que siempre siguen el diseño, el contacto y las fechas del maestro.

```bash
python3 tools/tailor.py new vacante.md --company "Acme" --position "Senior Backend Engineer" --lang en   # o `new -` desde stdin
python3 tools/tailor.py analyze <nombre>          # qué pide la vacante, qué tiene el árbol y qué es relevante en cada empleo
python3 tools/tailor.py show <id> [<id>…]         # records en los dos idiomas, para escribir desde ahí
python3 tools/tailor.py build <nombre>            # valida el spec, escribe el HTML y revisa que quepa en una hoja
```

## Desarrollo local

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # genera dist/
python3 tools/gen.py   # regenera las páginas estáticas (CV, About, Timeline, Backups, /tailor-cv/), src/shell/ y llms.txt (requiere Python 3.12+)
```

- `public/Backups/` — las 9 variantes de diseño evaluadas (`public/Backups/index.html` es el selector).
- `public/favicons/` — las 6 opciones de favicon; la elegida está en `public/` como `favicon.svg`, `favicon.ico` y `apple-touch-icon.png`.
- `src/shell/` — CSS, head, header y scripts del cascarón, exportados por `tools/gen.py` y usados por `src/layouts/Shell.astro`, más `cards.json` (las link cards de CV, Timeline y About). No editar a mano.
- `public/cv-export.js` — la descarga en PDF/DOCX. Este sí se edita a mano; `tools/gen.py` solo lo enlaza desde el CV junto con el JSON de datos.
