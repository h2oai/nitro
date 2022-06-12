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

import { Position, SpinButton } from '@fluentui/react';
import React from 'react';
import { isS, toN, valueFromRange } from './core';
import { BoxProps, make } from './ui';

export const Spinbox = make(({ box }: BoxProps) => {
  const
    { context, text, value, min, max, step, precision, placeholder } = box,
    defaultValue = valueFromRange(value, min, max, step),
    onChange = (_: React.SyntheticEvent<HTMLElement>, value?: string): void => {
      let v = isS(value) ? parseFloat(value) : NaN
      if (!isNaN(v)) context.record(v)
    },
    render = () => {
      return (
        <SpinButton
          label={text}
          placeholder={placeholder}
          labelPosition={Position.top}
          defaultValue={defaultValue !== undefined ? String(defaultValue) : undefined}
          min={toN(min)}
          max={toN(max)}
          step={step}
          precision={precision}
          styles={{ labelWrapper: { marginBottom: -4 } }} // Make textbox top match textfield
          onChange={onChange}
        />
      )
    }

  context.record(defaultValue ?? 0)

  return { render }
})
