// Copyright 2022 H2O.ai, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { IButtonProps, IconButton, Label, Panel, Stack, TeachingBubble } from '@fluentui/react';
import { createRef, useEffect, useState } from 'react';
import { B, Dict, on, S, Signal, splitLines, xid } from './core';
import { markdown } from './markdown';
import { Box, labeledBoxModes } from './protocol';
import { BoxProps, Context } from './ui';

const tokenize = (hint?: S) => {
  if (!hint) return []
  const
    s = hint.trim(),
    lines = splitLines(s)
  return lines.length > 1 ? [lines.slice(1).join('\n'), lines[0]] : lines
}

const Hint = ({ context, hint: rawHint, help }: { context: Context, hint?: S, help?: S }) => {
  const
    id = xid(),
    [visible, setVisible] = useState(false),
    [hint, headline] = tokenize(rawHint),
    showHint = () => {
      if (hint) {
        setVisible(true)
      } else if (help) {
        context.help(help)
      }
    },
    hideHint = () => setVisible(false),
    moreButton: IButtonProps | undefined = help ? {
      children: 'More...',
      onClick: () => {
        context.help(help)
        setVisible(false)
      }
    } : undefined,
    bubble = visible && hint
      ? (
        <TeachingBubble
          target={'#' + id}
          primaryButtonProps={moreButton}
          hasCloseButton={true}
          onDismiss={hideHint}
          headline={headline}
        >{hint}</TeachingBubble>
      )
      : null
  return (
    <>
      {bubble}
      <IconButton id={id} iconProps={{ iconName: 'Info' }} onClick={showHint} />
    </>
  )
}

const hasLabel = (box: Box): B => {
  const { modes } = box
  for (const t of labeledBoxModes) if (modes.has(t) && box.text) return true
  return false
}

export const Help = ({ context, box, children }: BoxProps & { children: JSX.Element }) => {
  const { help, hint } = box

  if (!(hint || help)) return children

  const
    button = <Hint context={context} hint={hint} help={help} />,
    maybeWithLabel = hasLabel(box)
      ? (
        <Stack>
          <Stack.Item><Label>&nbsp;</Label></Stack.Item>
          <Stack.Item>{button}</Stack.Item>
        </Stack>
      )
      : button

  return (
    <Stack horizontal tokens={{ childrenGap: 5 }}>
      <Stack.Item grow>{children}</Stack.Item>
      <Stack.Item>{maybeWithLabel}</Stack.Item>
    </Stack>
  )
}

const Doc = ({ html, loadHelp }: { html: S, loadHelp: (id: S) => void }) => {
  const ref = createRef<HTMLDivElement>()
  useEffect(() => {
    const el = ref.current
    if (!el) return

    el.querySelectorAll<HTMLAnchorElement>('a[data-jump]').forEach(link => {
      const id = link.getAttribute('data-jump')
      if (id) link.onclick = e => {
        loadHelp(id)
        e.preventDefault()
      }
    })
  })

  return <div className='prose' ref={ref} dangerouslySetInnerHTML={{ __html: html }} />
}

export const HelpPanel = ({ helpE, helpB }: { helpE: Signal<S>, helpB: Signal<Dict<S>> }) => {
  const
    [open, setOpen] = useState(false),
    [html, setHtml] = useState(''),
    onDismiss = () => setOpen(false),
    loadHelp = (id: S) => {
      const d = helpB()
      setHtml(d[id] ?? d['missing'] ?? 'Help topic not found.')
    }

  useEffect(() => {
    const onHelp = on(helpE, help => {
      const [html] = markdown(help)
      setHtml(html)
      setOpen(true)
    })
    return onHelp.dispose
  })

  return (
    <Panel
      isBlocking={false}
      isOpen={open}
      onDismiss={onDismiss}
    ><Doc html={html} loadHelp={loadHelp} /></Panel>
  )
}