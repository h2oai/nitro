import { DatePicker } from '@fluentui/react';
import React from 'react';
import { dateToString, udate } from './core';
import { BoxProps, make } from './ui';


export const XDatePicker = make(({ context, box }: BoxProps) => {
  const
    { index, value } = box,
    defaultDate = udate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date | null) => {
      console.log('in select', d)
      context.capture(index, dateToString(d ?? defaultDate))
    },
    render = () => {
      const
        { text, placeholder, value, min, max, required } = box,
        date = udate(value),
        minDate = udate(min),
        maxDate = udate(max)

      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <DatePicker
          label={text}
          value={date}
          minDate={minDate}
          maxDate={maxDate}
          placeholder={placeholder}
          onSelectDate={onSelectDate}
          isRequired={required}
          highlightSelectedMonth
          showGoToToday
        />
      )
    }

  context.capture(index, defaultValue)

  return { render }
})
