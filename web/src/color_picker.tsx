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

import { ColorPicker as FColorPicker, cssColor, IColor, IRGB, Label } from '@fluentui/react';
import React from 'react';
import { css } from './css';
import { BoxProps, make } from './ui';


export const ColorPicker = make(({ context, box }: BoxProps) => {
  const
    { modes, text, value, style } = box,
    live = modes.has('live'),
    colorValue = value ? String(value) : '#000',
    defaultColor = cssColor(colorValue),
    colorToTuple = ({ r, g, b, a }: IRGB) => [r, g, b, a ?? 100],
    record = (color: IRGB) => {
      context.record(colorToTuple(color))
      if (live) context.commit()
    },
    onChange = (_: React.SyntheticEvent<HTMLElement>, color: IColor) => record(color),
    render = () => {
      return (
        <div className={css('flex flex-col', style)}>
          {text && <Label>{text}</Label>}
          <FColorPicker
            color={colorValue}
            alphaType='alpha'
            onChange={onChange}
            showPreview
          />
        </div>
      )
    }

  context.record(defaultColor ? colorToTuple(defaultColor) : null)

  return { render }
})
