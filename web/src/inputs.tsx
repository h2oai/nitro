import { Calendar, Checkbox, ChoiceGroup, ColorPicker, ComboBox, CompoundButton, ContextualMenu, ContextualMenuItemType, DateRangeType, DefaultButton, Dropdown, DropdownMenuItemType, IButtonStyles, IChoiceGroupOption, IColorCellProps, IContextualMenuItem, IContextualMenuProps, IDropdownOption, ISliderProps, ISpinButtonStyles, IStackItemStyles, IStackTokens, ITag, ITextFieldProps, Label, MaskedTextField, optionProperties, Position, PrimaryButton, Rating, Slider, SpinButton, Stack, SwatchColorPicker, TagPicker, TextField, Toggle } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B, box, gensym, I, isN, isO, isPair, isS, isV, N, on, S, U, V, xid } from './core';
import { Markdown } from './markdown';
import { Input, Widget, MsgType, Option, WidgetT, InputMode } from './protocol';
import { Send } from './socket';
import { make } from './ui';

const newCaptureContext = (send: Send, data: V[]) => {
  const capture = (index: any, value: V) => {
    if (index >= 0) data[index] = value
  }
  const submit = () => send({ t: MsgType.Input, d: data })
  return { capture, submit }
}

type Context = ReturnType<typeof newCaptureContext>

type InputProps = { context: Context, input: Input }

const words = (x: S) => x.trim().split(/\s+/g)
const unum = (x: any): N | undefined => isN(x) ? x : undefined
const ustr = (x: any): S | undefined => isS(x) ? x : undefined
const udate = (x: any): Date | undefined => isS(x) ? new Date(x) : undefined
const snakeToCamelCase = (s: S): S => s.replace(/(_\w)/g, m => m[1].toUpperCase())
const sanitizeOptions = (x: any): Option[] => { // recursive
  if (!x) return []
  if (Array.isArray(x)) {
    const c: Option[] = []
    for (const v of x) {
      if (isV(v)) { // value
        c.push({ t: WidgetT.Option, text: String(v), value: v })
      } else if (isPair(v)) { // [value, text]
        const [value, text] = v
        if (isS(text) && isV(value)) {
          c.push({ t: WidgetT.Option, text, value })
        } else {
          console.warn('Invalid choice pair. Want [string, value], got ', v)
        }
      } else if (isO(v) && isV(v.value)) { // { value: v }
        if (!v.text) v.text = String(v.value)
        if (v.options) v.options = sanitizeOptions(v.options)
        c.push(v)
      }
    }
    return c
  }
  if (isS(x)) { // 'value1 value2 value3...'
    return words(x).map((value): Option => ({ t: WidgetT.Option, text: value, value }))
  }
  if (isO(x)) { // { text1: value1, text2: value2, ... }
    const c: Option[] = []
    for (const text in x) {
      const value = x[text]
      if (isV(value)) {
        c.push({ t: WidgetT.Option, text, value })
      } else {
        console.warn('Invalid choice value in dictionary. Want string or number, got ', value)
      }
    }
    return c
  }
  console.warn('Invalid choice list. Want string or array or dictionary, got ', x)
  return []
}

const getDefaultValue = (value: any, min: any, max: any, step: any): N | undefined => {
  if (isN(value)) return value
  if (isN(min)) return Math.max(0, min)
  if (isN(max)) return Math.min(0, max)
  if (isN(step)) return 0
  return undefined
}

const XTextField = make(({ context, input }: InputProps) => {
  const { index, value } = input
  context.capture(index, (value as any) ?? '')
  const
    onChange = ({ target }: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, v?: S) => {
      v = v ?? (target as HTMLInputElement).value ?? value ?? ''
      // TODO live?
      context.capture(index, v)
    },
    render = () => {
      const
        { text, placeholder, icon, value, mask, prefix, suffix, error, lines, required, password } = input,
        field: Partial<ITextFieldProps> = {
          label: text,
          defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
          placeholder: placeholder ?? (text ? undefined : 'Enter some text...'),
          errorMessage: error,
          required: required === true,
          onChange,
        }

      return password === true
        ? <TextField {...field} type='password' canRevealPassword revealPasswordAriaLabel='Show password' />
        : mask
          ? <MaskedTextField {...field} mask={mask} />
          : lines && (lines >= 1)
            ? <TextField {...field} multiline resizable autoAdjustHeight rows={lines} />
            : <TextField {...field} iconProps={icon ? { iconName: icon } : undefined} prefix={prefix} suffix={suffix} />
    }

  return { render }
})


