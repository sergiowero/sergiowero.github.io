# How to add entries to the Timeline page

A step-by-step guide to the timeline data in `tools/gen.py`, including two-level entries.

The **Timeline** tab (`/timeline/`) is generated from a small Python list in `tools/gen.py`. This doc walks through adding an entry.

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

### Two levels: entries inside an entry

Any entry can carry `children` — a list of the same kind of dicts — and they are drawn as a nested timeline under it. That is how the four Wizeline engagements are modelled: the job is the parent, each client project is a child.

For a job in `JOBS`, put the children in `history_children` (the Resume keeps its normal bullets; only the History page nests them):

```python
dict(role="Senior Software Engineer / Tech Lead", co="Wizeline", frm="2020-02", to=None, …,
     history_children=[
         dict(kind="project", slug="wizeline-global-news", role="", co="Dow Jones",   # role="" → headline is just the company
              loc="Remote", inds=["News"], tech=[".NET", "AWS", "PostgreSQL", "Claude Code"],
              pts=["Engineered new features and resolved production issues…"]),
         dict(kind="project", slug="wizeline-media", role="Tech Lead", co="Fox Corp",   # a role of its own → "Tech Lead · Fox Corp"
              loc="Remote", inds=["Media & Entertainment"], tech=["Java", "Spring Boot", "AWS"], pts=["…"]),
         dict(kind="milestone", slug="wizeline-tech-lead", role="Promoted to Tech Lead", co="Wizeline",
              frm="2022-03", loc="Remote", inds=[], tech=[], pts=[]),
     ]),
```

For anything in `EXTRA_HISTORY`, use `children` directly:

```python
dict(kind="milestone", slug="gamejam-2024", role="Game jam — 1st place", co="GDL Jam", frm="2024-10",
     loc="Guadalajara, México", inds=["Gaming"], tech=["Unity"], pts=[],
     children=[
         dict(kind="project", slug="gamejam-2024-game", role="The game", co="Team of 3", inds=[], tech=["C#"],
              pts=["48-hour prototype, later polished for itch.io."]),
     ]),
```

Rules of thumb:

- **Two levels only** — children cannot have children.
- Children may omit `frm`/`to`; undated children keep the order you wrote them, after the dated ones.
- When a job has `history_children`, its own bullets are hidden on the History page (the children tell the story); the Resume is untouched.
- A job can also carry `history=dict(...)` with the long-form fields (`lede`, `facts`, `groups`, `deliverables`, `links`; `pts`/`tech` there override the Resume's on the History page only). That is how 1 Simple Idea tells its full story while the Resume keeps four bullets.
- The side panel shows `↳ inside <parent>` and the mini-timeline nests the children, so the reader always knows where they are.

### Field reference

- `kind` — `job`, `project`, `education` or `milestone`. Changes the marker on the timeline:
  - `job` → circle
  - `project` → square
  - `education` → diamond
  - `milestone` → pin
- `role` / `co` — the headline is `{role} · {co}`. The industry is **not** part of it (that is what `inds` is for); on a child that keeps its parent's position, set `role=""` and the headline is the company alone.
- `slug` — used in the panel header: `cat timeline/<slug>.md`
- `frm` / `to` — `"YYYY-MM"`. Omit `to` for a one-day event; `to=None` means *present*.
- `inds`, `tech` — chips; either can be `[]`.
- `pts` — bullets (HTML allowed); `[]` hides the list.
- `children` (or `history_children` on a job) — nested entries, one level deep.

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
