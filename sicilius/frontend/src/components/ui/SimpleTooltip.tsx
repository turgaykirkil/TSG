'use client';

import * as React from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';

type SimpleTooltipProps = {
  content: React.ReactNode;
  side?: 'top' | 'right' | 'bottom' | 'left';
  children: React.ReactNode;
};

export default function SimpleTooltip({ content, side = 'top', children }: SimpleTooltipProps) {
  return (
    <Tooltip.Provider delayDuration={200}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>{children}</Tooltip.Trigger>
        <Tooltip.Content
          side={side}
          sideOffset={8}
          className="z-50 rounded bg-slate-900 px-2 py-1 text-xs text-white shadow-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
        >
          {content}
          <Tooltip.Arrow className="fill-slate-900" />
        </Tooltip.Content>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
