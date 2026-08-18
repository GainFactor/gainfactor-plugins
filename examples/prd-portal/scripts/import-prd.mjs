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
const headingNames = new Map([
  ['Summary 版本说明', '版本说明'],
  ['Problem & Goals 问题与目标', '问题与目标'],
  ['Scope 需求范围', '需求范围'],
  ['Design 需求设计', '需求设计'],
  ['Rollout & Risks 上线与风险', '上线与风险'],
  ['Quality 质量保障', '质量保障'],
  ['Appendix 附录', '附录'],
]);
const body = markdown
  .slice(titleMatch.index + titleMatch[0].length)
  .trimStart()
  .replace(/^## (一|二|三|四|五|六|七)、(.+)$/gm, (heading, number, name) =>
    headingNames.has(name) ? `## ${number}、${headingNames.get(name)}` : heading,
  );
const description = '课程、学生、阶段、作业、测试、集中点评、服务与飞书文档权限的产品需求文档。';
const frontmatter = `---\ntitle: ${title}\ndescription: ${description}\n---\n\n`;

await writeFile(outputPath, frontmatter + body);
console.log(`Imported ${sourcePath} -> ${outputPath}`);