class XSpinButton extends React.Component<InputProps, {}> {
  // TODO format string
  render() {
    const
      { text, value, min, max, step, precision } = this.props.input

    return (
      <SpinButton
        label={text}
        labelPosition={Position.top}
        defaultValue={isS(value) ? value : isN(value) ? String(value) : undefined}
        min={unum(min)}
        max={unum(max)}
        step={step}
        precision={precision}
        styles={{ labelWrapper: { marginBottom: -4 } }} // Make textbox top match textfield
      />
    )
  }
}

class XSlider extends React.Component<InputProps, {}> {
  // TODO format string
  render() {
    const
      { text, value, min, max, step } = this.props.input,
      originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
      props: Partial<ISliderProps> = { label: text, min: unum(min), max: unum(max), step, originFromZero }

    return Array.isArray(value) && value.length === 2 && isN(value[0]) && isN(value[1])
      ? (
        <Slider
          {...props}
          ranged
          defaultLowerValue={getDefaultValue(value[0], min, max, step)}
          defaultValue={getDefaultValue(value[1], min, max, step)}
        />
      ) : (
        <Slider
          {...props}
          defaultValue={getDefaultValue(value, min, max, step)}
        />
      )

  }
}

const WithLabel = ({ label, children }: { label?: S, children: JSX.Element }) => (
  label
    ? (
      <Stack>
        <Stack.Item>
          <Label>{label}</Label>
        </Stack.Item>
        <Stack.Item>{children}</Stack.Item>
      </Stack>
    ) : (
      children
    )
)


class XRating extends React.Component<InputProps, {}> {
  // TODO format string; aria-label
  render() {
    const
      { text: label, value, min, max } = this.props.input
    return (
      <WithLabel label={label}>
        <Rating
          defaultRating={unum(value)}
          allowZeroStars={isN(min) && min <= 0}
          max={unum(max)}
        />
      </WithLabel>
    )
  }
}


class XTimePicker extends React.Component<InputProps, {}> {
  render() {
    const
      { text, value } = this.props.input,
      t = String(value).toLowerCase(),
      am = t.endsWith('am'),
      pm = !am && t.endsWith('pm'),
      c24 = !(am || pm),
      hhmmss = c24 ? t : t.substring(0, t.length - 2),
      tokens = hhmmss.split(':'),
      [hh, mm, ss] = tokens.map(t => parseInt(t, 10)),
      hhp = !isNaN(hh),
      mmp = !isNaN(mm),
      ssp = !isNaN(ss),
      hide: IStackItemStyles = { root: { display: 'none' } },
      narrow: Partial<ISpinButtonStyles> = { labelWrapper: { marginBottom: -4 }, spinButtonWrapper: { width: 50 } }


    return (
      <WithLabel label={text}>
        <Stack horizontal horizontalAlign='start' tokens={gap5}>
          <Stack.Item styles={hhp ? undefined : hide}>
            <SpinButton label='Hours' labelPosition={Position.top} defaultValue={String(hh)} min={c24 ? 0 : 1} max={c24 ? 23 : 12} styles={narrow} />
          </Stack.Item>
          <Stack.Item styles={mmp ? undefined : hide}>
            <SpinButton label='Minutes' labelPosition={Position.top} defaultValue={String(mm)} min={0} max={59} styles={narrow} />
          </Stack.Item>
          <Stack.Item styles={ssp ? undefined : hide}>
            <SpinButton label='Seconds' labelPosition={Position.top} defaultValue={String(ss)} min={0} max={59} styles={narrow} />
          </Stack.Item>
          <Stack.Item styles={!c24 ? undefined : hide} align='end'>
            <Toggle offText='AM' onText='PM' defaultChecked={pm} />
          </Stack.Item>
        </Stack>
      </WithLabel>
    )
  }
}

