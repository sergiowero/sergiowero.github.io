---
title: "Cómo agregar entradas a la página de Historial"
description: "Guía paso a paso de los datos de la línea de tiempo en tools/gen.py (incluidas entradas de dos niveles) — y una muestra de todos los formatos Markdown que renderiza este blog."
pubDate: 2026-09-19
tags: ["meta", "history", "markdown", "how-to"]
---

La pestaña **Historial** se genera a partir de una pequeña lista en Python dentro de `tools/gen.py`. Esta entrada explica cómo agregar un elemento y, de paso, sirve como *prueba de formatos*: encabezados, listas, tablas, código, citas, notas al pie… todo lo que el blog puede renderizar.

## 1. Dónde viven los datos

Hay dos fuentes, ambas en `tools/gen.py`:

| Fuente | Qué contiene | Aparece en |
|---|---|---|
| `JOBS` | Historial laboral (puesto, empresa, fechas, bullets, industrias, tech) | Resume **e** Historial |
| `EXTRA_HISTORY` | Todo lo demás: charlas, proyectos, certificaciones, hitos | Solo Historial |

La educación se agrega sola desde `EDU`, así que eso no se toca.

## 2. Agregar un empleo (Resume + Historial)

Agrega un `dict` a `JOBS`. Por convención van del más reciente al más antiguo, aunque el Historial ordena por fecha de todos modos.

```python
dict(
    role="Staff Engineer",
    co="Acme Corp",
    tech=["Go", "AWS", "PostgreSQL"],          # chips en el panel lateral del Historial
    period="Mar 2027 — Present",              # solo respaldo sin JS; las fechas se calculan de frm/to
    frm="2027-03", to=None,                   # to="YYYY-MM" cuando termine, None = presente
    loc="Guadalajara, México",
    cur=True,                                 # resalta la entrada en la línea de tiempo del Resume
    inds=["Fintech", "Payments"],             # etiquetas de industria
    pts=[
        "<b>Plataforma de pagos:</b> lideré la migración a servicios orientados a eventos.",
        "Reduje la latencia p95 un 40% moviendo las rutas críticas a Go.",
    ],
),
```

> **Tip:** los bullets son HTML, así que `<b>…</b>` y `<a href="…">…</a>` funcionan dentro de `pts`.

## 3. Agregar cualquier otra cosa (solo Historial)

Agrega a `EXTRA_HISTORY`:

```python
EXTRA_HISTORY = [
    dict(kind="milestone", slug="unity-talk-2023",
         role="Speaker — Patrones IoC y DI para Unity",
         co="Game Dev Meetup GDL",
         frm="2023-05",                       # fecha única: sin `to`
         loc="Guadalajara, México",
         inds=["Community"], tech=["Unity", "C#"],
         pts=["Charla de 45 minutos con demo en vivo de la arquitectura modular usada en <i>The Lullaby of Life</i>."]),
]
```

### Dos niveles: entradas dentro de una entrada

Cualquier entrada puede llevar `children` —una lista de dicts iguales— y se dibujan como una línea de tiempo anidada debajo de ella. Así están modelados los cuatro proyectos de Wizeline: el empleo es el padre y cada proyecto de cliente es un hijo.

Para un empleo de `JOBS`, pon los hijos en `history_children` (el Resume conserva sus bullets normales; solo el Historial los anida):

```python
dict(role="Senior Software Engineer / Tech Lead", co="Wizeline", frm="2020-02", to=None, …,
     history_children=[
         dict(kind="project", slug="wizeline-global-news", role="Global News Industry", co="Wizeline client",
              loc="Remote", inds=["News"], tech=[".NET", "AWS", "PostgreSQL", "Claude Code"],
              pts=["Engineered new features and resolved production issues…"]),
         dict(kind="milestone", slug="wizeline-tech-lead", role="Promoted to Tech Lead", co="Wizeline",
              frm="2022-03", loc="Remote", inds=[], tech=[], pts=[]),
     ]),
```

Para cualquier cosa en `EXTRA_HISTORY`, usa `children` directamente:

```python
dict(kind="milestone", slug="gamejam-2024", role="Game jam — 1er lugar", co="GDL Jam", frm="2024-10",
     loc="Guadalajara, México", inds=["Gaming"], tech=["Unity"], pts=[],
     children=[
         dict(kind="project", slug="gamejam-2024-game", role="El juego", co="Equipo de 3", inds=[], tech=["C#"],
              pts=["Prototipo de 48 horas, después pulido para itch.io."]),
     ]),
```

Reglas prácticas:

- **Solo dos niveles** — los hijos no pueden tener hijos.
- Los hijos pueden omitir `frm`/`to`; los que no tienen fecha conservan el orden en que los escribiste, después de los que sí la tienen.
- Cuando un empleo tiene `history_children`, sus propios bullets se ocultan en el Historial (los hijos cuentan la historia); el Resume no cambia.
- El panel lateral muestra `↳ inside <padre>` y la mini-línea de tiempo anida a los hijos, así que siempre se sabe dónde estás.

### Referencia de campos

- `kind` — `job`, `project`, `education` o `milestone`. Cambia el marcador en la línea de tiempo:
  - `job` → círculo
  - `project` → cuadrado
  - `education` → rombo
  - `milestone` → pin
- `slug` — se usa en el encabezado del panel: `cat history/<slug>.md`
- `frm` / `to` — `"YYYY-MM"`. Omite `to` para un evento de un solo día; `to=None` significa *presente*.
- `inds`, `tech` — chips; cualquiera puede ser `[]`.
- `pts` — bullets (se permite HTML); `[]` oculta la lista.
- `children` (o `history_children` en un empleo) — entradas anidadas, un solo nivel.

#### Checklist antes de regenerar

- [x] Fechas en `YYYY-MM`
- [x] `slug` único
- [ ] Chips de `tech` cortos (una o dos palabras)
- [ ] Bullets que empiezan con un verbo

## 4. Regenerar y publicar

```bash
python3 tools/gen.py
```

```bash
git add -A && git commit -m "History: add Acme Corp" && git push
```

GitHub Actions reconstruye el sitio en aproximadamente un minuto. Las duraciones como `6 yrs 8 mos` se calculan **en el navegador**, así que se mantienen al día sin tocar nada.

---

## Apéndice: muestra de formatos

Estilos de texto: **negritas**, *cursivas*, ***ambas***, ~~tachado~~, `código en línea` y un [enlace a la página de Historial](/history/). Las notas al pie también funcionan[^1].

1. Listas ordenadas
2. Con varios elementos
   1. y números anidados
   2. como este
3. De vuelta al nivel superior

- Listas sin orden
  - con viñetas anidadas
    - tres niveles de profundidad

> Una cita.
>
> — con más de un párrafo, y **negritas** adentro.

Código en otro lenguaje:

```yaml
title: "Hola, mundo"
pubDate: 2026-09-18
tags: ["meta", "astro"]
```

```js
const years = new Date().getFullYear() - 2010;
console.log(`${years}+ años construyendo software`);
```

Una imagen (el favicon del sitio), con tamaño fijado con una etiqueta HTML `<img>`:

<img src="/favicon.svg" alt="Favicon de llaves" width="64" height="64">

<details>
<summary>El HTML crudo también funciona — clic para expandir</summary>

Este bloque es un elemento `<details>` escrito directamente en el archivo Markdown.

</details>

Emoji: 🚀 🎮 🤖

[^1]: Esta es la nota al pie. Se renderiza al final de la entrada.
