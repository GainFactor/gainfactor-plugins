'use client';

import Link from 'next/link';
import { PanelLeft } from 'lucide-react';
import { useNotebookLayout } from 'fumadocs-ui/layouts/notebook';

export function DocsHeader() {
  const { slots } = useNotebookLayout();
  const CollapseTrigger = slots.sidebar?.collapseTrigger;
  const SidebarTrigger = slots.sidebar?.trigger;
  const ThemeSwitch = slots.themeSwitch;

  return <header id="nd-subnav" className="docs-topbar">
    <nav className="docs-breadcrumb" aria-label="面包屑导航">
      <Link href="/docs">产品文档</Link><span aria-hidden="true">/</span><span>PRD 阅读与评审</span>
    </nav>
    <div className="docs-topbar-actions">
      {ThemeSwitch && <ThemeSwitch />}
      {CollapseTrigger && <CollapseTrigger className="docs-collapse"><PanelLeft aria-hidden="true" /></CollapseTrigger>}
      {SidebarTrigger && <SidebarTrigger className="docs-mobile-menu"><PanelLeft aria-hidden="true" /></SidebarTrigger>}
    </div>
  </header>;
}
