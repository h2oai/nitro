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

import { Dialog, DialogType } from '@fluentui/react';
import React from 'react';
import { B, isB, signal, xid } from './core';
import { Box } from './protocol';
import { Send } from './socket';
import { make, newCaptureContext } from './ui';
import { Zone } from './zone';

const
  continueButton: Box = {
    xid: xid(),
    mode: 'button',
    index: -1, //don't capture
    options: [{ value: 'continue', text: 'Continue' }]
  },
  hasActions = (boxes: Box[]): B => { // recursive
    for (const box of boxes) {
      if (box.items) {
        if (hasActions(box.items)) return true
      } else {
        const { mode } = box
        switch (mode) {
          case 'button':
            if (box.options.length) return true
            break
          case 'md':
            if (box.index >= 0) return true
            break
          case 'toggle':
            return true
          case 'table':
            if (isB(box.multiple)) return true
            if (box.headers) for (const header of box.headers) if (header.mode === 'link') return true
        }
      }
    }
    return false
  },

  makeContinuable = (boxes: Box[]): Box[] => hasActions(boxes) ? boxes : [...boxes, continueButton]


export const Body = (props: { send: Send, boxes: Box[] }) => {
  const
    boxes: Box[] = makeContinuable(props.boxes),
    context = newCaptureContext(props.send, [])
  return (
    <div className='main'>
      <Zone context={context} boxes={boxes} box={{}} />
    </div>
  )
}

export const Popup = make((props: { send: Send, boxes: Box[] }) => {
  const
    hiddenB = signal(false),
    boxes: Box[] = makeContinuable(props.boxes),
    context = newCaptureContext(props.send, []),
    styles = { main: { maxWidth: 450 } },
    hide = () => {
      hiddenB(true)
    },
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
          modalProps={{
            isBlocking: false,
            styles,
            // TODO dragOptions
          }}
          onDismiss={hide}
          hidden={hidden}
        >
          <Zone context={context} boxes={boxes} box={{}} />
        </Dialog >
      )
    }
  return { render, hiddenB }
})