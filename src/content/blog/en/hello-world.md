---
title: "Hello, world"
description: "First post: how this blog is built and how to add a new entry in English and Spanish."
pubDate: 2026-09-18
tags: ["meta", "astro", "github-pages"]
---

This blog is part of my site and shares the same shell as the CV: same background, same sheet, same header, and the **dark / light** and **ES / EN** switches keep their state across pages.

## How a post is published

1. Write a Markdown file in `src/content/blog/en/` (and, optionally, the Spanish version with the **same file name** in `src/content/blog/es/`).
2. Commit and push to `main`.
3. GitHub Actions builds the site with [Astro](https://astro.build) and deploys it to GitHub Pages.

The front matter looks like this:

```yaml
---
title: "Hello, world"
description: "One line shown in the index."
pubDate: 2026-09-18
tags: ["meta", "astro"]
---
```

> When a post exists in both languages, the ES / EN switch jumps between the two versions.

That's it — no build step to run locally, no HTML to touch.
