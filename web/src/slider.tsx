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

import { ISliderProps, Slider as FSlider } from '@fluentui/react';
import React from 'react';
import { isN, isPair, toN, U, valueFromRange } from './core';
import { BoxProps, make } from './ui';

export const Slider = make(({ box }: BoxProps) => {
  const
    { context, text, value, placeholder, min, max, step } = box,
    originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
    ranged = isPair(value) && isN(value[0]) && isN(value[1]),
    defaultValue = ranged ? 0 : valueFromRange(value, min, max, step),
    defaultValueMin = ranged ? valueFromRange(value[0], min, max, step) : 0,
    defaultValueMax = ranged ? valueFromRange(value[1], min, max, step) : 0,
    onChange = (v: U, range?: [U, U]) => {
      context.record(range ? range : v)
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
    context.record((defaultValueMin !== undefined && defaultValueMax !== undefined) ? [defaultValueMin, defaultValueMax] : null)
  } else {
    context.record(defaultValue ?? null)
  }

  return { render }
})
