'use client';

import { useEffect, useState, type ReactNode } from 'react';
import { ClipboardCheck, List } from 'lucide-react';
import type { ReviewIssue } from '@/lib/portal-data';

type TocItem = { title: ReactNode; url: string; depth: number };

export function ReviewNavigation({ toc }: { toc: TocItem[] }) {
  const [activeId, setActiveId] = useState('');
  useEffect(() => {
    const headings = toc.map((item) => document.getElementById(item.url.replace(/^#/, ''))).filter((item): item is HTMLElement => Boolean(item));
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.find((entry) => entry.isIntersecting);
      if (visible) setActiveId(visible.target.id);
    }, { rootMargin: '-15% 0px -75% 0px' });
    headings.forEach((heading) => observer.observe(heading));
    return () => observer.disconnect();
  }, [toc]);

  return <aside className="review-navigation" aria-label="本节目录">
    <h2><List aria-hidden="true" />本节目录</h2>
    <nav className="review-toc">{toc.map((item) => <a key={item.url} href={item.url} data-depth={item.depth} data-active={activeId === item.url.replace(/^#/, '') || undefined}>{item.title}</a>)}</nav>
  </aside>;
}

export function ReviewIssues({ conclusion, issues }: { conclusion: string; issues: ReviewIssue[] }) {
  const [activeIssueId, setActiveIssueId] = useState('');

  const locateIssue = (issue: ReviewIssue) => {
    const target = document.getElementById(issue.sectionId);
    if (!target) return;

    document.querySelectorAll('[data-review-focus]').forEach((element) => element.removeAttribute('data-review-focus'));
    target.setAttribute('data-review-focus', 'true');
    setActiveIssueId(issue.id);
    window.history.replaceState(null, '', `#${issue.sectionId}`);
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return <aside className="review-issues-panel" aria-label="评审问题">
    <h2><ClipboardCheck aria-hidden="true" />评审问题{issues.length > 0 && <span>{issues.length}</span>}</h2>
    <p className="review-conclusion">{conclusion}</p>
    {issues.length === 0 ? <p className="review-empty">当前没有可展示的评审问题。</p> : <ol>{issues.map((issue) => <li key={issue.id}><a href={`#${issue.sectionId}`} aria-current={activeIssueId === issue.id ? 'location' : undefined} onClick={(event) => { event.preventDefault(); locateIssue(issue); }}><span className={`review-severity review-severity-${issue.severity.toLowerCase()}`}>{issue.severity}</span><strong>{issue.title}</strong>{issue.sectionTitle && <span className="review-location">定位到：{issue.sectionTitle}</span>}{issue.suggestion && <small>{issue.suggestion}</small>}</a></li>)}</ol>}
  </aside>;
}
