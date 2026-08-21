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
import { BadgeCheck, CalendarDays, FileText, Tag, UserRound } from 'lucide-react';
import { portalData } from '@/lib/portal-data';
import { ReviewIssues, ReviewNavigation } from '@/components/review-panels';
import { ReportPresentation } from '@/components/report-presentation';
import { Theme } from '@radix-ui/themes';

export default async function Page(props: PageProps<'/docs/[[...slug]]'>) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;
  const markdownUrl = getPageMarkdownUrl(page).url;
  const portalDocument = portalData.documents[page.slugs.join('/')] ?? {
    documentType: '文档',
    collection: '文档中心',
    version: '—',
    status: '未评审',
    owner: '未指定',
    updated: '—',
    review: { conclusion: '尚未生成评审结果', issues: [] },
  };
  const isReport = portalDocument.presentation?.layout === 'report';
  const hasReviewIssues = portalDocument.review.issues.length > 0;
  const description = page.data.description;

  return (
    <DocsPage full tableOfContent={{ enabled: false }} footer={{ enabled: false }}>
      <div className={`prd-review-layout${hasReviewIssues ? ' has-review-issues' : ''}${isReport ? ' report-document' : ''}`}>
      <ReviewNavigation toc={page.data.toc.filter((item) => item.depth <= 3).map((item) => ({ title: item.title, url: item.url, depth: item.depth }))} />
      <main className="prd-document">
      <header className="prd-header">
        <div className="prd-eyebrow"><FileText aria-hidden="true" /> {portalDocument.collection} <span>/</span> {portalDocument.documentType}</div>
        <div className="prd-heading-row">
          <div className="prd-heading-copy">
            <DocsTitle className="prd-title">{page.data.title}</DocsTitle>
            <DocsDescription className="prd-description">{description}</DocsDescription>
          </div>
          <div className="page-actions">
            <MarkdownCopyButton markdownUrl={markdownUrl} />
            <ViewOptionsPopover markdownUrl={markdownUrl} />
          </div>
        </div>
        <div className="prd-metadata" aria-label="文档信息" role="list">
          <div role="listitem"><Tag aria-hidden="true" /><span><span className="prd-metadata-label">版本</span><span className="prd-metadata-value">{portalDocument.version}</span></span></div>
          <div role="listitem"><BadgeCheck aria-hidden="true" /><span><span className="prd-metadata-label">状态</span><span className="prd-metadata-value"><span className="prd-status">{portalDocument.status}</span></span></span></div>
          <div role="listitem"><UserRound aria-hidden="true" /><span><span className="prd-metadata-label">负责人</span><span className="prd-metadata-value">{portalDocument.owner}</span></span></div>
          <div role="listitem"><CalendarDays aria-hidden="true" /><span><span className="prd-metadata-label">更新时间</span><span className="prd-metadata-value">{portalDocument.updated}</span></span></div>
        </div>
      </header>
      <ReportPresentation data={portalDocument.presentation} />
      <Theme asChild appearance="inherit" accentColor="orange" grayColor="slate" radius="medium" scaling="100%" panelBackground="solid" hasBackground={false}>
      <DocsBody>
        <MDX
          components={getMDXComponents({
            // this allows you to link to other pages with relative file paths
            a: createRelativeLink(source, page),
          })}
        />
      </DocsBody>
      </Theme>
      </main>
      {hasReviewIssues ? <ReviewIssues conclusion={portalDocument.review.conclusion} issues={portalDocument.review.issues} /> : null}
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
