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
import { B, Dict, S, xid } from './core';
import { Box } from './protocol';
import { Context } from './ui';

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

const applyBoxStyles = (css: React.CSSProperties, { align, width, height, margin, padding, color, background, border, grow, shrink, basis }: Partial<Box>, isRow: B) => {

  if (align) css.textAlign = align as any

  if (width !== undefined) {
    if (Array.isArray(width)) {
      switch (width.length) {
        case 1:
          {
            const [min] = width
            if (min) css.minWidth = min
          }
          break
        case 2:
          {
            const [min, max] = width
            if (min) css.minWidth = min
            if (max) css.maxWidth = max
          }
          break
        case 3:
          {
            const [min, max, initial] = width
            if (min) css.minWidth = min
            if (max) css.maxWidth = max
            if (initial) css.width = initial
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
            if (min) css.minHeight = min
          }
          break
        case 2:
          {
            const [min, max] = height
            if (min) css.minHeight = min
            if (max) css.maxHeight = max
          }
          break
        case 3:
          {
            const [min, max, initial] = height
            if (min) css.minHeight = min
            if (max) css.maxHeight = max
            if (initial) css.height = initial
          }
          break
      }
    } else {
      css.height = height
    }
  }

  if (margin !== undefined) css.margin = margin
  if (padding !== undefined) css.padding = padding

  if (background) css.background = background
  if (color) {
    css.color = color
  } else {
    if (background) {
      const bg = cssColor(background)
      if (bg) {
        css.color = isBright(bg) ? '#000' : '#fff' // XXX use theme colors
      }
    }
  }

  if (border) {
    css.borderWidth = 1
    css.borderStyle = 'solid'
    css.borderColor = border
  }

  if ((border || background) && padding === undefined) {
    css.padding = 10
  }

  if (basis !== undefined) css.flexBasis = basis
  if (grow !== undefined) css.flexGrow = grow
  if (shrink !== undefined) css.flexShrink = shrink

  if (isRow && width === undefined && height === undefined && grow === undefined && shrink === undefined) {
    css.flexGrow = '1'
    if (basis === undefined) {
      // Default flex-basis to 0 to get more predictable grow/shrink behavior
      css.flexBasis = '0'
    }
  }

  return css
}
const ZoneItemContainer = styled.div`
  box-sizing: border-box;
`

const ZoneItem = ({ stackable, isRow, children }: { stackable: Box, isRow: B, children: JSX.Element }) => (
  <ZoneItemContainer style={applyBoxStyles({}, stackable, isRow)}>
    {children}
  </ZoneItemContainer>
)

const Container = styled.div`
  display: flex;
  box-sizing: border-box;
`

export const Zone = ({ context, boxes, stack }: { context: Context, boxes: Box[], stack: Partial<Box> }) => {
  const
    { row, tile, cross_tile, wrap, gap } = stack,
    isRow = row ? true : false,
    children = boxes.map(box => {
      if (box.items) {
        return (
          <Zone key={xid()} context={context} boxes={box.items} stack={box} />
        )
      } else {
        return (
          <ZoneItem key={xid()} stackable={box} isRow={isRow}>
            <XBox key={box.xid} context={context} box={box} />
          </ZoneItem>
        )
      }
    }),
    css: React.CSSProperties = {
      flexDirection: isRow ? 'row' : 'column',
      flexWrap: wrap ? 'wrap' : 'nowrap',
      gap: gap ?? 10,
      justifyContent: tile ? toFlexStyle(tile) : undefined,
      alignItems: cross_tile ? toFlexStyle(cross_tile) : undefined,
      alignContent: wrap ? toFlexStyle(wrap) : undefined,
    }

  return (
    <Container style={applyBoxStyles(css, stack, isRow)}>
      {children}
    </Container>
  )
}