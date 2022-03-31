import { ChoiceGroup as FChoiceGroup, IChoiceGroupOption } from '@fluentui/react';
import React from 'react';
import { selectedOf } from './options';
import { BoxProps, make } from './ui';

export const ChoiceGroup = make(({ context, box }: BoxProps) => {
  const
    { index, text, placeholder, required, options } = box,
    selected = selectedOf(box),
    items: IChoiceGroupOption[] = options.map(({ value, text, icon: iconName }) => ({
      key: String(value),
      text: String(text),
      iconProps: iconName ? { iconName } : undefined,
    })),
    selectedKey = selected ? selected.value : undefined,
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IChoiceGroupOption) => {
      if (option) context.capture(index, option?.key)
    },
    render = () => {
      return (
        <FChoiceGroup
          label={text}
          placeholder={placeholder}
          options={items}
          defaultSelectedKey={selectedKey}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})
