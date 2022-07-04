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

import { Rating as FRating } from '@fluentui/react';
import React from 'react';
import { isN, toN } from './core';
import { Labeled } from './label';
import { BoxProps, make } from './ui';

export const Rating = make(({ box }: BoxProps) => {
  const
    { context, text, placeholder, min, max, value, live } = box,
    allowZeroStars = isN(min) && min <= 0,
    defaultRating = toN(value) ?? (allowZeroStars ? 0 : 1),
    onChange = (event: React.FormEvent<HTMLElement>, rating?: number) => {
      if (rating === undefined) return
      context.record(rating)
      if (live) context.commit()
    },
    render = () => {
      return (
        <Labeled label={text}>
          <FRating
            defaultRating={defaultRating}
            allowZeroStars={allowZeroStars}
            max={toN(max)}
            onChange={onChange}
            placeholder={placeholder}
          />
        </Labeled>
      )
    }

  context.record(defaultRating)

  return { render }
})
