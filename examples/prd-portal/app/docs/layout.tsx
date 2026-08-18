import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';
import Image from 'next/image';
import Link from 'next/link';

export default function Layout({ children }: LayoutProps<'/docs'>) {
  return (
    <div className="docs-shell">
      <header className="docs-topbar">
        <Link href="/docs" className="brand-lockup" aria-label="GainFactor PRD 文档首页">
          <Image src="/gainfactor-mark.png" alt="" width={28} height={28} priority unoptimized />
          <span>GainFactor</span>
        </Link>
        <span className="docs-product-title">教务系统 V1.0 需求</span>
      </header>
      <DocsLayout tree={source.getPageTree()} {...baseOptions()} containerProps={{ className: 'docs-layout' }}>
        {children}
      </DocsLayout>
    </div>
  );
}
