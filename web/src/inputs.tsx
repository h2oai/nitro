import { Calendar, Checkbox, ChoiceGroup, ColorPicker, ComboBox, CompoundButton, DateRangeType, DefaultButton, Dropdown, DropdownMenuItemType, IButtonStyles, IChoiceGroupOption, IColorCellProps, IContextualMenuItem, IContextualMenuProps, IDropdownOption, ISliderProps, ISpinButtonStyles, IStackItemStyles, IStackTokens, ITag, ITextFieldProps, Label, MaskedTextField, Position, PrimaryButton, Rating, Slider, SpinButton, Stack, SwatchColorPicker, TagPicker, TextField, Toggle } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B, gensym, I, isN, isO, isPair, isS, isV, N, S, U, V, xid } from './core';
import { Markdown } from './markdown';
import { Input, Widget, MsgType, Option, WidgetT } from './protocol';
import { Send } from './socket';
import { make } from './ui';

const newCaptureContext = (send: Send, data: V[]) => {
  const capture = (index: I, value: V) => {
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
const toOptions = (x: any): Option[] => {
  if (!x) return []
  if (Array.isArray(x)) {
    const c: Option[] = []
    for (const v of x) {
      if (isV(v)) { // value
        c.push({ t: WidgetT.Option, label: String(v), value: v })
      } else if (isPair(v)) { // [label, value]
        const label = v[0], value = v[1]
        if (isS(label) && isV(value)) {
          c.push({ t: WidgetT.Option, label, value })
        } else {
          console.warn('Invalid choice pair. Want [string, value], got ', v)
        }
      } else if (isO(v) && isV(v.value)) { // { value: v }
        if (!v.label) v.label = String(v.value)
        if (v.options) v.options = toOptions(v.options)
        c.push(v)
      }
    }
    return c
  }
  if (isS(x)) { // 'value1 value2 value3...'
    return words(x).map(value => ({ t: WidgetT.Option, label: value, value }))
  }
  if (isO(x)) { // { label1: value1, label2: value2, ... }
    const c: Option[] = []
    for (const label in x) {
      const value = x[label]
      if (isV(value)) {
        c.push({ t: WidgetT.Option, label, value })
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
        { text: label, placeholder, icon, value, mask, prefix, suffix, error, lines, required, password } = input,
        field: Partial<ITextFieldProps> = {
          label,
          defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
          placeholder: placeholder ?? label ? undefined : 'Enter some text...',
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
      { text: label, value, min, max, step, precision } = this.props.input

    return (
      <SpinButton
        label={label}
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
      { text: label, value, min, max, step } = this.props.input,
      originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
      props: Partial<ISliderProps> = { label: label, min: unum(min), max: unum(max), step, originFromZero }

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
      { text: label, value } = this.props.input,
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
      <WithLabel label={label}>
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
      { text: label, mode, value, min, max } = this.props.input,
      date = udate(value),
      minDate = udate(min),
      maxDate = udate(max),
      dateRangeType = mode === 'week'
        ? DateRangeType.Week
        : mode === 'month'
          ? DateRangeType.Month
          : DateRangeType.Day
    return (
      <WithLabel label={label}>
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
      { text: label, value } = this.props.input
    return (
      <WithLabel label={label}>
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
      { text: label, options } = this.props.input,
      checkboxes = options.map(c => (
        <CheckboxContainer key={c.value}>
          <Checkbox label={c.label} checked={c.selected ? true : false} />
        </CheckboxContainer>
      ))

    return (
      <WithLabel label={label}><div>{checkboxes}</div></WithLabel>
    )
  }
}

class XDropdown extends React.Component<InputProps, {}> {
  render() {
    const
      { text: label, placeholder, error, required, options } = this.props.input,
      hasGroups = options.some(c => c.options?.length ? true : false),
      items: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(options) : options.map(toDropdownOption),
      selectedItem = options.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <Dropdown
        label={label}
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
      { text: label, placeholder, error, required, options } = this.props.input,
      items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.label) })),
      selectedKeys = options.filter(c => c.selected).map(c => String(c.value))

    return (

      <Dropdown
        multiSelect
        label={label}
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
      { text: label, placeholder, options } = this.props.input,
      items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.label) })),
      selectedItem = options.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <ComboBox
        allowFreeform
        label={label}
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
      { text: label, placeholder, options } = this.props.input,
      items: IDropdownOption[] = options.map(c => ({ key: c.value, text: String(c.label) })),
      selectedKeys = options.filter(c => c.selected).map(c => String(c.value))

    return (
      <ComboBox
        allowFreeform
        multiSelect
        label={label}
        placeholder={placeholder}
        options={items}
        selectedKey={selectedKeys}
      />
    )
  }
}

const toContextualMenuItem = (c: Option): IContextualMenuItem => ({
  key: String(c.value),
  text: String(c.label),
  iconProps: c.icon ? { iconName: c.icon } : undefined,
})
const toContextualMenuProps = (cs: Option[]): IContextualMenuProps => ({ items: cs.map(toContextualMenuItem) })

class XMenu extends React.Component<InputProps, {}> {
  render() {
    const
      { text: label, actions } = this.props.input
    return <PrimaryButton text={label ?? 'Choose an action'} menuProps={toContextualMenuProps(actions)} />
  }
}

const continueAction: Option = { t: WidgetT.Option, value: 'continue', label: 'Continue', selected: true }
const continueWidget: Widget = { t: WidgetT.Input, xid: xid(), index: -1 /* don't capture */, options: [], actions: [continueAction] }

const XButtons = make(({ context, input }: InputProps) => {
  const
    render = () => {
      const
        { index, inline, actions } = input,
        horizontal = inline !== false,
        styles: IButtonStyles = horizontal ? {} : { root: { width: '100%' } },
        compoundStyles: IButtonStyles = horizontal ? {} : { root: { width: '100%', maxWidth: 'auto' } },
        buttons = actions.map(c => {
          const
            text = c.label,
            onClick = () => {
              context.capture(index, c.value)
              context.submit()
            },
            button = c.selected
              ? c.options
                ? <PrimaryButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.options)} onClick={onClick} />
                : c.caption
                  ? <CompoundButton primary text={text} secondaryText={c.caption} styles={compoundStyles} onClick={onClick} />
                  : <PrimaryButton text={text} styles={styles} onClick={onClick} />
              : c.options
                ? <DefaultButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.options)} onClick={onClick} />
                : c.caption
                  ? <CompoundButton text={text} secondaryText={c.caption} styles={compoundStyles} onClick={onClick} />
                  : <DefaultButton text={text} styles={styles} onClick={onClick} />
          return <Stack.Item key={c.value}>{button}</Stack.Item>
        })
      return <Stack horizontal={horizontal} tokens={gap5}>{buttons}</Stack>
    }
  return { render }
})


