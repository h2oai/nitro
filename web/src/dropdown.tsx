import { Dropdown, IDropdownOption } from '@fluentui/react';
import React from 'react';
import { selectedOf, toDropdownOption, toGroupedDropdownOptions } from './options';
import { BoxProps, make } from './ui';

// TODO support icons on items. See "Customized Dropdown" Fluent example.
export const XDropdown = make(({ context, box }: BoxProps) => {
  const
    { index, text, placeholder, error, required, options } = box,
    selected = selectedOf(box),
    hasGroups = options.some(c => c.options?.length ? true : false),
    items: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(options) : options.map(toDropdownOption),
    selectedKey = selected ? selected.value : undefined,
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IDropdownOption) => {
      if (option) context.capture(index, option.key)
    },
    render = () => {
      return (
        <Dropdown
          label={text}
          placeholder={placeholder}
          options={items}
          selectedKey={selectedKey}
          errorMessage={error}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})