import { ISliderProps, Slider as FSlider } from '@fluentui/react';
import React from 'react';
import { valueFromRange, isN, isPair, U, toN } from './core';
import { BoxProps, make } from './ui';

export const Slider = make(({ context, box }: BoxProps) => {
  const
    { index, text, value, placeholder, min, max, step } = box,
    originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
    ranged = isPair(value) && isN(value[0]) && isN(value[1]),
    defaultValue = ranged ? 0 : valueFromRange(value, min, max, step),
    defaultValueMin = ranged ? valueFromRange(value[0], min, max, step) : 0,
    defaultValueMax = ranged ? valueFromRange(value[1], min, max, step) : 0,
    onChange = (v: U, range?: [U, U]) => {
      context.capture(index, range ? range : v)
    },
    render = () => {
      const
        props: Partial<ISliderProps> = {
          label: text,
          placeholder,
          min: toN(min),
          max: toN(max),
          step,
          originFromZero,
          ranged,
          onChange,
        }

      return ranged
        ? (
          <FSlider
            {...props}
            defaultLowerValue={defaultValueMin}
            defaultValue={defaultValueMax}
          />
        ) : (
          <FSlider
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
