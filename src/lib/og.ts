// Link cards: the 1200×630 image that WhatsApp, LinkedIn, Slack, X, Discord, Teams… show for a shared link.
// Drawn at build time in the site's "Dark Terminal" look: satori lays the card out as SVG, resvg rasterises it to PNG.
// One template for every page; src/lib/cards.ts says what goes on each one.
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join } from 'node:path';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import generated from '../shell/cards.json';

export const OG_WIDTH = 1200;
export const OG_HEIGHT = 630;

export interface Card {
  /** Path of the page the card stands for, shown in the footer: "/timeline/". */
  path: string;
  /** The shell command after the prompt, as the page's header has it: "cat timeline.md". */
  prompt: string;
  title: string;
  /** Subtitle drawn like the CV header: the first role in green, the rest muted, a "/" between them. */
  roles?: string[];
  subtitle?: string;
  text?: string;
  stats?: { n: string; l: string }[];
  chips?: string[];
  /** Rows the chips may wrap onto (default: 1 under stats, else 2); the ones that don't fit are left out. */
  chipRows?: number;
  /** Monospace facts row: date, reading time… */
  meta?: string[];
  /** The portrait on the right (CV, About); otherwise a small avatar in the footer. */
  photo?: boolean;
  /** Footer badge: the site section. */
  section: string;
  /** Footer, after the badge: "EN · ES". */
  lang?: string;
}

// the dark theme of the site (tools/gen.py, v3 dark terminal)
const C = {
  bg: '#0b0f14', panel: '#141b23', line: '#1f2a35', text: '#d6dde6', muted: '#7d8a99',
  green: '#3ddc84', cyan: '#4cc9f0', amber: '#ffb454', fg: '#ffffff', body: '#b9c3cf', onGreen: '#06130c',
};
const MONO = 'JetBrains Mono';
const SANS = 'Inter';
const HOST = new URL(generated.site.url).host;

const require = createRequire(import.meta.url);
const font = (pkg: string, file: string) => readFileSync(require.resolve(`@fontsource/${pkg}/files/${file}`));
let fonts: Parameters<typeof satori>[1]['fonts'] | undefined;
function loadFonts() {
  // latin + latin-ext covers Spanish and most European titles; satori falls back glyph by glyph in this order
  return (fonts ??= [
    ...([400, 600, 700] as const).flatMap((weight) => [
      { name: SANS, data: font('inter', `inter-latin-${weight}-normal.woff`), weight, style: 'normal' as const },
      { name: SANS, data: font('inter', `inter-latin-ext-${weight}-normal.woff`), weight, style: 'normal' as const },
    ]),
    ...([400, 700] as const).map((weight) =>
      ({ name: MONO, data: font('jetbrains-mono', `jetbrains-mono-latin-${weight}-normal.woff`), weight, style: 'normal' as const })),
  ]);
}

let photo: string | null | undefined;
function loadPhoto() {
  if (photo === undefined) {
    try {
      photo = `data:image/jpeg;base64,${readFileSync(join(process.cwd(), 'public/about/photo.jpg')).toString('base64')}`;
    } catch {
      photo = null;   // no portrait: the card simply goes without it
    }
  }
  return photo;
}

// A tiny hyperscript for satori's element tree. Every box is flex (satori's rule for boxes with several children).
type Node = { type: string; props: Record<string, unknown> } | string | null | false | undefined | Node[];
const flat = (xs: Node[]): Node[] => xs.flatMap((x) => (Array.isArray(x) ? flat(x) : [x]));
function el(type: string, style: Record<string, unknown>, ...children: Node[]): Node {
  const kids = flat(children).filter((c) => c !== null && c !== false && c !== undefined);
  // a lone child goes in bare: satori counts an array as several children, which only a flex box may have
  return { type, props: { style: { display: 'flex', ...style }, children: kids.length === 1 ? kids[0] : kids } };
}
const div = (style: Record<string, unknown>, ...children: Node[]) => el('div', style, ...children);
const img = (src: string, size: number, style: Record<string, unknown>): Node =>
  ({ type: 'img', props: { src, width: size, height: size, style: { width: size, height: size, ...style } } });

/** Font size that keeps a title within ~2–3 lines of the text column. */
function titleSize(title: string, narrow: boolean) {
  const n = title.length * (narrow ? 1.3 : 1);
  return n <= 22 ? 76 : n <= 40 ? 64 : n <= 64 ? 52 : 42;
}

/** At most `max` characters, cut at a word. */
const clip = (s: string, max: number) => (s.length > max ? s.slice(0, s.lastIndexOf(' ', max - 1)).replace(/[\s,;:.]+$/, '') + '…' : s);

function prompt(cmd: string) {
  return div({ flexShrink: 0, fontFamily: MONO, fontSize: 24, color: C.muted, whiteSpace: 'pre' },
    el('span', { color: C.green }, 'sergio'), '@', el('span', { color: C.cyan }, HOST), ':~$ ',
    el('span', { color: C.amber }, cmd));
}

function title(text: string, narrow: boolean) {
  const size = titleSize(text, narrow);
  const words = clip(text, 140).split(/\s+/);
  // one box per word so the blinking-cursor block can sit right after the last one, wherever the line breaks
  return div({ flexShrink: 0, flexWrap: 'wrap', alignItems: 'flex-end', columnGap: size * 0.26, rowGap: size * 0.08, marginTop: 14,
               fontFamily: SANS, fontWeight: 700, fontSize: size, lineHeight: 1.08, letterSpacing: -size * 0.03, color: C.fg },
    ...words.map((w) => div({}, w)),
    div({ width: size * 0.45, height: size * 0.82, background: C.green, marginBottom: size * 0.1, marginLeft: -size * 0.14 }));
}

