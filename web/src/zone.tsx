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
import { ClientContext, clicker } from './client';
import { B } from './core';
import { css } from './css';
import { Expander } from './expander';
import { Help } from './help';
import { Box } from './protocol';

const labeledBoxes = ['text', 'number', 'menu', 'date', 'button', 'tag', 'rating']
const hasLabel = (box: Box): B => {
  const { modes } = box
  for (const t of labeledBoxes) if (modes.has(t) && box.text) return true
  return false
}

type Container = { context: ClientContext, box: Box }

const Accordion = ({ context, box, items }: Container & { items: Box[] }) => {
  const { style } = box
  const tabs = items.map((box, i) => (
    <Expander key={box.xid} headerText={box.title ?? `Tab ${i + 1}`}>
      <Zone key={box.xid} context={context} box={box} />
    </Expander>
  ))
  return <div className={css(style)} data-name={box.name ?? undefined}>{tabs}</div>
}

const Tabset = ({ context, box, items }: Container & { items: Box[] }) => {
  const { style } = box
  const tabs = items.map((box, i) => (
    <PivotItem key={box.xid} headerText={box.title ?? `Tab ${i + 1}`} itemIcon={box.icon ?? undefined} style={{ padding: '8px 0' }}>
      <Zone key={box.xid} context={context} box={box} />
    </PivotItem>
  ))
  return (
    <div className={css(style)} data-name={box.name ?? undefined} >
      <Pivot>{tabs}</Pivot>
    </div>
  )
}

export const Zone = ({ context, box }: Container) => {
  const { modes, items, image, path, style } = box
  if (items) {
    if (modes.has('tab')) {
      return modes.has('vertical')
        ? <Accordion context={context} box={box} items={items} />
        : <Tabset context={context} box={box} items={items} />
    }
    const
      children = items.map(box => (
        <Zone key={box.xid} context={context} box={box} />
      )),
      background = image ? { backgroundImage: `url(${image})` } : undefined,
      flex = modes.has('col') ? 'flex flex-col gap-2' : modes.has('row') ? 'flex flex-row gap-2' : undefined,
      onClick = path ? clicker(path) : undefined,
      pointer = path ? 'cursor-pointer' : undefined
    return (
      <div
        className={css(flex, pointer, style)}
        data-name={box.name ?? undefined}
        onClick={onClick}
        style={background}
      >{children}</div>
    )
  }

  if (modes.has('image')) {
    return (
      <img
        className={css(style)}
        data-name={box.name ?? undefined}
        alt={box.text}
        src={box.image} />
    )
  }

  const
    component = <XBox context={context.scoped(box.index, box.xid)} box={box} />
  return box.hint || box.help
    ? <Help context={context} hint={box.hint} help={box.help} offset={hasLabel(box)}>{component}</Help>
    : component
}