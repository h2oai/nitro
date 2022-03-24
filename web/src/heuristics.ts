import { isN, isO, isPair, isS, isV, newIncr, Incr, words, xid } from './core';
import { markdown } from './markdown';
import { Input, InputMode, Option, Widget, WidgetT } from './protocol';

const determineMode = (input: Input): InputMode => {
  // This function contains the heuristics for determining which widget to use.
  const { options, editable, multiple } = input

  if (options.length) {
    if (multiple) {
      if (editable) {
        return 'menu'
      }
      const hasShortLabels = options.some(({ text }) => text && (text.length <= 50))
      if (hasShortLabels && options.length > 7) {
        return 'menu'
      }
      return 'check'
    }

    const hasGroups = options.some(c => c.options?.length ? true : false)
    if (editable || hasGroups) {
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

  const { value, min, max, step, precision } = input

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

const sanitizeInput = (input: Input) => {
  const { mode, options } = input
  input.options = sanitizeOptions(options)
  input.index = 0
  sanitizeRange(input)
  if (!mode) input.mode = determineMode(input)

  if (input.mode === 'md') {
    const [md, hasLinks] = markdown(input.text ?? '')
    input.text = md
    if (!hasLinks) {
      input.index = -1 // don't capture
    }
  }
}

const sanitizeRange = (input: Input) => {
  const { range } = input
  if (Array.isArray(range)) {
    switch (range.length) {
      case 2:
        {
          const [x, y] = range
          if ((isN(x) && isN(y)) || (isS(x) && isS(y))) {
            input.min = x
            input.max = y
          }
        }
        break
      case 3:
        {
          const [x, y, z] = range
          // TODO string x, y?
          if (isN(x) && isN(y) && isN(z)) {
            input.min = x
            input.max = y
            input.step = z
          }
        }
        break
      case 4:
        {
          const [x, y, z, p] = range
          // TODO string x, y?
          if (isN(x) && isN(y) && isN(z) && isN(p)) {
            input.min = x
            input.max = y
            input.step = z
            input.precision = p
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
        c.push({ t: WidgetT.Option, text: String(v), value: v })
      } else if (isPair(v)) { // [value, text]
        const [value, text] = v
        if (isS(text) && isV(value)) {
          c.push({ t: WidgetT.Option, text, value })
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
    return words(x).map((value): Option => ({ t: WidgetT.Option, text: value, value }))
  }
  if (isO(x)) { // { value1: text1, value2: text2, ... }
    const c: Option[] = []
    for (const value in x) {
      const text = x[value]
      c.push({ t: WidgetT.Option, text, value })
    }
    return c
  }
  console.warn('Invalid choice list. Want string or array or dictionary, got ', x)
  return []
}

export const sanitizeWidget = (widget: Widget): Widget => {
  if (isS(widget)) {
    widget = { t: WidgetT.Input, xid: xid(), index: 0, mode: 'md', text: widget, options: [] }
  }
  switch (widget.t) {
    case WidgetT.Stack:
      widget.items = widget.items.map(w => sanitizeWidget(w))
      break
    case WidgetT.Input:
      sanitizeInput(widget)
      break
  }
  return widget
}

export const reIndex = (widgets: Widget[], incr: Incr) => {
  for (const w of widgets) {
    switch (w.t) {
      case WidgetT.Stack:
        reIndex(w.items, incr)
        break
      case WidgetT.Input:
        if (w.index >= 0) {
          w.index = incr()
        }
        break
    }
  }
}
