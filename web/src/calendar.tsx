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

import { Calendar as FCalendar, DateRangeType } from '@fluentui/react';
import { dateToString, signal, toDate } from './core';
import { Labeled } from './label';
import { BoxProps, make } from './ui';

export const Calendar = make(({ context, box }: BoxProps) => {
  const
    { text, mode, value, min, max, live } = box,
    dateB = signal(toDate(value) ?? new Date()),
    minDate = toDate(min),
    maxDate = toDate(max),
    dateRangeType = mode === 'week'
      ? DateRangeType.Week
      : mode === 'month'
        ? DateRangeType.Month
        : DateRangeType.Day,
    onSelectDate = (d?: Date) => {
      const date = d ?? new Date()
      context.record(dateToString(date))
      if (live) context.commit()
      dateB(date)
    },
    render = () => {
      // TODO format string; aria-label
      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <Labeled label={text}>
          <FCalendar
            dateRangeType={dateRangeType}
            value={dateB()}
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

  context.record(dateToString(dateB()))

  return { render, dateB }
})
