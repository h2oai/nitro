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
import { B, Dict, S, U } from './core';

type CSS = React.CSSProperties
type Match = (s: S) => any
type Apply = (css: CSS, value: any) => void
type Handler = [Match, Apply]

const
  mapS = (xs: U[]) => xs.map(x => '' + x),
  isEq = (k: S) => (x: S) => { if (x === k) return x },
  empty = isEq(''),
  isNone = isEq('none'),
  isAuto = isEq('auto'),
  isAs = (find: S, replace: any) => (x: S) => { if (x === find) return replace },
  isOf = (dict: Dict<S | U>) => (x: S) => { if (x in dict) return dict[x] },
  isIn = (...xs: S[]) => {
    const set = new Set(xs)
    return (x: S) => { if (set.has(x)) return x }
  },
  either = (...matchers: Match[]) => (x: S) => {
    for (const m of matchers) {
      const v = m(x)
      if (v !== undefined) return v
    }
  },
  isInOf = (xs: S[], f: (x: S) => S) => {
    const d: Dict<S> = {}
    for (const x of xs) d[x] = f(x)
    return isOf(d)
  },
  _seq = (m: U, n: U) => {
    const
      k = n - m + 1,
      ns = new Array<U>(k)
    for (let i = 0; i < k; i++, m++) ns[i] = m
    return ns
  },
  isN = (...xs: U[]) => {
    const d: Dict<U> = {}
    for (const x of xs) d['' + x] = x
    return isOf(d)
  },
  isBetween = (m: U, n: U) => isN(..._seq(m, n)),
  isNOf = (ns: U[], f: (x: S) => S) => isInOf(mapS(ns), f),
  isBetweenOf = (m: U, n: U, f: (k: S) => S) => isNOf(_seq(m, n), f)

