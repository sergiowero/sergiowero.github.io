---
name: tailor-cv
description: Tailor Sergio's one-page CV to a job description (JD, vacante, oferta) and publish it at /tailor-cv/<company>-<position>-<yyyymmdd>.html, with the JD saved beside it as <same name>.md. Same design and three downloads as the master CV; the content is picked and rewritten from the career tree, never invented. Use when the user pastes, links or points to a job description and wants a CV / resume / currículum for it.
argument-hint: <job description — pasted text, a file path or a URL>
---

# /tailor-cv — a CV for one job description

One run produces three files that share one name, `<company>-<position>-<yyyymmdd>` (slugged, e.g.
`acme-senior-backend-engineer-20260929`):

| File | What | Published |
|---|---|---|
| `tailor-cv/<name>.json` | the **spec**: what this CV shows instead of the master's, with the records each bullet comes from | no |
| `public/tailor-cv/<name>.html` | the **CV**, drawn by `tools/gen.py`'s own renderer: the master's exact design, EN/ES switch, DOCX ATS · PDF ATS · PDF | `/tailor-cv/<name>.html` |
| `public/tailor-cv/<name>.md` | the **job description** it answers, as given, with a small front matter | `/tailor-cv/<name>.md` |

`build` also rewrites `public/tailor-cv/index.html`, the **explorer** at `/tailor-cv/`: every tailored CV in one list,
newest first, filtered by a `grep -i` bar, with a live preview of the selected one (`tailor.py index` rewrites it alone).

`tools/tailor.py` does everything mechanical and **refuses a spec that breaks the rules** below. Your job is the
judgment (what is relevant) and the writing (EN and ES). Run it with Python 3.12+, like `gen.py`: if
`python3 --version` is older, use `python3.12` / `python3.13` (Windows: `py -3.12`).

## Rules (Sergio's, not negotiable)

Original wording:

> - debes conservar los 6 empleos principales
> - en el caso de Wizeline u otros empleos futuros con "hijos": solo muestra los hijos que sean relevantes al JD; si
>   ningún hijo es relevante, muestra el contenido que ya existe pero modifícalo de manera que se adapte al JD lo más
>   posible sin mentir; agrega contenido a Wizeline (no a los hijos) si es relevante para el JD
> - para los jobs que no tienen hijos: agrega solo los detalles en bullet points que sean relevantes; si nada de este
>   job es relevante, deja los bullet points existentes y trata de generar un texto que encaje lo mejor posible
> - el número de bullets dentro de cada job puede cambiar, no tiene que ser fijo
> - el profile o bio puede cambiar un poco para mejorar la compatibilidad con el JD
> - la información de contacto se conserva tal cual
> - las core skills deben cambiar solamente si el JD estrictamente pide ciertos skills que sí tenemos
> - la salida es una página ATS friendly en /tailor-cv/{name}.html, con exactamente el estilo del CV maestro y sus
>   3 botones de descarga; el job description se guarda junto al CV, mismo nombre, extensión .md

What that means in the spec (`build` enforces every line):

- **The 6 jobs**, in the master's order, each with ≥ 1 bullet. Titles, companies, dates, places and industries always
  come from the master; so do contact, stats, the AI box, education and languages — the spec has no key for them.
- **A job with children** (Wizeline → Dow Jones, Fox Corp, Inditex, Cerby; any future job with client projects):
  - `"mode": "tailored"` — bullets only for the **relevant** children (`"child": "<id>"`), one or two each.
  - `"mode": "fallback"` — no child is relevant: **every** child's master bullet, in order, rewritten toward the JD
    without lying (each cites its master bullet, e.g. `wizeline/cv2`).
  - Either mode may add bullets from the job's **own** content (no `child`): Wizeline's role, AI work, mentoring and
    training — only when relevant to the JD.
- **A job without children**:
  - `"tailored"` — only the relevant bullets, from any of its records (master bullets or timeline highlights).
  - `"fallback"` — nothing is relevant: its master bullets **one for one**, reworded to fit the JD as well as the
    truth allows.
- **Bullets** — any number per job. Each one cites `sources` (record ids) inside its job; a child bullet, inside that
  child. The text may not name a technology, tool or number its sources don't back, nor anything in
  `tools/tailor.py` → `UNBACKED` (technologies that are nowhere in the tree).
