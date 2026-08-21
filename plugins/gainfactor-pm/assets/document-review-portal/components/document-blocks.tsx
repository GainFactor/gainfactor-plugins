import type { ReactNode } from 'react';
import { Icon } from './lucide-icon';

export type FieldItem = { label: string; value: ReactNode; span?: 1 | 2 | 'full' };

function hasContent(value: ReactNode): boolean {
  if (value === null || value === undefined || value === false) return false;
  return typeof value !== 'string' || value.trim().length > 0;
}

function visibleFields(items?: FieldItem[]) {
  return (items ?? []).filter((item) => item.label.trim() && hasContent(item.value));
}

function visibleTags(tags?: string[]) {
  return (tags ?? []).map((tag) => tag.trim()).filter(Boolean);
}

export type FieldListProps = {
  items: FieldItem[];
  columns?: 1 | 2 | 3 | 4 | 'auto';
  variant?: 'plain' | 'grid';
};

export function FieldList({ items, columns = 'auto', variant = 'plain' }: FieldListProps) {
  const fields = visibleFields(items);
  if (fields.length === 0) return null;
  return <dl className={`gf-field-list gf-field-list-${variant} gf-field-list-${columns}`} data-doc-component="field-list">
    {fields.map((item, index) => {
      const inferredSpan = typeof item.value === 'string' && item.value.trim().length > 80 ? 'full' : 1;
      return <div className={`gf-field-item gf-field-span-${item.span ?? inferredSpan}`} key={`${item.label}-${index}`}><dt className="gf-field-label">{item.label}</dt><dd className="gf-field-value">{item.value}</dd></div>;
    })}
  </dl>;
}

function stableAnchor(value: string) {
  return value.trim().toLowerCase().replace(/[^\p{Letter}\p{Number}]+/gu, '-').replace(/^-|-$/g, '') || 'section';
}

export type SectionHeadingProps = { title: string; level?: 2 | 3 | 4; icon?: string; id?: string };

export function SectionHeading({ title, level = 2, icon, id }: SectionHeadingProps) {
  const anchor = id?.trim() || stableAnchor(title);
  const content = <>{icon ? <Icon name={icon} className="gf-section-heading-icon" /> : null}<span className="gf-section-heading-text">{title}</span></>;
  if (level === 4) return <h4 id={anchor} className="gf-section-heading" data-toc-title={title}>{content}</h4>;
  if (level === 3) return <h3 id={anchor} className="gf-section-heading" data-toc-title={title}>{content}</h3>;
  return <h2 id={anchor} className="gf-section-heading" data-toc-title={title}>{content}</h2>;
}

export function Citation({ source, children }: { source: string; children?: ReactNode }) {
  const sourceId = source.trim();
  if (!sourceId) return null;
  return <a className="gf-citation" href={`#source-${sourceId}`} data-citation={sourceId}>{children ?? `[${sourceId}]`}</a>;
}

export function Source({ id, children }: { id: string; children: ReactNode }) {
  const sourceId = id.trim();
  if (!sourceId || !hasContent(children)) return null;
  return <li id={`source-${sourceId}`} className="gf-source" data-source={sourceId}><span>[{sourceId}]</span><div>{children}</div></li>;
}

export function SourceIndex({ children, label = '来源索引' }: { children: ReactNode; label?: string }) {
  if (!hasContent(children)) return null;
  return <section className="gf-source-index" aria-label={label}><ol>{children}</ol></section>;
}

export type PersonaBriefProps = {
  name: string;
  identity?: string;
  situation?: string;
  priority?: string;
  image?: { src: string; alt: string };
  traits?: string[];
  facts?: FieldItem[];
};

export function PersonaBrief({ name, identity, situation, priority, image, traits, facts }: PersonaBriefProps) {
  const personaTraits = visibleTags(traits);
  const personaFacts = visibleFields(facts);
  const hasImage = Boolean(image?.src && image.alt);
  return <section className={`gf-persona-brief${hasImage ? '' : ' gf-persona-brief-no-image'}`} data-doc-component="persona-brief" aria-label={`${name}的画像摘要`}>
    {hasImage ? <div className="gf-persona-brief-media">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={image!.src} alt={image!.alt} />
    </div> : null}
    <div className="gf-persona-brief-body">
      <header className="gf-persona-brief-heading">
        {priority?.trim() ? <span className="gf-persona-brief-priority">{priority}</span> : null}
        <div className="gf-persona-brief-identity"><strong className="gf-entity-title">{name}</strong>{identity?.trim() ? <span>{identity}</span> : null}</div>
        {situation?.trim() ? <p className="gf-persona-brief-situation">{situation}</p> : null}
      </header>
      {personaTraits.length ? <ul className="gf-tags" aria-label={`${name}的关键特征`}>{personaTraits.map((trait) => <li key={trait}>{trait}</li>)}</ul> : null}
      {personaFacts.length ? <FieldList variant="plain" columns={2} items={personaFacts} /> : null}
    </div>
  </section>;
}

export type PanelProps = { id?: string; title: string; icon?: string; eyebrow?: string; description?: ReactNode; children?: ReactNode };

export function Panel({ id, title, icon, eyebrow, description, children }: PanelProps) {
  return <article id={id} className="gf-panel" data-doc-component="panel">
    <header className="gf-panel-heading">{eyebrow?.trim() ? <span className="gf-panel-eyebrow">{eyebrow}</span> : null}<h3 className="gf-component-title gf-heading-with-icon">{icon ? <Icon name={icon} /> : null}<span>{title}</span></h3>{hasContent(description) ? <div className="gf-panel-description">{description}</div> : null}</header>
    {hasContent(children) ? <div className="gf-panel-content">{children}</div> : null}
  </article>;
}

export type BoardProps = {
  label?: string;
  columns?: 1 | 2 | 3 | 'auto';
  groups: Array<{ id?: string; title: string; icon?: string; tone?: 'neutral' | 'info' | 'warning' | 'critical'; description?: ReactNode; children: ReactNode }>;
};

export function Board({ label, columns = 'auto', groups }: BoardProps) {
  const visibleGroups = groups.filter((group) => group.title.trim() && hasContent(group.children));
  if (visibleGroups.length === 0) return null;
  return <div className={`gf-board gf-board-${columns}`} data-doc-component="board" role="group" aria-label={label}>
    {visibleGroups.map((group, index) => <section id={group.id} className="gf-board-group" data-tone={group.tone ?? 'neutral'} key={group.id || `${group.title}-${index}`}>
      <header className="gf-board-heading"><h3 className="gf-component-title gf-heading-with-icon">{group.icon ? <Icon name={group.icon} /> : null}<span>{group.title}</span></h3>{hasContent(group.description) ? <div>{group.description}</div> : null}</header>
      <div className="gf-board-content">{group.children}</div>
    </section>)}
  </div>;
}
