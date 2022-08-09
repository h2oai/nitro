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

import { Pivot, PivotItem } from '@fluentui/react';
import { XBox } from './box';
import { ClientContext } from './client';
import { B } from './core';
import { Expander } from './expander';
import { Help } from './help';
import { Box } from './protocol';

const labeledBoxes = ['text', 'number', 'menu', 'date', 'button', 'tag', 'rating']
const hasLabel = (box: Box): B => {
  const { modes } = box
  for (const t of labeledBoxes) if (modes.has(t) && box.text) return true
  return false
}

export const Zone = ({ context, box, inRow }: { context: ClientContext, box: Box, inRow: B }) => {
  const
    { modes, items, style: className } = box,
    isRow = modes.has('row')

  if (items) {
    if (modes.has('tab')) {
      if (modes.has('vertical')) {
        const tabs = items.map((box, i) => (
          <Expander key={box.xid} headerText={box.title ?? `Tab ${i + 1}`}>
            <Zone key={box.xid} context={context} box={box} inRow={isRow} />
          </Expander>
        ))
        return <div className={className} data-name={box.name ?? undefined}>{tabs}</div>
      } else {
        const tabs = items.map((box, i) => (
          <PivotItem key={box.xid} headerText={box.title ?? `Tab ${i + 1}`} itemIcon={box.icon ?? undefined}>
            <Zone key={box.xid} context={context} box={box} inRow={isRow} />
          </PivotItem>
        ))
        return (
          <div className={className} data-name={box.name ?? undefined} >
            <Pivot>{tabs}</Pivot>
          </div>
        )
      }
    } else {
      const
        children = items.map(box => (
          <Zone key={box.xid} context={context} box={box} inRow={isRow} />
        )),
        style = box.image ? { backgroundImage: `url(${box.image})` } : undefined
      return (
        <div className={className} data-name={box.name ?? undefined} style={style} >{children}</div>
      )
    }
  } else {
    if (modes.has('image')) {
      return (
        <img
          className={className}
          data-name={box.name ?? undefined}
          alt={box.text}
          src={box.image} />
      )
    } else {
      const
        component = <XBox context={context.scoped(box.index, box.xid)} box={box} />
      return box.hint || box.help
        ? <Help context={context} hint={box.hint} help={box.help} offset={hasLabel(box)}>{component}</Help>
        : component

    }
  }
}