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
import { ClientContext } from './client';
import { B, Dict, on, S, Signal, signal } from './core';
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

export const HelpPanel = make(({ helpE, docsB }: { helpE: Signal<S>, docsB: Signal<Dict<S>> }) => {
  const
    closed = { open: false, doc: '' },
    stateB = signal(closed),
    onDismiss = () => stateB(closed),
    showHelp = (id: S) => {
      stateB({
        open: true,
        doc: docsB()[id] ?? `Aw, snap! Help topic "${id}" not found.`,
      })
    },
    init = () => {
      on(helpE, showHelp)
    },
    render = () => {
      const { open, doc } = stateB()
      return (
        <Panel
          headerText='Help'
          isBlocking={false}
          isOpen={open}
          onDismiss={onDismiss}
        >{doc}</Panel>
      )
    }
  return { init, render, stateB }
})