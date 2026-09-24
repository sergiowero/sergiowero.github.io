import { getPosts, langOf, translationOf, urlOf, type Post } from './blog';

// /llms.txt and /llms-full.txt: the templates come from tools/gen.py (src/llms/*.md, same data as the CV);
// here they get the live years of experience and the blog posts, so a new post needs no gen.py run.
const START_YEAR = 2010; // same as START_YEAR in FIT_JS (tools/gen.py)

const date = (d: Date) => d.toISOString().slice(0, 10);

/** Posts in English, plus the Spanish ones that have no English version. */
async function postsForLlms(site: URL) {
  const all = await getPosts();
  return all
    .filter((p) => langOf(p) === 'en' || !translationOf(p, all))
    .map((p) => ({ post: p, url: new URL(urlOf(p), site).href }));
}

/** Pushes every heading of a post down `by` levels, leaving code fences alone. */
function demote(body: string, by: number) {
  return body
    .split(/(^(?:```|~~~)[\s\S]*?^(?:```|~~~))/m)
    .map((part, i) => (i % 2 ? part : part.replace(/^(#{1,6})(?=\s)/gm, (h) => '#'.repeat(Math.min(6, h.length + by)))))
    .join('');
}

const meta = (p: Post) => `${langOf(p) === 'es' ? 'Spanish · ' : ''}${date(p.data.pubDate)}`;

export function fill(template: string, blog: string) {
  return template.replaceAll('{{years}}', String(new Date().getFullYear() - START_YEAR)).replace('{{blog}}', blog);
}

/** llms.txt: one link per post. */
export async function blogLinks(site: URL) {
  const posts = await postsForLlms(site);
  if (!posts.length) return `- [Blog](${new URL('/blog/', site).href}): notes on software, games and AI-assisted engineering`;
  return posts.map(({ post, url }) => `- [${post.data.title}](${url}): ${post.data.description} (${meta(post)})`).join('\n');
}

/** llms-full.txt: every post in full, its headings nested under `### title`. */
export async function blogFull(site: URL) {
  const posts = await postsForLlms(site);
  if (!posts.length) return 'No posts yet.';
  return posts
    .map(({ post, url }) =>
      [
        `### ${post.data.title}`,
        '',
        `- **URL:** ${url}`,
        `- **Published:** ${meta(post)}${post.data.tags.length ? ` · **Tags:** ${post.data.tags.join(', ')}` : ''}`,
        '',
        demote((post.body ?? '').trim(), 2),
        '',
      ].join('\n'),
    )
    .join('\n');
}

export const textResponse = (body: string) =>
  new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