// Tailwind palette
// https://tailwindcss.com/docs/customizing-colors
const shades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900']
const spectrum: Dict<S[]> = {
  slate: ['#f8fafc', '#f1f5f9', '#e2e8f0', '#cbd5e1', '#94a3b8', '#64748b', '#475569', '#334155', '#1e293b', '#0f172a'],
  gray: ['#f9fafb', '#f3f4f6', '#e5e7eb', '#d1d5db', '#9ca3af', '#6b7280', '#4b5563', '#374151', '#1f2937', '#111827'],
  zinc: ['#fafafa', '#f4f4f5', '#e4e4e7', '#d4d4d8', '#a1a1aa', '#71717a', '#52525b', '#3f3f46', '#27272a', '#18181b'],
  neutral: ['#fafafa', '#f5f5f5', '#e5e5e5', '#d4d4d4', '#a3a3a3', '#737373', '#525252', '#404040', '#262626', '#171717'],
  stone: ['#fafaf9', '#f5f5f4', '#e7e5e4', '#d6d3d1', '#a8a29e', '#78716c', '#57534e', '#44403c', '#292524', '#1c1917'],
  red: ['#fef2f2', '#fee2e2', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d'],
  orange: ['#fff7ed', '#ffedd5', '#fed7aa', '#fdba74', '#fb923c', '#f97316', '#ea580c', '#c2410c', '#9a3412', '#7c2d12'],
  amber: ['#fffbeb', '#fef3c7', '#fde68a', '#fcd34d', '#fbbf24', '#f59e0b', '#d97706', '#b45309', '#92400e', '#78350f'],
  yellow: ['#fefce8', '#fef9c3', '#fef08a', '#fde047', '#facc15', '#eab308', '#ca8a04', '#a16207', '#854d0e', '#713f12'],
  lime: ['#f7fee7', '#ecfccb', '#d9f99d', '#bef264', '#a3e635', '#84cc16', '#65a30d', '#4d7c0f', '#3f6212', '#365314'],
  green: ['#f0fdf4', '#dcfce7', '#bbf7d0', '#86efac', '#4ade80', '#22c55e', '#16a34a', '#15803d', '#166534', '#14532d'],
  emerald: ['#ecfdf5', '#d1fae5', '#a7f3d0', '#6ee7b7', '#34d399', '#10b981', '#059669', '#047857', '#065f46', '#064e3b'],
  teal: ['#f0fdfa', '#ccfbf1', '#99f6e4', '#5eead4', '#2dd4bf', '#14b8a6', '#0d9488', '#0f766e', '#115e59', '#134e4a'],
  cyan: ['#ecfeff', '#cffafe', '#a5f3fc', '#67e8f9', '#22d3ee', '#06b6d4', '#0891b2', '#0e7490', '#155e75', '#164e63'],
  sky: ['#f0f9ff', '#e0f2fe', '#bae6fd', '#7dd3fc', '#38bdf8', '#0ea5e9', '#0284c7', '#0369a1', '#075985', '#0c4a6e'],
  blue: ['#eff6ff', '#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8', '#1e40af', '#1e3a8a'],
  indigo: ['#eef2ff', '#e0e7ff', '#c7d2fe', '#a5b4fc', '#818cf8', '#6366f1', '#4f46e5', '#4338ca', '#3730a3', '#312e81'],
  violet: ['#f5f3ff', '#ede9fe', '#ddd6fe', '#c4b5fd', '#a78bfa', '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', '#4c1d95'],
  purple: ['#faf5ff', '#f3e8ff', '#e9d5ff', '#d8b4fe', '#c084fc', '#a855f7', '#9333ea', '#7e22ce', '#6b21a8', '#581c87'],
  fuchsia: ['#fdf4ff', '#fae8ff', '#f5d0fe', '#f0abfc', '#e879f9', '#d946ef', '#c026d3', '#a21caf', '#86198f', '#701a75'],
  pink: ['#fdf2f8', '#fce7f3', '#fbcfe8', '#f9a8d4', '#f472b6', '#ec4899', '#db2777', '#be185d', '#9d174d', '#831843'],
  rose: ['#fff1f2', '#ffe4e6', '#fecdd3', '#fda4af', '#fb7185', '#f43f5e', '#e11d48', '#be123c', '#9f1239', '#881337'],
}

const mergeSpectrum = (palette: Dict<S>) => {
  for (const name in spectrum) {
    const colors = spectrum[name]
    for (let i = 0; i < shades.length; i++) {
      palette[`${name}-${shades[i]}`] = colors[i]
    }
  }
  return palette
}

const palette = mergeSpectrum({
  inherit: 'inherit',
  current: 'currentColor',
  transparent: 'transparent',
  white: '#fff',
  black: '#000',
})

// Tailwind size scale
const isSize = isOf({
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
})

const isRatio = isOf({
  full: '100%',
  '1/2': '50%',
  '1/3': '33.333333%',
  '2/3': '66.666667%',
  '1/4': '25%',
  '2/4': '50%',
  '3/4': '75%',
  '1/5': '20%',
  '2/5': '40%',
  '3/5': '60%',
  '4/5': '80%',
  '1/6': '16.666667%',
  '2/6': '33.333333%',
  '3/6': '50%',
  '4/6': '66.666667%',
  '5/6': '83.333333%',
  '1/12': '8.333333%',
  '2/12': '16.666667%',
  '3/12': '25%',
  '4/12': '33.333333%',
  '5/12': '41.666667%',
  '6/12': '50%',
  '7/12': '58.333333%',
  '8/12': '66.666667%',
  '9/12': '75%',
  '10/12': '83.333333%',
  '11/12': '91.666667%',
})

const isRatioSubset = isOf({
  full: '100%',
  '1/2': '50%',
  '1/3': '33.333333%',
  '2/3': '66.666667%',
  '1/4': '25%',
  '2/4': '50%',
  '3/4': '75%',
})

const isContentSize = isOf({
  min: 'min-content',
  max: 'max-content',
  fit: 'fit-content',
})

const rules: Dict<Handler[]> = {}
const rule = (name: S, ...handlers: Handler[]) => rules[name] = handlers
const rule0 = (name: S, apply: Apply) => rule(name, [empty, apply])

rule('aspect', [isOf({ 'auto': 'auto', 'square': '1 / 1', 'video': '16 / 9' }), (css, v) => css.aspectRatio = v])
const isColumnSize = isOf({
  '3xs': 256,
  '2xs': 288,
  'xs': 320,
  'sm': 384,
  'md': 448,
  'lg': 512,
  'xl': 576,
  '2xl': 672,
  '3xl': 768,
  '4xl': 896,
  '5xl': 1024,
  '6xl': 1152,
  '7xl': 1280,
})
rule('columns', [either(isBetween(1, 12), isAuto, isColumnSize), (css, v) => css.columns = v])
const isBreakAfter = isIn('auto', 'avoid', 'all', 'avoid-page', 'page', 'left', 'right', 'column')
rule('break-after', [isBreakAfter, (css, v) => css.breakAfter = v])
rule('break-before', [isBreakAfter, (css, v) => css.breakBefore = v])
rule('break-inside', [isIn('auto', 'avoid', 'avoid-page', 'avoid-column'), (css, v) => css.breakInside = v])
rule('box-decoration', [isIn('clone', 'slice'), (css, v) => css.boxDecorationBreak = v])
rule('box', [isOf({ 'border': 'border-box', 'content': 'content-box' }), (css, v) => css.boxSizing = v])
rule0('block', css => css.display = 'block')
rule0('inline-block', css => css.display = 'inline-block')
rule0('inline', css => css.display = 'inline')
rule('flex',
  [empty, (css) => css.display = 'flex'],
  [either(isIn('row', 'row-reverse'), isOf({ 'col': 'column', 'col-reverse': 'column-reverse' })), (css, v) => css.flexDirection = v],
  [isIn('wrap', 'wrap-reverse', 'nowrap', ''), (css, v) => css.flexWrap = v],
  [isOf({ '1': '1 1 0%', 'auto': '1 1 auto', 'initial': '0 1 auto', 'none': 'none' }), (css, v) => css.flex = v]
)
rule0('inline-flex', css => css.display = 'inline-flex')
rule('table', [isOf({
  '': 'table',
  caption: 'table-caption',
  cell: 'table-cell',
  column: 'table-column',
  'column-group': 'table-column-group',
  'footer-group': 'table-footer-group',
  'header-group': 'table-header-group',
  'row-group': 'table-row-group',
  row: 'table-row',
}), (css, v) => css.display = v])
rule0('inline-table', css => css.display = 'inline-table')
rule0('flow-root', css => css.display = 'flow-root')
rule0('grid', css => css.display = 'grid')
rule0('inline-grid', css => css.display = 'inline-grid')
rule0('contents', css => css.display = 'contents')
rule0('list-item', css => css.display = 'list-item')
rule0('hidden', css => css.display = 'none')
rule('float', [isIn('right', 'left', 'none'), (css, v) => css.float = v])
rule('clear', [isIn('left', 'right', 'both', 'none'), (css, v) => css.clear = v])
rule0('isolate', css => css.isolation = 'isolate')
rule0('isolation-auto', css => css.isolation = 'auto')
const isObjectPosition = isOf({
  'bottom': 'bottom',
  'center': 'center',
  'left': 'left',
  'left-bottom': 'left bottom',
  'left-top': 'left top',
  'right': 'right',
  'right-bottom': 'right bottom',
  'right-top': 'right top',
  'top': 'top',
})
rule('object',
  [isIn('contain', 'cover', 'fill', 'none', 'scale-down'), (css, v) => css.objectFit = v],
  [isObjectPosition, (css, v) => css.objectPosition = v],
)
const isOverflow = isIn('auto', 'hidden', 'clip', 'visible', 'scroll')
rule('overflow', [isOverflow, (css, v) => css.overflow = v])
rule('overflow-x', [isOverflow, (css, v) => css.overflowX = v])
rule('overflow-y', [isOverflow, (css, v) => css.overflowY = v])
const isOverscroll = isIn('auto', 'contain', 'none')
rule('overscroll', [isOverscroll, (css, v) => css.overscrollBehavior = v])
rule('overscroll-x', [isOverscroll, (css, v) => css.overscrollBehaviorX = v])
rule('overscroll-y', [isOverscroll, (css, v) => css.overscrollBehaviorY = v])
rule0('static', css => css.position = 'static')
rule0('fixed', css => css.position = 'fixed')
rule0('absolute', css => css.position = 'absolute')
rule0('relative', css => css.position = 'relative')
rule0('sticky', css => css.position = 'sticky')
const isInset = either(isAuto, isSize, isRatioSubset)
rule('inset', [isInset, (css, v) => { css.top = v; css.right = v; css.bottom = v; css.left = v }])
rule('inset-x', [isInset, (css, v) => { css.left = v; css.right = v }])
rule('inset-y', [isInset, (css, v) => { css.top = v; css.bottom = v }])
rule('top', [isInset, (css, v) => css.top = v])
rule('right', [isInset, (css, v) => css.right = v])
rule('bottom', [isInset, (css, v) => css.bottom = v])
rule('left', [isInset, (css, v) => css.left = v])
rule0('visible', (css) => css.visibility = 'visible')
rule0('invisible', (css) => css.visibility = 'hidden')
rule('z', [either(isAuto, isN(0, 10, 20, 30, 40, 50)), (css, v) => css.zIndex = v])
rule('basis', [either(isAuto, isSize, isRatio), (css, v) => css.flexBasis = v])
rule('grow', [isOf({ '': 1, '0': 0 }), (css, v) => css.flexGrow = v])
rule('shrink', [isOf({ '': 1, '0': 0 }), (css, v) => css.flexShrink = v])
rule('order', [either(isBetween(1, 12), isOf({ first: -9999, last: 9999, none: 0 })), (css, v) => css.order = v])
rule('grid-cols', [either(isNone, isBetweenOf(1, 12, n => `repeat(${n}, minmax(0, 1fr))`)), (css, v) => css.gridTemplateColumns = v])
rule0('col-auto', (css) => css.gridColumn = 'auto')
rule('col-span', [either(isBetweenOf(1, 12, n => `span ${n} / span ${n}`), isOf({ full: '1 / -1' })), (css, v) => css.gridColumn = v])
const isGridColStart = either(isAuto, isBetween(1, 13))
rule('col-start', [isGridColStart, (css, v) => css.gridColumnStart = v])
rule('col-end', [isGridColStart, (css, v) => css.gridColumnEnd = v])
rule('grid-rows', [either(isBetweenOf(1, 6, n => `repeat(${n}, minmax(0, 1fr))`), isNone), (css, v) => css.gridTemplateRows = v])
rule0('row-auto', (css) => css.gridRow = 'auto')
rule('row-span', [either(isBetweenOf(1, 6, n => `span ${n} / span ${n}`), isOf({ full: '1 / -1' })), (css, v) => css.gridRow = v])
const isGridRowStart = either(isAuto, isBetween(1, 7))
rule('row-start', [isGridRowStart, (css, v) => css.gridRowStart = v])
rule('row-end', [isGridColStart, (css, v) => css.gridRowEnd = v])
rule('grid-flow', [isOf({
  row: 'row',
  col: 'column',
  dense: 'dense',
  'row-dense': 'row dense',
  'col-dense': 'column dense',
}), (css, v) => css.gridAutoFlow = v])
const isGridAuto = isOf({ min: 'min-content', max: 'max-content', fr: 'minmax(0, 1fr)' })
rule('auto-cols', [either(isAuto, isGridAuto), (css, v) => css.gridAutoColumns = v])
rule('auto-rows', [either(isAuto, isGridAuto), (css, v) => css.gridAutoRows = v])
rule('gap', [isSize, (css, v) => css.gap = v])
rule('gap-x', [isSize, (css, v) => css.columnGap = v])
rule('gap-y', [isSize, (css, v) => css.rowGap = v])
const isFlexAlign = isOf({
  start: 'flex-start',
  end: 'flex-end',
  center: 'center',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
})
rule('justify', [isFlexAlign, (css, v) => css.justifyContent = v])
const isFlexJustify = isIn('start', 'end', 'center', 'stretch')
rule('justify-items', [isFlexJustify, (css, v) => css.justifyItems = v])
rule('justify-self', [either(isAuto, isFlexJustify), (css, v) => css.justifySelf = v])
rule('content',
  [isFlexAlign, (css, v) => css.alignContent = v],
  [isNone, css => css.content = 'none'],
)
const isAlignItems = isOf({
  start: 'flex-start',
  end: 'flex-end',
  center: 'center',
  baseline: 'baseline',
  stretch: 'stretch',
})
rule('items', [isAlignItems, (css, v) => css.alignItems = v])
rule('place-content', [isOf({
  center: 'center',
  start: 'start',
  end: 'end',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
  stretch: 'stretch',
}), (css, v) => css.placeContent = v])
rule('self', [either(isAuto, isAlignItems), (css, v) => css.alignSelf = v])
rule('place-items', [isFlexJustify, (css, v) => css.placeItems = v])
rule('place-self', [either(isAuto, isFlexJustify), (css, v) => css.placeSelf = v])

rule('font',
  [isOf({
    sans: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
    serif: 'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
    mono: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
  }), (css, v) => css.fontFamily = v],
  [isOf({
    'thin': 100,
    'extralight': 200,
    'light': 300,
    'normal': 400,
    'medium': 500,
    'semibold': 600,
    'bold': 700,
    'extrabold': 800,
    'black': 900,
  }), (css, v) => css.fontWeight = v],
)

const textSizes: [S, U, S | U][] = [
  ['xs', 12, '16px'],
  ['sm', 14, '20px'],
  ['base', 16, '24px'],
  ['lg', 18, '28px'],
  ['xl', 20, '28px'],
  ['2xl', 24, '32px'],
  ['3xl', 30, '36px'],
  ['4xl', 36, '40px'],
  ['5xl', 48, 1],
  ['6xl', 60, 1],
  ['7xl', 72, 1],
  ['8xl', 96, 1],
  ['9xl', 128, 1],
]

textSizes.forEach(([n, fs, lh]) => rule0('text-' + n, (css) => { css.fontSize = fs; css.lineHeight = lh }))

rule0('italic', (css) => css.fontStyle = 'italic')
rule0('not-italic', (css) => css.fontStyle = 'normal')

rule0('normal-nums', css => css.fontVariantNumeric = 'normal')
rule0('ordinal', css => css.fontVariantNumeric = 'ordinal')
rule0('slashed-zero', css => css.fontVariantNumeric = 'slashed-zero')
rule0('lining-nums', css => css.fontVariantNumeric = 'lining-nums')
rule0('oldstyle-nums', css => css.fontVariantNumeric = 'oldstyle-nums')
rule0('proportional-nums', css => css.fontVariantNumeric = 'proportional-nums')
rule0('tabular-nums', css => css.fontVariantNumeric = 'tabular-nums')
rule0('diagonal-fractions', css => css.fontVariantNumeric = 'diagonal-fractions')
rule0('stacked-fractions', css => css.fontVariantNumeric = 'stacked-fractions')

rule('tracking', [isOf({
  tighter: '-0.05em',
  tight: '-0.025em',
  normal: '0em',
  wide: '0.025em',
  wider: '0.05em',
  widest: '0.1em',
}), (css, v) => css.letterSpacing = v])

rule('leading', [isOf({
  '3': '12px',
  '4': '16px',
  '5': '20px',
  '6': '24px',
  '7': '28px',
  '8': '32px',
  '9': '36px',
  '10': '40px',
  'none': 1,
  'tight': 1.25,
  'snug': 1.375,
  'normal': 1.5,
  'relaxed': 1.625,
  'loose': 2,
}), (css, v) => css.lineHeight = v])

rule('list',
  [isIn('none', 'disc', 'decimal'), (css, v) => css.listStyleType = v],
  [isIn('inside', 'outside'), (css, v) => css.listStylePosition = v],
)

rule('p', [isSize, (css, v) => css.padding = v])
rule('px', [isSize, (css, v) => { css.paddingLeft = v; css.paddingRight = v }])
rule('py', [isSize, (css, v) => { css.paddingTop = v; css.paddingBottom = v }])
rule('pt', [isSize, (css, v) => css.paddingTop = v])
rule('pr', [isSize, (css, v) => css.paddingRight = v])
rule('pb', [isSize, (css, v) => css.paddingBottom = v])
rule('pl', [isSize, (css, v) => css.paddingLeft = v])

const isAutoOrSize = either(isAuto, isSize)
rule('m', [isAutoOrSize, (css, v) => css.margin = v])
rule('mx', [isAutoOrSize, (css, v) => { css.marginLeft = v; css.marginRight = v }])
rule('my', [isAutoOrSize, (css, v) => { css.marginTop = v; css.marginBottom = v }])
rule('mt', [isAutoOrSize, (css, v) => css.marginTop = v])
rule('mr', [isAutoOrSize, (css, v) => css.marginRight = v])
rule('mb', [isAutoOrSize, (css, v) => css.marginBottom = v])
rule('ml', [isAutoOrSize, (css, v) => css.marginLeft = v])

const isWidthOrHeight = either(isSize, isAuto, isContentSize, isRatio)
rule('w', [either(isWidthOrHeight, isAs('screen', '100vw')), (css, v) => css.width = v])
rule('min-w', [either(isAs('0', 0), isAs('full', '100%'), isContentSize), (css, v) => css.minWidth = v])

const isMaxWidth = isOf({
  '0': 0,
  'none': 'none',
  'xs': 320,
  'sm': 384,
  'md': 448,
  'lg': 512,
  'xl': 576,
  '2xl': 672,
  '3xl': 768,
  '4xl': 896,
  '5xl': 1024,
  '6xl': 1152,
  '7xl': 1280,
  'full': '100%',
  'min': 'min-content',
  'max': 'max-content',
  'fit': 'fit-content',
  'prose': '65ch',
  'screen-sm': 640,
  'screen-md': 768,
  'screen-lg': 1024,
  'screen-xl': 1280,
  'screen-2xl': 1536,
})
rule('max-w', [either(isMaxWidth, isContentSize), (css, v) => css.maxWidth = v])
rule('h', [either(isWidthOrHeight, isAs('screen', '100vh')), (css, v) => css.height = v])
rule('min-h', [either(isAs('0', 0), isAs('full', '100%'), isContentSize, isAs('screen', '100vh')), (css, v) => css.minHeight = v])
rule('max-h', [either(isWidthOrHeight, isContentSize, isAs('screen', '100vh')), (css, v) => css.maxHeight = v])

const isColor = isOf(palette)
rule('text',
  [isIn('left', 'center', 'right', 'justify', 'start', 'end'), (css, v) => css.textAlign = v],
  [isColor, (css, v) => css.color = v],
  [isIn('ellipsis', 'clip'), (css, v) => css.textOverflow = v],
)
rule0('underline', (css) => css.textDecorationLine = 'underline')
rule0('overline', (css) => css.textDecorationLine = 'overline')
rule0('line-through', (css) => css.textDecorationLine = 'line-through')
rule0('no-underline', (css) => css.textDecorationLine = 'none')

const is01248 = isN(0, 1, 2, 4, 8)
rule('decoration',
  [isColor, (css, v) => css.textDecorationColor = v],
  [isIn('solid', 'double', 'dotted', 'dashed', 'wavy'), (css, v) => css.textDecorationStyle = v],
  [either(isAuto, isEq('from-font'), is01248), (css, v) => css.textDecorationThickness = v]
)
rule('underline-offset', [either(isAuto, is01248), (css, v) => css.textUnderlineOffset = v])
rule0('uppercase', (css) => css.textTransform = 'uppercase')
rule0('lowercase', (css) => css.textTransform = 'lowercase')
rule0('capitalize', (css) => css.textTransform = 'capitalize')
rule0('normal-case', (css) => css.textTransform = 'none')
rule0('truncate', (css) => { css.overflow = 'hidden'; css.textOverflow = 'ellipsis'; css.whiteSpace = 'nowrap' })
rule('indent', [isSize, (css, v) => css.textIndent = v])
rule('align', [isIn('baseline', 'top', 'middle', 'bottom', 'text-top', 'text-bottom', 'sub', 'super'), (css, v) => css.verticalAlign = v])
rule('whitespace', [isIn('normal', 'nowrap', 'pre', 'pre-line', 'pre-wrap'), (css, v) => css.whiteSpace = v])
rule0('break-normal', css => { css.overflowWrap = 'normal'; css.wordBreak = 'normal' })
rule0('break-words', css => css.overflowWrap = 'break-word')
rule0('break-all', css => css.wordBreak = 'break-all')
rule('bg',
  [isColor, (css, v) => css.backgroundColor = v],
  [isEq('no-repeat'), (css, v) => css.backgroundRepeat = v],
  [isIn('fixed', 'local', 'scroll'), (css, v) => css.backgroundAttachment = v],
  [isObjectPosition, (css, v) => css.backgroundPosition = v],
  [isIn('auto', 'cover', 'contain'), (css, v) => css.backgroundSize = v],
)
rule('bg-repeat', [isOf({
  '': 'repeat',
  'x': 'repeat-x',
  'y': 'repeat-y',
  'round': 'round',
  'space': 'space',
}), (css, v) => css.backgroundRepeat = v])
rule('bg-clip', [isOf({
  'border': 'border-box',
  'padding': 'padding-box',
  'content': 'content-box',
  'text': 'text',
}), (css, v) => css.backgroundClip = v])
rule('bg-origin', [isOf({
  'border': 'border-box',
  'padding': 'padding-box',
  'content': 'content-box',
}), (css, v) => css.backgroundOrigin = v])


const is0248 = isOf({ '': 1, '0': 0, '2': 2, '4': 4, '8': 8 })
rule('border',
  [is0248, (css, v) => css.borderWidth = v],
  [isIn('solid', 'dashed', 'dotted', 'double', 'hidden', 'none'), (css, v) => css.borderStyle = v],
  [isColor, (css, v) => css.borderColor = v],
)
rule('border-x',
  [is0248, (css, v) => { css.borderLeftWidth = v; css.borderRightWidth = v }],
  [isColor, (css, v) => { css.borderLeftColor = v; css.borderRightColor = v }],
)
rule('border-y',
  [is0248, (css, v) => { css.borderTopWidth = v; css.borderBottomWidth = v }],
  [isColor, (css, v) => { css.borderTopColor = v; css.borderBottomColor = v }],
)
rule('border-t',
  [is0248, (css, v) => css.borderTopWidth = v],
  [isColor, (css, v) => css.borderTopColor = v],
)
rule('border-r',
  [is0248, (css, v) => css.borderRightWidth = v],
  [isColor, (css, v) => css.borderRightColor = v],
)
rule('border-b',
  [is0248, (css, v) => css.borderBottomWidth = v],
  [isColor, (css, v) => css.borderBottomColor = v],
)
rule('border-l',
  [is0248, (css, v) => css.borderLeftWidth = v],
  [isColor, (css, v) => css.borderLeftColor = v],
)

const isCorner = isOf({
  none: 0,
  sm: 2,
  '': 4,
  md: 6,
  lg: 8,
  xl: 12,
  '2xl': 16,
  '3xl': 24,
  full: 9999,
})
rule('rounded', [isCorner, (css, v) => css.borderRadius = v])
rule('rounded-t', [isCorner, (css, v) => { css.borderTopLeftRadius = v; css.borderTopRightRadius = v }])
rule('rounded-r', [isCorner, (css, v) => { css.borderTopRightRadius = v; css.borderBottomRightRadius = v }])
rule('rounded-b', [isCorner, (css, v) => { css.borderBottomLeftRadius = v; css.borderBottomRightRadius = v }])
rule('rounded-l', [isCorner, (css, v) => { css.borderTopLeftRadius = v; css.borderBottomLeftRadius = v }])
rule('rounded-tr', [isCorner, (css, v) => css.borderTopRightRadius = v])
rule('rounded-tl', [isCorner, (css, v) => css.borderTopLeftRadius = v])
rule('rounded-br', [isCorner, (css, v) => css.borderBottomRightRadius = v])
rule('rounded-bl', [isCorner, (css, v) => css.borderBottomLeftRadius = v])

rule('outline',
  [isOf({ '0': 0, '1': 1, '2': 2, '4': 4, '8': 8 }), (css, v) => css.outlineWidth = v],
  [isColor, (css, v) => css.outlineColor = v],
  [isNone, (css) => { css.outline = '2px solid transparent'; css.outlineOffset = 2 }],
  [isEq(''), (css) => css.outlineStyle = 'solid'],
  [isIn('dashed', 'dotted', 'double', 'hidden'), (css, v) => css.outlineStyle = v],
)
rule('outline-offset', [isOf({ '0': 0, '1': 1, '2': 2, '4': 4, '8': 8 }), (css, v) => css.outlineOffset = v])


const isBoxShadow = isOf({
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  '': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
  none: '0 0 #0000',
})

rule('shadow', [isBoxShadow, (css, v) => css.boxShadow = v])
const isOpacity = isOf({
  '0': 0,
  '5': 0.05,
  '10': 0.1,
  '20': 0.2,
  '25': 0.25,
  '30': 0.3,
  '40': 0.4,
  '50': 0.5,
  '60': 0.6,
  '70': 0.7,
  '75': 0.75,
  '80': 0.8,
  '90': 0.9,
  '95': 0.95,
  '100': 1,
})
rule('opacity', [isOpacity, (css, v) => css.opacity = v])

const isBlendMode = isIn(
  'normal',
  'multiply',
  'screen',
  'overlay',
  'darken',
  'lighten',
  'color-dodge',
  'color-burn',
  'hard-light',
  'soft-light',
  'difference',
  'exclusion',
  'hue',
  'saturation',
  'color',
  'luminosity',
  'plus-lighter',
)
rule('mix-blend', [isBlendMode, (css, v) => css.mixBlendMode = v])
rule('bg-blend', [isBlendMode, (css, v) => css.backgroundBlendMode = v])

const filter = (f: S) => (css: CSS, v: any) => css.filter = `${f}(${v})`
const isBlur = isOf({
  'none': '0',
  'sm': '4px',
  '': '8px',
  'md': '12px',
  'lg': '16px',
  'xl': '24px',
  '2xl': '40px',
  '3xl': '64px',
})
rule('blur', [isBlur, filter('blur')])
const isBrightness = isOf({
  '0': '0',
  '50': '.5',
  '75': '.75',
  '90': '.9',
  '95': '.95',
  '100': '1',
  '105': '1.05',
  '110': '1.1',
  '125': '1.25',
  '150': '1.5',
  '200': '2',
})
rule('brightness', [isBrightness, filter('brightness')])

const isContrast = isOf({
  '0': '0',
  '50': '.5',
  '75': '.75',
  '100': '1',
  '125': '1.25',
  '150': '1.5',
  '200': '2',
})
rule('contrast', [isContrast, filter('contrast')])

rule('drop-shadow', [isOf({
  'sm': 'drop-shadow(0 1px 1px rgb(0 0 0 / 0.05))',
  '': 'drop-shadow(0 1px 2px rgb(0 0 0 / 0.1)) drop-shadow(0 1px 1px rgb(0 0 0 / 0.06))',
  'md': 'drop-shadow(0 4px 3px rgb(0 0 0 / 0.07)) drop-shadow(0 2px 2px rgb(0 0 0 / 0.06))',
  'lg': 'drop-shadow(0 10px 8px rgb(0 0 0 / 0.04)) drop-shadow(0 4px 3px rgb(0 0 0 / 0.1))',
  'xl': 'drop-shadow(0 20px 13px rgb(0 0 0 / 0.03)) drop-shadow(0 8px 5px rgb(0 0 0 / 0.08))',
  '2xl': 'drop-shadow(0 25px 25px rgb(0 0 0 / 0.15))',
  'none': 'drop-shadow(0 0 #0000)',
}), (css, v) => css.filter = v])
const isGrayscale = isOf({
  '0': '0',
  '': '100%',
})
rule('grayscale', [isGrayscale, filter('grayscale')])
const isHueRotate = isOf({
  '0': '0deg',
  '15': '15deg',
  '30': '30deg',
  '60': '60deg',
  '90': '90deg',
  '180': '180deg',
})
rule('hue-rotate', [isHueRotate, filter('hue-rotate')])
const isInvert = isOf({
  '0': '0',
  '': '100%',
})
rule('invert', [isInvert, filter('invert')])
const isSaturate = isOf({
  '0': '0',
  '50': '.5',
  '100': '1',
  '150': '1.5',
  '200': '2',
})
rule('saturate', [isSaturate, filter('saturate')])
const isSepia = isOf({
  '0': '0',
  '': '100%',
})
rule('sepia', [isSepia, filter('sepia')])

const backdropFilter = (f: S) => (css: CSS, v: any) => css.backdropFilter = `${f}(${v})`
rule('backdrop-blur', [isBlur, backdropFilter('blur')])
rule('backdrop-brightness', [isBrightness, backdropFilter('brightness')])
rule('backdrop-contrast', [isContrast, backdropFilter('contrast')])
rule('backdrop-grayscale', [isGrayscale, backdropFilter('grayscale')])
rule('backdrop-hue-rotate', [isHueRotate, backdropFilter('hue-rotate')])
rule('backdrop-invert', [isInvert, backdropFilter('invert')])
rule('backdrop-opacity', [isOpacity, backdropFilter('opacity')])
rule('backdrop-saturate', [isSaturate, backdropFilter('saturate')])
rule('backdrop-sepia', [isSepia, backdropFilter('sepia')])

const isDuration = isNOf([75, 100, 150, 200, 300, 500, 700, 1000], v => v + 'ms')
rule('duration', [isDuration, (css, v) => css.transitionDuration = v])


const easeInOut = 'cubic-bezier(0.4, 0, 0.2, 1)'
rule('transition',
  [isNone, (css, s) => css.transitionProperty = s],
  [either(isIn('all', 'opacity', 'transform'), isOf({
    '': 'color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter',
    'colors': 'color, background-color, border-color, text-decoration-color, fill, stroke',
    'shadow': 'box-shadow',
  })), (css, s) => {
    css.transitionProperty = s;
    css.transitionTimingFunction = easeInOut;
    css.transitionDuration = '150ms';
  }],
)
rule('ease', [isOf({
  'linear': 'linear',
  'in': 'cubic-bezier(0.4, 0, 1, 1)',
  'out': 'cubic-bezier(0, 0, 0.2, 1)',
  'in-out': easeInOut,
}), (css, v) => css.transitionTimingFunction = v])
rule('delay', [isDuration, (css, v) => css.transitionDelay = v])
rule('animate', [isOf({
  'none': 'none',
  'spin': 'spin 1s linear infinite',
  'ping': 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
  'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  'bounce': 'bounce 1s infinite',
}), (css, v) => css.animation = v])

const isScaleTransform = isOf({
  '0': '0',
  '50': '.5',
  '75': '.75',
  '90': '.9',
  '95': '.95',
  '100': '1',
  '105': '1.05',
  '110': '1.1',
  '125': '1.25',
  '150': '1.5',
})

const _transform = (u: S) => (f: S) => (css: CSS, v: S) => {
  const t = `${f}(${v}${u})`
  if (css.transform) {
    css.transform += ' ' + t
  } else {
    css.transform = t
  }
}
const transform = _transform('')
const transformDeg = _transform('deg')
const transformPx = _transform('px')
rule('scale', [isScaleTransform, transform('scale')])
rule('scale-x', [isScaleTransform, transform('scaleX')])
rule('scale-y', [isScaleTransform, transform('scaleY')])

rule('rotate', [isIn('0', '1', '2', '3', '6', '12', '45', '90', '180'), transformDeg('rotate')])
rule('translate-x',
  [isSize, transformPx('translateX')],
  [isRatioSubset, transform('translateX')],
)
rule('translate-y',
  [isSize, transformPx('translateY')],
  [isRatioSubset, transform('translateY')],
)
rule('skew-x', [isIn('0', '1', '2', '3', '6', '12'), transformDeg('skewX')])
rule('skew-y', [isIn('0', '1', '2', '3', '6', '12'), transformDeg('skewY')])
rule('origin', [isOf({
  'center': 'center',
  'top': 'top',
  'top-right': 'top right',
  'right': 'right',
  'bottom-right': 'bottom right',
  'bottom': 'bottom',
  'bottom-left': 'bottom left',
  'left': 'left',
  'top-left': 'top left',
}), (css, v) => css.transformOrigin = v])
rule('accent', [either(isColor, isEq('auto')), (css, v) => css.accentColor = v])
rule('appearance', [isNone, (css, v) => css.appearance = v])

const cursors: S[] = [
  'auto',
  'default',
  'pointer',
  'wait',
  'text',
  'move',
  'help',
  'not-allowed',
  'none',
  'context-menu',
  'progress',
  'cell',
  'crosshair',
  'vertical-text',
  'alias',
  'copy',
  'no-drop',
  'grab',
  'grabbing',
  'all-scroll',
  'col-resize',
  'row-resize',
  'n-resize',
  'e-resize',
  's-resize',
  'w-resize',
  'ne-resize',
  'nw-resize',
  'se-resize',
  'sw-resize',
  'ew-resize',
  'ns-resize',
  'nesw-resize',
  'nwse-resize',
  'zoom-in',
  'zoom-out',
]
rule('cursor', [isIn(...cursors), (css, v) => css.cursor = v])
rule('caret', [isColor, (css, v) => css.caretColor = v])
rule('pointer-events', [isIn('none', 'auto'), (css, v) => css.pointerEvents = v])
rule('resize', [isOf({ none: 'none', x: 'horizontal', y: 'vertical', '': 'both' }), (css, v) => css.resize = v])
rule('scroll', [isIn('auto', 'smooth'), (css, v) => css.scrollBehavior = v])
rule('scroll-m', [isSize, (css, v) => css.scrollMargin = v])
rule('scroll-mx', [isSize, (css, v) => { css.scrollMarginLeft = v; css.scrollMarginRight = v }])
rule('scroll-my', [isSize, (css, v) => { css.scrollMarginTop = v; css.scrollMarginBottom = v }])
rule('scroll-mt', [isSize, (css, v) => css.scrollMarginTop = v])
rule('scroll-mr', [isSize, (css, v) => css.scrollMarginRight = v])
rule('scroll-mb', [isSize, (css, v) => css.scrollMarginBottom = v])
rule('scroll-ml', [isSize, (css, v) => css.scrollMarginLeft = v])
rule('scroll-p', [isSize, (css, v) => css.scrollPadding = v])
rule('scroll-px', [isSize, (css, v) => { css.scrollPaddingLeft = v; css.scrollPaddingRight = v }])
rule('scroll-py', [isSize, (css, v) => { css.scrollPaddingTop = v; css.scrollPaddingBottom = v }])
rule('scroll-pt', [isSize, (css, v) => css.scrollPaddingTop = v])
rule('scroll-pr', [isSize, (css, v) => css.scrollPaddingRight = v])
rule('scroll-pb', [isSize, (css, v) => css.scrollPaddingBottom = v])
rule('scroll-pl', [isSize, (css, v) => css.scrollPaddingLeft = v])
rule('snap',
  [isNone, (css, v) => css.scrollSnapType = v],
  [isOf({
    start: 'start',
    end: 'end',
    center: 'center',
    'align-none': 'none',
  }), (css, v) => css.scrollSnapAlign = v],
  [isIn('normal', 'always'), (css, v) => css.scrollSnapStop = v]
)
rule('touch', [isIn('auto', 'none', 'pan-x', 'pan-left', 'pan-right', 'pan-y', 'pan-up', 'pan-down', 'pinch-zoom', 'manipulation'), (css, v) => css.touchAction = v])
rule('select', [isIn('none', 'text', 'all', 'auto'), (css, v) => css.userSelect = v])

rule('will-change', [isOf({
  auto: 'auto',
  scroll: 'scroll-position',
  contents: 'contents',
  transform: 'transform',
}), (css, v) => css.willChange = v])


const tryExpand = (css: CSS, handles: Handler[], arg: S): B => {
  if (!handles) return false
  for (const [match, apply] of handles) {
    const v = match(arg)
    if (v !== undefined) {
      apply(css, v)
      return true
    }
  }
  return false
}

const expand = (s: S, css: CSS): B => {
  if (tryExpand(css, rules[s], '')) return true
  let pos = s.indexOf('-')
  while (pos >= 0 && pos < s.length) {
    const handles = rules[s.substring(0, pos)]
    if (tryExpand(css, handles, s.substring(pos + 1))) return true
    pos = s.indexOf('-', pos + 1)
  }
  return false
}

export const stylize = (css: CSS, spec: S) => {
  const styles = spec.split(/\s+/g)
  for (const s of styles) if (!expand(s, css)) console.warn(`Unknown style: "${s}"`)
  return css
}
