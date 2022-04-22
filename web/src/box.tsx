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

import React from 'react';
import { Buttons } from './buttons';
import { Calendar } from './calendar';
import { Checkbox } from './checkbox';
import { Checklist } from './checklist';
import { ChoiceGroup } from './choice_group';
import { ColorPalette } from './color_palette';
import { ColorPicker } from './color_picker';
import { ComboBox } from './combobox';
import { DatePicker } from './date_picker';
import { Dropdown } from './dropdown';
import { Droplist } from './droplist';
import { Rating } from './rating';
import { Slider } from './slider';
import { Spinbox } from './spinbox';
import { Table } from './table';
import { TagPicker } from './tag_picker';
import { Textbox } from './textbox';
import { TextBlock } from './text_block';
import { TimePicker } from './time_picker';
import { Toggle } from './toggle';
import { BoxProps } from './ui';

export const XBox = ({ context, box }: BoxProps) => { // recursive 
  const { mode, options, editable, multiple } = box
  switch (mode) {
    case 'md':
      return <TextBlock context={context} box={box} />
    case 'button':
      return <Buttons context={context} box={box} />
    case 'check':
      return options.length
        ? <Checklist context={context} box={box} />
        : <Checkbox context={context} box={box} />
    case 'toggle':
      return <Toggle context={context} box={box} />
    case 'color':
      return options.length
        ? <ColorPalette context={context} box={box} />
        : <ColorPicker context={context} box={box} />
    case 'date':
      return <DatePicker context={context} box={box} />
    case 'day':
    case 'month':
    case 'week':
      return <Calendar context={context} box={box} />
    case 'menu':
      return editable
        ? <ComboBox context={context} box={box} />
        : multiple
          ? <Droplist context={context} box={box} />
          : <Dropdown context={context} box={box} />
    case 'number':
      return <Spinbox context={context} box={box} />
    case 'radio':
      return <ChoiceGroup context={context} box={box} />
    case 'range':
      return <Slider context={context} box={box} />
    case 'rating':
      return <Rating context={context} box={box} />
    case 'table':
      return <Table context={context} box={box} />
    case 'tag':
      return <TagPicker context={context} box={box} />
    case 'text':
      return <Textbox context={context} box={box} />
    case 'time':
      return <TimePicker context={context} box={box} />
  }
  return null
}
