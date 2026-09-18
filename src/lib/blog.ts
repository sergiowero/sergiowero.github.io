import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'blog'>;
export type Lang = 'en' | 'es';

export const langOf = (post: Post): Lang => post.id.split('/')[0] as Lang;
export const slugOf = (post: Post) => post.id.split('/').slice(1).join('/');
export const urlOf = (post: Post) => `/blog/${langOf(post)}/${slugOf(post)}/`;
export const tagSlug = (tag: string) => tag.toLowerCase().trim().replace(/[^a-z0-9áéíóúñü]+/gi, '-').replace(/(^-|-$)/g, '');

export async function getPosts(): Promise<Post[]> {
  const all = await getCollection('blog', ({ data }) => import.meta.env.PROD ? !data.draft : true);
  return all.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

/** The same post in the other language, if it exists. */
export function translationOf(post: Post, all: Post[]): Post | undefined {
  const other: Lang = langOf(post) === 'en' ? 'es' : 'en';
  return all.find((p) => langOf(p) === other && slugOf(p) === slugOf(post));
}

export function formatDate(d: Date, lang: Lang) {
  return d.toLocaleDateString(lang === 'es' ? 'es-MX' : 'en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
}

export function readingTime(body: string | undefined) {
  const words = (body ?? '').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}

/** All tags with post counts, per language. */
export function tagIndex(posts: Post[]) {
  const map = new Map<string, { tag: string; slug: string; count: { en: number; es: number } }>();
  for (const p of posts) {
    for (const t of p.data.tags) {
      const s = tagSlug(t);
      const e = map.get(s) ?? { tag: t, slug: s, count: { en: 0, es: 0 } };
      e.count[langOf(p)]++;
      map.set(s, e);
    }
  }
  return [...map.values()].sort((a, b) => a.tag.localeCompare(b.tag));
}
