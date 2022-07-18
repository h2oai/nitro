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
import { Dict, S, U } from './core';

type CSS = React.CSSProperties

export const sizeScale: Dict<U> = {
  '0': 0,
  'px': 1,
  '0.5': 2,
  '1': 4,
  '1.5': 6,
  '2': 8,
  '2.5': 10,
  '3': 12,
  '3.5': 14,
  '4': 16,
  '5': 20,
  '6': 24,
  '7': 28,
  '8': 32,
  '9': 36,
  '10': 40,
  '11': 44,
  '12': 48,
  '14': 56,
  '16': 64,
  '20': 80,
  '24': 96,
  '28': 112,
  '32': 128,
  '36': 144,
  '40': 160,
  '44': 176,
  '48': 192,
  '52': 208,
  '56': 224,
  '60': 240,
  '64': 256,
  '72': 288,
  '80': 320,
  '96': 384,
}

const miscSizings: Dict<S> = {
  auto: 'auto',
  full: '100%',
  screen: '100vw',
  min: 'min-content',
  max: 'max-content',
  fit: 'fit-content',
}

const textAlignments = new Set(['left', 'center', 'right', 'justify', 'start', 'end'])

type V = string | number

type Matcher = (v: S) => V | undefined

const
  matchValue = (k: S) => (v: S) => { if (k === v) return v },
  matchSet = (set: Set<S>) => (v: S) => { if (set.has(v)) return v },
  matchDict = (dict: Dict<V>) => (k: S) => { if (k in dict) return dict[k] },
  matchPercent = (s: S) => {
    if (/^\d+\/\d+$/.test(s)) {
      const
        [x, y] = s.split('/'),
        p = 100 * parseInt(x) / parseInt(y)
      return (Number.isInteger(p) ? p : p.toFixed(6)) + '%'
    }
  },
  matchOne = (...matchers: Matcher[]) => (s: S) => {
    for (const m of matchers) {
      const v = m(s)
      if (v !== undefined) return v
    }
  },
  matchSizeScale = matchDict(sizeScale),
  matchAuto = matchValue('auto'),
  matchSizeOrAuto = matchOne(matchAuto, matchSizeScale),
  matchSize = matchOne(matchSizeScale, matchDict(miscSizings), matchPercent)

type Handler = (css: CSS, tokens: S[]) => void

const handlers: Dict<Handler> = {
  p: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) css.padding = p
  },
  px: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) {
      css.paddingLeft = p
      css.paddingRight = p
    }
  },
  py: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) {
      css.paddingTop = p
      css.paddingBottom = p
    }
  },
  pt: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) css.paddingTop = p
  },
  pr: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) css.paddingRight = p
  },
  pb: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) css.paddingBottom = p
  },
  pl: (css: CSS, [s]: S[]) => {
    const p = matchSizeScale(s)
    if (p !== undefined) css.paddingLeft = p
  },
  m: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) css.margin = p
  },
  mx: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) {
      css.marginLeft = p
      css.marginRight = p
    }
  },
  my: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) {
      css.marginTop = p
      css.marginBottom = p
    }
  },
  mt: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) css.marginTop = p
  },
  mr: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) css.marginRight = p
  },
  mb: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) css.marginBottom = p
  },
  ml: (css: CSS, [s]: S[]) => {
    const p = matchSizeOrAuto(s)
    if (p !== undefined) css.marginLeft = p
  },
  w: (css: CSS, [s]: S[]) => {
    const w = matchSize(s)
    if (w !== undefined) css.width = w
  },
  h: (css: CSS, [s]: S[]) => {
    const h = matchSize(s)
    if (h !== undefined) css.height = h
  },
  text: (css: CSS, [s]: S[]) => {
    const textAlign = matchSet(textAlignments)(s)
    if (textAlign !== undefined) {
      css.textAlign = textAlign as any
      return
    }
  },
}

export const stylize = (css: CSS, spec: S) => {
  const styles = spec.split(/\s+/g)
  for (const style of styles) {
    const
      tokens = style.split('-'),
      handle = handlers[tokens[0]]
    if (handle) handle(css, tokens.slice(1))
  }
}