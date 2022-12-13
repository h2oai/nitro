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

import { anyD, anyN, B, Dict, Incr, isB, isN, isO, isPair, isS, isV, newIncr, S, U, words, xid } from './core';
import { css } from './css';
import { Formatter } from './format';
import { markdown } from './markdown';
import { allBoxModes, Box, BoxMode, BoxT, Header, inputBoxModes, Option } from './protocol';

const isInput = (modes: Set<BoxT>) => {
  for (const m of inputBoxModes) if (modes.has(m)) return true
  return false
}

const determineMode = (box: Box): BoxMode => {
  const { modes, options } = box

  if (options) {
    if (box.headers?.length && options.every(o => o.options?.length ? true : false)) {
      return 'table'
    }
    if (modes.has('editable')) {
      return 'menu'
    }
    if (modes.has('multi')) {
      const hasShortLabels = options.some(({ text }) => text && (text.length <= 50))
      if (hasShortLabels && options.length > 7) {
        return 'menu'
      }
      return 'check'
    }

    const hasGroups = options.some(c => c.options?.length ? true : false)
    if (hasGroups) {
      return 'menu'
    }
    if (options.length <= 3) {
      return 'button'
    }
    if (options.length <= 7) {
      return 'radio'
    }
    return 'menu'
  }

  const { value, min, max, step, precision } = box

  if (isB(value)) return 'check'

  if (isPair(value)) {
    const [a, b] = value
    if (isN(a) && isN(b)) {
      return 'range'
    }
  }

  if (anyN(value, min, max, step, precision)) {
    return 'number'
  }

  const { mask, prefix, suffix, placeholder, error, lines, icon } = box

  if (anyD(value, mask, prefix, suffix, placeholder, error, lines, icon) || modes.has('required')) {
    return 'text'
  }

  if (box.text && !box.link && !box.style) {
    return 'md'
  }

  return 'box'
}

const sanitizeRange = (box: Box) => {
  const { range } = box
  if (Array.isArray(range)) {
    switch (range.length) {
      case 2:
        {
          const [x, y] = range
          if ((isN(x) && isN(y)) || (isS(x) && isS(y))) {
            box.min = x
            box.max = y
          }
        }
        break
      case 3:
        {
          const [x, y, z] = range
          // TODO string x, y?
          if (isN(x) && isN(y) && isN(z)) {
            box.min = x
            box.max = y
            box.step = z
          }
        }
        break
      case 4:
        {
          const [x, y, z, p] = range
          // TODO string x, y?
          if (isN(x) && isN(y) && isN(z) && isN(p)) {
            box.min = x
            box.max = y
            box.step = z
            box.precision = p
          }
        }
        break
    }
  }
}

export const sanitizeOptions = (x: any): Option[] => { // recursive
  if (Array.isArray(x)) {
    const c: Option[] = []
    for (const v of x) {
      if (isV(v)) { // value
        c.push({ text: String(v), value: v })
      } else if (isPair(v)) { // [value, text]
        const [value, text] = v
        if (isS(text) && isV(value)) {
          c.push({ text, value })
        } else {
          console.warn('Invalid choice pair. Want [string, value], got ', v)
        }
      } else if (isO(v) && isV(v.value)) { // { value: v }
        if (!v.text) v.text = String(v.value)
        if (v.options) v.options = sanitizeOptions(v.options)
        c.push(v)
      }
    }
    return c
  }
  if (isS(x)) { // 'value1 value2 value3...'
    return words(x).map((value): Option => ({ text: value, value }))
  }
  if (isO(x)) { // { value1: text1, value2: text2, ... }
    const c: Option[] = []
    for (const value in x) {
      const text = x[value]
      c.push({ text, value })
    }
    return c
  }
  console.warn('Invalid choice list. Want string or array or dictionary, got ', x)
  return []
}

const localizeBox = (fmt: Formatter, box: Box) => {
  const { text, title, caption, placeholder, prefix, suffix, hint, help, options, headers, data } = box
  if (text) box.text = fmt.translate(text, data)
  if (title) box.title = fmt.translate(title, data)
  if (caption) box.caption = fmt.translate(caption, data)
  if (placeholder) box.placeholder = fmt.translate(placeholder, data)
  if (prefix) box.prefix = fmt.translate(prefix, data)
  if (suffix) box.suffix = fmt.translate(suffix, data)
  if (hint) box.hint = fmt.translate(hint, data)
  if (help) box.help = fmt.translate(help, data)
  if (options) for (const option of options) localizeOption(fmt, option)
  if (headers) for (const header of headers) localizeHeader(fmt, header)
}

const localizeOption = (fmt: Formatter, option: Option) => {
  const { text, caption, options, data } = option
  if (text) option.text = fmt.translate(text, data)
  if (caption) option.caption = fmt.translate(caption, data)
  if (options) for (const option of options) localizeOption(fmt, option)
}

const localizeHeader = (fmt: Formatter, header: Header) => {
  const { text } = header
  if (text) header.text = fmt.translate(text) ?? '' // TODO data?
}

const hasNoMode = (modes: Set<S>): B => { // TODO PERF speed up
  if (modes.size === 0) return true
  for (const m of allBoxModes) if (modes.has(m)) return false
  for (const m of modes.values()) if (m.startsWith('plugin:')) return false
  return true
}

