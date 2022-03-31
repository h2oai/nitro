import { Calendar as FCalendar, DateRangeType } from '@fluentui/react';
import React from 'react';
import { dateToString, toDate } from './core';
import { Labeled } from './label';
import { BoxProps, make } from './ui';

export const Calendar = make(({ context, box }: BoxProps) => {
  const
    { index, value } = box,
    defaultDate = toDate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date) => {
      context.capture(index, dateToString(d ?? new Date()))
    },
    render = () => {
      // TODO format string; aria-label
      const
        { text, mode, value, min, max } = box,
        date = toDate(value),
        minDate = toDate(min),
        maxDate = toDate(max),
        dateRangeType = mode === 'week'
          ? DateRangeType.Week
          : mode === 'month'
            ? DateRangeType.Month
            : DateRangeType.Day
      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <Labeled label={text}>
          <FCalendar
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
