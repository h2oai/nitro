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
import React, { useEffect } from 'react';
import { Banner } from './banner';
import { Buttons } from './buttons';
import { Calendar } from './calendar';
import { Checkbox } from './checkbox';
import { Checklist } from './checklist';
import { ChoiceGroup } from './choice_group';
import { jump } from './client';
import { ColorPalette } from './color_palette';
import { ColorPicker } from './color_picker';
import { ComboBox } from './combobox';
import { B, by, on, signal, Signal, zip } from './core';
import { css } from './css';
import { DatePicker } from './date_picker';
import { Dropdown } from './dropdown';
import { Droplist } from './droplist';
import { Expander } from './expander';
import { FileUpload } from './file_upload';
import { Graphic, Graphic2, GraphicLabel } from './graphics';
import { Help } from './help';
import { PluginBox } from './plugin';
import { ProgressBar } from './progress';
import { Box } from './protocol';
import { Rating } from './rating';
import { Separator } from './separator';
import { Slider } from './slider';
import { Spinbox } from './spinbox';
import { Spinner } from './spinner';
import { SVGBox } from './svg';
import { Table } from './table';
import { TagPicker } from './tag_picker';
import { Textbox } from './textbox';
import { TextBlock } from './text_block';
import { TimePicker } from './time_picker';
import { Toggle } from './toggle';
import { BoxProps, Context, make } from './ui';
import { WebView } from './webview';

export const XBox = ({ context: root, box }: BoxProps) => { // recursive
  const
    { modes, options, items } = box,
    context = box.index >= 0 ? root.scoped(box.index, box.pid ?? box.xid) : root

  if (items) {
    if (options?.length) return modes.has('col')
      ? <NavSet context={context} box={box} />
      : <TabSet context={context} box={box} />

    const children = items.map(box => (
      <Help key={box.xid} context={context} box={box}>
        <XBox context={context} box={box} />
      </Help>
    ))

    return modes.has('group')
      ? <Expander box={box}>{children}</Expander>
      : <NonTerminal context={context} box={box}>{children}</NonTerminal>

  } // !items

  if (box.image) return (
    <img
      className={css(box.style)}
      data-name={box.name}
      alt={box.text}
      src={box.image}
    />
  )

  if (modes.has('md')) return <TextBlock context={context} box={box} />
  if (modes.has('button')) return <Buttons context={context} box={box} />
  if (modes.has('check')) return (
    options
      ? <Checklist context={context} box={box} />
      : <Checkbox context={context} box={box} />
  )
  if (modes.has('toggle')) return <Toggle context={context} box={box} />
  if (modes.has('color')) return (
    options
      ? <ColorPalette context={context} box={box} />
      : <ColorPicker context={context} box={box} />
  )
  if (modes.has('date')) return <DatePicker context={context} box={box} />
  if (modes.has('day') || modes.has('month') || modes.has('week'))
    return <Calendar context={context} box={box} />
  if (modes.has('file')) return <FileUpload context={context} box={box} />

  if (modes.has('g-label')) return <GraphicLabel context={context} box={box} />
  // TODO simplify:
  if (modes.has('g-rect')) return <Graphic2 context={context} box={box} />
  if (modes.has('g-circle')) return <Graphic2 context={context} box={box} />
  if (modes.has('g')) return <Graphic context={context} box={box} />

  if (modes.has('menu')) return (
    modes.has('editable')
      ? <ComboBox context={context} box={box} />
      : modes.has('multi')
        ? <Droplist context={context} box={box} />
        : <Dropdown context={context} box={box} />
  )
  if (modes.has('number')) return <Spinbox context={context} box={box} />
  if (modes.has('radio')) return <ChoiceGroup context={context} box={box} />
  if (modes.has('range')) return <Slider context={context} box={box} />
  if (modes.has('rating')) return <Rating context={context} box={box} />
  if (modes.has('progress')) return <ProgressBar context={context} box={box} />
  if (modes.has('separator')) return <Separator context={context} box={box} />
  if (modes.has('spinner')) return <Spinner context={context} box={box} />
  if (modes.has('svg')) return <SVGBox context={context} box={box} />
  if (
    modes.has('info')
    || modes.has('success')
    || modes.has('warning')
    || modes.has('critical')
    || modes.has('blocked')
    || modes.has('error')
  ) return <Banner context={context} box={box} />
  if (modes.has('table')) return <Table context={context} box={box} />
  if (modes.has('tag')) return <TagPicker context={context} box={box} />
  if (modes.has('text') || modes.has('password')) return <Textbox context={context} box={box} />
  if (modes.has('time')) return <TimePicker context={context} box={box} />
  if (modes.has('web')) return <WebView context={context} box={box} />


  for (const mode of modes) {
    const i = mode.indexOf(':')
    if (i >= 0) {
      const type = mode.substring(0, i), name = mode.substring(i + 1)
      if (type === 'plugin') return <PluginBox context={context} box={box} name={name} />
    }
  }

  return <Terminal context={context} box={box} />
}

