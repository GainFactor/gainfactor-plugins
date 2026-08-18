'use client';

import { Expand, Minus, Plus, RotateCcw } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useEffect, useId, useRef, useState } from 'react';

const controls = [
  { icon: Minus, label: '缩小', delta: -0.1 },
  { icon: Plus, label: '放大', delta: 0.1 },
] as const;

export function Mermaid({ chart }: { chart: string }) {
  const id = useId().replace(/:/g, '');
  const { resolvedTheme } = useTheme();
  const containerRef = useRef<HTMLDivElement>(null);
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(false);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    let cancelled = false;

    void import('mermaid').then(async ({ default: mermaid }) => {
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: resolvedTheme === 'dark' ? 'dark' : 'base',
        themeVariables: {
          primaryColor: resolvedTheme === 'dark' ? '#1c2b41' : '#e9f2ff',
          primaryTextColor: resolvedTheme === 'dark' ? '#f1f2f4' : '#172b4d',
          primaryBorderColor: resolvedTheme === 'dark' ? '#579dff' : '#0c66e4',
          lineColor: resolvedTheme === 'dark' ? '#9fadbc' : '#44546f',
          secondaryColor: resolvedTheme === 'dark' ? '#22272b' : '#f7f8f9',
          tertiaryColor: resolvedTheme === 'dark' ? '#161a1d' : '#ffffff',
          fontFamily: 'var(--font-sans)',
        },
        flowchart: { htmlLabels: true, curve: 'basis' },
      });

      try {
        const result = await mermaid.render(`mermaid-${id}`, chart);
        if (!cancelled) {
          setSvg(result.svg);
          setError(false);
        }
      } catch {
        if (!cancelled) setError(true);
      }
    });

    return () => {
      cancelled = true;
    };
  }, [chart, id, resolvedTheme]);

  const reset = () => setScale(1);
  const fullscreen = () => containerRef.current?.requestFullscreen?.();

  return (
    <figure className="mermaid-frame" ref={containerRef}>
      <figcaption>
        <span>流程图</span>
        <span className="mermaid-controls">
          {controls.map(({ icon: Icon, label, delta }) => (
            <button key={label} type="button" aria-label={label} onClick={() => setScale((value) => Math.min(1.8, Math.max(0.6, value + delta)))}>
              <Icon aria-hidden="true" />
            </button>
          ))}
          <button type="button" aria-label="重置缩放" onClick={reset}>
            <RotateCcw aria-hidden="true" />
          </button>
          <button type="button" aria-label="全屏查看" onClick={fullscreen}>
            <Expand aria-hidden="true" />
          </button>
        </span>
      </figcaption>
      <div className="mermaid-canvas">
        {error ? (
          <p role="alert">流程图暂时无法渲染，请检查图表语法。</p>
        ) : svg ? (
          <div className="mermaid-svg" style={{ transform: `scale(${scale})` }} dangerouslySetInnerHTML={{ __html: svg }} />
        ) : (
          <p>正在渲染流程图…</p>
        )}
      </div>
    </figure>
  );
}
