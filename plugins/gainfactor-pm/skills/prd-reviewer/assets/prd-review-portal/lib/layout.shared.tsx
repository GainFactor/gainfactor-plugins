import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { appName } from './shared';
import Image from 'next/image';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: (
        <span className="brand-lockup">
          <span className="brand-mark">
            <Image src="/gainfactor-mark.png" alt="" width={24} height={24} priority unoptimized />
          </span>
          <span className="brand-copy">
            <strong>{appName}</strong>
            <small>Human × AI, Multiply Your Career</small>
          </span>
        </span>
      ),
    },
  };
}
