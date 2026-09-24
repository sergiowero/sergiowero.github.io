import type { APIRoute } from 'astro';
import template from '../llms/llms-full.md?raw';
import { blogFull, fill, textResponse } from '../lib/llms';

// The whole profile (CV, timeline, About, blog posts) in one Markdown file, linked from /llms.txt.
export const GET: APIRoute = async ({ site }) => textResponse(fill(template, await blogFull(site!)));
