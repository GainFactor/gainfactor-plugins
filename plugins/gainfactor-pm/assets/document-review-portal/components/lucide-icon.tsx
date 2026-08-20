'use client';

import { DynamicIcon, iconNames, type IconName } from 'lucide-react/dynamic';

const availableIcons = new Set<string>(iconNames);

export type PortalIconProps = {
  name: string;
  label?: string;
  size?: number;
  strokeWidth?: number;
  color?: string;
  className?: string;
};

export function Icon({
  name,
  label,
  size = 18,
  strokeWidth = 2,
  color = 'currentColor',
  className,
}: PortalIconProps) {
  const classes = ['portal-icon', className].filter(Boolean).join(' ');
  if (!availableIcons.has(name)) {
    return (
      <span
        className={`${classes} portal-icon-missing`}
        role="img"
        aria-label={label ?? `未知 Lucide 图标：${name}`}
        title={`未知 Lucide 图标：${name}`}
      >
        ?
      </span>
    );
  }

  return (
    <span
      className={classes}
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      title={label}
    >
      <DynamicIcon
        name={name as IconName}
        size={size}
        strokeWidth={strokeWidth}
        color={color}
        aria-hidden="true"
      />
    </span>
  );
}
