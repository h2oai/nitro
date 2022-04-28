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

import React from 'react';
import { B, isB, xid } from './core';
import { Box } from './protocol';
import { Send } from './socket';
import { newCaptureContext } from './ui';
import { Zone } from './zone';

const continueButton: Box = {
  xid: xid(),
  mode: 'button',
  index: -1, //don't capture
  options: [{ value: 'continue', text: 'Continue' }]
}

const hasActions = (boxes: Box[]): B => { // recursive
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
}

export const Body = (props: { send: Send, boxes: Box[] }) => {
  const
    original = props.boxes,
    canContinue = hasActions(original),
    boxes: Box[] = canContinue ? original : [...original, continueButton],
    context = newCaptureContext(props.send, [])
  return (
    <div className='main'>
      <Zone context={context} boxes={boxes} box={{}} />
    </div>
  )
}