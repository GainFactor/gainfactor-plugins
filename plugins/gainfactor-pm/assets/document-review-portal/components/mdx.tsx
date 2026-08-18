import defaultMdxComponents from 'fumadocs-ui/mdx';
import type { MDXComponents } from 'mdx/types';
import { Mermaid } from './mermaid';
import { MessageSquareQuote } from 'lucide-react';

export function getMDXComponents(components?: MDXComponents) {
  return {
    ...defaultMdxComponents,
    Mermaid,
    blockquote: ({ children, ...props }) => (
      <blockquote className="prd-note" {...props}>
        <div className="prd-note-icon">
          <MessageSquareQuote aria-hidden="true" />
        </div>
        <div className="prd-note-body">{children}</div>
      </blockquote>
    ),
    ...components,
  } satisfies MDXComponents;
}

export const useMDXComponents = getMDXComponents;

declare global {
  type MDXProvidedComponents = ReturnType<typeof getMDXComponents>;
}
