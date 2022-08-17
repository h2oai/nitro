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

import { Checkbox, Label } from '@fluentui/react';
import { B, S, V } from './core';
import { css } from './css';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';

export const Checklist = make(({ context, box }: BoxProps) => {
  const
    { modes, text, options: rawOptions, style } = box,
    options = rawOptions ?? [],
    live = modes.has('live'),
    selecteds = selectedsOf(box),
    selection = new Set<S>(selecteds.map(s => String(s.value))),
    record = () => context.record(Array.from(selection)),
    onChecked = (value?: V, checked?: B) => {
      if (checked) {
        selection.add(String(value))
      } else {
        selection.delete(String(value))
      }
      record()
      if (live) context.commit()
    },
    render = () => {
      const
        checkboxes = options.map(c => (
          <div key={c.value}>
            <Checkbox
              label={c.text}
              defaultChecked={selection.has(String(c.value))}
              onChange={(_, checked) => onChecked(c.value, checked)}
            />
          </div>
        )),
        contents = checkboxes.length
          ? <div className={css('flex flex-col gap-2', style)}>{checkboxes}</div>
          : <div>&mdash;</div>

      return (
        <div className={css('flex flex-col gap-2')}>
          {text && <Label>{text}</Label>}
          {contents}
        </div>
      )
    }

  record()

  return { render }
})
