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

import { ColorPicker as FColorPicker, cssColor, IColor, IRGB } from '@fluentui/react';
import React from 'react';
import { Labeled } from './label';
import { BoxProps, make } from './ui';


export const ColorPicker = make(({ context, box }: BoxProps) => {
  const
    { index, text, value } = box,
    colorValue = value ? String(value) : '#000',
    defaultColor = cssColor(colorValue),
    colorToTuple = ({ r, g, b, a }: IRGB) => [r, g, b, a ?? 100],
    capture = (color: IRGB) => context.capture(index, colorToTuple(color)),
    onChange = (_: React.SyntheticEvent<HTMLElement>, color: IColor) => capture(color),
    render = () => {
      return (
        <Labeled label={text}>
          <FColorPicker
            color={colorValue}
            alphaType='alpha'
            onChange={onChange}
            showPreview
          />
        </Labeled>
      )
    }

  if (defaultColor) capture(defaultColor)

  return { render }
})
