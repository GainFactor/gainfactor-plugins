import type { Metadata } from 'next';
import { Theme } from '@radix-ui/themes';
import { BookOpen, Box, CircleCheck, FileText, FolderOpen, PanelsTopLeft } from 'lucide-react';
import { Card, Cards } from 'fumadocs-ui/components/card';
import { CodeBlock, Pre } from 'fumadocs-ui/components/codeblock';
import { File, Files, Folder } from 'fumadocs-ui/components/files';
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';
import { Step, Steps } from 'fumadocs-ui/components/steps';
import { Tabs, TabsContent, TabsList, TabsTrigger } from 'fumadocs-ui/components/tabs';
import { TypeTable } from 'fumadocs-ui/components/type-table';
import { Board, Citation, FieldList, Panel, PersonaBrief, SectionHeading, Source, SourceIndex } from '@/components/document-blocks';
import { DocumentCallout } from '@/components/mdx';
import { Infographic } from '@/components/infographic';
import { Icon } from '@/components/lucide-icon';
import { Mermaid } from '@/components/mermaid';
import { EvidenceStep, Screenshot, ScreenshotGallery } from '@/components/screenshots';

export const metadata: Metadata = { title: '文档组件陈列页', robots: { index: false, follow: false } };

const bar = `infographic chart-bar-plain-text
data
  title 图表组件
  values
    - label 第一项
      value 42
    - label 第二项
      value 68
    - label 第三项
      value 91`;

function Demo({ id, name, source, children }: { id: string; name: string; source: string; children: React.ReactNode }) {
  return <section id={id} className="component-demo" data-component-demo={id}>
    <header className="component-demo-heading"><div><code>{name}</code><span>{source}</span></div><a href={`#${id}`}>#</a></header>
    <div className="component-demo-stage">{children}</div>
  </section>;
}

