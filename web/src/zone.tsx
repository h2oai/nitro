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

import { cssColor, IRGB } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { XBox } from './box';
import { ClientContext } from './client';
import { B, Dict, isS, S } from './core';
import { ImageBlock } from './image';
import { Box } from './protocol';

// http://www.w3.org/TR/AERT#color-contrast
const isBright = ({ r, g, b }: IRGB) => (r * 299 + g * 587 + b * 114) / 1000 > 125

const flexStyles: Dict<S> = {
  start: 'flex-start',
  end: 'flex-end',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
}

const toFlexStyle = (s: S): S => flexStyles[s] ?? s

const translate = (s: S): S => isS(s) ? s.replace(/\$([\w-]+)/gi, 'var(--$1)') : s

const computeStyle = (box: Partial<Box>, inRow: B) => {
  const
    { mode, row, tile, cross_tile, wrap, gap, align, width, height, margin, padding, color, background, border, grow, shrink, basis } = box,
    isRow = row ? true : false,
    css: React.CSSProperties = {
      position: 'relative',
      flexDirection: isRow ? 'row' : 'column',
      flexWrap: wrap ? 'wrap' : 'nowrap',
      gap: gap ?? '1rem',
      justifyContent: tile ? toFlexStyle(tile) : undefined,
      alignItems: cross_tile ? toFlexStyle(cross_tile) : undefined,
      alignContent: wrap ? toFlexStyle(wrap) : undefined,
    }

  if (align) css.textAlign = translate(align) as any

  if (width !== undefined) {
    if (Array.isArray(width)) {
      switch (width.length) {
        case 1:
          {
            const [min] = width
            if (min) css.minWidth = translate(min)
          }
          break
        case 2:
          {
            const [min, max] = width
            if (min) css.minWidth = translate(min)
            if (max) css.maxWidth = translate(max)
          }
          break
        case 3:
          {
            const [min, max, initial] = width
            if (min) css.minWidth = translate(min)
            if (max) css.maxWidth = translate(max)
            if (initial) css.width = translate(initial)
          }
          break
      }
    } else {
      css.width = width
    }
  }

  if (height !== undefined) {
    if (Array.isArray(height)) {
      switch (height.length) {
        case 1:
          {
            const [min] = height
            if (min) css.minHeight = translate(min)
          }
          break
        case 2:
          {
            const [min, max] = height
            if (min) css.minHeight = translate(min)
            if (max) css.maxHeight = translate(max)
          }
          break
        case 3:
          {
            const [min, max, initial] = height
            if (min) css.minHeight = translate(min)
            if (max) css.maxHeight = translate(max)
            if (initial) css.height = translate(initial)
          }
          break
      }
    } else {
      css.height = translate(height)
    }
  }

  if (width !== undefined || height !== undefined) css.overflow = 'auto'

  if (margin !== undefined) css.margin = translate(margin)
  if (padding !== undefined) css.padding = translate(padding)

  if (background) css.backgroundColor = translate(background)

  if (mode === 'image') {
    const { fit } = box
    if (fit) css.objectFit = fit as any
  } else {
    const { image, fit } = box
    if (image) {
      css.backgroundImage = `url(${image})`
      // TODO document that scale-down is not supported
      const size = fit === 'cover'
        ? 'cover'
        : fit === 'contain'
          ? 'contain'
          : fit === 'fill' // not part of spec
            ? '100% 100%' // mimic object-fit
            : fit === 'none' // not part of spec
              ? undefined // mimic object-fit
              : 'cover' // default to image object-fit default

      css.backgroundSize = size
      css.backgroundPosition = '50% 50%' // mimic default object-fit position
      if (size) {
        css.backgroundRepeat = 'no-repeat'
      }
    }
  }

  if (color) {
    css.color = translate(color)
  } else {
    if (background) {
      const bg = cssColor(background)
      if (bg) {
        css.color = translate(isBright(bg) ? '$foreground' : '$background') // BUG Evaluate css var first
      }
    }
  }

  if (border) {
    css.borderWidth = 1
    css.borderStyle = 'solid'
    css.borderColor = translate(border)
  }

  if (padding === undefined && (border || background || css.backgroundImage)) {
    css.padding = '1rem'
  }

  if (basis !== undefined) css.flexBasis = basis
  if (grow !== undefined) css.flexGrow = grow
  if (shrink !== undefined) css.flexShrink = shrink

  if (inRow && width === undefined && height === undefined && grow === undefined && shrink === undefined) {
    css.flexGrow = '1'
    if (basis === undefined) {
      // Default flex-basis to 0 to get more predictable grow/shrink behavior
      css.flexBasis = '0'
    }
  }

  return css
}

const Container = styled.div`
  display: flex;
  box-sizing: border-box;
`
export const Zone = ({ context, box, inRow }: { context: ClientContext, box: Box, inRow: B }) => {
  const { items, row } = box, isRow = row === true

  if (items) {
    const children = items.map(box => (
      <Zone key={box.xid} context={context} box={box} inRow={isRow} />
    ))
    return (
      <Container data-name={box.name ?? undefined} style={computeStyle(box, inRow)}>{children}</Container>
    )
  } else {
    const style = computeStyle(box, inRow)

    if (box.mode === 'image') {
      return (
        <ImageBlock
          key={box.xid}
          data-name={box.name ?? undefined}
          context={context.scoped(box.index, box.xid)}
          box={box}
          style={style} />
      )
    }

    return (
      <Container key={box.xid} data-name={box.name ?? undefined} style={style}>
        <XBox context={context.scoped(box.index, box.xid)} box={box} />
      </Container>
    )
  }
}