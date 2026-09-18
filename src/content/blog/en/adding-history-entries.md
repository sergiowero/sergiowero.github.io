---
title: "How to add entries to the History page"
description: "A step-by-step guide to the timeline data in tools/gen.py — and a showcase of every Markdown format this blog renders."
pubDate: 2026-09-19
tags: ["meta", "history", "markdown", "how-to"]
---

The **History** tab is generated from a small Python list in `tools/gen.py`. This post walks through adding an entry, and doubles as a *format test*: headings, lists, tables, code, quotes, footnotes… everything the blog can render.

## 1. Where the data lives

There are two sources, both in `tools/gen.py`:

| Source | What it holds | Shows up in |
|---|---|---|
| `JOBS` | Employment history (role, company, dates, bullets, industries, tech) | Resume **and** History |
| `EXTRA_HISTORY` | Anything else: talks, projects, certifications, milestones | History only |

Education is added automatically from `EDU`, so you never touch that.

## 2. Add a job (Resume + History)

Append a `dict` to `JOBS`. Newest first is the convention, but the History page sorts by date anyway.

```python
dict(
    role="Staff Engineer",
    co="Acme Corp",
    tech=["Go", "AWS", "PostgreSQL"],          # chips in the History side panel
    period="Mar 2027 — Present",              # only a no-JS fallback; dates are computed from frm/to
    frm="2027-03", to=None,                   # to="YYYY-MM" once it ends, None = present
    loc="Guadalajara, México",
    cur=True,                                 # highlights the entry in the Resume timeline
    inds=["Fintech", "Payments"],             # industry tags
    pts=[
        "<b>Payments platform:</b> led the migration to event-driven services.",
        "Cut p95 latency by 40% by moving hot paths to Go.",
    ],
),
```

> **Tip:** bullets are HTML, so `<b>…</b>` and `<a href="…">…</a>` work inside `pts`.

## 3. Add anything else (History only)

Append to `EXTRA_HISTORY`:

```python
EXTRA_HISTORY = [
    dict(kind="milestone", slug="unity-talk-2023",
         role="Speaker — IoC & DI patterns for Unity",
         co="Game Dev Meetup GDL",
         frm="2023-05",                       # single date: no `to`
         loc="Guadalajara, México",
         inds=["Community"], tech=["Unity", "C#"],
         pts=["45-minute talk plus live demo of the modular architecture used in <i>The Lullaby of Life</i>."]),
]
```

### Field reference

- `kind` — `job`, `education` or `milestone`. Changes the marker on the timeline:
  - `job` → circle
  - `education` → diamond
  - `milestone` → circle (for now)
- `slug` — used in the panel header: `cat history/<slug>.md`
- `frm` / `to` — `"YYYY-MM"`. Omit `to` for a one-day event; `to=None` means *present*.
- `inds`, `tech` — chips; either can be `[]`.
- `pts` — bullets (HTML allowed); `[]` hides the list.

#### Checklist before you regenerate

- [x] Dates in `YYYY-MM`
- [x] `slug` is unique
- [ ] `tech` chips are short (one or two words)
- [ ] Bullets start with a verb

## 4. Regenerate and publish

```bash
python3 tools/gen.py
```

```bash
git add -A && git commit -m "History: add Acme Corp" && git push
```

GitHub Actions rebuilds the site in about a minute. Duration labels such as `6 yrs 8 mos` are computed **in the browser**, so they stay current without touching anything.

---

## Appendix: format showcase

Text styles: **bold**, *italic*, ***both***, ~~strikethrough~~, `inline code`, and a [link to the History page](/history/). Footnotes work too[^1].

1. Ordered lists
2. With several items
   1. and nested numbers
   2. like this
3. Back to the top level

- Unordered lists
  - with nested bullets
    - three levels deep

> A blockquote.
>
> — with more than one paragraph, and **bold** inside.

Code with a different language:

```yaml
title: "Hello, world"
pubDate: 2026-09-18
tags: ["meta", "astro"]
```

```js
const years = new Date().getFullYear() - 2010;
console.log(`${years}+ years building software`);
```

An image (the site favicon), sized with an HTML `<img>` tag:

<img src="/favicon.svg" alt="Braces favicon" width="64" height="64">

<details>
<summary>Raw HTML also works — click to expand</summary>

This block is a `<details>` element written directly in the Markdown file.

</details>

Emoji: 🚀 🎮 🤖

[^1]: This is the footnote. It is rendered at the bottom of the post.
