import { ISliderProps, Slider } from '@fluentui/react';
import React from 'react';
import { getDefaultValue, isN, isPair, U, unum } from './core';
import { BoxProps, make } from './ui';


export const XSlider = make(({ context, box }: BoxProps) => {
  const
    { index, text, value, placeholder, min, max, step } = box,
    originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
    ranged = isPair(value) && isN(value[0]) && isN(value[1]),
    defaultValue = ranged ? 0 : getDefaultValue(value, min, max, step),
    defaultValueMin = ranged ? getDefaultValue(value[0], min, max, step) : 0,
    defaultValueMax = ranged ? getDefaultValue(value[1], min, max, step) : 0,
    onChange = (v: U, range?: [U, U]) => {
      context.capture(index, range ? range : v)
    },
    render = () => {
      const
        props: Partial<ISliderProps> = {
          label: text,
          placeholder,
          min: unum(min),
          max: unum(max),
          step,
          originFromZero,
          ranged,
          onChange,
        }

      return ranged
        ? (
          <Slider
            {...props}
            defaultLowerValue={defaultValueMin}
            defaultValue={defaultValueMax}
          />
        ) : (
          <Slider
            {...props}
            defaultValue={defaultValue}
          />
        )
    }

  if (ranged) {
    if (defaultValueMin !== undefined && defaultValueMax !== undefined) {
      context.capture(index, [defaultValueMin, defaultValueMax])
    }
  } else {
    if (defaultValue !== undefined) {
      context.capture(index, defaultValue)
    }
  }

  return { render }
})
