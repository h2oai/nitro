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

import { INavLink, INavLinkGroup, Nav, Pivot, PivotItem } from '@fluentui/react';
import React from 'react';
import { XBox } from './box';
import { clicker, ClientContext } from './client';
import { B, by, on, signal, Signal, zip } from './core';
import { css } from './css';
import { Expander } from './expander';
import { Help } from './help';
import { labeledModes } from './heuristics';
import { Box } from './protocol';
import { make } from './ui';

const hasLabel = (box: Box): B => {
  const { modes } = box
  for (const t of labeledModes) if (modes.has(t) && box.text) return true
  return false
}

type Container = { context: ClientContext, box: Box }

const Accordion = ({ context, box, items }: Container & { items: Box[] }) => {
  const { style } = box
  const tabs = items.map((box, i) => (
    <Expander key={box.xid} headerText={box.title ?? `Tab ${i + 1}`}>
      <Zone context={context} box={box} />
    </Expander>
  ))
  return <div className={css(style)} data-name={box.name ?? undefined}>{tabs}</div>
}

const NavSetItem = make(({ visibleB, children }: { visibleB: Signal<B>, children: React.ReactNode }) => {
  const
    render = () => {
      const style: React.CSSProperties = { display: visibleB() ? 'block' : 'none' }
      return <div style={style}>{children}</div>
    }
  return { render, visibleB }
})


const NavSet = make(({ context, box, items }: Container & { items: Box[] }) => {
  const
    { style, options } = box,
    selectedIndexB = signal(0),
    selectedKeyB = by(selectedIndexB, i => String(options[i].value)),
    visibleBs = options.map((_, i) => signal(i === selectedIndexB() ? true : false)),
    tabs = zip(items, visibleBs, (box, visibleB) => (
      <NavSetItem key={box.xid} visibleB={visibleB}><Zone key={box.xid} context={context} box={box} /></NavSetItem>
    )),
    links: INavLink[] = zip(items, options, (box, o) => ({
      key: String(o.value),
      name: o.text ?? '',
      url: '',
      icon: box.icon,
    })),
    groups: INavLinkGroup[] = [{ links }],
    onLinkClick = (ev?: React.MouseEvent<HTMLElement>, item?: INavLink) => {
      if (item) selectedIndexB(links.indexOf(item))
    },
    render = () => (
      <div className={css('flex gap-4', style)}>
        <div className={css('border-r')}>
          <Nav groups={groups} onLinkClick={onLinkClick} selectedKey={selectedKeyB()} />
        </div>
        <div className={css('grow')}>{tabs}</div>
      </div>
    )

  on(selectedIndexB, k => visibleBs.forEach((v, i) => v(i === k ? true : false)))

  return { render, selectedKeyB }
})

const TabSet = ({ context, box, items }: Container & { items: Box[] }) => {
  const
    { style, options } = box,
    tabs = zip(options, items, (opt, box, i) => (
      <PivotItem key={box.xid} headerText={opt.text ?? `Tab ${i + 1}`} itemIcon={box.icon ?? undefined} style={{ padding: '8px 0' }}>
        <Zone context={context} box={box} />
      </PivotItem>
    ))

  return (
    <div className={css(style)} data-name={box.name ?? undefined} >
      <Pivot>{tabs}</Pivot>
    </div>
  )
}

export const Zone = ({ context, box }: Container) => {
  const { modes, items, options, image, path, style } = box
  if (items) {
    if (options?.length) {
      return modes.has('col')
        ? <NavSet context={context} box={box} items={items} />
        : <TabSet context={context} box={box} items={items} />
    }

    const children = items.map(box => <Zone key={box.xid} context={context} box={box} />)

    if (modes.has('group')) return (
      <Expander headerText={box.title ?? 'Group'}>{children}</Expander>
    )

    const
      background = image ? { backgroundImage: `url(${image})` } : undefined,
      flex = modes.has('col') ? 'flex flex-col gap-2' : modes.has('row') ? 'flex gap-2' : undefined,
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