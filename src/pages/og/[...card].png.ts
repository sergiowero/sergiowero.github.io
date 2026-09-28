// The link-card images: /og/<card>.png, one per page (src/lib/cards.ts), drawn at build time.
import type { APIRoute, GetStaticPaths } from 'astro';
import { allCards } from '../../lib/cards';
import { renderCard, type Card } from '../../lib/og';

export const getStaticPaths = (async () =>
  Object.entries(await allCards()).map(([card, data]) => ({ params: { card }, props: { data } }))) satisfies GetStaticPaths;

export const GET: APIRoute<{ data: Card }> = async ({ props }) =>
  new Response(await renderCard(props.data), { headers: { 'Content-Type': 'image/png' } });