class XCalendar extends React.Component<InputProps, {}> {
  // TODO format string; aria-label
  render() {
    const
      { text, mode, value, min, max } = this.props.input,
      date = udate(value),
      minDate = udate(min),
      maxDate = udate(max),
      dateRangeType = mode === 'week'
        ? DateRangeType.Week
        : mode === 'month'
          ? DateRangeType.Month
          : DateRangeType.Day
    return (
      <WithLabel label={text}>
        <Calendar
          dateRangeType={dateRangeType}
          value={date}
          minDate={minDate}
          maxDate={maxDate}
          isDayPickerVisible={mode !== 'month'}
          highlightSelectedMonth
          showGoToToday
        />
      </WithLabel>
    )
  }
}

class XColorPicker extends React.Component<InputProps, {}> {
  render() {
    const
      { text, value } = this.props.input
    return (
      <WithLabel label={text}>
        <ColorPicker color={isS(value) ? value : '#ff0000'} />
      </WithLabel>
    )
  }
}

const CheckboxContainer = styled.div`
    margin: 0.5rem 0;
  `
class XCheckList extends React.Component<InputProps, {}> {
  render() {
    const
      { text, options } = this.props.input,
      checkboxes = options.map(c => (
        <CheckboxContainer key={c.value}>
          <Checkbox label={c.text} checked={c.selected ? true : false} />
        </CheckboxContainer>
      ))

    return (
      <WithLabel label={text}><div>{checkboxes}</div></WithLabel>
    )
  }
}

class XDropdown extends React.Component<InputProps, {}> {
  render() {
    const
      { text, placeholder, error, required, options } = this.props.input,
      hasGroups = options.some(c => c.options?.length ? true : false),
      items: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(options) : options.map(toDropdownOption),
      selectedItem = options.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <Dropdown
        label={text}
        placeholder={placeholder}
        options={items}
        selectedKey={selectedKey}
        errorMessage={error}
        required={required ? true : false}
      />
    )
  }
}

class XMultiSelectDropdown extends React.Component<InputProps, {}> {
  render() {
    const
      { text, placeholder, error, required, options } = this.props.input,
      items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.text) })),
      selectedKeys = options.filter(c => c.selected).map(c => String(c.value))

    return (

      <Dropdown
        multiSelect
        label={text}
        placeholder={placeholder}
        options={items}
        defaultSelectedKeys={selectedKeys}
        errorMessage={error}
        required={required ? true : false}
      />
    )
  }
}

class XComboBox extends React.Component<InputProps, {}> {
  render() {
    const
      { text, placeholder, options } = this.props.input,
      items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.text) })),
      selectedItem = options.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <ComboBox
        allowFreeform
        label={text}
        placeholder={placeholder}
        options={items}
        selectedKey={selectedKey}
      />
    )
  }
}

class XMultiSelectComboBox extends React.Component<InputProps, {}> {
  render() {
    const
      { text, placeholder, options } = this.props.input,
      items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.text) })),
      selectedKeys = options.filter(c => c.selected).map(c => String(c.value))

    return (
      <ComboBox
        allowFreeform
        multiSelect
        label={text}
        placeholder={placeholder}
        options={items}
        selectedKey={selectedKeys}
      />
    )
  }
}

const toContextualMenuItem = (c: Option, capture: (v: V) => void): IContextualMenuItem => ({
  key: String(c.value),
  text: String(c.text),
  iconProps: c.icon ? { iconName: c.icon } : undefined,
  onClick: () => capture(c.value),
})
const toContextualMenuProps = (cs: Option[], capture: (v: V) => void): IContextualMenuProps => ({ items: cs.map(c => toContextualMenuItem(c, capture)) })

const continueAction: Option = { t: WidgetT.Option, value: 'continue', text: 'Continue', selected: true }
const continueWidget: Widget = { t: WidgetT.Input, xid: xid(), mode: 'button', index: -1 /* don't capture */, options: [continueAction] }

