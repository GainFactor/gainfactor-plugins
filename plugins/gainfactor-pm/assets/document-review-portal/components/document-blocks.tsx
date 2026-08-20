import type { ReactNode } from 'react';

type Field = { label: string; value: ReactNode };

function hasContent(value: ReactNode): boolean {
  if (value === null || value === undefined || value === false) return false;
  return typeof value !== 'string' || value.trim().length > 0;
}

function visibleFields<T extends Field>(items?: T[]) {
  return (items ?? []).filter((item) => item.label.trim() && hasContent(item.value));
}

function visibleTags(tags?: string[]) {
  return (tags ?? []).map((tag) => tag.trim()).filter(Boolean);
}

export type InfoGridProps = {
  columns?: 2 | 3 | 4 | 'auto';
  items: Array<Field & { span?: 1 | 2 | 'full' }>;
};

export function InfoGrid({ columns = 'auto', items }: InfoGridProps) {
  const fields = visibleFields(items);
  if (fields.length === 0) return null;
  return (
    <dl className={`gf-info-grid gf-info-grid-${columns}`}>
      {fields.map((item, index) => (
        <div
          key={`${item.label}-${index}`}
          className={`gf-info-grid-item gf-info-grid-span-${item.span ?? 1}`}
        >
          <dt>{item.label}</dt>
          <dd>{item.value}</dd>
        </div>
      ))}
    </dl>
  );
}

export type ProfileProps = {
  name: string;
  role?: string;
  summary?: string;
  image?: { src: string; alt: string };
  facts?: Field[];
  tags?: string[];
  children?: ReactNode;
};

export function Profile({ name, role, summary, image, facts, tags, children }: ProfileProps) {
  const profileFacts = visibleFields(facts);
  const profileTags = visibleTags(tags);
  const hasImage = Boolean(image?.src && image.alt);
  return (
    <section className={`gf-profile${hasImage ? '' : ' gf-profile-no-image'}`}>
      {hasImage ? (
        <div className="gf-profile-media">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={image!.src} alt={image!.alt} />
        </div>
      ) : null}
      <div className="gf-profile-body">
        <header className="gf-profile-heading">
          <h3>{name}</h3>
          {role?.trim() ? <p className="gf-profile-role">{role}</p> : null}
          {summary?.trim() ? <p className="gf-profile-summary">{summary}</p> : null}
        </header>
        {profileFacts.length ? <InfoGrid items={profileFacts} columns="auto" /> : null}
        {profileTags.length ? (
          <ul className="gf-tags" aria-label={`${name}的标签`}>
            {profileTags.map((tag) => <li key={tag}>{tag}</li>)}
          </ul>
        ) : null}
        {hasContent(children) ? <div className="gf-profile-content">{children}</div> : null}
      </div>
    </section>
  );
}

export type StructuredStepsProps = {
  items: Array<{
    id?: string;
    title: string;
    content?: ReactNode;
    fields?: Array<Field & { tone?: 'default' | 'muted' | 'attention' }>;
  }>;
};

export function StructuredSteps({ items }: StructuredStepsProps) {
  const steps = items.filter((item) => item.title.trim());
  if (steps.length === 0) return null;
  return (
    <ol className="gf-structured-steps">
      {steps.map((item, index) => {
        const fields = visibleFields(item.fields);
        return (
          <li id={item.id || `structured-step-${index + 1}`} key={item.id || `${item.title}-${index}`}>
            <div className="gf-step-marker" aria-hidden="true">{index + 1}</div>
            <div className="gf-step-body">
              <h3>{item.title}</h3>
              {hasContent(item.content) ? <div className="gf-step-content">{item.content}</div> : null}
              {fields.length ? (
                <dl className="gf-step-fields">
                  {fields.map((field, fieldIndex) => (
                    <div key={`${field.label}-${fieldIndex}`} data-tone={field.tone ?? 'default'}>
                      <dt>{field.label}</dt>
                      <dd>{field.value}</dd>
                    </div>
                  ))}
                </dl>
              ) : null}
            </div>
          </li>
        );
      })}
    </ol>
  );
}

