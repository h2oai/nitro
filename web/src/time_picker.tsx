import { ISpinButtonStyles, IStackItemStyles, Position, SpinButton, Stack, Toggle } from '@fluentui/react';
import React from 'react';
import { B, leftPad, S, U } from './core';
import { Labeled } from './label';
import { BoxProps, make } from './ui';

const lpad2 = leftPad('0', 2)

type Clock = {
  hh: U, mm: U, ss: U,
  pm: B, c24: B,
}
const
  parseClock = (t: S): Clock => {
    const
      am = t.endsWith('am'),
      pm = !am && t.endsWith('pm'),
      c24 = !(am || pm),
      hhmmss = c24 ? t : t.substring(0, t.length - 2),
      [hh, mm, ss] = hhmmss.split(':').map(t => parseInt(t, 10))
    return { hh, mm, ss, pm, c24 }
  },
  clockToString = ({ hh, mm, ss, pm, c24 }: Clock) => {
    const parts: S[] = []
    if (!isNaN(hh)) parts.push(lpad2(String(hh)))
    if (!isNaN(mm)) parts.push(lpad2(String(mm)))
    if (!isNaN(ss)) parts.push(lpad2(String(ss)))
    const s = parts.join(':')
    return c24 ? s : s + (pm ? 'PM' : 'AM')
  }

export const XTimePicker = make(({ context, box }: BoxProps) => {
  const
    { index, text, value } = box,
    clock = parseClock(String(value).toLowerCase()),
    capture = () => context.capture(index, clockToString(clock)),
    hide: IStackItemStyles = { root: { display: 'none' } },
    narrow: Partial<ISpinButtonStyles> = { labelWrapper: { marginBottom: -4 }, spinButtonWrapper: { width: 50 } },
    onHoursChange = (_: React.SyntheticEvent<HTMLElement>, value?: S): void => {
      if (value) clock.hh = parseInt(value)
      capture()
    },
    onMinutesChange = (_: React.SyntheticEvent<HTMLElement>, value?: S): void => {
      if (value) clock.mm = parseInt(value)
      capture()
    },
    onSecondsChange = (_: React.SyntheticEvent<HTMLElement>, value?: S): void => {
      if (value) clock.ss = parseInt(value)
      capture()
    },
    onToggleChange = (_: React.SyntheticEvent<HTMLElement>, checked?: B): void => {
      if (checked !== undefined) clock.pm = checked
      capture()
    },
    render = () => {
      return (
        <Labeled label={text}>
          <Stack horizontal horizontalAlign='start' tokens={{ childrenGap: 5 }}>
            <Stack.Item styles={isNaN(clock.hh) ? hide : undefined}>
              <SpinButton
                label='Hours'
                labelPosition={Position.top}
                defaultValue={String(clock.hh)}
                min={clock.c24 ? 0 : 1}
                max={clock.c24 ? 23 : 12}
                styles={narrow}
                onChange={onHoursChange}
              />
            </Stack.Item>
            <Stack.Item styles={isNaN(clock.mm) ? hide : undefined}>
              <SpinButton
                label='Minutes'
                labelPosition={Position.top}
                defaultValue={String(clock.mm)}
                min={0}
                max={59}
                styles={narrow}
                onChange={onMinutesChange}
              />
            </Stack.Item>
            <Stack.Item styles={isNaN(clock.ss) ? hide : undefined}>
              <SpinButton
                label='Seconds'
                labelPosition={Position.top}
                defaultValue={String(clock.ss)}
                min={0}
                max={59}
                styles={narrow}
                onChange={onSecondsChange}
              />
            </Stack.Item>
            <Stack.Item styles={clock.c24 ? hide : undefined} align='end'>
              <Toggle
                offText='AM'
                onText='PM'
                defaultChecked={clock.pm}
                onChange={onToggleChange}
              />
            </Stack.Item>
          </Stack>
        </Labeled>
      )
    }

  capture()

  return { render }
})