export const sanitizeHelp = (formatter: Formatter, help: Dict<S>): Dict<S> => {
  for (const k in help) {
    const
      s = help[k],
      md = formatter.translate(s),
      [html] = markdown(md ?? '')
    help[k] = html
  }
  return help
}

const mergeBoxes_ = (layout: Box, body: Box) => {
  const { items } = layout
  if (Array.isArray(items)) {
    for (let i = 0, n = items.length; i < n; i++) {
      const item = items[i]
      if (item && !isS(item) && !Array.isArray(item)) {
        const b = item as any
        if (b.mode === 'body') {
          items[i] = body
          return true
        }
        if (mergeBoxes_(item, body)) return true
      }
    }
  }
  return false
}

export const mergeBoxes = (layout: Box, body: Box) => {
  // This function is called pre-santization.
  // Find and replace the first occurance of a 'body' box with the actual body.
  mergeBoxes_(layout, body)
  return layout
}

export const sanitizeBox = (formatter: Formatter, box: Box): Box => {
  if (isN(box)) box = String(box) as any // number -> string, if a number was passed in

  if (isS(box)) {
    box = { xid: xid(), index: 0, modes: new Set(['md']), text: box, options: [] }
  } else if (Array.isArray(box)) {
    box = { xid: xid(), index: 0, modes: new Set(), options: box }
  } else {
    const mode: any = (box as any).mode
    box.modes = isS(mode) ? new Set(words(mode) as BoxT[]) : new Set()
  }

  const { modes } = box

  if (modes.has('column' as BoxMode)) modes.add('col') // QOL
  if (box.title) modes.add('group')

  const isRowOrCol = modes.has('row') || modes.has('col')
  const isContainer = isRowOrCol || modes.has('group')

  if (box.items && !isContainer) {
    const
      { items } = box,
      k = items.length
    switch (k) {
      case 0: // box()
        box.items = undefined
        break
      case 1:
        const [x] = items
        if (isS(x)) { // box('foo')
          box.text = x
          box.items = undefined
        } else if (Array.isArray(x)) { // box([a, b, c])
          box.options = x
          box.items = undefined
        }
        break
    }
  }

  const fmt = box.locale ? formatter.load(box.locale) : formatter

  let mdHasLinks = false
  if (box.items) {
    box.items = box.items.map(b => sanitizeBox(fmt, b))
  } else {
    const { value, options } = box

    if (options) box.options = sanitizeOptions(options)

    sanitizeRange(box)

    if (hasNoMode(modes)) modes.add(determineMode(box))

    if (isB(value)) box.value = value ? 1 : 0 // TODO ugly: protocol should accept boolean

    localizeBox(fmt, box)

    if (modes.has('md')) {
      const [md, hasLinks] = markdown(box.text ?? '')
      box.text = md
      if (hasLinks) mdHasLinks = true
    }

    if (modes.has('table') && box.headers) {
      for (const h of box.headers) {
        const mode: any = (h as any).mode
        h.modes = isS(mode) ? new Set(words(mode)) : new Set()
      }
    }
  }

  // if 0, box.index is set to a 1-up index later during re-indexing.
  box.index = !box.ignore && (mdHasLinks || isInput(modes)) ? 0 : -1

  // special-casing for row/col modes:
  if (isRowOrCol && box.items && !box.options && box.items.every(b => b.modes.has('group'))) {
    // make tabs if all children are groups
    box.items.forEach(b => b.modes.delete('group'))
    box.options = box.items.map(b => ({ value: b.xid, text: b.title }))
  }

  if (box.style) box.style = css(box.style)

  return box
}

export const freeze = (boxes: Box[]) => {
  reindex(boxes, newIncr())
  assignParents(boxes)
}

const reindex = (boxes: Box[], incr: Incr) => {
  for (const box of boxes) {
    if (box.items) reindex(box.items, incr)
    if (box.index >= 0) box.index = incr()
  }
}

const assignParents = (boxes: Box[]) => {
  for (const box of boxes) {
    if (box.items) {
      if (box.modes.has('input')) assignParent(box.index, box.xid, box.items)
      assignParents(box.items)
    }
  }
}

const assignParent = (index: U, pid: S, boxes: Box[]) => {
  for (const box of boxes) {
    if (box.modes.has('tap')) {
      box.index = index
      box.pid = pid
      // Don't recurse: ignore nested interactive areas.
    } else if (box.items) {
      assignParent(index, pid, box.items)
    }
  }
}

export const hasActions = (boxes: Box[]): B => { // recursive
  for (const box of boxes) {
    const { modes } = box
    if (box.halt || modes.has('live') || modes.has('input')) return true
    if (box.items && hasActions(box.items)) return true
    if (modes.has('button')) {
      if (box.options) return true
    } else if (modes.has('md')) {
      if (box.index >= 0) return true
    } else if (modes.has('toggle') || modes.has('progress') || modes.has('spinner')) {
      return true
    } else if (modes.has('table')) {
      if (modes.has('selectable') || modes.has('multi')) return false
      if (box.headers) for (const header of box.headers) if (header.modes.has('link')) return true
    }
  }
  return false
}