- **Summary** — may change a little (`build` warns under ~50% of the master's wording). Write `{years}` for the years
  of experience. **Roles** — the master's, reordered or fewer, never new ones.
- **Skills** — core skills, the tech chips and "Best skills" change **only** through `jd.required`: the JD's strict
  requirements (must-have, not nice-to-have) that the tree backs, each with a quote copied from the JD. What they name
  moves to the front; a required technology with no chip gets one. Levels come from `gen.CORE` / `gen.CORE_EXTRA`,
  never from the spec. Empty `required` → exactly the master's skills.
- **One sheet**: the plain PDF must stay one A4 page in EN and in ES (`build` prints the free space).

## Workflow

### 1. Get the job description

Pasted text as is; a file path → read it; a URL → fetch it (WebFetch) and keep the posting's text only (drop the
site's menus and footers). Work out, from the JD itself:

- `--company` and `--position` as the JD writes them (they name the files and title the page);
- `--lang`: the JD's language, `en` or `es` — the page opens in it (the other one is a click away);
- `--url` where it was published, if known.

If the company or the position isn't in the JD, ask the user; never guess them.

### 2. Start the spec

```bash
python3 tools/tailor.py new - --company "Acme" --position "Senior Backend Engineer" --lang en --url "https://…" <<'EOF'
<the job description>
EOF
```

This saves the JD as `public/tailor-cv/<name>.md` and writes `tailor-cv/<name>.json` as **the master CV** (every job in
`fallback`, the master's summary, no requirements) — a valid spec you now edit. `--force` starts an existing one over;
`--date YYYY-MM-DD` if it is not today's.

### 3. Read the JD against the tree

```bash
python3 tools/tailor.py analyze <name>
```

It lists what the JD names that the tree has (technologies with years and jobs; practices; competencies), the **gaps**
(named in the JD, nowhere in the tree), `jd.required` candidates with a quote each, and then, job by job, the master
bullets, the job's own content and each child, ranked by overlap with the JD. It is a helper: **your reading of the JD
decides**. For a Spanish JD the tag patterns (English) miss things: put the ids of what you read in it in the spec's
`jd.terms` (e.g. `["game-dev", "leadership", "dependency-injection"]`, ids from `public/cv/en/tree.json` →
`vocabulary`) — `analyze` and `build`'s relevance hints use them — or try them first with `--also game-dev,leadership`.

### 4. Decide, job by job, and write down why

For each job, in `why`: which children / records are relevant to this JD and why, or that none is (→ `fallback`).
Relevant means it shows something the JD asks for — its must-haves first, then its responsibilities; a nice-to-have
alone rarely makes a child relevant. Irrelevant children are **left out**, not squeezed in.

### 5. Read the records you will write from, in both languages

```bash
python3 tools/tailor.py show wizeline-media/tech-lead/1 wizeline-media/legacy-media-cloud-video-migration-service …
```

Containers count as sources too: an entry's lede (`wizeline-media`), a milestone with its result
(`wizeline-media/legacy-media-cloud-video-migration-service`), a topic.

### 6. Write the spec

Edit `tailor-cv/<name>.json`:

```json
{
  "schema": "tailor-cv/1",
  "name": "acme-senior-backend-engineer-20260929",
  "jd": {
    "company": "Acme", "position": "Senior Backend Engineer", "date": "2026-09-29", "lang": "en", "url": "https://…",
    "terms": [],
    "required": [{"id": "java", "quote": "Strong experience with Java and Spring Boot."}],
    "gaps": ["Kubernetes", "Java 17 (the tree has Java 8 and 11)"]
  },
  "profile": {
    "summary": {"en": "… with **{years} years of experience** …", "es": "… con **{years} años de experiencia** …"},
    "roles": ["Senior Software Engineer", "Backend & Full-Stack", "Tech Lead", "AI-Assisted"],
    "sources": []
  },
  "experience": [
    {"id": "wizeline", "mode": "tailored", "why": "Fox Corp and Inditex match the Java/AWS stack; Cerby does not …",
     "bullets": [
       {"child": "wizeline-media", "en": "Tech Lead of a squad of 5 engineers …", "es": "Tech Lead de un equipo de 5 …",
        "tech": ["Java", "Spring Boot", "Amazon SQS"], "sources": ["wizeline-media", "wizeline-media/tech-lead/1"]},
       {"en": "Trained by Wizeline as **mentor** …", "es": "Formado por Wizeline como **mentor** …",
        "sources": ["wizeline/mentor-associate-manager/1"]}]},
    {"id": "kaxan-games", "mode": "fallback", "why": "Nothing relevant to a backend role.",
     "bullets": [{"en": "…", "es": "…", "sources": ["kaxan-games/cv1"]}, "… one per master bullet …"]}
  ],
  "skills": {"drop": []},
  "notes": ""
}
```

- `jd.terms`: optional — vocabulary ids the JD asks for that `analyze` did not detect (Spanish JDs).
- `jd.required`: ids from the vocabulary (`java`, `spring-boot`, `aws-sqs`, `microservices`, …), each with its
  `quote` copied **word for word** from the JD. Only strict requirements the tree has; everything else the JD asks
  for and the tree lacks goes to `jd.gaps` (never into the CV).
- `profile.roles`: optional — the master's roles by their English names, reordered or fewer.
- `profile.sources`: records the summary borrows a number or a fact from.
- A bullet: `en` and `es` in the Markdown subset (`**bold**`, `[text](url)`, no HTML); `child` for a client
  bullet (the page prints "**Fox Corp:**" itself — don't write it); `tech`, the "Tech: …" line the master's client
  bullets end with (names as the vocabulary writes them); `sources`.
- `skills.drop`: master chips to leave out when the aside runs out of room — never a required one.

### 7. Build, fix, repeat

```bash
python3 tools/tailor.py build <name>
```

Errors name the rule and the bullet (`experience[wizeline].bullets[2]: …`); fix the spec, not the rule. Then the
one-page check (headless Chrome / Chromium / Edge; set `TAILOR_CHROME` if it isn't found): the plain PDF must be
**1 page in EN and ES**; it prints the experience column's free space (~12 px per line). Over → drop the least relevant
bullet or tighten wording (both languages); lots of room → a relevant bullet you left out may fit. The ATS PDF is one
column and runs to 2 pages, like the master's.

**Never** edit `public/tailor-cv/*.html` by hand, and never touch the master's data in `tools/gen.py` to make a JD fit.
The one exception: a language, framework or engine the JD strictly requires, that the tree backs but has no level
(`build` warns). Ask Sergio for his 1–10 level, add it to `gen.CORE_EXTRA` with his number, and rebuild — it can then
enter the core skills.

### 8. Review before you hand it over

- [ ] Every claim is in its sources; nothing from `gaps` slipped in; numbers exactly as the sources say them.
- [ ] Each job's bullets are the relevant ones (or `fallback` when nothing is), and `why` says so.
- [ ] JD vocabulary is used only where the sources say the same thing in other words (sources: "services published
      and consumed messages" → JD: "event-driven" is fine; "Kafka" is not).
- [ ] Bullets open with a past-tense verb (EN) / pretérito (ES), one idea each, the master's tone; no "Tech:" in the text.
- [ ] The ES is natural Mexican Spanish with the same facts, numbers and technologies as the EN — not a word-for-word
      translation. `show` gives Sergio's own Spanish wording to follow.
- [ ] The summary still reads as Sergio's, changed a little; `{years}`, not a number.
- [ ] `build` passes and the plain PDF is one page in both languages.

### 9. Commit and report

```bash
git add tailor-cv/<name>.json public/tailor-cv/<name>.html public/tailor-cv/<name>.md public/tailor-cv/index.html
git commit -m "tailor-cv: <Company> — <Position>"
```

Push per the session's git instructions (in Claude Code on the web, its branch); locally, push only if asked.
Then tell the user: the URL (`https://sergiowero.github.io/tailor-cv/<name>.html`, live once merged to `main`; the
explorer at `https://sergiowero.github.io/tailor-cv/` lists it with the others), job by job what the CV shows and why,
what changed in the skills, the **gaps**, and any level you need from them.

`python3 tools/gen.py` re-renders every tailored CV with the current design and master data (contact, dates, levels),
so they never drift from the master CV's look.
