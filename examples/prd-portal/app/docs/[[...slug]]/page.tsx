import { getPageImageUrl, getPageMarkdownUrl, source } from '@/lib/source';
import {
  DocsBody,
  DocsDescription,
  DocsPage,
  DocsTitle,
  MarkdownCopyButton,
  ViewOptionsPopover,
} from 'fumadocs-ui/layouts/notebook/page';
import { notFound } from 'next/navigation';
import { getMDXComponents } from '@/components/mdx';
import type { Metadata } from 'next';
import { createRelativeLink } from 'fumadocs-ui/mdx';
import { gitConfig } from '@/lib/shared';
import { BadgeCheck, CalendarDays, FileText, Tag, UserRound } from 'lucide-react';
import { ReviewIssues, ReviewNavigation } from '@/components/review-panels';
import { reviewData } from '@/lib/review-data';

export default async function Page(props: PageProps<'/docs/[[...slug]]'>) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;
  const markdownUrl = getPageMarkdownUrl(page).url;

  return (
    <DocsPage full tableOfContent={{ enabled: false }} footer={{ enabled: false }}>
      <div className="prd-review-layout">
      <ReviewNavigation toc={page.data.toc.filter((item) => item.depth <= 3).map((item) => ({ title: item.title, url: item.url, depth: item.depth }))} />
      <main className="prd-document">
      <header className="prd-header">
        <div className="prd-eyebrow"><FileText aria-hidden="true" /> 产品文档 <span>/</span> PRD</div>
        <div className="prd-heading-row">
          <div className="prd-heading-copy">
            <DocsTitle className="prd-title">{page.data.title}</DocsTitle>
            <DocsDescription className="prd-description">{page.data.description}</DocsDescription>
          </div>
          <div className="page-actions">
            <MarkdownCopyButton markdownUrl={markdownUrl} />
            <ViewOptionsPopover
              markdownUrl={markdownUrl}
              githubUrl={`https://github.com/${gitConfig.user}/${gitConfig.repo}/blob/${gitConfig.branch}/content/docs/${page.path}`}
            />
          </div>
        </div>
        <dl className="prd-metadata" aria-label="文档信息">
          <div><Tag aria-hidden="true" /><span><dt>版本</dt><dd>V1.0</dd></span></div>
          <div><BadgeCheck aria-hidden="true" /><span><dt>状态</dt><dd><span className="prd-status">已评审</span></dd></span></div>
          <div><UserRound aria-hidden="true" /><span><dt>负责人</dt><dd>GainFactor 项目负责人</dd></span></div>
          <div><CalendarDays aria-hidden="true" /><span><dt>更新时间</dt><dd>2026-07-19</dd></span></div>
        </dl>
      </header>
      <DocsBody>
        <MDX
          components={getMDXComponents({
            // this allows you to link to other pages with relative file paths
            a: createRelativeLink(source, page),
          })}
        />
      </DocsBody>
      </main>
      <ReviewIssues conclusion={reviewData.conclusion} issues={reviewData.issues} />
      </div>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(props: PageProps<'/docs/[[...slug]]'>): Promise<Metadata> {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  return {
    title: page.data.title,
    description: page.data.description,
    openGraph: {
      images: getPageImageUrl(page).url,
    },
  };
}
