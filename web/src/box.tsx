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
import { TagPicker } from './tag_picker';
import { Textbox } from './textbox';
import { TextBlock } from './text_block';
import { TimePicker } from './time_picker';
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
    case 'tag':
      return <TagPicker context={context} box={box} />
    case 'text':
      return <Textbox context={context} box={box} />
    case 'time':
      return <TimePicker context={context} box={box} />
    default:
      return <div>Unknown item</div>
  }
}
