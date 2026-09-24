import type { APIRoute } from 'astro';
import template from '../llms/llms.md?raw';
import { blogLinks, fill, textResponse } from '../lib/llms';

// https://llmstxt.org — a short Markdown index of the site for LLMs and AI crawlers.
export const GET: APIRoute = async ({ site }) => textResponse(fill(template, await blogLinks(site!)));
