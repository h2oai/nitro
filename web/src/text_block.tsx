import React from 'react';
import { Markdown } from './markdown';
import { BoxProps, make } from './ui';

export const TextBlock = make(({ context, box }: BoxProps) => {
  const
    ref = React.createRef<HTMLDivElement>(),
    update = () => {
      const { index } = box
      if (index < 0) return

      const el = ref.current
      if (!el) return

      el.querySelectorAll<HTMLAnchorElement>('a[data-jump]').forEach(link => {
        const value = link.getAttribute('data-jump')
        if (value) {
          link.onclick = e => {
            context.capture(index, value)
            context.submit()
            e.preventDefault()
          }
        }
      })
    },
    render = () => {
      return <Markdown ref={ref} dangerouslySetInnerHTML={{ __html: box.text ?? '' }} />
    }
  return { init: update, update, render }
})