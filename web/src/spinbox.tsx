import { Position, SpinButton } from '@fluentui/react';
import React from 'react';
import { getDefaultValue, isS, unum } from './core';
import { BoxProps, make } from './ui';


export const XSpinbox = make(({ context, box }: BoxProps) => {
  const
    { index, text, value, min, max, step, precision, placeholder } = box,
    defaultValue = getDefaultValue(value, min, max, step),
    onChange = (_: React.SyntheticEvent<HTMLElement>, value?: string): void => {
      let v = isS(value) ? parseFloat(value) : NaN
      if (!isNaN(v)) context.capture(index, v)
    },
    render = () => {
      return (
        <SpinButton
          label={text}
          placeholder={placeholder}
          labelPosition={Position.top}
          defaultValue={defaultValue !== undefined ? String(defaultValue) : undefined}
          min={unum(min)}
          max={unum(max)}
          step={step}
          precision={precision}
          styles={{ labelWrapper: { marginBottom: -4 } }} // Make textbox top match textfield
          onChange={onChange}
        />
      )
    }

  context.capture(index, defaultValue ?? 0)

  return { render }
})
