import type { Metadata } from 'next';
import { Callout, Theme } from '@radix-ui/themes';
import { Step, Steps } from 'fumadocs-ui/components/steps';
import { Board, Citation, FieldList, Panel, PersonaBrief, SectionHeading, Source, SourceIndex } from '@/components/document-blocks';
import { Infographic } from '@/components/infographic';

export const metadata: Metadata = { title: '门户视觉发布检查', robots: { index: false, follow: false } };

const bar = `infographic chart-bar-plain-text
data
  title 图表渲染检查
  values
    - label 第一项
      value 42
    - label 第二项
      value 68
    - label 第三项
      value 91`;

const relation = `infographic relation-dagre-flow-tb-badge-card
data
  title 关系图渲染检查
  nodes
    - id source
      label 来源
    - id review
      label 评审
    - id publish
      label 发布
  relations
    - from source
      to review
    - from review
      to publish`;

export default function PortalReleaseCheckPage() {
  return <Theme asChild appearance="inherit" accentColor="orange" grayColor="slate" radius="medium" scaling="100%" panelBackground="solid" hasBackground={false}><main className="portal-release-check prose">
    <h1>门户视觉发布检查</h1>
    <SectionHeading id="layout-check" title="响应式布局" icon="layout-grid" />
    <SectionHeading id="design-system-subsection" title="统一视觉尺度" level={3} icon="ruler" />
    <p>本页使用接近正式报告的中文长度，验证标题、正文和富组件不会互相覆盖视觉层级。</p>
    <FieldList variant="grid" items={[
      { label: '字段一', value: '短值' }, { label: '字段二', value: '短值' }, { label: '字段三', value: '短值' },
      { label: '字段四', value: '短值' }, { label: '字段五', value: '短值' },
      { label: '长字段', value: '这是一段用于确认长内容不会被自动塞入横向多列的文本。'.repeat(5) },
    ]} />
    <Panel title="报告结构" icon="file-text" eyebrow="检查项" description="眉题、标题与摘要">
      <FieldList items={[{ label: '短字段', value: '短值' }]} />
      <section><h4 className="gf-component-subtitle">分段正文</h4><p>长内容采用纵向结构展示。</p></section>
      <Callout.Root color="blue" variant="surface"><Callout.Text><strong>证据边界</strong><br />该结论仅使用当前可验证资料。</Callout.Text></Callout.Root>
    </Panel>
    <PersonaBrief name="检查对象" identity="产品研究参与者" priority="核心用户" situation="临时获得三天假期，只有两个晚间完成规划，需要形成少量且可共同确认的候选。" traits={['体验优先', '控制退改损失']} facts={[{ label: '年龄', value: '31 岁' }, { label: '地区', value: '上海' }, { label: '同行人', value: '伴侣' }, { label: '时间与预算', value: '三天；两人 6000 元' }]} />
    <SectionHeading id="profile-section" title="画像内部章节" level={4} icon="scan-face" />
    <Steps><Step><h3>带图标步骤</h3><p>确认步骤标题和正文节奏。</p></Step></Steps>
    <Board label="优先级色调检查" columns={3} groups={[
      { title: 'P0', icon: 'circle-alert', tone: 'critical', children: <p>阻断项</p> },
      { title: 'P1', icon: 'circle-dot', tone: 'warning', children: <p>重要项</p> },
      { title: 'P2', tone: 'info', children: <p>优化项</p> },
    ]} />
    <SectionHeading id="chart-check" title="图形渲染" icon="chart-bar" />
    <Infographic syntax={bar} caption="chart-bar-plain-text" />
    <Infographic syntax={relation} caption="relation-dagre-flow-tb-badge-card" />
    <SectionHeading id="source-check" title="引用跳转" icon="book-open" />
    <p>引用必须能跳转到真实来源 <Citation source="S01" />。</p>
    <SourceIndex><Source id="S01">发布门禁内置检查来源</Source></SourceIndex>
  </main></Theme>;
}
