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

import { Banner } from './banner';
import { Buttons } from './buttons';
import { Calendar } from './calendar';
import { Checkbox } from './checkbox';
import { Checklist } from './checklist';
import { ChoiceGroup } from './choice_group';
import { clicker } from './client';
import { ColorPalette } from './color_palette';
import { ColorPicker } from './color_picker';
import { ComboBox } from './combobox';
import { css } from './css';
import { DatePicker } from './date_picker';
import { Dropdown } from './dropdown';
import { Droplist } from './droplist';
import { FileUpload } from './file_upload';
import { PluginBox } from './plugin';
import { ProgressBar } from './progress';
import { Rating } from './rating';
import { Separator } from './separator';
import { Slider } from './slider';
import { Spinbox } from './spinbox';
import { Spinner } from './spinner';
import { SVGBox } from './svg';
import { Table } from './table';
import { TagPicker } from './tag_picker';
import { Textbox } from './textbox';
import { TextBlock } from './text_block';
import { TimePicker } from './time_picker';
import { Toggle } from './toggle';
import { BoxProps } from './ui';
import { WebView } from './webview';

export const XBox = ({ context, box }: BoxProps) => { // recursive
  const
    { modes, options } = box,
    editable = modes.has('editable'),
    multiple = modes.has('multi')
  if (modes.has('md')) {
    return <TextBlock context={context} box={box} />
  } else if (modes.has('button')) {
    return <Buttons context={context} box={box} />
  } else if (modes.has('check')) {
    return options.length
      ? <Checklist context={context} box={box} />
      : <Checkbox context={context} box={box} />
  } else if (modes.has('toggle')) {
    return <Toggle context={context} box={box} />
  } else if (modes.has('color')) {
    return options.length
      ? <ColorPalette context={context} box={box} />
      : <ColorPicker context={context} box={box} />
  } else if (modes.has('date')) {
    return <DatePicker context={context} box={box} />
  } else if (modes.has('day') || modes.has('month') || modes.has('week')) {
    return <Calendar context={context} box={box} />
  } else if (modes.has('file')) {
    return <FileUpload context={context} box={box} />
  } else if (modes.has('menu')) {
    return editable
      ? <ComboBox context={context} box={box} />
      : multiple
        ? <Droplist context={context} box={box} />
        : <Dropdown context={context} box={box} />
  } else if (modes.has('number')) {
    return <Spinbox context={context} box={box} />
  } else if (modes.has('radio')) {
    return <ChoiceGroup context={context} box={box} />
  } else if (modes.has('range')) {
    return <Slider context={context} box={box} />
  } else if (modes.has('rating')) {
    return <Rating context={context} box={box} />
  } else if (modes.has('progress')) {
    return <ProgressBar context={context} box={box} />
  } else if (modes.has('separator')) {
    return <Separator context={context} box={box} />
  } else if (modes.has('spinner')) {
    return <Spinner context={context} box={box} />
  } else if (modes.has('svg')) {
    return <SVGBox context={context} box={box} />
  } else if (modes.has('info') || modes.has('success') || modes.has('warning') || modes.has('critical') || modes.has('blocked') || modes.has('error')) {
    return <Banner context={context} box={box} />
  } else if (modes.has('table')) {
    return <Table context={context} box={box} />
  } else if (modes.has('tag')) {
    return <TagPicker context={context} box={box} />
  } else if (modes.has('text') || modes.has('password')) {
    return <Textbox context={context} box={box} />
  } else if (modes.has('time')) {
    return <TimePicker context={context} box={box} />
  } else if (modes.has('web')) {
    return <WebView context={context} box={box} />
  }

  for (const mode of modes) {
    const i = mode.indexOf(':')
    if (i >= 0) {
      const type = mode.substring(0, i), name = mode.substring(i + 1)
      if (type === 'plugin') return <PluginBox context={context} box={box} name={name} />
    }
  }

  const onClick = box.path ? clicker(box.path) : undefined
  const className = box.path ? css('cursor-pointer', box.style) : css(box.style)
  return <div className={className} onClick={onClick}>{box.text ?? ''}</div>
}
