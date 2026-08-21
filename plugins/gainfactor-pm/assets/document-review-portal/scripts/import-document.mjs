import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { basename, dirname, extname, resolve } from 'node:path';

const args = process.argv.slice(2);
const sourcePath = args.shift();
const outputPath = args.shift() ?? 'content/docs/document.mdx';
if (!sourcePath || !outputPath) {
  console.error('Usage: node scripts/import-document.mjs <source.md> <output.mdx>');
  process.exit(1);
}

let markdown = await readFile(sourcePath, 'utf8');
const titleMatch = markdown.match(/^#\s+(.+)$/m);
const frontmatterMatch = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
const frontmatterTitle = frontmatterMatch?.[1].match(/^title:\s*["']?(.+?)["']?\s*$/m)?.[1];

if ((!titleMatch || titleMatch.index === undefined) && !frontmatterTitle) {
  throw new Error(`No title found in frontmatter or level-one heading in ${basename(sourcePath)}`);
}

const title = (titleMatch?.[1] ?? frontmatterTitle).trim();

const route = outputPath
  .replace(/^content\/docs\//, '')
  .replace(/\.(?:md|mdx)$/i, '');
const assetOutputDir = resolve('public/document-assets', route);
const copiedImages = new Map();
let copiedImageCount = 0;

async function importLocalImage(rawTarget) {
  if (/^(?:[a-z]+:|\/|#)/i.test(rawTarget)) return rawTarget;
  let portalUrl = copiedImages.get(rawTarget);
  if (portalUrl) return portalUrl;
  const decodedTarget = decodeURIComponent(rawTarget);
  const sourceAsset = resolve(dirname(resolve(sourcePath)), decodedTarget);
  const extension = extname(sourceAsset).toLowerCase();
  const stem = basename(sourceAsset, extension)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '') || 'image';
  copiedImageCount += 1;
  const outputName = `${String(copiedImageCount).padStart(2, '0')}-${stem}${extension}`;
  await mkdir(assetOutputDir, { recursive: true });
  await copyFile(sourceAsset, resolve(assetOutputDir, outputName));
  portalUrl = `/document-assets/${route}/${outputName}`;
  copiedImages.set(rawTarget, portalUrl);
  return portalUrl;
}

const imagePattern = /!\[([^\]]*)\]\((<[^>]+>|[^)\s]+)(\s+["'][^)]*["'])?\)/g;
const imageMatches = [...markdown.matchAll(imagePattern)];

for (const match of imageMatches) {
  const rawTarget = match[2].replace(/^<|>$/g, '');
  const portalUrl = await importLocalImage(rawTarget);
  if (portalUrl === rawTarget) continue;
  markdown = markdown.replace(match[0], `![${match[1]}](${portalUrl}${match[3] ?? ''})`);
}

const personaBriefPattern = /<PersonaBrief\b[\s\S]*?>/g;
const personaBriefMatches = [...markdown.matchAll(personaBriefPattern)];
for (const personaBriefMatch of personaBriefMatches) {
  const imageObject = personaBriefMatch[0].match(/\bimage\s*=\s*\{\{([\s\S]*?)\}\}/);
  if (!imageObject) continue;
  const source = imageObject[1].match(/\bsrc\s*:\s*(["'])([^"']+)\1/);
  const alt = imageObject[1].match(/\balt\s*:\s*(["'])([^"']*)\1/);
  if (!source) throw new Error('PersonaBrief image must contain a string src field');
  if (!alt?.[2].trim()) throw new Error('PersonaBrief image must contain a non-empty alt field');
  const portalUrl = await importLocalImage(source[2]);
  if (portalUrl === source[2]) continue;
  const rewrittenImage = imageObject[0].replace(source[0], `src: ${source[1]}${portalUrl}${source[1]}`);
  const rewrittenPersonaBrief = personaBriefMatch[0].replace(imageObject[0], rewrittenImage);
  markdown = markdown.replace(personaBriefMatch[0], rewrittenPersonaBrief);
}

const imageComponentPattern = /<(?:Screenshot|ImageZoom)\b[\s\S]*?>/g;
const imageComponentMatches = [...markdown.matchAll(imageComponentPattern)];
for (const imageComponentMatch of imageComponentMatches) {
  const component = imageComponentMatch[0].match(/^<([A-Za-z]+)/)?.[1] ?? 'Image component';
  const source = imageComponentMatch[0].match(/\bsrc\s*=\s*(["'])([^"']+)\1/);
  if (!source) throw new Error(`${component} must contain a string src field`);
  const portalUrl = await importLocalImage(source[2]);
  if (portalUrl === source[2]) continue;
  const rewrittenComponent = imageComponentMatch[0].replace(source[0], `src=${source[1]}${portalUrl}${source[1]}`);
  markdown = markdown.replace(imageComponentMatch[0], rewrittenComponent);
}

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
