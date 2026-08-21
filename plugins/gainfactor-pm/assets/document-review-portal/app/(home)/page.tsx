import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'GainFactor 文档中心' };

export default function HomePage() {
  return (
    <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-6 py-20">
      <p className="mb-4 text-sm font-medium text-fd-primary">GainFactor 文档中心</p>
      <h1 className="max-w-3xl text-4xl font-semibold tracking-tight sm:text-6xl">
        让研发文档更容易阅读、检索和评审
      </h1>
      <p className="mt-6 max-w-2xl text-lg leading-8 text-fd-muted-foreground">
        PRD、BRD、HLD、LLD、测试策略等文档继续使用 Markdown/MDX 管理，页面负责统一的目录、搜索与评审体验。
      </p>
      <div className="mt-10">
        <Link
          href="/docs"
          className="inline-flex rounded-md bg-fd-primary px-5 py-3 text-sm font-medium text-fd-primary-foreground transition-opacity hover:opacity-90"
        >
          打开文档中心
        </Link>
      </div>
    </main>
  );
}
