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

import { Checkbox as FCheckbox } from '@fluentui/react';
import { B } from './core';
import { css } from './css';
import { BoxProps, make } from './ui';

export const Checkbox = make(({ context, box }: BoxProps) => {
  const
    { modes, value, text, } = box,
    live = modes.has('live'),
    onChecked = (checked?: B) => {
      context.record(checked ? true : false)
      if (live) context.commit()
    },
    render = () => {
      return (
        <div className={css(box.style)}>
          <FCheckbox
            label={text}
            defaultChecked={value ? true : false}
            onChange={(_, checked) => onChecked(checked)}
          />
        </div>
      )
    }

  context.record(value ? true : false)

  return { render }
})

