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

import { IColorCellProps, Label, SwatchColorPicker } from '@fluentui/react';
import React from 'react';
import { S } from './core';
import { css } from './css';
import { selectedOf } from './options';
import { BoxProps, make } from './ui';

const swatchCellSize = 25
export const ColorPalette = make(({ context, box }: BoxProps) => {
  const
    { name, modes, text, options: rawOptions, style, disabled: rawDisabled } = box,
    disabled = rawDisabled === true,
    options = rawOptions ?? [],
    live = modes.has('live'),
    selected = selectedOf(box),
    cells: IColorCellProps[] = options.map(c => ({
      id: String(c.value),
      label: String(c.text),
      color: String(c.value),
    })),
    onChange = (_e: React.FormEvent<HTMLElement>, _id?: S, color?: S) => {
      if (color) {
        context.record(color)
        if (live) context.commit()
      }
    },
    render = () => {
      return (
        <div className={css('flex flex-col', style)} data-name={name}>
          {text && <Label disabled={disabled}>{text}</Label>}
          <SwatchColorPicker
            columnCount={10}
            colorCells={cells}
            cellWidth={swatchCellSize}
            cellHeight={swatchCellSize}
            defaultSelectedId={selected ? String(selected.value) : undefined}
            onChange={onChange}
            disabled={disabled}
          />
        </div>
      )
    }

  context.record(selected ? selected.value : null)

  return { render }
})