export type ContentPanelProps = {
  id?: string;
  title: string;
  eyebrow?: string;
  description?: ReactNode;
  tags?: string[];
  fields?: Field[];
  notice?: {
    label?: string;
    content: ReactNode;
    tone?: 'info' | 'warning' | 'success' | 'neutral';
  };
  href?: string;
  children?: ReactNode;
};

export function ContentPanel({
  id,
  title,
  eyebrow,
  description,
  tags,
  fields,
  notice,
  href,
  children,
}: ContentPanelProps) {
  const panelFields = visibleFields(fields);
  const panelTags = visibleTags(tags);
  const hasNotice = Boolean(notice && hasContent(notice.content));
  return (
    <article id={id} className="gf-content-panel">
      <header className="gf-content-panel-heading">
        {eyebrow?.trim() ? <span className="gf-content-panel-eyebrow">{eyebrow}</span> : null}
        <h3>{href ? <a href={href}>{title}</a> : title}</h3>
        {hasContent(description) ? <div className="gf-content-panel-description">{description}</div> : null}
        {panelTags.length ? (
          <ul className="gf-tags" aria-label={`${title}的标签`}>
            {panelTags.map((tag) => <li key={tag}>{tag}</li>)}
          </ul>
        ) : null}
      </header>
      {panelFields.length ? <InfoGrid items={panelFields} columns="auto" /> : null}
      {hasContent(children) ? <div className="gf-content-panel-content">{children}</div> : null}
      {hasNotice ? (
        <aside className="gf-content-panel-notice" data-tone={notice!.tone ?? 'neutral'}>
          <strong>{notice!.label?.trim() || '提示'}</strong>
          <div>{notice!.content}</div>
        </aside>
      ) : null}
    </article>
  );
}

export type GroupedBoardProps = {
  label?: string;
  columns?: 2 | 3 | 4 | 'auto';
  groups: Array<{
    id?: string;
    title: string;
    description?: ReactNode;
    items: Array<{
      id?: string;
      title: string;
      description?: ReactNode;
      href?: string;
      tags?: string[];
      fields?: Field[];
      children?: ReactNode;
    }>;
  }>;
};

export function GroupedBoard({ label, columns = 'auto', groups }: GroupedBoardProps) {
  const visibleGroups = groups
    .map((group) => ({
      ...group,
      items: group.items.filter((item) => item.title.trim()),
    }))
    .filter((group) => group.title.trim() && group.items.length > 0);
  if (visibleGroups.length === 0) return null;

  return (
    <div
      className={`gf-grouped-board gf-grouped-board-${columns}`}
      role="group"
      aria-label={label}
    >
      {visibleGroups.map((group, groupIndex) => (
        <section
          id={group.id || `grouped-board-group-${groupIndex + 1}`}
          className="gf-board-group"
          key={group.id || `${group.title}-${groupIndex}`}
        >
          <header className="gf-board-group-heading">
            <h3>{group.title}</h3>
            {hasContent(group.description) ? <div>{group.description}</div> : null}
          </header>
          <ul className="gf-board-items">
            {group.items.map((item, itemIndex) => {
              const itemTags = visibleTags(item.tags);
              const itemFields = visibleFields(item.fields);
              return (
                <li
                  id={item.id || `${group.id || `grouped-board-group-${groupIndex + 1}`}-item-${itemIndex + 1}`}
                  key={item.id || `${item.title}-${itemIndex}`}
                >
                  <article className="gf-board-item">
                    <header>
                      <h4>{item.href ? <a href={item.href}>{item.title}</a> : item.title}</h4>
                      {hasContent(item.description) ? <div className="gf-board-item-description">{item.description}</div> : null}
                    </header>
                    {itemTags.length ? (
                      <ul className="gf-tags" aria-label={`${item.title}的标签`}>
                        {itemTags.map((tag) => <li key={tag}>{tag}</li>)}
                      </ul>
                    ) : null}
                    {itemFields.length ? (
                      <dl className="gf-board-item-fields">
                        {itemFields.map((field, fieldIndex) => (
                          <div key={`${field.label}-${fieldIndex}`}>
                            <dt>{field.label}</dt>
                            <dd>{field.value}</dd>
                          </div>
                        ))}
                      </dl>
                    ) : null}
                    {hasContent(item.children) ? <div className="gf-board-item-content">{item.children}</div> : null}
                  </article>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </div>
  );
}
