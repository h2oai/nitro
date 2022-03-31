import { ITextFieldProps, MaskedTextField, TextField } from '@fluentui/react';
import React from 'react';
import { isN, isS, S } from './core';
import { BoxProps, make } from './ui';


export const XTextbox = make(({ context, box }: BoxProps) => {
  const
    { index, text, value, placeholder, icon, mask, prefix, suffix, error, lines, required, password } = box,
    onChange = ({ target }: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, v?: S) => {
      v = v ?? (target as HTMLInputElement).value ?? value ?? ''
      // TODO live?
      context.capture(index, v)
    },
    render = () => {
      const
        field: Partial<ITextFieldProps> = {
          label: text,
          defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
          placeholder: placeholder ?? (text ? undefined : 'Enter some text...'),
          errorMessage: error,
          required: required === true,
          onChange,
        }
      return password === true
        ? <TextField {...field} type='password' canRevealPassword revealPasswordAriaLabel='Show password' />
        : mask
          ? <MaskedTextField {...field} mask={mask} />
          : lines && (lines >= 1)
            ? <TextField {...field} multiline resizable autoAdjustHeight rows={lines} />
            : <TextField {...field} iconProps={icon ? { iconName: icon } : undefined} prefix={prefix} suffix={suffix} />
    }

  context.capture(index, (value as any) ?? '')
  return { render }
})
