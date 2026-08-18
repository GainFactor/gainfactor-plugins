import { readFile, writeFile } from 'node:fs/promises';
import { basename, resolve } from 'node:path';

const args = process.argv.slice(2);
const sourcePath = args.shift();
const outputPath = args.shift() ?? 'content/docs/prd.mdx';
const options = Object.fromEntries(args.map((value) => {
  const [key, ...rest] = value.replace(/^--/, '').split('=');
  return [key, rest.join('=')];
}));

if (!sourcePath || !outputPath) {
  console.error('Usage: node scripts/import-prd.mjs <source.md> <output.mdx>');
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
const headingNames = new Map([
  ['Summary 版本说明', '版本说明'],
  ['Problem & Goals 问题与目标', '问题与目标'],
  ['Scope 需求范围', '需求范围'],
  ['Design 需求设计', '需求设计'],
  ['Rollout & Risks 上线与风险', '上线与风险'],
  ['Quality 质量保障', '质量保障'],
  ['Appendix 附录', '附录'],
]);
const contentStart = titleMatch?.index !== undefined
  ? titleMatch.index + titleMatch[0].length
  : frontmatterMatch?.[0].length ?? 0;
const body = markdown
  .slice(contentStart)
  .trimStart()
  .replace(/^## (一|二|三|四|五|六|七)、(.+)$/gm, (heading, number, name) =>
    headingNames.has(name) ? `## ${number}、${headingNames.get(name)}` : heading,
  );
const firstParagraph = body
  .split(/\n\s*\n/)
  .map((value) => value.replace(/^>\s?/gm, '').replace(/\s+/g, ' ').trim())
  .find((value) => value && !value.startsWith('#') && !value.startsWith('<!--'));
const description = options.description || firstParagraph?.slice(0, 140) || '产品需求文档评审稿。';
const frontmatter = `---\ntitle: ${JSON.stringify(title)}\ndescription: ${JSON.stringify(description)}\n---\n\n`;

await writeFile(resolve(outputPath), frontmatter + body);

const inferredVersion = title.match(/\bV?\d+(?:\.\d+)+\b/i)?.[0] ?? '—';
const metadata = {
  version: options.version || inferredVersion,
  status: options.status || '待评审',
  owner: options.owner || '未指定',
  updated: options.updated || new Date().toISOString().slice(0, 10),
};
await writeFile(
  resolve('lib/document-meta.ts'),
  `export const documentMeta = ${JSON.stringify(metadata, null, 2)} as const;\n`,
);
console.log(`Imported ${sourcePath} -> ${outputPath}`);
