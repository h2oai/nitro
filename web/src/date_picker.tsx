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

import { DatePicker as FDatePicker } from '@fluentui/react';
import React from 'react';
import { dateToString, toDate } from './core';
import { BoxProps, make } from './ui';


export const DatePicker = make(({ box }: BoxProps) => {
  const
    { context, value } = box,
    defaultDate = toDate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date | null) => {
      console.log('in select', d)
      context.record(dateToString(d ?? defaultDate))
    },
    render = () => {
      const
        { text, placeholder, value, min, max, required } = box,
        date = toDate(value),
        minDate = toDate(min),
        maxDate = toDate(max)

      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <FDatePicker
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

  context.record(defaultValue)

  return { render }
})