const XButtons = make(({ context, input }: InputProps) => {
  const
    render = () => {
      const
        { text, index, inline, options } = input,
        horizontal = inline !== false,
        styles: IButtonStyles = horizontal ? {} : { root: { width: '100%' } },
        compoundStyles: IButtonStyles = horizontal ? {} : { root: { width: '100%', maxWidth: 'auto' } },
        capture = (value: V) => {
          context.capture(index, value)
          context.submit()
        },
        buttons = options.map(c => {
          const
            text = c.text,
            onClick = () => capture(c.value),
            button = c.selected
              ? c.options
                ? c.value === ''
                  ? <PrimaryButton text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(c.options, capture)} />
                  : <PrimaryButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.options, capture)} onClick={onClick} />
                : c.caption
                  ? <CompoundButton primary text={text} secondaryText={c.caption} styles={compoundStyles} onClick={onClick} />
                  : <PrimaryButton text={text} styles={styles} onClick={onClick} />
              : c.options
                ? c.value === ''
                  ? <DefaultButton text={text ?? 'Choose an action'} menuProps={toContextualMenuProps(c.options, capture)} />
                  : <DefaultButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.options, capture)} onClick={onClick} />
                : c.caption
                  ? <CompoundButton text={text} secondaryText={c.caption} styles={compoundStyles} onClick={onClick} />
                  : <DefaultButton text={text} styles={styles} onClick={onClick} />
          return <Stack.Item key={c.value}>{button}</Stack.Item>
        })
      return (
        <WithLabel label={text}>
          <Stack horizontal={horizontal} tokens={gap5}>{buttons}</Stack>
        </WithLabel>
      )
    }
  return { render }
})


const toDropdownOption = (c: Option): IDropdownOption => ({ key: c.value, text: String(c.text) })
const toGroupedDropdownOptions = (options: Option[]): IDropdownOption[] => {
  const
    items: IDropdownOption[] = [],
    sepSym = gensym('s'),
    groupSym = gensym('g')
  for (const g of options) {
    if (g.options?.length) {
      if (options.length) items.push({ key: sepSym(), text: '-', itemType: DropdownMenuItemType.Divider })
      items.push({ key: groupSym(), text: String(g.text), itemType: DropdownMenuItemType.Header })
      for (const c of g.options) {
        items.push(toDropdownOption(c))
      }
    } else {
      items.push(toDropdownOption(g))
    }
  }
  return items
}

const createAutocompleter = (options: Option[]) => {
  const
    items: ITag[] = options.map(c => ({ key: c.value, name: String(c.text) })),
    listContainsTagList = (tag: ITag, tagList?: ITag[]) => (!tagList || !tagList.length || tagList.length === 0)
      ? false
      : tagList.some(compareTag => compareTag.key === tag.key),
    suggest = (filterText: string, tagList?: ITag[]): ITag[] =>
      filterText
        ? items.filter(
          tag => tag.name.toLowerCase().indexOf(filterText.toLowerCase()) === 0 && !listContainsTagList(tag, tagList),
        )
        : [],
    resolve = (item: ITag) => item.name

  return { resolve, suggest }
}


type TagPickerState = {
  autocompleter: ReturnType<typeof createAutocompleter>
}

class XTagPicker extends React.Component<InputProps, TagPickerState> {
  constructor(props: InputProps) {
    super(props)
    const { options } = props.input
    this.state = {
      autocompleter: createAutocompleter(options)
    }
  }
  render() {
    const
      { text } = this.props.input,
      { autocompleter } = this.state
    return (
      <WithLabel label={text}>
        <TagPicker onResolveSuggestions={autocompleter.suggest} getTextFromItem={autocompleter.resolve} />
      </WithLabel>
    )
  }
}

const swatchCellSize = 25
class XSwatchPicker extends React.Component<InputProps, {}> {
  render() {
    const
      { text, options } = this.props.input,
      cells: IColorCellProps[] = options.map(c => ({ id: String(c.value), label: String(c.text), color: String(c.value) }))

    return (
      <WithLabel label={text}>
        <SwatchColorPicker columnCount={10} colorCells={cells} cellWidth={swatchCellSize} cellHeight={swatchCellSize} />
      </WithLabel>
    )
  }
}