const NonTerminal = ({ context, box, children }: BoxProps & { children: React.ReactNode }) => {
  const
    { name, modes, hotkey } = box,
    background = box.image ? { backgroundImage: `url(${box.image})` } : undefined,
    flex = modes.has('col') ? 'flex flex-col gap-2' : modes.has('row') ? 'flex gap-2' : undefined,
    onClick = createOnClick(context, box),
    unbind = hotkey && onClick ? context.hotkey(hotkey, onClick) : undefined,
    dispose = () => {
      if (unbind) unbind()
    }

  useEffect(() => dispose)

  return (
    <div
      className={css(flex, onClick ? 'cursor-pointer' : undefined, box.style)}
      onClick={onClick}
      style={background}
      data-name={name}
    >{children}</div>
  )
}

const Terminal = ({ context, box }: BoxProps) => {
  const
    { name, hotkey } = box,
    onClick = createOnClick(context, box),
    unbind = hotkey && onClick ? context.hotkey(hotkey, onClick) : undefined,
    dispose = () => {
      if (unbind) unbind()
    }

  useEffect(() => dispose)

  return (
    <div
      className={css(onClick ? 'cursor-pointer' : undefined, box.style)}
      onClick={onClick}
      data-name={name}
    >{box.text ?? ''}</div>
  )
}

const NavSetItem = make(({ visibleB, children }: { visibleB: Signal<B>, children: React.ReactNode }) => {
  const
    render = () => {
      const style: React.CSSProperties = { display: visibleB() ? 'block' : 'none' }
      return <div style={style}>{children}</div>
    }
  return { render, visibleB }
})

const NavSet = make(({ context, box }: BoxProps) => {
  const
    { name, style, items: rawItems, options: rawOptions } = box,
    items = rawItems ?? [],
    options = rawOptions ?? [],
    selectedIndex = items.findIndex(box => box.modes.has('open')),
    selectedIndexB = signal(selectedIndex < 0 ? 0 : selectedIndex),
    selectedKeyB = by(selectedIndexB, i => String(options[i].value)),
    visibleBs = options.map((_, i) => signal(i === selectedIndexB() ? true : false)),
    tabs = zip(items, visibleBs, (box, visibleB) => (
      <NavSetItem key={box.xid} visibleB={visibleB}>
        <XBox context={context} box={box} />
      </NavSetItem>
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
      <div className={css('flex gap-4', style)} data-name={name}>
        <div className={css('border-r')}>
          <Nav groups={groups} onLinkClick={onLinkClick} selectedKey={selectedKeyB()} />
        </div>
        <div className={css('grow')}>{tabs}</div>
      </div>
    )

  on(selectedIndexB, k => visibleBs.forEach((v, i) => v(i === k ? true : false)))

  return { render, selectedKeyB }
})

const TabSet = ({ context, box }: BoxProps) => {
  const
    { name, style, items: rawItems, options: rawOptions } = box,
    items = rawItems ?? [],
    options = rawOptions ?? [],
    tabs = zip(options, items, (opt, box, i) => (
      <PivotItem
        key={box.xid}
        headerText={opt.text ?? `Tab ${i + 1}`}
        itemKey={box.xid} itemIcon={box.icon ?? undefined}
        style={{ padding: '8px 0' }}
      >
        <XBox context={context} box={box} />
      </PivotItem>
    )),
    selectedKey = (items.find(box => box.modes.has('open')) ?? items[0]).xid

  return (
    <div className={css(style)} data-name={name} >
      <Pivot defaultSelectedKey={selectedKey}>{tabs}</Pivot>
    </div>
  )
}

const createOnClick = (context: Context, box: Box) => {
  const { modes, link } = box
  return modes.has('tap')
    ? () => {
      const v = box.value ?? box.name ?? box.text
      if (v) {
        context.record(v as any)
        context.commit()
      }
    }
    : link
      ? (e?: React.MouseEvent<HTMLDivElement>) => {
        jump(link ?? '')
        if (e) e.preventDefault()
      }
      : undefined
}
