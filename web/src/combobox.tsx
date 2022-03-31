import { ComboBox, IComboBox, IComboBoxOption } from '@fluentui/react';
import React from 'react';
import { N, S } from './core';
import { selectedOf } from './options';
import { BoxProps, make } from './ui';


export const XComboBox = make(({ context, box }: BoxProps) => {
  const
    { index, value, text, placeholder, required, error, options } = box,
    items: IComboBoxOption[] = options.map(c => ({ key: String(c.value), text: c.text ?? '' })),
    selected = selectedOf(box),
    selectedKey = selected ? String(selected.value) : undefined,
    // Double-test because value may not be an available option.
    initialValue = selected ? String(selected.value) : value ? String(value) : undefined,
    onChange = (_: React.FormEvent<IComboBox>, option?: IComboBoxOption, _index?: N, value?: S) => {
      const v = option ? option.text : value
      if (v) context.capture(index, v)
    },
    render = () => {
      return (
        <ComboBox
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
      )
    }
  if (initialValue) context.capture(index, initialValue)
  return { render }
})