class XChoiceGroup extends React.Component<InputProps, {}> {
  render() {
    const
      { text, placeholder, required, options } = this.props.input,
      items: IChoiceGroupOption[] = options.map(({ value, text, icon: iconName }) => ({
        key: String(value),
        text: String(text),
        iconProps: iconName ? { iconName } : undefined,
      })),
      selectedItem = options.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <ChoiceGroup
        label={text}
        placeholder={placeholder}
        options={items}
        defaultSelectedKey={selectedKey}
        required={required ? true : false}
      />
    )
  }
}

const Stackable = ({ inline, size, children }: { inline?: B, size?: S | U, children: JSX.Element }) => {
  const
    width = inline ? size : undefined, // only process if inline
    styles = isS(width) ? { root: { width } } : undefined,
    grow = isN(width) ? width : styles ? undefined : 1 // set only if not sized
  return (
    <Stack.Item grow={grow} styles={styles} disableShrink>
      {children}
    </Stack.Item >
  )
}

const Stackables = ({ context, widgets, inline, size }: { context: Context, widgets: Widget[], inline?: B, size?: S | U }) => {
  const children = widgets.map(widget => {
    const child = (widget.t === WidgetT.Input)
      ? <XInput key={widget.xid} context={context} input={widget} />
      : (widget.t === WidgetT.Text)
        ? <Markdown key={widget.xid} text={widget.value} />
        : <div>Unknown widget</div>
    return <Stackable key={xid()} inline={inline} size={size}>{child}</Stackable>
  })

  return inline
    ? <Stack horizontal tokens={gap5}>{children}</Stack>
    : <Stack tokens={gap5}>{children}</Stack>
}

const gap5: IStackTokens = { childrenGap: 5 }

const inputHasActions = (input: Input): B => { // recursive
  const { mode, options, items } = input
  if (mode === 'button' && options.length) return true
  if (items) {
    for (const item of items) if (item.t === WidgetT.Input && inputHasActions(item)) return true
  }
  return false
}

const widgetsHaveActions = (widgets: Widget[]): B => {
  for (const widget of widgets) if (widget.t === WidgetT.Input && inputHasActions(widget)) return true
  return false
}

const determineMode = (input: Input): InputMode => {
  // This function contains the heuristics for determining which widget to use.
  const { options, editable, multiple } = input

  if (options.length) {
    if (multiple) {
      if (editable) {
        return 'menu'
      }
      const hasLongLabels = options.some(({ text }) => text && (text.length > 75))
      if (!hasLongLabels && options.length > 10) {
        return 'menu'
      }
      return 'check'
    }

    const hasGroups = options.some(c => c.options?.length ? true : false)
    if (editable) {
      return 'menu'
    }
    if (options.length <= 3) {
      return 'button'
    }
    if (options.length <= 7 && !hasGroups) {
      return 'radio'
    }
    return 'menu'
  }

  const
    { value, min, max, step } = input,
    hasRange = isN(min) && isN(max) && min < max

  if (isN(value) || hasRange) {
    if (!editable && hasRange) {
      const steps = (max - min) / (isN(step) ? step : 1)
      if (steps <= 16) {
        return 'range'
      }
    }
    return 'number'
  }
  return 'text'
}

const XInput = ({ context, input }: InputProps) => { // recursive 
  const { mode, items, options, editable, multiple } = input
  if (items) {
    return <Stackables context={context} widgets={items} inline={input.inline} size={input.size} />
  }
  switch (mode) {
    case 'button':
      return <XButtons context={context} input={input} />
    case 'check':
      return <XCheckList context={context} input={input} />
    case 'color':
      return options.length
        ? <XSwatchPicker context={context} input={input} />
        : <XColorPicker context={context} input={input} />
    case 'day':
    case 'month':
    case 'week':
      return <XCalendar context={context} input={input} />
    case 'menu':
      return editable
        ? multiple
          ? <XMultiSelectComboBox context={context} input={input} />
          : <XComboBox context={context} input={input} />
        : multiple
          ? <XMultiSelectDropdown context={context} input={input} />
          : <XDropdown context={context} input={input} />
    case 'number':
      return <XSpinButton context={context} input={input} />
    case 'radio':
      return <XChoiceGroup context={context} input={input} />
    case 'range':
      return <XSlider context={context} input={input} />
    case 'rating':
      return <XRating context={context} input={input} />
    case 'tag':
      return <XTagPicker context={context} input={input} />
    case 'text':
      return <XTextField context={context} input={input} />
    case 'time':
      return <XTimePicker context={context} input={input} />
    default:
      return <div>Unknown input</div>
  }
}

