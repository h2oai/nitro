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
import { FileUpload } from './file_upload';
import { PluginBox } from './plugin';
import { Rating } from './rating';
import { ProgressBar } from './progress';
import { Separator } from './separator';
import { Slider } from './slider';
import { Spinbox } from './spinbox';
import { Table } from './table';
import { TagPicker } from './tag_picker';
import { Textbox } from './textbox';
import { TextBlock } from './text_block';
import { TimePicker } from './time_picker';
import { Toggle } from './toggle';
import { BoxProps } from './ui';
import { WebView } from './webview';
import { Spinner } from './spinner';

export const XBox = ({ box }: BoxProps) => { // recursive
  const { mode, options, editable, multiple } = box
  switch (mode) {
    case 'md':
      return <TextBlock box={box} />
    case 'button':
      return <Buttons box={box} />
    case 'check':
      return options.length
        ? <Checklist box={box} />
        : <Checkbox box={box} />
    case 'toggle':
      return <Toggle box={box} />
    case 'color':
      return options.length
        ? <ColorPalette box={box} />
        : <ColorPicker box={box} />
    case 'date':
      return <DatePicker box={box} />
    case 'day':
    case 'month':
    case 'week':
      return <Calendar box={box} />
    case 'file':
      return <FileUpload box={box} />
    case 'menu':
      return editable
        ? <ComboBox box={box} />
        : multiple
          ? <Droplist box={box} />
          : <Dropdown box={box} />
    case 'number':
      return <Spinbox box={box} />
    case 'radio':
      return <ChoiceGroup box={box} />
    case 'range':
      return <Slider box={box} />
    case 'rating':
      return <Rating box={box} />
    case 'progress':
      return <ProgressBar box={box} />
    case 'spinner':
      return <Spinner box={box} />
    case 'separator':
      return <Separator box={box} />
    case 'table':
      return <Table box={box} />
    case 'tag':
      return <TagPicker box={box} />
    case 'text':
      return <Textbox box={box} />
    case 'time':
      return <TimePicker box={box} />
    case 'web':
      return <WebView box={box} />

  }

  if (mode?.startsWith('plugin:')) return <PluginBox box={box} />

  return null
}
