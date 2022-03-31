import { Dropdown, IDropdownOption } from '@fluentui/react';
import React from 'react';
import { S } from './core';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';

export const XDroplist = make(({ context, box }: BoxProps) => {
  const
    { index, text, placeholder, error, required, options } = box,
    selecteds = selectedsOf(box),
    selection = new Set<S>(selecteds.map(s => String(s.value))),
    items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.text) })),
    selectedKeys = selecteds.map(c => String(c.value)),
    capture = () => context.capture(index, Array.from(selection)),
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IDropdownOption) => {
      if (option) {
        const key = String(option.key)
        if (option.selected) {
          selection.add(key)
        } else {
          selection.delete(key)
        }
        capture()
      }
    },
    render = () => {
      return (
        <Dropdown
          multiSelect
          label={text}
          placeholder={placeholder}
          options={items}
          defaultSelectedKeys={selectedKeys}
          errorMessage={error}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  capture()

  return { render }
})