const newIncr = () => {
  let i = 0
  return () => i++
}
type Incr = ReturnType<typeof newIncr>

const sanitizeRange = (input: Input) => {
  const { range } = input
  if (Array.isArray(range)) {
    switch (range.length) {
      case 2:
        {
          const [x, y] = range
          if ((isN(x) && isN(y)) || (isS(x) && isS(y))) {
            input.min = x
            input.max = y
          }
        }
        break
      case 3:
        {
          const [x, y, z] = range
          // TODO string x, y?
          if (isN(x) && isN(y) && isN(z)) {
            input.min = x
            input.max = y
            input.step = z
          }
        }
        break
      case 4:
        {
          const [x, y, z, p] = range
          // TODO string x, y?
          if (isN(x) && isN(y) && isN(z) && isN(p)) {
            input.min = x
            input.max = y
            input.step = z
            input.precision = p
          }
        }
        break
    }
  }
}

const sanitizeInput = (input: Input, incr: Incr): Input => {
  const { mode, options, items } = input
  input.index ??= incr()
  input.options = sanitizeOptions(options)

  sanitizeRange(input)

  if (Array.isArray(items)) {
    input.items = items.map(w => sanitizeWidget(w, incr))
  }

  if (!mode) input.mode = determineMode(input)

  return input
}

const sanitizeWidget = (widget: Widget, incr: Incr): Widget => {
  if (isS(widget)) return { t: WidgetT.Text, xid: xid(), value: widget }
  if (widget.t === WidgetT.Input) return sanitizeInput(widget, incr)
  return widget
}

const Logo = ({ size }: { size: U }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width={size} height={size} focusable="false">
    <path d="M2048 0v64q0 182-32 340t-99 299-166 268-234 249l-191 572h-302v-227q-138 81-279 156l-418-418q75-141 156-279H256V722l572-190q121-135 248-235t269-166 299-98 340-33h64zM558 896q29-46 58-91t62-89l-294 98v82h174zm211 666q51-29 102-57t102-58l-372-372q-29 51-57 102t-58 103l283 282zm563-192q-44 32-89 61t-91 59v174h82l98-294zm183-327q99-99 172-201t124-214 76-235 32-264q-140 5-263 31t-235 77-215 123-203 172q-99 97-181 204T668 962l418 418q118-72 225-154t204-183zm-235-19q-53 0-99-20t-82-55-55-81-20-100q0-53 20-99t55-82 81-55 100-20q53 0 99 20t82 55 55 81 20 100q0 53-20 99t-55 82-81 55-100 20zm0-384q-27 0-50 10t-40 27-28 41-10 50q0 27 10 50t27 40 41 28 50 10q27 0 50-10t40-27 28-41 10-50q0-27-10-50t-27-40-41-28-50-10zM256 1536q53 0 99 20t82 55 55 81 20 100q0 53-20 99t-55 82-81 55-100 20H0v-256q0-53 20-99t55-82 81-55 100-20zm0 384q27 0 50-10t40-27 28-41 10-50q0-27-10-50t-27-40-41-28-50-10q-27 0-50 10t-40 27-28 41-10 50v128h128z" />
  </svg>
)

const NavIcon = ({ size }: { size: U }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width={size} height={size} focusable="false">
    <path d="M2048 640H0V512h2048v128zm0 1024H0v-128h2048v128zm0-513H0v-127h2048v127z" />
  </svg>
)

const NavActiveIcon = ({ size }: { size: U }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width={size} height={size} focusable="false">
    <path d="M1728 1024q-66 0-124-25t-102-68-69-102-25-125q0-66 25-124t68-102 102-69 125-25q66 0 124 25t102 68 69 102 25 125q0 66-25 124t-68 102-102 69-125 25zm-474-512q-12 31-19 63t-13 65H0V512h1254zm78 512q65 80 153 128H0v-128h1332zM0 1664v-128h2048v128H0z" />
  </svg>
)

