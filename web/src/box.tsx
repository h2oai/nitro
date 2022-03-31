import React from 'react';
import { XButtons } from './buttons';
import { XCalendar } from './calendar';
import { XCheckList } from './checklist';
import { XChoiceGroup } from './choice_group';
import { XColorPalette } from './color_palette';
import { XColorPicker } from './color_picker';
import { XComboBox } from './combobox';
import { XDatePicker } from './date_picker';
import { XDropdown } from './dropdown';
import { XDroplist } from './droplist';
import { XRating } from './rating';
import { XSlider } from './slider';
import { XSpinbox } from './spinbox';
import { XTagPicker } from './tag_picker';
import { XTextbox } from './textbox';
import { XTextBlock } from './text_block';
import { XTimePicker } from './time_picker';
import { BoxProps } from './ui';

export const XBox = ({ context, box }: BoxProps) => { // recursive 
  const { mode, options, editable, multiple } = box
  switch (mode) {
    case 'md':
      return <XTextBlock context={context} box={box} />
    case 'button':
      return <XButtons context={context} box={box} />
    case 'check':
      return <XCheckList context={context} box={box} />
    case 'color':
      return options.length
        ? <XColorPalette context={context} box={box} />
        : <XColorPicker context={context} box={box} />
    case 'date':
      return <XDatePicker context={context} box={box} />
    case 'day':
    case 'month':
    case 'week':
      return <XCalendar context={context} box={box} />
    case 'menu':
      return editable
        ? <XComboBox context={context} box={box} />
        : multiple
          ? <XDroplist context={context} box={box} />
          : <XDropdown context={context} box={box} />
    case 'number':
      return <XSpinbox context={context} box={box} />
    case 'radio':
      return <XChoiceGroup context={context} box={box} />
    case 'range':
      return <XSlider context={context} box={box} />
    case 'rating':
      return <XRating context={context} box={box} />
    case 'tag':
      return <XTagPicker context={context} box={box} />
    case 'text':
      return <XTextbox context={context} box={box} />
    case 'time':
      return <XTimePicker context={context} box={box} />
    default:
      return <div>Unknown item</div>
  }
}
