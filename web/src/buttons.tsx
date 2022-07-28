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

import { CompoundButton, DefaultButton, IButtonStyles, Label, PrimaryButton } from '@fluentui/react';
import { isB, V } from './core';
import { css } from './css';
import { toContextualMenuProps } from './options';
import { BoxProps, make } from './ui';

export const Buttons = make(({ context, box }: BoxProps) => {
  const
    { value } = box,
    selection = new Set<V>(Array.isArray(value) ? value : value ? [value] : []),
    render = () => {
      const
        { text, options, style, modes } = box,
        horizontal = !modes.has('vertical'),
        styles: IButtonStyles = horizontal ? {} : { root: { width: '100%' } },
        compoundStyles: IButtonStyles = horizontal ? {} : { root: { width: '100%', maxWidth: 'auto' } },
        capture = (value: V) => {
          context.record(value)
          context.commit()
        },
        hasNoPrimary = options.every(o => !isB(o.selected)),
        buttons = options.map((o, i) => {
          const
            text = o.text,
            onClick = () => capture(o.value)
          return (hasNoPrimary && i === 0) || o.selected || selection.has(o.value) // make first button primary if none are.
            ? o.options
              ? o.value === ''
                ? <PrimaryButton key={o.value} data-name={o.name} text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(o.options, capture)} />
                : <PrimaryButton key={o.value} data-name={o.name} split text={text} styles={styles} menuProps={toContextualMenuProps(o.options, capture)} onClick={onClick} />
              : o.caption
                ? <CompoundButton key={o.value} data-name={o.name} primary text={text} secondaryText={o.caption} styles={compoundStyles} onClick={onClick} />
                : <PrimaryButton key={o.value} data-name={o.name} text={text} styles={styles} onClick={onClick} />
            : o.options
              ? o.value === ''
                ? <DefaultButton key={o.value} data-name={o.name} text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(o.options, capture)} />
                : <DefaultButton key={o.value} data-name={o.name} split text={text} styles={styles} menuProps={toContextualMenuProps(o.options, capture)} onClick={onClick} />
              : o.caption
                ? <CompoundButton key={o.value} data-name={o.name} text={text} secondaryText={o.caption} styles={compoundStyles} onClick={onClick} />
                : <DefaultButton key={o.value} data-name={o.name} text={text} styles={styles} onClick={onClick} />
        })
      return (
        <div className={css('flex flex-col')}>
          {text ? <Label>{text}</Label> : <Label>&nbsp;</Label>}
          <div className={css('flex gap-2', horizontal ? 'flex-row' : 'flex-col', style)}>{buttons}</div>
        </div>
      )
    }
  context.record(null)
  return { render }
})