const NavContainer = styled.div`
  cursor: pointer;
  width: 20px;
  height: 20px;
`
const XNav = make(() => {
  const
    containerRef = React.createRef<HTMLDivElement>(),
    showMenuB = box(false),
    showMenu = () => showMenuB(true),
    hideMenu = () => showMenuB(false),
    render = () => {
      const isMenuVisible = showMenuB()
      return (
        <NavContainer ref={containerRef} onClick={showMenu}>
          {isMenuVisible ? <NavActiveIcon size={20} /> : <NavIcon size={20} />}
          <ContextualMenu
            items={menuItems}
            hidden={!isMenuVisible}
            target={containerRef}
            onItemClick={hideMenu}
            onDismiss={hideMenu}
          />
        </NavContainer>
      )
    }
  return { render, showMenuB }
})
const WidgetsContainer = styled.div`
  max-width: 640px;
  background-color: #fff;
  margin: 1rem auto 2rem;
`
const Header = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
`
const HeaderTitle = styled.div` 
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1rem;
  color: #555;
  margin-left: 1rem;
`
const HeaderSubtitle = styled.div`
  font-weight: 400;
  color: #999;
  margin-left: 0.5rem;
`
const Body = styled.div`
  padding: 1rem 2rem 2rem;
`
const menuItems: IContextualMenuItem[] = [
  { key: 'newItem', iconProps: { iconName: 'Add' }, text: 'New' },
  {
    key: 'upload',
    iconProps: { iconName: 'Upload', style: { color: 'salmon' } },
    text: 'Upload',
    title: 'Upload a file',
  },
  { key: 'divider_1', itemType: ContextualMenuItemType.Divider },
  { key: 'share', iconProps: { iconName: 'Share' }, text: 'Share' },
  { key: 'print', iconProps: { iconName: 'Print' }, text: 'Print' },
  { key: 'music', iconProps: { iconName: 'MusicInCollectionFill' }, text: 'Music' },
  {
    key: 'newItem2',
    text: 'New',
    onClick: () => console.log('New clicked'),
  },
  {
    key: 'divider_2',
    itemType: ContextualMenuItemType.Divider,
  },
  {
    key: 'rename',
    text: 'Rename',
    onClick: () => console.log('Rename clicked'),
  },
  {
    key: 'edit',
    text: 'Edit',
    onClick: () => console.log('Edit clicked'),
  },
  {
    key: 'properties',
    text: 'Properties',
    onClick: () => console.log('Properties clicked'),
  },
  {
    key: 'linkNoTarget',
    text: 'Link same window',
    href: 'http://bing.com',
  },
  {
    key: 'linkWithTarget',
    text: 'Link new window',
    href: 'http://bing.com',
    target: '_blank',
  },
  {
    key: 'linkWithOnClick',
    name: 'Link click',
    href: 'http://bing.com',
    onClick: (ev) => {
      alert('Link clicked')
      if (ev) ev.preventDefault()
    },
    target: '_blank',
  },
  {
    key: 'disabled',
    text: 'Disabled item',
    disabled: true,
    onClick: () => console.error('Disabled item should not be clickable.'),
  },
]
export const XWidgets = (props: { send: Send, widgets: Widget[] }) => {
  // console.log(JSON.stringify(props.widgets))
  const
    next = newIncr(),
    sanitizedWidgets = props.widgets.map(w => sanitizeWidget(w, next)),
    hasActions = widgetsHaveActions(sanitizedWidgets),
    widgets: Widget[] = hasActions ? sanitizedWidgets : [...sanitizedWidgets, continueWidget],
    context = newCaptureContext(props.send, [])
  // console.log(JSON.stringify(widgets))
  return (
    <WidgetsContainer>
      <Header>
        <XNav />
        <HeaderTitle>Nitro App</HeaderTitle>
        <HeaderSubtitle>v1.0</HeaderSubtitle>
      </Header>
      <Body>
        <Stackables context={context} widgets={widgets} />
      </Body>
    </WidgetsContainer>
  )
}
