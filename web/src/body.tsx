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

import { ContextualMenu, Dialog, DialogType, IModalProps } from '@fluentui/react';
import { Client, defaultLayout } from './client';
import { signal, xid } from './core';
import { hasActions } from './heuristics';
import { Box } from './protocol';
import { make } from './ui';
import { XBox } from './box';

const
  continueButton: Box = {
    xid: xid(),
    modes: new Set(['button']),
    index: -1, //don't record
    options: [{ value: 'continue', text: 'Continue' }],
  },
  makeContinuable = (boxes: Box[]): Box[] => hasActions(boxes) ? boxes : [...boxes, continueButton]

export const Body = ({ client }: { client: Client }) => {
  const boxes: Box[] = client.layoutB() === defaultLayout ? makeContinuable(client.body) : client.body
  return (
    <div className='main'>
      <XBox context={client.context} box={{ xid: 'main', index: -1, modes: new Set(['col']), items: boxes, options: [] }} />
    </div>
  )
}
const modalProps: IModalProps = {
  isBlocking: false,
  dragOptions: {
    menu: ContextualMenu,
    moveMenuItemText: 'Move',
    closeMenuItemText: 'Close',
    keepInBounds: true,
  },
  styles: { main: { maxWidth: 450 } },
}

export const Popup = make(({ client }: { client: Client }) => {
  const
    hiddenB = signal(false),
    boxes: Box[] = makeContinuable(client.popup),
    render = () => {
      const
        { title } = boxes[0], // popups have exactly one box.
        hidden = hiddenB()

      return (
        <Dialog
          dialogContentProps={{
            type: DialogType.normal, // TODO largeheader
            title: title ?? 'Alert',
            closeButtonAriaLabel: 'Close',
          }}
          modalProps={modalProps}
          hidden={hidden}
        >
          <XBox context={client.context} box={{ xid: 'popup', index: -1, modes: new Set(['col']), items: boxes, options: [] }} />
        </Dialog >
      )
    }
  return { render, hiddenB }
})