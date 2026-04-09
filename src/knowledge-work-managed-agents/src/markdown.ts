/**
 * Markdown processing — parse, render, and extract structure from markdown.
 *
 * Uses markdown-it for parsing/rendering and provides utilities for
 * extracting headings, code blocks, and frontmatter — the operations
 * most needed by agentstreams skill loaders and taxonomy extractors.
 *
 * Uses CLAUDE_CODE_OAUTH_TOKEN for API auth (never ANTHROPIC_API_KEY).
 */

import MarkdownIt from "markdown-it";
import type Token from "markdown-it/lib/token.mjs";

// ── Types ──────────────────────────────────────────────────────

export interface Heading {
  level: number;
  text: string;
  line: number;
}

export interface CodeBlock {
  language: string;
  content: string;
  line: number;
}

export interface Frontmatter {
  raw: string;
  fields: Record<string, string>;
}

export interface MarkdownStructure {
  headings: Heading[];
  codeBlocks: CodeBlock[];
  frontmatter: Frontmatter | null;
  links: Array<{ text: string; href: string }>;
}

// ── Renderer ───────────────────────────────────────────────────

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: false,
});

/** Render markdown to HTML */
export function renderMarkdown(source: string): string {
  return md.render(source);
}

/** Parse markdown to token stream */
export function parseMarkdown(source: string): Token[] {
  return md.parse(source, {});
}

// ── Extractors ─────────────────────────────────────────────────

/** Extract YAML frontmatter from --- delimited block */
export function extractFrontmatter(source: string): Frontmatter | null {
  const match = source.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const raw = match[1];
  const fields: Record<string, string> = {};
  for (const line of raw.split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, "");
      fields[key] = value;
    }
  }
  return { raw, fields };
}

/** Extract all headings with levels and line numbers */
export function extractHeadings(source: string): Heading[] {
  const headings: Heading[] = [];
  const lines = source.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const match = lines[i].match(/^(#{1,6})\s+(.+)/);
    if (match) {
      headings.push({
        level: match[1].length,
        text: match[2].trim(),
        line: i + 1,
      });
    }
  }
  return headings;
}

/** Extract fenced code blocks with language and line numbers */
export function extractCodeBlocks(source: string): CodeBlock[] {
  const blocks: CodeBlock[] = [];
  const lines = source.split("\n");
  let inBlock = false;
  let lang = "";
  let content: string[] = [];
  let startLine = 0;

  for (let i = 0; i < lines.length; i++) {
    const fence = lines[i].match(/^```(\w*)/);
    if (fence && !inBlock) {
      inBlock = true;
      lang = fence[1] || "";
      content = [];
      startLine = i + 1;
    } else if (lines[i].startsWith("```") && inBlock) {
      blocks.push({ language: lang, content: content.join("\n"), line: startLine });
      inBlock = false;
    } else if (inBlock) {
      content.push(lines[i]);
    }
  }
  return blocks;
}

/** Extract markdown links */
export function extractLinks(
  source: string,
): Array<{ text: string; href: string }> {
  const links: Array<{ text: string; href: string }> = [];
  const re = /\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  while ((match = re.exec(source))) {
    links.push({ text: match[1], href: match[2] });
  }
  return links;
}

/** Full structural extraction — headings, code blocks, frontmatter, links */
export function extractStructure(source: string): MarkdownStructure {
  return {
    headings: extractHeadings(source),
    codeBlocks: extractCodeBlocks(source),
    frontmatter: extractFrontmatter(source),
    links: extractLinks(source),
  };
}
