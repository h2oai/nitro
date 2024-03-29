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
import { dateToString, toDate } from './core';
import { css } from './css';
import { BoxProps, make } from './ui';

export const DatePicker = make(({ context, box }: BoxProps) => {
  const
    { name, modes, text, placeholder, value, min, max, style, disabled } = box,
    required = modes.has('required'),
    live = modes.has('live'),
    defaultDate = toDate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    minDate = toDate(min),
    maxDate = toDate(max),
    onSelectDate = (d?: Date | null) => {
      context.record(dateToString(d ?? defaultDate))
      if (live) context.commit()
    },
    render = () => {
      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <div className={css(style)} data-name={name}>
          <FDatePicker
            label={text}
            value={defaultDate}
            minDate={minDate}
            maxDate={maxDate}
            placeholder={placeholder}
            onSelectDate={onSelectDate}
            isRequired={required}
            highlightSelectedMonth
            showGoToToday
            disabled={disabled === true}
          />
        </div>
      )
    }

  context.record(defaultValue)

  return { render }
})
