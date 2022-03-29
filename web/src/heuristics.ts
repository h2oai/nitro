import { Incr, isN, isO, isPair, isS, isV, words, xid } from './core';
import { markdown } from './markdown';
import { Box, BoxMode, BoxT, Option } from './protocol';

const determineMode = (box: Box): BoxMode => {
  const { options, editable, multiple } = box

  if (options.length) {
    if (editable) {
      return 'menu'
    }
    if (multiple) {
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

  if (isPair(value)) {
    const [a, b] = value
    if (isN(a) && isN(b)) {
      return 'range'
    }
  }

  if (isN(value) || isN(min) || isN(max) || isN(step) || isN(precision)) {
    return 'number'
  }
  return 'text'
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

const sanitizeOptions = (x: any): Option[] => { // recursive
  if (!x) return []
  if (Array.isArray(x)) {
    const c: Option[] = []
    for (const v of x) {
      if (isV(v)) { // value
        c.push({ t: BoxT.Option, text: String(v), value: v })
      } else if (isPair(v)) { // [value, text]
        const [value, text] = v
        if (isS(text) && isV(value)) {
          c.push({ t: BoxT.Option, text, value })
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
    return words(x).map((value): Option => ({ t: BoxT.Option, text: value, value }))
  }
  if (isO(x)) { // { value1: text1, value2: text2, ... }
    const c: Option[] = []
    for (const value in x) {
      const text = x[value]
      c.push({ t: BoxT.Option, text, value })
    }
    return c
  }
  console.warn('Invalid choice list. Want string or array or dictionary, got ', x)
  return []
}

export const sanitizeBox = (box: Box): Box => {
  if (isS(box)) {
    box = { t: BoxT.Box, xid: xid(), index: 0, mode: 'md', text: box, options: [] }
  }
  if (box.items) {
    box.items = box.items.map(w => sanitizeBox(w))
  } else {
    const { mode, options } = box
    box.options = sanitizeOptions(options)
    box.index = 0
    sanitizeRange(box)
    if (!mode) box.mode = determineMode(box)

    if (box.mode === 'md') {
      const [md, hasLinks] = markdown(box.text ?? '')
      box.text = md
      if (!hasLinks) {
        box.index = -1 // don't capture
      }
    }
  }
  return box
}

export const reIndex = (boxes: Box[], incr: Incr) => {
  for (const box of boxes) {
    if (box.items) {
      reIndex(box.items, incr)
    } else {
      if (box.index >= 0) {
        box.index = incr()
      }
    }
  }
}
