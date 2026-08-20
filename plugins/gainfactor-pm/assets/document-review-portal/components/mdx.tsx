import defaultMdxComponents from 'fumadocs-ui/mdx';
import type { MDXComponents } from 'mdx/types';
import { Mermaid } from './mermaid';
import { NodeGraph } from './node-graph';
import { Infographic } from './infographic';
import { Icon } from './lucide-icon';
import { ContentPanel, GroupedBoard, InfoGrid, Profile, StructuredSteps } from './document-blocks';
import { MessageSquareQuote } from 'lucide-react';
import { Tab, Tabs, TabsContent, TabsList, TabsTrigger } from 'fumadocs-ui/components/tabs';
import { Step, Steps } from 'fumadocs-ui/components/steps';
import { File, Files, Folder } from 'fumadocs-ui/components/files';
import { TypeTable } from 'fumadocs-ui/components/type-table';
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';
import { Card, Cards } from 'fumadocs-ui/components/card';
import { Callout, CalloutContainer, CalloutDescription, CalloutTitle } from 'fumadocs-ui/components/callout';
import { CodeBlock, Pre } from 'fumadocs-ui/components/codeblock';

export function getMDXComponents(components?: MDXComponents) {
  return {
    ...defaultMdxComponents,
    Mermaid,
    NodeGraph,
    Infographic,
    Icon,
    Profile,
    InfoGrid,
    StructuredSteps,
    ContentPanel,
    GroupedBoard,
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
    Callout,
    CalloutContainer,
    CalloutDescription,
    CalloutTitle,
    CodeBlock,
    Pre,
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
