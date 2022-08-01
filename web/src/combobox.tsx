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

import { ComboBox as FComboBox, IComboBox, IComboBoxOption } from '@fluentui/react';
import React from 'react';
import { N, S } from './core';
import { css } from './css';
import { selectedOf } from './options';
import { BoxProps, make } from './ui';

export const ComboBox = make(({ context, box }: BoxProps) => {
  const
    { modes, value, text, placeholder, error, options, style } = box,
    required = modes.has('required'),
    items: IComboBoxOption[] = options.map(c => ({ key: String(c.value), text: c.text ?? '' })),
    selected = selectedOf(box),
    selectedKey = selected ? String(selected.value) : undefined,
    // Double-test because value may not be an available option.
    initialValue = selected ? String(selected.value) : value ? String(value) : undefined,
    onChange = (_: React.FormEvent<IComboBox>, option?: IComboBoxOption, _index?: N, value?: S) => {
      const v = option ? option.text : value
      if (v) context.record(v)
    },
    render = () => (
      <div className={css(style)}>
        <FComboBox
          label={text}
          text={initialValue}
          placeholder={placeholder}
          options={items}
          defaultSelectedKey={selectedKey}
          required={required}
          errorMessage={error}
          onChange={onChange}
          allowFreeform
          autoComplete='on'
        />
      </div>
    )


  context.record(initialValue ?? null)

  return { render }
})