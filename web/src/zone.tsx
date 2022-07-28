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

import { cssColor, IRGB, Pivot, PivotItem } from '@fluentui/react';
import React from 'react';
import { XBox } from './box';
import { ClientContext } from './client';
import { B, Dict, isS, S } from './core';
import { Expander } from './expander';
import { Help } from './help';
import { Box } from './protocol';

// http://www.w3.org/TR/AERT#color-contrast
const isBright = ({ r, g, b }: IRGB) => (r * 299 + g * 587 + b * 114) / 1000 > 125

const translate = (s: S): S => isS(s) ? s.replace(/\$([\w-]+)/gi, 'var(--$1)') : s

const hasLabel = (box: Box): B => {
  switch (box.mode) {
    case 'text':
    case 'number':
    case 'menu':
    case 'date':
    case 'button':
    case 'tag':
    case 'rating':
      if (box.text) return true
  }
  return false
}

export const Zone = ({ context, box, inRow }: { context: ClientContext, box: Box, inRow: B }) => {
  const
    { mode, items, layout, style: className } = box,
    isRow = mode === 'row'

  if (items) {
    switch (mode) {
      case 'tabs':
        {
          if (layout === 'col') {
            const tabs = items.map((box, i) => (
              <Expander key={box.xid} headerText={box.text ?? `Tab ${i + 1}`}>
                <Zone key={box.xid} context={context} box={box} inRow={isRow} />
              </Expander>
            ))
            return <div className={className} data-name={box.name ?? undefined}>{tabs}</div>
          } else {
            const tabs = items.map((box, i) => (
              <PivotItem key={box.xid} headerText={box.text ?? `Tab ${i + 1}`} itemIcon={box.icon ?? undefined}>
                <Zone key={box.xid} context={context} box={box} inRow={isRow} />
              </PivotItem>
            ))
            return (
              <div className={className} data-name={box.name ?? undefined} >
                <Pivot>{tabs}</Pivot>
              </div>
            )
          }
        }
      default:
        {
          const
            children = items.map(box => (
              <Zone key={box.xid} context={context} box={box} inRow={isRow} />
            )),
            style = box.image ? { backgroundImage: `url(${box.image})` } : undefined
          return (
            <div className={className} data-name={box.name ?? undefined} style={style} >{children}</div>
          )
        }
    }
  } else {
    switch (mode) {
      case 'image':
        {
          return (
            <img
              className={className}
              data-name={box.name ?? undefined}
              alt={box.text}
              src={box.image} />
          )
        }
      default:
        {
          const
            component = <XBox context={context.scoped(box.index, box.xid)} box={box} />
          return box.hint || box.help
            ? <Help context={context} hint={box.hint} help={box.help} offset={hasLabel(box)}>{component}</Help>
            : component
        }
    }
  }
}