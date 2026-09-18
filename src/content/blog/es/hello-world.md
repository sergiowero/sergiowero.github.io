---
title: "Hola, mundo"
description: "Primera entrada: cómo está hecho este blog y cómo agregar una entrada en inglés y en español."
pubDate: 2026-09-18
tags: ["meta", "astro", "github-pages"]
---

Este blog es parte de mi sitio y comparte el mismo cascarón que el CV: mismo fondo, misma hoja, mismo encabezado, y los interruptores de **oscuro / claro** y **ES / EN** conservan su estado entre páginas.

## Cómo se publica una entrada

1. Escribe un archivo Markdown en `src/content/blog/es/` (y, opcionalmente, la versión en inglés con el **mismo nombre de archivo** en `src/content/blog/en/`).
2. Haz commit y push a `main`.
3. GitHub Actions construye el sitio con [Astro](https://astro.build) y lo publica en GitHub Pages.

El front matter se ve así:

```yaml
---
title: "Hola, mundo"
description: "Una línea que se muestra en el índice."
pubDate: 2026-09-18
tags: ["meta", "astro"]
---
```

> Cuando una entrada existe en ambos idiomas, el interruptor ES / EN salta entre las dos versiones.

Eso es todo: nada que compilar localmente, ningún HTML que tocar.
