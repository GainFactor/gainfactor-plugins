'use client';

import {
  getFonts,
  Infographic as AntVInfographic,
  loadSVGResource,
  registerResourceLoader,
  setDefaultFont,
} from '@antv/infographic';
import { useEffect, useRef } from 'react';
import dynamicIconImports from 'lucide-react/dynamicIconImports';

type IconName = keyof typeof dynamicIconImports;

const localIcon = '<symbol viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 12h8M12 8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>';

function escapeAttribute(value: unknown) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

async function loadLucideIcon(name: string) {
  const loader = dynamicIconImports[name as IconName];
  if (!loader) return loadSVGResource(localIcon) as unknown as SVGSymbolElement;
  const icon = await loader();
  const body = icon.__iconNode.map(([tag, attributes]) => {
    const serialized = Object.entries(attributes)
      .filter(([key]) => key !== 'key')
      .map(([key, value]) => `${key}="${escapeAttribute(value)}"`)
      .join(' ');
    return `<${tag}${serialized ? ` ${serialized}` : ''}/>`;
  }).join('');
  return loadSVGResource(
    `<symbol viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${body}</symbol>`,
  ) as unknown as SVGSymbolElement;
}

// Disable AntV's built-in remote font stylesheets and semantic icon service.
for (const font of getFonts()) {
  font.baseUrl = '';
  font.fontWeight = {};
}
setDefaultFont('system-ui');
registerResourceLoader(async ({ data }) => loadLucideIcon(data));

export function Infographic({ syntax, caption }: { syntax: string; caption?: string }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    containerRef.current.classList.remove('antv-infographic-error');
    containerRef.current.replaceChildren();
    const infographic = new AntVInfographic({
      container: containerRef.current,
      width: '100%',
      height: '100%',
      editable: false,
    });
    try {
      if (/(?:https?:\/\/|ref:(?:url|remote|search):)/i.test(syntax)) {
        throw new Error('Remote Infographic resources are disabled in the document portal');
      }
      infographic.render(syntax);
    } catch {
      containerRef.current.classList.add('antv-infographic-error');
      containerRef.current.textContent = syntax;
    }
    return () => infographic.destroy();
  }, [syntax]);

  return <figure className="antv-infographic">
    <div ref={containerRef} className="antv-infographic-canvas" />
    {caption ? <figcaption>{caption}</figcaption> : null}
  </figure>;
}
