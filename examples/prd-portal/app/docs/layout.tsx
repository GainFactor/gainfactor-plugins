import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';
import Image from 'next/image';
import Link from 'next/link';
import type { Root } from 'fumadocs-core/page-tree';

const documentUrl = '/docs/gainfactor-education-system-v1';
const chapters = [
  { name: '一、版本说明', id: '一版本说明' },
  {
    name: '二、问题与目标', id: '二问题与目标', children: [
      ['2.1 业务背景', '21-业务背景'],
      ['2.2 用户角色', '22-用户角色'],
      ['2.3 业务目标', '23-业务目标北极星指标--kr'],
      ['2.4 非目标', '24-非目标no-gos--本期明确不做'],
      ['2.5 端到端流程图', '25-端到端流程图'],
    ],
  },
  {
    name: '三、需求范围', id: '三需求范围', children: [
      ['3.1 需求清单', '31-需求清单按优先级排序'],
      ['3.2 非功能性需求', '32-非功能性需求'],
    ],
  },
  {
    name: '四、需求设计', id: '四需求设计', children: [
      ['4.1 业务对象关系', '41-业务对象关系'],
      ['4.2 页面功能详细设计', '42-页面功能详细设计'],
    ],
  },
  {
    name: '五、上线与风险', id: '五上线与风险', children: [
      ['5.1 启用计划', '51-启用计划'],
      ['5.2 暂停扩大与回滚预案', '52-暂停扩大与回滚预案'],
      ['5.3 上下游依赖', '53-上下游依赖'],
      ['5.4 已知风险', '54-已知风险'],
    ],
  },
  {
    name: '六、质量保障', id: '六质量保障', children: [
      ['6.1 数据埋点', '61-数据埋点'],
      ['6.2 线上质量指标', '62-线上质量指标'],
      ['6.3 验收清单', '63-验收清单'],
    ],
  },
  {
    name: '七、附录', id: '七附录', children: [
      ['7.1 术语表', '71-术语表'],
      ['7.2 ADR 关键决策记录', '72-adr-关键决策记录'],
      ['7.3 历史版本', '73-历史版本'],
      ['7.4 链接补充', '74-链接补充'],
    ],
  },
] as const;

const chapterTree: Root = {
  type: 'root',
  name: 'PRD 章节',
  children: chapters.map((chapter) => {
    const index = { type: 'page' as const, name: chapter.name, url: `${documentUrl}#${chapter.id}` };
    if (!('children' in chapter)) return index;

    return {
      type: 'folder' as const,
      name: chapter.name,
      defaultOpen: true,
      index,
      children: chapter.children.map(([name, id]) => ({
        type: 'page' as const,
        name,
        url: `${documentUrl}#${id}`,
      })),
    };
  }),
};

export default function Layout({ children }: LayoutProps<'/docs'>) {
  return (
    <div className="docs-shell">
      <header className="docs-topbar">
        <div className="docs-topbar-inner">
          <Link href="/docs" className="brand-lockup" aria-label="GainFactor PRD 文档首页">
            <Image src="/gainfactor-mark.png" alt="" width={28} height={28} priority unoptimized />
            <span>GainFactor</span>
          </Link>
          <span className="docs-product-title">教务系统 V1.0 需求</span>
        </div>
      </header>
      <DocsLayout
        tree={chapterTree}
        {...baseOptions()}
        containerProps={{
          className: 'docs-layout',
          style: {
            gridTemplate: `"sidebar sidebar header toc toc"
"sidebar sidebar toc-popover toc toc"
"sidebar sidebar main toc toc" 1fr / 0px var(--fd-sidebar-col) minmax(0, min(1000px, calc(100vw - var(--fd-sidebar-col) - var(--fd-toc-width)))) var(--fd-toc-width) minmax(0, 1fr)`,
          },
        }}
      >
        {children}
      </DocsLayout>
    </div>
  );
}
