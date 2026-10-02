// What each page's link card shows. CV, Timeline and About come from tools/gen.py (src/shell/cards.json); the blog's
// are built here from the posts, so a new post gets its card on the next deploy with nothing else to do.
// Card names are the image paths: /og/<name>.png, drawn by src/pages/og/[...card].png.ts.
import generated from '../shell/cards.json';
import type { Card } from './og';
import { BLOG_DESCRIPTION, excerpt, formatDate, getPosts, langOf, readingTime, slugOf, tagIndex, tagSlug, urlOf, type Lang, type Post } from './blog';

export const SITE_NAME = generated.site.name;
export const LOCALES: Record<Lang, string> = generated.site.locales;

export const postCard = (post: Post) => `blog/${langOf(post)}/${slugOf(post)}`;
export const tagCard = (tag: string) => `blog/tags/${tagSlug(tag)}`;

const READ: Record<Lang, (n: number) => string> = { en: (n) => `${n} min read`, es: (n) => `${n} min de lectura` };
const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

export async function allCards(): Promise<Record<string, Card>> {
  const posts = await getPosts();
  const tags = tagIndex(posts);
  const cards: Record<string, Card> = { ...(generated.cards as Record<string, Card>) };
  const entries = new Set(posts.map(slugOf));   // one post in two languages is one entry

  cards.blog = {
    path: '/blog/', prompt: 'ls -l blog/', title: 'Blog', text: BLOG_DESCRIPTION.en,
    meta: [plural(entries.size, 'post', 'posts'), ...(posts[0] ? [`latest: ${formatDate(posts[0].data.pubDate, 'en')}`] : [])],
    chips: tags.map((t) => `#${t.tag}`), section: 'Blog', lang: 'EN · ES',
  };
  for (const post of posts) {
    const lang = langOf(post);
    cards[postCard(post)] = {
      path: urlOf(post), prompt: `cat blog/${lang}/${slugOf(post)}.md`, title: post.data.title,
      text: post.data.description || excerpt(post.body),
      meta: [formatDate(post.data.pubDate, lang), READ[lang](readingTime(post.body))],
      chips: post.data.tags.map((t) => `#${t}`), section: 'Blog', lang: lang.toUpperCase(),
    };
  }
  for (const t of tags) {
    const tagged = posts.filter((p) => p.data.tags.some((x) => tagSlug(x) === t.slug));
    cards[tagCard(t.tag)] = {
      path: `/blog/tags/${t.slug}/`, prompt: `grep -rl "#${t.tag}" blog/`, title: `#${t.tag}`,
      meta: [plural(new Set(tagged.map(slugOf)).size, 'post', 'posts')],
      text: [...new Set(tagged.map((p) => p.data.title))].join(' · '), section: 'Blog', lang: 'EN · ES',
    };
  }
  return cards;
}
