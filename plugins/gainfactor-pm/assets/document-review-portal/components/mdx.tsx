import defaultMdxComponents from 'fumadocs-ui/mdx';
import type { MDXComponents } from 'mdx/types';
import type { ComponentProps } from 'react';
import { Callout as RadixCallout } from '@radix-ui/themes';
import { Mermaid } from './mermaid';
import { Infographic } from './infographic';
import { EvidenceStep, Screenshot, ScreenshotGallery } from './screenshots';
import { Icon } from './lucide-icon';
import { Board, Citation, FieldList, Panel, PersonaBrief, SectionHeading, Source, SourceIndex } from './document-blocks';
import { MessageSquareQuote } from 'lucide-react';
import { Tab, Tabs, TabsContent, TabsList, TabsTrigger } from 'fumadocs-ui/components/tabs';
import { Step, Steps } from 'fumadocs-ui/components/steps';
import { File, Files, Folder } from 'fumadocs-ui/components/files';
import { TypeTable } from 'fumadocs-ui/components/type-table';
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';
import { Card, Cards } from 'fumadocs-ui/components/card';
import { Callout as FumadocsCallout, CalloutContainer, CalloutDescription, CalloutTitle } from 'fumadocs-ui/components/callout';
import { CodeBlock, Pre } from 'fumadocs-ui/components/codeblock';

export function DocumentCallout({ children, title, type = 'info', icon, className, ...props }: ComponentProps<typeof FumadocsCallout>) {
  const tone = type === 'warn' ? 'warning' : type;
  const color: ComponentProps<typeof RadixCallout.Root>['color'] = tone === 'warning' ? 'amber' : tone === 'error' ? 'red' : tone === 'success' ? 'green' : tone === 'idea' ? 'orange' : 'blue';
  const iconName = tone === 'warning' ? 'triangle-alert' : tone === 'error' ? 'circle-x' : tone === 'success' ? 'circle-check' : tone === 'idea' ? 'lightbulb' : 'info';
  const rootProps = props as ComponentProps<typeof RadixCallout.Root>;
  return (
    <RadixCallout.Root {...rootProps} className={['gf-callout', className].filter(Boolean).join(' ')} color={color} variant="surface" size="2">
      <RadixCallout.Icon>{icon ?? <Icon name={iconName} />}</RadixCallout.Icon>
      <div>{title ? <strong className="gf-callout-title">{title}</strong> : null}<div className="gf-callout-content">{children}</div></div>
    </RadixCallout.Root>
  );
}

export function getMDXComponents(components?: MDXComponents) {
  return {
    ...defaultMdxComponents,
    Mermaid,
    Infographic,
    Screenshot,
    ScreenshotGallery,
    EvidenceStep,
    Icon,
    PersonaBrief,
    FieldList,
    Panel,
    Board,
    SectionHeading,
    Citation,
    Source,
    SourceIndex,
    Tab,
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
    Step,
    Steps,
    File,
    Files,
    Folder,
    TypeTable,
    ImageZoom,
    Card,
    Cards,
    Callout: DocumentCallout,
    CalloutContainer,
    CalloutDescription,
    CalloutTitle,
    CodeBlock,
    Pre,
    table: (props: ComponentProps<'table'>) => (
      <div className="gf-table-scroll" tabIndex={0} role="region" aria-label="可横向滚动的表格">
        <table {...props} />
      </div>
    ),
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
