import { readFile, writeFile } from 'node:fs/promises';
import { basename, resolve } from 'node:path';

const args = process.argv.slice(2);
const sourcePath = args.shift();
const outputPath = args.shift() ?? 'content/docs/document.mdx';
if (!sourcePath || !outputPath) {
  console.error('Usage: node scripts/import-document.mjs <source.md> <output.mdx>');
  process.exit(1);
}

const markdown = await readFile(sourcePath, 'utf8');
const titleMatch = markdown.match(/^#\s+(.+)$/m);
const frontmatterMatch = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
const frontmatterTitle = frontmatterMatch?.[1].match(/^title:\s*["']?(.+?)["']?\s*$/m)?.[1];

if ((!titleMatch || titleMatch.index === undefined) && !frontmatterTitle) {
  throw new Error(`No title found in frontmatter or level-one heading in ${basename(sourcePath)}`);
}

const title = (titleMatch?.[1] ?? frontmatterTitle).trim();
const contentStart = titleMatch?.index !== undefined
  ? titleMatch.index + titleMatch[0].length
  : frontmatterMatch?.[0].length ?? 0;
const body = markdown
  .slice(contentStart)
  .trimStart();
const firstParagraph = body
  .split(/\n\s*\n/)
  .map((value) => value.replace(/^>\s?/gm, '').replace(/\s+/g, ' ').trim())
  .find((value) => value && !value.startsWith('#') && !value.startsWith('<!--'));
const description = firstParagraph?.slice(0, 140) || '文档阅读与评审稿。';
const frontmatter = `---\ntitle: ${JSON.stringify(title)}\ndescription: ${JSON.stringify(description)}\n---\n\n`;

await writeFile(resolve(outputPath), frontmatter + body);
console.log(`Imported ${sourcePath} -> ${outputPath}`);