export default function ComponentGalleryPage() {
  return <Theme asChild appearance="inherit" accentColor="orange" grayColor="slate" radius="medium" scaling="100%" panelBackground="solid" hasBackground={false}>
    <main className="component-gallery prose" data-component-gallery>
      <header className="component-gallery-intro">
        <p className="component-gallery-eyebrow">Document Publisher</p>
        <h1>文档组件陈列页</h1>
        <p>集中查看全部公开文档能力。每个区块都标注组件名与来源，可直接用名称沟通样式调整。</p>
        <nav aria-label="组件分组"><a href="#native">基础正文</a><a href="#fumadocs">Fumadocs</a><a href="#gainfactor">GainFactor</a><a href="#visual">图形与媒体</a></nav>
      </header>

      <SectionHeading id="native" title="基础正文" icon="pilcrow" />
      <Demo id="demo-markdown" name="Markdown" source="浏览器基础样式">
        <h3>三级标题示例</h3><p>正文用于观察中文行高、段落间距、<strong>加粗</strong>、<em>强调</em>、<code>行内代码</code>与<a href="#demo-citation">内部链接</a>。</p>
        <blockquote>引用内容应保持轻量层级，不抢夺正文标题。</blockquote>
        <ul><li>无序列表第一项</li><li>无序列表第二项</li></ul>
        <table><thead><tr><th>字段</th><th>说明</th></tr></thead><tbody><tr><td>状态</td><td>用于观察表格边界和密度</td></tr></tbody></table>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/screenshot-check-desktop.svg" alt="裸 Markdown 图片安全样式示例" />
      </Demo>

      <SectionHeading id="fumadocs" title="Fumadocs 通用组件" icon="blocks" />
      <Demo id="demo-code-block" name="CodeBlock" source="Fumadocs"><CodeBlock title="example.tsx"><Pre><code>{`export function Example() {\n  return <p>Hello</p>;\n}`}</code></Pre></CodeBlock></Demo>
      <Demo id="demo-cards" name="Cards / Card" source="Fumadocs"><Cards><Card title="组件卡片" description="带标题与说明的入口卡片" icon={<Box />} /><Card title="文档入口" description="适合关联内容导航" icon={<BookOpen />} /></Cards></Demo>
      <Demo id="demo-callout" name="Callout" source="Fumadocs + Radix Themes"><DocumentCallout title="提示信息" type="idea" icon={<CircleCheck />}>用于表达证据边界、注意事项和状态反馈。</DocumentCallout></Demo>
      <Demo id="demo-tabs" name="Tabs" source="Fumadocs"><Tabs defaultValue="overview"><TabsList><TabsTrigger value="overview">概览</TabsTrigger><TabsTrigger value="details">详情</TabsTrigger></TabsList><TabsContent value="overview"><p>概览内容。</p></TabsContent><TabsContent value="details"><p>详情内容。</p></TabsContent></Tabs></Demo>
      <Demo id="demo-steps" name="Steps / Step" source="Fumadocs"><Steps><Step><h3>收集证据</h3><p>确认输入资料与边界。</p></Step><Step><h3>形成结论</h3><p>输出可追溯的判断。</p></Step></Steps></Demo>
      <Demo id="demo-files" name="Files / Folder / File" source="Fumadocs"><Files><Folder name="docs" defaultOpen><File name="overview.mdx" icon={<FileText />} /><File name="evidence.mdx" /></Folder><File name="README.md" icon={<FolderOpen />} /></Files></Demo>
      <Demo id="demo-type-table" name="TypeTable" source="Fumadocs"><TypeTable type={{ title: { type: 'string', required: true, description: '组件标题' }, columns: { type: '2 | 3 | 4', default: 'auto', description: '显式列数' } }} /></Demo>
      <Demo id="demo-image-zoom" name="ImageZoom" source="Fumadocs"><ImageZoom src="/screenshot-check-desktop.svg" alt="可缩放图片示例" width={960} height={540} /></Demo>
      <Demo id="demo-icon" name="Icon" source="Lucide"><p className="component-icon-row"><Icon name="chart-bar" /><Icon name="circle-alert" /><Icon name="clipboard-check" /><Icon name="scan-face" /> Lucide 图标使用稳定名称。</p></Demo>

      <SectionHeading id="gainfactor" title="GainFactor 文档组件" icon="panels-top-left" />
      <Demo id="demo-persona-brief" name="PersonaBrief" source="GainFactor"><PersonaBrief name="林岚" identity="品牌策划" priority="核心用户" situation="只有两个工作日晚间完成双人短途决策，希望住宿体验优先，同时控制退改损失。" traits={['体验优先', '少量候选', '可取消']} facts={[{ label: '年龄', value: '31 岁' }, { label: '地区', value: '上海' }, { label: '同行人', value: '伴侣' }, { label: '预算', value: '6000 元' }]} /></Demo>
      <Demo id="demo-field-list" name="FieldList" source="GainFactor"><FieldList variant="grid" columns={4} items={[{ label: '状态', value: '进行中' }, { label: '负责人', value: '产品团队' }, { label: '周期', value: '两周' }, { label: '范围', value: '门户组件' }, { label: '长文本', value: '长内容会占满整行，避免被压缩到狭窄的横向列中。'.repeat(4) }]} /></Demo>
      <Demo id="demo-steps-with-fields" name="Steps + FieldList" source="Fumadocs + GainFactor"><Steps><Step><h3>定义问题</h3><p>明确对象和判断标准。</p><FieldList items={[{ label: '输出', value: '问题清单' }]} /></Step><Step><h3>验证结果</h3><p>通过视觉门禁确认结果。</p></Step></Steps></Demo>
      <Demo id="demo-panel" name="Panel" source="GainFactor"><Panel title="结论面板" icon="file-check" eyebrow="研究结论" description="支持眉题、标题、摘要与组合正文。"><FieldList items={[{ label: '结论', value: '统一组件视觉基础' }]} /><section><h4>判断依据</h4><p>组件使用共享 Token，并在明暗主题和多尺寸下检查。</p></section><DocumentCallout title="证据边界">当前示例只说明组件表达方式。</DocumentCallout></Panel></Demo>
      <Demo id="demo-section-heading" name="SectionHeading" source="GainFactor"><SectionHeading id="gallery-heading-h2" title="二级标题" level={2} icon="layers" /><SectionHeading id="gallery-heading-h3" title="三级标题" level={3} icon="layers-2" /><SectionHeading id="gallery-heading-h4" title="四级标题" level={4} icon="layers-3" /></Demo>
      <Demo id="demo-citation" name="Citation / Source / SourceIndex" source="GainFactor"><p>正文引用可点击跳转 <Citation source="S01" />。</p><SourceIndex><Source id="S01">组件陈列页内置示例来源</Source></SourceIndex></Demo>
      <Demo id="demo-board" name="Board" source="GainFactor"><Board label="优先级示例" columns={3} groups={[{ title: 'P0', icon: 'circle-alert', tone: 'critical', children: <p><strong>阻断问题</strong><br />必须在发布前解决。</p> }, { title: 'P1', icon: 'circle-dot', tone: 'warning', children: <p><strong>重要优化</strong><br />影响主要阅读体验。</p> }, { title: 'P2', icon: 'sparkles', tone: 'info', children: <p><strong>体验增强</strong><br />用于进一步提升质量。</p> }]} /></Demo>

      <SectionHeading id="visual" title="图形与媒体" icon="image" />
      <Demo id="demo-mermaid" name="Mermaid" source="Mermaid"><Mermaid chart={`flowchart LR\n  A[资料] --> B[评审]\n  B --> C[发布]`} /></Demo>
      <Demo id="demo-infographic" name="Infographic" source="AntV"><Infographic syntax={bar} caption="chart-bar-plain-text" /></Demo>
      <Demo id="demo-screenshot" name="Screenshot" source="GainFactor"><Screenshot src="/screenshot-check-desktop.svg" title="产品页面" caption="桌面端关键状态截图" evidenceId="EV-01" device="desktop" step={1} /></Demo>
      <Demo id="demo-screenshot-gallery" name="ScreenshotGallery" source="GainFactor"><ScreenshotGallery columns={2} layout="rail"><Screenshot src="/screenshot-check-desktop.svg" title="桌面端" caption="横向滚动查看截图证据" evidenceId="EV-02" /><Screenshot src="/screenshot-check-mobile.svg" title="移动端" caption="灯箱中可纵向滚动查看长图" evidenceId="EV-03" device="mobile" /></ScreenshotGallery></Demo>
      <Demo id="demo-evidence-step" name="EvidenceStep" source="GainFactor"><EvidenceStep step={2} title="确认候选" evidence={<Screenshot src="/screenshot-check-mobile.svg" title="确认页" caption="步骤旁挂载截图证据" evidenceId="EV-04" device="mobile" />}><p>用户比较候选并完成共同确认。</p></EvidenceStep></Demo>
      <footer className="component-gallery-footer"><PanelsTopLeft aria-hidden="true" />统一组件能力陈列</footer>
    </main>
  </Theme>;
}
