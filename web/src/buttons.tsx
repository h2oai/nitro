import { Alignment, CompoundButton, DefaultButton, IButtonStyles, PrimaryButton, Stack } from '@fluentui/react';
import React from 'react';
import { isB, V } from './core';
import { Labeled } from './label';
import { toContextualMenuProps } from './options';
import { BoxProps, make } from './ui';

export const Buttons = make(({ context, box }: BoxProps) => {
  const
    { value } = box,
    selection = new Set<V>(Array.isArray(value) ? value : value ? [value] : []),
    render = () => {
      const
        { text, index, row, options, align } = box,
        horizontal = row !== false,
        horizontalAlign = horizontal
          ? align === 'center'
            ? 'center'
            : align === 'right' ? 'end' : undefined
          : undefined,
        styles: IButtonStyles = horizontal ? {} : { root: { width: '100%' } },
        compoundStyles: IButtonStyles = horizontal ? {} : { root: { width: '100%', maxWidth: 'auto' } },
        capture = (value: V) => {
          context.capture(index, value)
          context.submit()
        },
        hasNoPrimary = options.every(o => !isB(o.selected)),
        buttons = options.map((o, i) => {
          const
            text = o.text,
            onClick = () => capture(o.value),
            button = (hasNoPrimary && i === 0) || o.selected || selection.has(o.value) // make first button primary if none are.
              ? o.options
                ? o.value === ''
                  ? <PrimaryButton data-name={o.name} text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(o.options, capture)} />
                  : <PrimaryButton data-name={o.name} split text={text} styles={styles} menuProps={toContextualMenuProps(o.options, capture)} onClick={onClick} />
                : o.caption
                  ? <CompoundButton data-name={o.name} primary text={text} secondaryText={o.caption} styles={compoundStyles} onClick={onClick} />
                  : <PrimaryButton data-name={o.name} text={text} styles={styles} onClick={onClick} />
              : o.options
                ? o.value === ''
                  ? <DefaultButton data-name={o.name} text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(o.options, capture)} />
                  : <DefaultButton data-name={o.name} split text={text} styles={styles} menuProps={toContextualMenuProps(o.options, capture)} onClick={onClick} />
                : o.caption
                  ? <CompoundButton data-name={o.name} text={text} secondaryText={o.caption} styles={compoundStyles} onClick={onClick} />
                  : <DefaultButton data-name={o.name} text={text} styles={styles} onClick={onClick} />
          return <Stack.Item key={o.value}>{button}</Stack.Item>
        })
      return (
        <Labeled label={text ?? ' '}>
          <Stack horizontal={horizontal} horizontalAlign={horizontalAlign} tokens={{ childrenGap: 5 }} >{buttons}</Stack>
        </Labeled>
      )
    }
  return { render }
})

