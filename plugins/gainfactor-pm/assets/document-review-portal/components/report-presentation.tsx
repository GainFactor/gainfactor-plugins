import { Quote } from 'lucide-react';
import type { PortalModule, PortalPresentation } from '@/lib/portal-data';

function ModuleHeading({ module }: { module: PortalModule }) {
  if (!module.title && !module.description) return null;
  return <header className="portal-module-heading">
    {module.title ? <h2>{module.title}</h2> : null}
    {module.description ? <p>{module.description}</p> : null}
  </header>;
}

function PortalModuleView({ module }: { module: PortalModule }) {
  if (module.type === 'metrics') return <section className="portal-module">
    <ModuleHeading module={module} />
    <div className="report-summary-grid">{module.items.map((item) => <article key={`${item.label}-${item.value}`} className="report-summary-card">
      <span>{item.label}</span><strong>{item.value}</strong>
      {item.note ? <p>{item.note}</p> : null}
      {item.change || item.definition || item.source ? <dl>
        {item.change ? <div><dt>同比</dt><dd>{item.change}</dd></div> : null}
        {item.definition ? <div><dt>口径</dt><dd>{item.definition}</dd></div> : null}
        {item.source ? <div><dt>来源</dt><dd>{item.source}</dd></div> : null}
      </dl> : null}
    </article>)}</div>
  </section>;

  if (module.type === 'cards') return <section className="portal-module persona-showcase">
    <ModuleHeading module={module} />
    <div className="persona-showcase-grid">{module.items.map((item) => <article key={item.title} className={`persona-card${item.image ? '' : ' no-image'}`}>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      {item.image ? <img src={item.image} alt={item.imageAlt || item.title} /> : null}
      <div className="persona-card-copy">
        {item.eyebrow ? <span className="persona-segment">{item.eyebrow}</span> : null}
        <h3>{item.title}</h3>
        {item.quote ? <blockquote><Quote aria-hidden="true" />{item.quote}</blockquote> : null}
        {item.description ? <p>{item.description}</p> : null}
        {item.fields?.map((field) => <p key={field.label}><b>{field.label}</b>{field.value}</p>)}
      </div>
    </article>)}</div>
  </section>;

  if (module.type === 'steps') return <section className="portal-module">
    <ModuleHeading module={module} />
    <ol className="portal-steps">{module.items.map((item, index) => <li key={`${index}-${item.title ?? item.content}`}>
      <span>{index + 1}</span><div>{item.title ? <strong>{item.title}</strong> : null}<p>{item.content}</p></div>
    </li>)}</ol>
  </section>;

  return <aside className={`portal-callout ${module.tone ?? 'info'}`}>
    <ModuleHeading module={module} /><p>{module.content}</p>
  </aside>;
}

export function ReportPresentation({ data }: { data?: PortalPresentation }) {
  if (!data || data.modules.length === 0) return null;
  return <section className={`report-presentation layout-${data.layout}`} aria-label="文档重点内容">
    {data.modules.map((module) => <PortalModuleView key={module.id} module={module} />)}
  </section>;
}