const toDropdownOption = (c: Option): IDropdownOption => ({ key: c.value, text: String(c.label) })
const toGroupedDropdownOptions = (options: Option[]): IDropdownOption[] => {
  const
    items: IDropdownOption[] = [],
    sepSym = gensym('s'),
    groupSym = gensym('g')
  for (const g of options) {
    if (g.options?.length) {
      if (options.length) items.push({ key: sepSym(), text: '-', itemType: DropdownMenuItemType.Divider })
      items.push({ key: groupSym(), text: String(g.label), itemType: DropdownMenuItemType.Header })
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
    items: ITag[] = options.map(c => ({ key: c.value, name: String(c.label) })),
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
      { text: label } = this.props.input,
      { autocompleter } = this.state
    return (
      <WithLabel label={label}>
        <TagPicker onResolveSuggestions={autocompleter.suggest} getTextFromItem={autocompleter.resolve} />
      </WithLabel>
    )
  }
}

const swatchCellSize = 25
class XSwatchPicker extends React.Component<InputProps, {}> {
  render() {
    const
      { text: label, options } = this.props.input,
      cells: IColorCellProps[] = options.map(c => ({ id: String(c.value), label: String(c.label), color: String(c.value) }))

    return (
      <WithLabel label={label}>
        <SwatchColorPicker columnCount={10} colorCells={cells} cellWidth={swatchCellSize} cellHeight={swatchCellSize} />
      </WithLabel>
    )
  }
}

class XChoiceGroup extends React.Component<InputProps, {}> {
  render() {
    const
      { text: label, placeholder, required, options } = this.props.input,
      items: IChoiceGroupOption[] = options.map(({ value, label, icon: iconName }) => ({
        key: String(value),
        text: String(label),
        iconProps: iconName ? { iconName } : undefined,
      })),
      selectedItem = options.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <ChoiceGroup
        label={label}
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
  const { actions, items } = input
  if (actions.length) return true
  if (items) {
    for (const item of items) if (item.t === WidgetT.Input && inputHasActions(item)) return true
  }
  return false
}

const widgetsHaveActions = (widgets: Widget[]): B => {
  for (const widget of widgets) if (widget.t === WidgetT.Input && inputHasActions(widget)) return true
  return false
}

const XInput = ({ context, input }: InputProps) => { // recursive

  // This function contains the heuristics for determining which widget to use.
  // TODO might need a widget= to force which widget to use.

  const { options, actions, editable, multiple, items } = input

  if (items) {
    return <Stackables context={context} widgets={items} inline={input.inline} size={input.size} />
  }

  if (options.length) {
    if (multiple) {
      if (editable) {
        return <XMultiSelectComboBox context={context} input={input} />
      }
      const hasLongLabels = options.some(({ label }) => label && (label.length > 75))
      if (!hasLongLabels && options.length > 10) {
        return <XMultiSelectDropdown context={context} input={input} />
      }
      return <XCheckList context={context} input={input} />
    }
    switch (input.mode) {
      case 'tag':
        // 'multiple' implied
        return <XTagPicker context={context} input={input} />
      case 'color':
        return <XSwatchPicker context={context} input={input} />
      default:
        if (editable) {
          return <XComboBox context={context} input={input} />
        }
        const hasGroups = options.some(c => c.options?.length ? true : false)
        if (hasGroups || (options.length > 7)) {
          return <XDropdown context={context} input={input} />
        }
        return <XChoiceGroup context={context} input={input} />
    }
  }

  if (actions.length) {
    if (actions.length > 5) {
      return <XMenu context={context} input={input} />
    }
    return <XButtons context={context} input={input} />
  }

  switch (input.mode) {
    case 'rating':
      return <XRating context={context} input={input} />
    case 'day':
    case 'month':
    case 'week':
      return <XCalendar context={context} input={input} />
    case 'time':
      return <XTimePicker context={context} input={input} />
    case 'color':
      return <XColorPicker context={context} input={input} />
  }

  const
    { value, min, max, step } = input,
    hasRange = isN(min) && isN(max) && min < max

  if (isN(value) || hasRange) {
    if (!editable && hasRange) {
      const steps = (max - min) / (isN(step) ? step : 1)
      if (steps <= 16) {
        return <XSlider context={context} input={input} />
      }
    }
    return <XSpinButton context={context} input={input} />
  }
  return <XTextField context={context} input={input} />
}

const WidgetsContainer = styled.div`
  padding: 2rem;
  max-width: 640px;
`


const newIncr = () => {
  let i = 0
  return () => i++
}
type Incr = ReturnType<typeof newIncr>

const sanitizeInput = (input: Input, incr: Incr): Input => {
  const { options, actions, range, items, index } = input
  input.index = index === -1 ? index : incr()
  input.options = toOptions(options)
  input.actions = toOptions(actions)
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
  if (Array.isArray(items)) {
    input.items = items.map(w => sanitizeWidget(w, incr))
  }
  return input
}

const sanitizeWidget = (widget: Widget, incr: Incr): Widget => {
  if (isS(widget)) return { t: WidgetT.Text, xid: xid(), value: widget }
  if (widget.t === WidgetT.Input) return sanitizeInput(widget, incr)
  return widget
}
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
      <Stackables context={context} widgets={widgets} />
    </WidgetsContainer>
  )
}
