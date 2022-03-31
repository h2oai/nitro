import { IColorCellProps, SwatchColorPicker } from '@fluentui/react';
import React from 'react';
import { S } from './core';
import { Labeled } from './label';
import { selectedOf } from './options';
import { BoxProps, make } from './ui';


const swatchCellSize = 25
export const XColorPalette = make(({ context, box }: BoxProps) => {
  const
    { index, text, options } = box,
    selected = selectedOf(box),
    cells: IColorCellProps[] = options.map(c => ({
      id: String(c.value),
      label: String(c.text),
      color: String(c.value),
    })),
    onChange = (_e: React.FormEvent<HTMLElement>, _id?: S, color?: S) => {
      if (color) context.capture(index, color)
    },
    render = () => {
      return (
        <Labeled label={text}>
          <SwatchColorPicker
            columnCount={10}
            colorCells={cells}
            cellWidth={swatchCellSize}
            cellHeight={swatchCellSize}
            defaultSelectedId={selected ? String(selected.value) : undefined}
            onChange={onChange}
          />
        </Labeled>
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})
