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
import React from 'react';
import { B, on, S, Signal, signal, splitLines, xid } from './core';
import { markdown } from './markdown';
import { Context, make } from './ui';

const tokenize = (hint?: S) => {
  if (!hint) return []
  const
    s = hint.trim(),
    lines = splitLines(s)
  return lines.length > 1 ? [lines.slice(1).join('\n'), lines[0]] : lines
}

const Hint = make(({ context, hint: rawHint, help }: { context: Context, hint?: S, help?: S }) => {
  const
    id = xid(),
    visibleB = signal(false),
    [hint, headline] = tokenize(rawHint),
    showHint = () => {
      if (hint) {
        visibleB(true)
      } else if (help) {
        context.help(help)
      }
    },
    hideHint = () => visibleB(false),
    moreButton: IButtonProps | undefined = help ? {
      children: 'More...',
      onClick: () => {
        context.help(help)
        visibleB(false)
      }
    } : undefined,
    render = () => {
      const
        bubble = visibleB() && hint
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
  return { render, visibleB }
})

export const Help = make(({ context, hint, help, offset, children }: { context: Context, hint?: S, help?: S, offset: B, children: JSX.Element }) => {
  const
    render = () => {
      const
        button = <Hint context={context} hint={hint} help={help} />,
        maybeWithLabel = offset
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
  return { render }
})

const Doc = make(({ html, helpE }: { html: S, helpE: Signal<S> }) => {
  const
    ref = React.createRef<HTMLDivElement>(),
    update = () => {
      const el = ref.current
      if (!el) return

      el.querySelectorAll<HTMLAnchorElement>('a[data-jump]').forEach(link => {
        const id = link.getAttribute('data-jump')
        if (id) link.onclick = _ => { helpE(id) }
      })
    },
    render = () => {
      return <div className='prose' ref={ref} dangerouslySetInnerHTML={{ __html: html }} />
    }
  return { init: update, update, render }
})

export const HelpPanel = make(({ helpE }: { helpE: Signal<S> }) => {
  const
    closed = { open: false, help: '' },
    stateB = signal(closed),
    onDismiss = () => stateB(closed),
    init = () => on(helpE, (help: S) => stateB({ open: true, help })),
    render = () => {
      const
        { open, help } = stateB(),
        [html] = markdown(help)
      return (
        <Panel
          isBlocking={false}
          isOpen={open}
          onDismiss={onDismiss}
        ><Doc html={html} helpE={helpE} /></Panel>
      )
    }
  return { init, render, stateB }
})