import { readFile, writeFile } from 'node:fs/promises';
import { basename } from 'node:path';

const [sourcePath, outputPath] = process.argv.slice(2);

if (!sourcePath || !outputPath) {
  console.error('Usage: node scripts/import-prd.mjs <source.md> <output.mdx>');
  process.exit(1);
}

const markdown = await readFile(sourcePath, 'utf8');
const titleMatch = markdown.match(/^#\s+(.+)$/m);

if (!titleMatch || titleMatch.index === undefined) {
  throw new Error(`No level-one heading found in ${basename(sourcePath)}`);
}

const title = titleMatch[1].trim();
const body = markdown.slice(titleMatch.index + titleMatch[0].length).trimStart();
const description = '课程、学生、阶段、作业、测试、集中点评、服务与飞书文档权限的产品需求文档。';
const frontmatter = `---\ntitle: ${title}\ndescription: ${description}\n---\n\n`;

await writeFile(outputPath, frontmatter + body);
console.log(`Imported ${sourcePath} -> ${outputPath}`);
