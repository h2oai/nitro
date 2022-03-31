import { ColorPicker, cssColor, IColor, IRGB } from '@fluentui/react';
import React from 'react';
import { Labeled } from './label';
import { BoxProps, make } from './ui';


export const XColorPicker = make(({ context, box }: BoxProps) => {
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
          <ColorPicker
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