function roles(list: string[]) {
  // the "/" rides at the end of each role, so a wrapped line never starts with one
  return div({ flexShrink: 0, flexWrap: 'wrap', columnGap: 8, marginTop: 16, fontFamily: SANS, fontSize: 25, lineHeight: 1.3 },
    ...list.map((r, i) => div({ whiteSpace: 'pre', color: i === 0 ? C.green : C.muted, fontWeight: i === 0 ? 600 : 400 },
      r, i < list.length - 1 && el('span', { color: C.amber, fontWeight: 400 }, ' /'))));
}

function stats(list: NonNullable<Card['stats']>) {
  return div({ flexShrink: 0, gap: 12, marginTop: 26 },
    ...list.map((s) => div({ flexDirection: 'column', padding: '12px 16px', borderRadius: 12, border: `1px solid ${C.line}`, background: C.panel },
      div({ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: C.fg, lineHeight: 1.1 }, s.n),
      div({ fontFamily: MONO, fontSize: 15, color: C.muted, marginTop: 6, textTransform: 'uppercase', letterSpacing: 1 }, s.l))));
}

/** Chips wrap onto at most `rows` rows; what doesn't fit is left out. */
function chips(list: string[], rows: number) {
  return div({ flexShrink: 0, flexWrap: 'wrap', gap: 10, marginTop: 24, maxHeight: rows * 48 - 10, overflow: 'hidden' },
    ...list.map((c) => div({ fontFamily: MONO, fontSize: 19, color: C.text, padding: '6px 14px', borderRadius: 999,
                              border: `1px solid ${C.line}`, background: C.panel }, c)));
}

function footer(card: Card, avatar: string | null) {
  return div({ alignItems: 'center', justifyContent: 'space-between', padding: '0 56px', height: 84,
               borderTop: `1px solid ${C.line}`, background: C.panel },
    div({ alignItems: 'center', gap: 16 },
      avatar && img(avatar, 48, { borderRadius: 999, border: `2px solid ${C.green}` }),
      div({ fontFamily: SANS, fontWeight: 600, fontSize: 24, color: C.text }, generated.site.name),
      div({ fontFamily: MONO, fontSize: 21, color: C.muted }, `${HOST}${card.path === '/' ? '' : card.path}`)),
    div({ alignItems: 'center', gap: 14 },
      card.lang && div({ fontFamily: MONO, fontSize: 19, color: C.muted }, card.lang),
      div({ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: C.onGreen, background: C.green, padding: '6px 16px', borderRadius: 10 }, card.section)));
}

function layout(card: Card) {
  const portrait = card.photo ? loadPhoto() : null;
  const avatar = card.photo ? null : loadPhoto();
  return div({ width: OG_WIDTH, height: OG_HEIGHT, flexDirection: 'column', background: C.bg,
               backgroundImage: 'radial-gradient(circle at 50% -20%, #10261d 0%, #0b0f14 60%)' },
    // window chrome
    div({ alignItems: 'center', height: 50, padding: '0 22px', borderBottom: `1px solid ${C.line}`, background: C.panel },
      div({ gap: 9 }, ...['#ff5f57', '#febc2e', '#28c840'].map((bg) => div({ width: 14, height: 14, borderRadius: 999, background: bg }))),
      div({ flex: 1, justifyContent: 'center', fontFamily: MONO, fontSize: 18, color: C.muted, marginRight: 60 },
        `sergio@${HOST}: ~${card.path === '/' ? '' : card.path.replace(/\/$/, '')}`)),
    // body
    div({ flex: 1, padding: '0 56px', gap: 44, overflow: 'hidden' },
      div({ flex: 1, flexDirection: 'column', justifyContent: 'center', minWidth: 0 },
        prompt(card.prompt),
        title(card.title, !!portrait),
        card.roles && roles(card.roles),
        card.subtitle && div({ flexShrink: 0, marginTop: 14, fontFamily: SANS, fontWeight: 600, fontSize: 28, color: C.green }, card.subtitle),
        card.meta && div({ flexShrink: 0, marginTop: 16, fontFamily: MONO, fontSize: 21, color: C.muted, whiteSpace: 'pre' }, card.meta.join('  ·  ')),
        card.text && el('div', { display: 'block', flexShrink: 0, marginTop: 18, fontFamily: SANS, fontSize: 26, lineHeight: 1.4, color: C.body,
                                 lineClamp: card.stats || card.chips ? 2 : 3 }, card.text),
        card.stats && stats(card.stats),
        card.chips && chips(card.chips, card.chipRows ?? (card.stats ? 1 : 2))),
      portrait && div({ flexDirection: 'column', justifyContent: 'center' },
        img(portrait, 236, { borderRadius: 999, border: `4px solid ${C.green}`, boxShadow: '0 0 0 10px rgba(61,220,132,.14)' }))),
    footer(card, avatar));
}

export async function renderCard(card: Card): Promise<Uint8Array<ArrayBuffer>> {
  const svg = await satori(layout(card) as Parameters<typeof satori>[0], { width: OG_WIDTH, height: OG_HEIGHT, fonts: loadFonts() });
  return new Uint8Array(new Resvg(svg, { fitTo: { mode: 'width', value: OG_WIDTH } }).render().asPng());
}
