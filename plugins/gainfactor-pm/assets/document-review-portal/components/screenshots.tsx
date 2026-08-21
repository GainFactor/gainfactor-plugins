'use client';

import type { CSSProperties, ReactNode } from 'react';
import { Children, useEffect, useState } from 'react';
import { Expand, X } from 'lucide-react';
import { FigureFrame } from './figure-frame';

export type ScreenshotProps = {
  src: string;
  title?: string;
  caption?: string;
  evidenceId?: string;
  device?: 'desktop' | 'tablet' | 'mobile';
  step?: string | number;
  maxHeight?: CSSProperties['maxHeight'];
};

export function Screenshot({
  src,
  title,
  caption,
  evidenceId,
  device = 'desktop',
  step,
  maxHeight = '70vh',
}: ScreenshotProps) {
  const [open, setOpen] = useState(false);
  const description = title?.trim() || caption?.trim() || evidenceId?.trim() || '产品截图';

  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false);
    };
    document.addEventListener('keydown', closeOnEscape);
    return () => document.removeEventListener('keydown', closeOnEscape);
  }, [open]);

  return <>
    <FigureFrame className="gf-screenshot" caption={<>
      <span className="gf-screenshot-number" />
      {step !== undefined ? <span className="gf-screenshot-step">步骤 {step}</span> : null}
      {title?.trim() ? <strong>{title}</strong> : null}
      {caption?.trim() ? <span className="gf-screenshot-copy">{caption}</span> : null}
      {evidenceId?.trim() ? <code>{evidenceId}</code> : null}
    </>}>
    <div data-device={device} data-missing-caption={caption?.trim() ? undefined : 'true'}>
      <button type="button" className="gf-screenshot-trigger" onClick={() => setOpen(true)} aria-label={`放大查看：${description}`}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={src} alt={description} style={{ maxHeight }} />
        <span className="gf-screenshot-expand"><Expand aria-hidden="true" />查看原图</span>
      </button>
    </div>
    </FigureFrame>
    {open ? (
      <div className="gf-screenshot-lightbox" data-device={device} role="dialog" aria-modal="true" aria-label={description} onClick={() => setOpen(false)}>
        <button type="button" onClick={() => setOpen(false)} aria-label="关闭原图"><X aria-hidden="true" /></button>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={src} alt={description} onClick={(event) => event.stopPropagation()} />
      </div>
    ) : null}
  </>;
}

export function ScreenshotGallery({
  children,
  columns = 2,
  layout = 'grid',
}: {
  children: ReactNode;
  columns?: 1 | 2 | 3;
  layout?: 'grid' | 'rail';
}) {
  if (Children.count(children) === 0) return null;
  return (
    <div
      className={`gf-screenshot-gallery gf-screenshot-gallery-${columns}`}
      data-layout={layout}
      aria-label={layout === 'rail' ? '横向截图证据，可左右滚动' : undefined}
    >
      {children}
    </div>
  );
}

export function EvidenceStep({
  id,
  step,
  title,
  children,
  evidence,
}: {
  id?: string;
  step: string | number;
  title: string;
  children?: ReactNode;
  evidence?: ReactNode;
}) {
  return (
    <section id={id} className="gf-evidence-step">
      <div className="gf-evidence-step-copy">
        <span className="gf-evidence-step-number">步骤 {step}</span>
        <h3>{title}</h3>
        {children ? <div>{children}</div> : null}
      </div>
      {evidence ? <div className="gf-evidence-step-evidence">{evidence}</div> : null}
    </section>
  );
}
