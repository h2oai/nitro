import { Calendar, DateRangeType } from '@fluentui/react';
import React from 'react';
import { dateToString, udate } from './core';
import { Labeled } from './label';
import { BoxProps, make } from './ui';

export const XCalendar = make(({ context, box }: BoxProps) => {
  const
    { index, value } = box,
    defaultDate = udate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date) => {
      context.capture(index, dateToString(d ?? new Date()))
    },
    render = () => {
      // TODO format string; aria-label
      const
        { text, mode, value, min, max } = box,
        date = udate(value),
        minDate = udate(min),
        maxDate = udate(max),
        dateRangeType = mode === 'week'
          ? DateRangeType.Week
          : mode === 'month'
            ? DateRangeType.Month
            : DateRangeType.Day
      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <Labeled label={text}>
          <Calendar
            dateRangeType={dateRangeType}
            value={date}
            minDate={minDate}
            maxDate={maxDate}
            isDayPickerVisible={mode !== 'month'}
            onSelectDate={onSelectDate}
            highlightSelectedMonth
            showGoToToday
          />
        </Labeled>
      )
    }

  context.capture(index, defaultValue)

  return { render }
})
