'use client';
import SearchDialog from '@/components/search';
import { RootProvider } from 'fumadocs-ui/provider/next';
import { type ReactNode } from 'react';

export function Provider({ children }: { children: ReactNode }) {
  return (
    <RootProvider
      search={{ SearchDialog }}
      i18n={{
        locale: 'zh-CN',
        translations: {
          'Search(search trigger)': '搜索文档',
          'Search(search dialog)': '搜索文档',
          'No results found(search dialog)': '未找到相关内容',
          'On this page(table of contents)': '本节目录',
          'Copy Markdown(page actions)': '复制 Markdown',
          'Open(page actions)': '更多',
          'Previous Page(pagination)': '上一篇',
          'Next Page(pagination)': '下一篇',
        },
      }}
    >
      {children}
    </RootProvider>
  );
}
