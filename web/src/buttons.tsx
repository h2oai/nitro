import { CompoundButton, DefaultButton, IButtonStyles, PrimaryButton, Stack } from '@fluentui/react';
import React from 'react';
import { V } from './core';
import { Labeled } from './label';
import { toContextualMenuProps } from './options';
import { BoxProps, make } from './ui';

export const Buttons = make(({ context, box }: BoxProps) => {
  const
    { value } = box,
    selection = new Set<V>(Array.isArray(value) ? value : value ? [value] : []),
    render = () => {
      const
        { text, index, row, options } = box,
        horizontal = row !== false,
        styles: IButtonStyles = horizontal ? {} : { root: { width: '100%' } },
        compoundStyles: IButtonStyles = horizontal ? {} : { root: { width: '100%', maxWidth: 'auto' } },
        capture = (value: V) => {
          context.capture(index, value)
          context.submit()
        },
        hasPrimary = options.some(o => o.selected === true),
        buttons = options.map((o, i) => {
          const
            text = o.text,
            onClick = () => capture(o.value),
            button = (!hasPrimary && i === 0) || o.selected || selection.has(o.value) // make first button primary if none are.
              ? o.options
                ? o.value === ''
                  ? <PrimaryButton text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(o.options, capture)} />
                  : <PrimaryButton split text={text} styles={styles} menuProps={toContextualMenuProps(o.options, capture)} onClick={onClick} />
                : o.caption
                  ? <CompoundButton primary text={text} secondaryText={o.caption} styles={compoundStyles} onClick={onClick} />
                  : <PrimaryButton text={text} styles={styles} onClick={onClick} />
              : o.options
                ? o.value === ''
                  ? <DefaultButton text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(o.options, capture)} />
                  : <DefaultButton split text={text} styles={styles} menuProps={toContextualMenuProps(o.options, capture)} onClick={onClick} />
                : o.caption
                  ? <CompoundButton text={text} secondaryText={o.caption} styles={compoundStyles} onClick={onClick} />
                  : <DefaultButton text={text} styles={styles} onClick={onClick} />
          return <Stack.Item key={o.value}>{button}</Stack.Item>
        })
      return (
        <Labeled label={text ?? ' '}>
          <Stack horizontal={horizontal} tokens={{ childrenGap: 5 }}>{buttons}</Stack>
        </Labeled>
      )
    }
  return { render }
})

