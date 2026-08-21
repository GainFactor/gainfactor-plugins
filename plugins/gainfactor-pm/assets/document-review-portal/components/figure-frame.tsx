import type { ReactNode } from 'react';

export function FigureFrame({ className, title, actions, children, caption, error }: { className: string; title?: ReactNode; actions?: ReactNode; children: ReactNode; caption?: ReactNode; error?: ReactNode }) {
  return <figure className={`gf-figure ${className}`}>
    {title || actions ? <header className="gf-figure-header"><span>{title}</span>{actions}</header> : null}
    <div className="gf-figure-stage">{children}</div>
    {error ? <div className="gf-figure-error" role="alert">{error}</div> : null}
    {caption ? <figcaption className="gf-figure-caption">{caption}</figcaption> : null}
  </figure>;
}
