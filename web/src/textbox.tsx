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

import { ITextFieldProps, MaskedTextField, TextField } from '@fluentui/react';
import React from 'react';
import { isN, isS, S } from './core';
import { css } from './css';
import { BoxProps, make } from './ui';

export const Textbox = make(({ context, box }: BoxProps) => {
  const
    { name, modes, text, value, placeholder, icon, mask, prefix, suffix, error, lines, style, disabled } = box,
    required = modes.has('required'),
    password = modes.has('password'),
    onChange = ({ target }: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, v?: S) => {
      v = v ?? (target as HTMLInputElement).value ?? value ?? ''
      // TODO live?
      context.record(v)
    },
    render = () => {
      const
        field: Partial<ITextFieldProps> = {
          label: text,
          defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
          placeholder: placeholder ?? (text ? undefined : 'Enter some text...'),
          iconProps: icon ? { iconName: icon } : undefined,
          prefix,
          suffix,
          errorMessage: error,
          required: required === true,
          disabled: disabled === true,
          onChange,
        }
      const textbox = password === true
        ? <TextField {...field} type='password' canRevealPassword revealPasswordAriaLabel='Show password' />
        : mask
          ? <MaskedTextField {...field} mask={mask} />
          : lines && (lines >= 1)
            ? <TextField {...field} multiline resizable autoAdjustHeight rows={lines} />
            : <TextField {...field} />
      return <div className={css(style)} data-name={name}>{textbox}</div>
    }

  context.record((value as any) ?? '')
  return { render }
})
