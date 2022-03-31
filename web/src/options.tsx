import { ContextualMenuItemType, DropdownMenuItemType, IContextualMenuItem, IContextualMenuProps, IDropdownOption } from '@fluentui/react';
import { gensym, V, xid } from './core';
import { Box, Option } from './protocol';

export const
  toContextualMenuItem = ({ value, text, caption, icon, options }: Option, capture: (v: V) => void): IContextualMenuItem => {
    return text
      ? {
        key: String(value),
        text,
        title: caption,
        iconProps: icon ? { iconName: icon } : undefined,
        subMenuProps: options ? toContextualMenuProps(options, capture) : undefined,
        onClick: () => capture(value),
      } : {
        key: xid(),
        itemType: ContextualMenuItemType.Divider,
      }
  },
  toContextualMenuProps = (cs: Option[], capture: (v: V) => void): IContextualMenuProps => ({
    items: cs.map(c => toContextualMenuItem(c, capture))
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
  selectedOf = ({ value, options }: Box): Option | undefined => value
    ? options.find(c => c.value === value)
    : options.find(c => c.selected),

  selectedsOf = ({ value, options }: Box): Option[] => Array.isArray(value)
    ? options.filter(c => value.includes(c.value))
    : options.filter(c => c.selected)
