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

import { IconButton, Label, Panel, Stack } from '@fluentui/react';
import React from 'react';
import { ClientContext } from './client';
import { B, Dict, on, S, Signal, signal } from './core';
import { markdown } from './markdown';
import { make } from './ui';

export const Help = make(({ context, help, offset, children }: { context: ClientContext, help: S, offset: B, children: JSX.Element }) => {
  const
    onClick = () => {
      context.help(help)
    },
    render = () => {
      const
        button = <IconButton iconProps={{ iconName: 'Info' }} onClick={onClick} />,
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
        if (id) link.onclick = e => { helpE(id) }
      })
    },
    render = () => {
      return <div className='md' ref={ref} dangerouslySetInnerHTML={{ __html: html }} />
    }
  return { init: update, update, render }
})

export const HelpPanel = make(({ helpE, docsB }: { helpE: Signal<S>, docsB: Signal<Dict<S>> }) => {
  const
    closed = { open: false, doc: '' },
    stateB = signal(closed),
    onDismiss = () => stateB(closed),
    showHelp = (id: S) => {
      stateB({
        open: true,
        doc: docsB()[id] ?? `> Aw, snap! Help topic "${id}" not found.`,
      })
    },
    init = () => {
      on(helpE, showHelp)
    },
    render = () => {
      const
        { open, doc } = stateB(),
        [html, _] = markdown(doc)
      return (
        <Panel
          headerText='Help'
          isBlocking={false}
          isOpen={open}
          onDismiss={onDismiss}
        ><Doc html={html} helpE={helpE} /></Panel>
      )
    }
  return { init, render, stateB }
})