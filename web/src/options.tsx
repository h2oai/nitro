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

import { ContextualMenuItemType, DropdownMenuItemType, IContextualMenuItem, IContextualMenuProps, IDropdownOption } from '@fluentui/react';
import { gensym, V, xid } from './core';
import { Box, Option } from './protocol';

export const
  toContextualMenuItem = ({ name, value, text, caption, icon, options }: Option, record: (v: V) => void): IContextualMenuItem => {
    return text
      ? {
        key: String(value),
        text,
        title: caption,
        iconProps: icon ? { iconName: icon } : undefined,
        subMenuProps: options ? toContextualMenuProps(options, record) : undefined,
        onClick: () => record(value),
        'data-name': name,
      } : {
        key: xid(),
        itemType: ContextualMenuItemType.Divider,
      }
  },
  toContextualMenuProps = (cs: Option[], record: (v: V) => void): IContextualMenuProps => ({
    items: cs.map(c => toContextualMenuItem(c, record))
  }),
  toDropdownOption = (c: Option): IDropdownOption => ({
    key: c.value,
    text: String(c.text)
  }),
  toGroupedDropdownOptions = (options: Option[]): IDropdownOption[] => {
    const
      items: IDropdownOption[] = [],
      sepSym = gensym('s'),
      groupSym = gensym('g')
    for (const g of options) {
      if (g.options?.length) {
        if (options.length) items.push({ key: sepSym(), text: '-', itemType: DropdownMenuItemType.Divider })
        items.push({ key: groupSym(), text: String(g.text), itemType: DropdownMenuItemType.Header })
        for (const c of g.options) {
          items.push(toDropdownOption(c))
        }
      } else {
        items.push(toDropdownOption(g))
      }
    }
    return items
  },
  selectedOf = ({ value, options }: Box): Option | undefined => options
    ? value
      ? options.find(c => c.value === value)
      : options.find(c => c.selected)
    : undefined,
  selectedsOf = ({ value, options }: Box): Option[] => options
    ? Array.isArray(value)
      ? options.filter(c => value.includes(c.value))
      : options.filter(c => c.selected)
    : []
