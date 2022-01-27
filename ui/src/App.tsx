import { Calendar, Checkbox, ChoiceGroup, ColorPicker, ComboBox, CompoundButton, DateRangeType, DefaultButton, Dropdown, DropdownMenuItemType, IButtonStyles, IChoiceGroupOption, IColorCellProps, IContextualMenuItem, IContextualMenuProps, IDropdownOption, ISliderProps, ISpinButtonStyles, IStackItemStyles, IStackTokens, ITag, ITextFieldProps, Label, MaskedTextField, Persona, PersonaPresence, PersonaSize, Position, PrimaryButton, Rating, Slider, SpinButton, Stack, SwatchColorPicker, TagPicker, TextField, Toggle } from '@fluentui/react';
import { micromark, Options as MicromarkOptions } from 'micromark';
import { gfmAutolinkLiteral, gfmAutolinkLiteralHtml } from 'micromark-extension-gfm-autolink-literal'
import { gfmStrikethrough, gfmStrikethroughHtml } from 'micromark-extension-gfm-strikethrough';
import React from 'react';
import styled from 'styled-components';
import './App.css';

type B = boolean
type S = string
type N = number
type U = N
type I = N
type F = N
type V = S | I | F
type Dict<T> = { [key: string]: T }
type Pair<T> = [T, T]

type InputBase = {
  label?: S
  mode?: 'text' | 'int' | 'float' | 'time' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating'
  icon?: S
  value?: V | Pair<V>
  min?: N | S
  max?: N | S
  step?: N
  precision?: U
  mask?: S
  prefix?: S
  suffix?: S
  // format?: S // TODO: displayed-value format string for spinbutton, slider
  placeholder?: S
  error?: S
  lines?: U
  size?: S | U
  multiple?: B
  required?: B
  password?: B
  editable?: B
  inline?: B

}

type Choice = {
  value: V
  label?: S
  icon?: S
  caption?: S
  selected?: B
  choices?: Choice[]
}

type Input = InputBase & {
  choices: Choice[]
  actions: Choice[]
  inputs?: Input[]
}

type InputMessage = Input & {
  t: 'i'
  id: S
}

type RawChoice = V | Pair<V>
type RawChoices = S | RawChoice[] | Dict<V> | Choice[]

type RawInput = InputBase & {
  choices?: RawChoices
  actions?: RawChoices
  inputs?: RawInput[]
  range?: Pair<V>
}

type Output = {
  author: S
  text?: S
}

type OutputMessage = Output & {
  t: 'o'
  id: S
}

type SessionMessage = {
  t: 's'
  outputs: OutputMessage[]
  input?: InputMessage
}

export type Message = InputMessage | OutputMessage | SessionMessage

const
  gap5: IStackTokens = { childrenGap: 5 }

const
  isN = (x: any): x is number => typeof x === 'number',
  isS = (x: any): x is string => typeof x === 'string',
  unum = (x: any): N | undefined => isN(x) ? x : undefined,
  ustr = (x: any): S | undefined => isS(x) ? x : undefined,
  udate = (x: any): Date | undefined => isS(x) ? new Date(x) : undefined,
  isV = (x: any): x is S | N => isS(x) || isN(x),
  isO = (x: any) => x && (typeof x === 'object'),
  isPair = (x: any): x is any[] => Array.isArray(x) && x.length === 2,
  words = (x: S) => x.trim().split(/\s+/g),
  toChoices = (x: any): Choice[] => {
    if (!x) return []
    if (Array.isArray(x)) {
      const c: Choice[] = []
      for (const v of x) {
        if (isV(v)) { // value
          c.push({ label: String(v), value: v })
        } else if (isPair(v)) { // [label, value]
          const label = v[0], value = v[1]
          if (isS(label) && isV(value)) {
            c.push({ label, value })
          } else {
            console.warn('Invalid choice pair. Want [string, value], got ', v)
          }
        } else if (isO(v) && isV(v.value)) { // { value: v }
          if (!v.label) v.label = String(v.value)
          if (v.choices) v.choices = toChoices(v.choices)
          c.push(v)
        }
      }
      return c
    }
    if (isS(x)) { // 'value1 value2 value3...'
      return words(x).map(value => ({ label: value, value }))
    }
    if (isO(x)) { // { label1: value1, label2: value2, ... }
      const c: Choice[] = []
      for (const label in x) {
        const value = x[label]
        if (isV(value)) {
          c.push({ label, value })
        } else {
          console.warn('Invalid choice value in dictionary. Want string or number, got ', value)
        }
      }
      return c
    }
    console.warn('Invalid choice list. Want string or array or dictionary, got ', x)
    return []
  }


type InputProps = { input: Input }

const
  WithOffset = ({ offset, children }: { offset?: any, children: JSX.Element }) =>
    (offset ?? true) ? (
      <div>
        <div><Label>&nbsp;</Label></div>
        <div>{children}</div>
      </div>
    ) : children


const
  WithSend = ({ offset, children }: { offset?: any, children: JSX.Element }) => (
    <Stack horizontal tokens={gap5} >
      <Stack.Item grow>{children}</Stack.Item>
      <Stack.Item>
        <WithOffset offset={offset}>
          <PrimaryButton iconProps={{ iconName: 'Send' }} />
        </WithOffset>
      </Stack.Item>
    </ Stack>
  )


const Markdown = styled.div`
/* Don't add margins before/after first/last paragraph */
&>p:first-child {
  margin-top: 0;
}
&>p:last-child {
  margin-bottom: 0;
}
&>p:only-child {
  margin: 0;
}
/* Don't indent lists */
&>ul, &>ol {
  padding-left: 1rem;
}
`

const
  micromarkOpts: MicromarkOptions = {
    extensions: [gfmStrikethrough(), gfmAutolinkLiteral],
    htmlExtensions: [gfmStrikethroughHtml, gfmAutolinkLiteralHtml]
  }

class XMarkdown extends React.Component<{ text: S }, {}> {
  render() {
    const
      { text } = this.props,
      html = micromark(text, micromarkOpts)

    return <Markdown dangerouslySetInnerHTML={{ __html: html }}></Markdown>
  }
}

class XTextField extends React.Component<InputProps, {}> {
  render() {
    const
      { label, placeholder, icon, value, mask, prefix, suffix, error, lines, required, password } = this.props.input,
      props: Partial<ITextFieldProps> = {
        label,
        defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
        placeholder: placeholder ?? label ? undefined : 'Message...',
        errorMessage: error,
        required: required === true
      }

    return password === true
      ? <TextField {...props} type='password' canRevealPassword revealPasswordAriaLabel='Show password' />
      : mask
        ? <MaskedTextField {...props} mask={mask} />
        : lines && (lines >= 1)
          ? <TextField {...props} multiline resizable autoAdjustHeight rows={lines} />
          : <TextField {...props} iconProps={icon ? { iconName: icon } : undefined} prefix={prefix} suffix={suffix} />
  }
}

class XSpinButton extends React.Component<InputProps, {}> {
  // TODO format string
  render() {
    const
      { label, value, min, max, step, precision } = this.props.input

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
      { label, value, min, max, step } = this.props.input,
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

const
  WithLabel = ({ label, children }: { label?: S, children: JSX.Element }) => (
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
      { label, value, min, max } = this.props.input
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
      { label, value } = this.props.input,
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
            <WithOffset>
              <Toggle offText='AM' onText='PM' defaultChecked={pm} />
            </WithOffset>
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
      { label, mode, value, min, max } = this.props.input,
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
      { label, value } = this.props.input
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
      { label, choices } = this.props.input,
      checkboxes = choices.map(c => (
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
      { label, placeholder, error, required, choices } = this.props.input,
      hasGroups = choices.some(c => c.choices?.length ? true : false),
      options: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(choices) : choices.map(toDropdownOption),
      selectedItem = choices.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <Dropdown
        label={label}
        placeholder={placeholder}
        options={options}
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
      { label, placeholder, error, required, choices } = this.props.input,
      options: IDropdownOption[] = choices.map(c => ({ key: c.value, text: String(c.label) })),
      selectedKeys = choices.filter(c => c.selected).map(c => String(c.value))

    return (

      <Dropdown
        multiSelect
        label={label}
        placeholder={placeholder}
        options={options}
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
      { label, placeholder, choices } = this.props.input,
      options: IDropdownOption[] = choices.map(c => ({ key: c.value, text: String(c.label) })),
      selectedItem = choices.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <ComboBox
        allowFreeform
        label={label}
        placeholder={placeholder}
        options={options}
        selectedKey={selectedKey}
      />
    )
  }
}

class XMultiSelectComboBox extends React.Component<InputProps, {}> {
  render() {
    const
      { label, placeholder, choices } = this.props.input,
      options: IDropdownOption[] = choices.map(c => ({ key: c.value, text: String(c.label) })),
      selectedKeys = choices.filter(c => c.selected).map(c => String(c.value))

    return (
      <ComboBox
        allowFreeform
        multiSelect
        label={label}
        placeholder={placeholder}
        options={options}
        selectedKey={selectedKeys}
      />
    )
  }
}

const
  toContextualMenuItem = (c: Choice): IContextualMenuItem => ({
    key: String(c.value),
    text: String(c.label),
    iconProps: c.icon ? { iconName: c.icon } : undefined,
  }),
  toContextualMenuProps = (cs: Choice[]): IContextualMenuProps => ({ items: cs.map(toContextualMenuItem) })

class XMenu extends React.Component<InputProps, {}> {
  render() {
    const
      { label, actions } = this.props.input
    return <PrimaryButton text={label ?? 'Choose an action'} menuProps={toContextualMenuProps(actions)} />
  }
}

class XButtons extends React.Component<InputProps, {}> {
  render() {
    const
      { inline, actions } = this.props.input,
      horizontal = inline ? true : false,
      styles: IButtonStyles = { root: { width: '100%' } },
      compoundStyles: IButtonStyles = { root: { width: '100%', maxWidth: 'auto' } },
      buttons = actions.map(c => {
        const
          text = c.label,
          button = c.selected
            ? c.choices
              ? <PrimaryButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.choices)} />
              : c.caption
                ? <CompoundButton primary text={text} secondaryText={c.caption} styles={compoundStyles} />
                : <PrimaryButton text={text} styles={styles} />
            : c.choices
              ? <DefaultButton split text={text} styles={styles} menuProps={toContextualMenuProps(c.choices)} />
              : c.caption
                ? <CompoundButton text={text} secondaryText={c.caption} styles={compoundStyles} />
                : <DefaultButton text={text} styles={styles} />
        return <Stack.Item key={c.value}>{button}</Stack.Item>
      })
    return <WithOffset><Stack horizontal={horizontal} tokens={gap5}>{buttons}</Stack></WithOffset>

  }
}

const
  gensym = (prefix: S) => {
    let k = 0
    return () => `__sidekick__${prefix}${++k}`
  },
  toDropdownOption = (c: Choice): IDropdownOption => ({ key: c.value, text: String(c.label) }),
  toGroupedDropdownOptions = (choices: Choice[]): IDropdownOption[] => {
    const
      options: IDropdownOption[] = [],
      sepSym = gensym('s'),
      groupSym = gensym('g')
    for (const g of choices) {
      if (g.choices?.length) {
        if (options.length) options.push({ key: sepSym(), text: '-', itemType: DropdownMenuItemType.Divider })
        options.push({ key: groupSym(), text: String(g.label), itemType: DropdownMenuItemType.Header })
        for (const c of g.choices) {
          options.push(toDropdownOption(c))
        }
      } else {
        options.push(toDropdownOption(g))
      }
    }
    return options
  }

const
  createAutocompleter = (choices: Choice[]) => {
    const
      items: ITag[] = choices.map(c => ({ key: c.value, name: String(c.label) })),
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
    const { choices } = props.input
    this.state = {
      autocompleter: createAutocompleter(choices)
    }
  }
  render() {
    const
      { label } = this.props.input,
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
      { label, choices } = this.props.input,
      cells: IColorCellProps[] = choices.map(c => ({ id: String(c.value), label: String(c.label), color: String(c.value) }))

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
      { label, placeholder, required, choices } = this.props.input,
      options: IChoiceGroupOption[] = choices.map(({ value, label, icon: iconName }) => ({
        key: String(value),
        text: String(label),
        iconProps: iconName ? { iconName } : undefined,
      })),
      selectedItem = choices.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <ChoiceGroup
        label={label}
        placeholder={placeholder}
        options={options}
        defaultSelectedKey={selectedKey}
        required={required ? true : false}
      />
    )
  }
}

type FormProps = {
  inputs: Input[]
  inline: B
}

const
  inputHasActions = (input: Input): B => { // recursive
    const { actions, inputs } = input
    if (actions.length) return true
    if (inputs) for (const child of inputs) if (inputHasActions(child)) return true
    return false
  },
  inputHasLabel = (input: Input): B => {
    const { label, inputs } = input
    if (label) return true
    if (inputs && inputs.length && inputHasLabel(inputs[0])) return true
    return false
  },
  XInput = ({ input }: InputProps) => { // recursive

    // This function contains the heuristics for determining which widget to use.
    // TODO might need a widget= to force which widget to use.

    const { choices, actions, editable, multiple, inputs, inline } = input

    if (inputs) {

      const children = inputs.map(input => {
        const
          size = inline ? input.size : undefined, // only process if inline
          styles = isS(size) ? { root: { width: size } } : undefined,
          grow = isN(size) ? size : styles ? undefined : 1 // set only if not sized

        return (
          <Stack.Item key={xid()} grow={grow} styles={styles} disableShrink>
            <XInput input={input} />
          </Stack.Item >
        )
      })

      return inline
        ? <Stack horizontal tokens={gap5}>{children}</Stack>
        : <Stack tokens={gap5}>{children}</Stack>
    }

    if (choices.length) {
      if (multiple) {
        if (editable) {
          return <XMultiSelectComboBox input={input} />
        }
        const hasLongLabels = choices.some(({ label }) => label && (label.length > 75))
        if (!hasLongLabels && choices.length > 10) {
          return <XMultiSelectDropdown input={input} />
        }
        return <XCheckList input={input} />
      }
      switch (input.mode) {
        case 'tag':
          // 'multiple' implied
          return <XTagPicker input={input} />
        case 'color':
          return <XSwatchPicker input={input} />
        default:
          if (editable) {
            return <XComboBox input={input} />
          }
          const hasGroups = choices.some(c => c.choices?.length ? true : false)
          if (hasGroups || (choices.length > 7)) {
            return <XDropdown input={input} />
          }
          return <XChoiceGroup input={input} />
      }
    }

    if (actions.length) {
      if (actions.length > 5) {
        return <XMenu input={input} />
      }
      return <XButtons input={input} />
    }

    switch (input.mode) {
      case 'rating':
        return <XRating input={input} />
      case 'day':
      case 'month':
      case 'week':
        return <XCalendar input={input} />
      case 'time':
        return <XTimePicker input={input} />
      case 'color':
        return <XColorPicker input={input} />
    }

    const
      { value, min, max, step } = input,
      hasRange = isN(min) && isN(max) && min < max

    if (isN(value) || hasRange) {
      if (!editable && hasRange) {
        const steps = (max - min) / (isN(step) ? step : 1)
        if (steps <= 16) {
          return <XSlider input={input} />
        }
      }
      return <XSpinButton input={input} />
    }
    return <XTextField input={input} />
  }


class InputView extends React.Component<InputProps, {}> {
  render() {
    const
      { input } = this.props,
      hasActions = inputHasActions(input),
      hasLabel = inputHasLabel(input),
      form = <XInput input={input}></XInput>,
      body = hasActions ? form : <WithSend offset={hasLabel}>{form}</WithSend>
    return <InputContainer>{body}</InputContainer>
  }
}



let _xid = 0

const
  fruits = words(`
    Apples Bananas Cherries Dates Elderberries Figs Grapes Huckleberries Jujubes Kiwis Lychees Mangos 
    Nectarines Oranges Peaches Quince Raspberries Strawberries Tangerines Watermelons
  `),
  lorem = `
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
  `.split(/\W+/g).filter(x => x.length > 0).map(x => x.toLowerCase()),
  toss = () => Math.random() > 0.5,
  range = (n: U) => {
    const xs = new Array<U>(n)
    for (let i = 0; i < n; i++) xs[i] = i
    return xs
  },
  rand = (min: I, max: I) => Math.floor(Math.random() * (max - min) + min),
  sentenceCase = (s: S) => s.length ? s[0].toUpperCase() + s.substring(1) + '.' : '',
  lipsum = () => {
    const n = lorem.length - 1
    return range(rand(1, 4)).map(_ => sentenceCase(range(rand(3, 8)).map(_ => lorem[rand(0, n)]).join(' '))).join(' ')
  },
  xid = () => `x${_xid++}`,
  newSocket = (handle: (m: Message) => void) => {
    const
      send = (m: Message) => window.setTimeout(() => handle(m), 0),
      input = (m: RawInput) => send({ t: 'i', id: xid(), ...sanitizeInput(m) }),
      output = async (author: S, text: S) => send({ t: 'o', id: xid(), author, text }),
      system = async (text: S) => await output('', text),
      user = async (text: S) => await output('user', text),
      connect = async () => {
        // connect to backend
        for (let i = 0; i < 20; i++) await (toss() ? system : user)(lipsum())

        system(`
Normal _italic_ *italic* __bold__ **bold** ~strikethrough~ \`code\` [Link](http://a.com)

> Blockquote

* List
* List
* List

1. One
2. Two
3. Three

Email foo@bar.baz
Link www.h2o.ai

\`\`\`
# code block
print '3 backticks or'
print 'indent 4 spaces'
\`\`\`
          
        `)

        // const response = await input()
        // await output(`hello, ${response}`)
        await input({})
        await input({ label: 'Text field with label' })
        await input({ label: 'Text field with placeholder', placeholder: 'Please enter text here' })
        await input({ label: 'Text field with value', value: 'Default value' })
        await input({ label: 'Text field, required', required: true })
        await input({ label: 'Text field with error message', error: 'Error message' })
        await input({ label: 'Text field with input mask', mask: '(999) 999 - 9999' })
        await input({ label: 'Text field with icon', icon: 'Calendar' })
        await input({ label: 'Text field with prefix', prefix: 'https://' })
        await input({ label: 'Text field with suffix', suffix: '.com' })
        await input({ label: 'Text field with prefix and suffix', prefix: 'https://', suffix: '.com' })
        await input({ label: 'Password field', password: true })
        await input({ label: 'Multiline text field', lines: 1 })
        await input({ label: 'Multiline text field, taller', lines: 5 })
        await input({ label: 'Integer', value: 5 })
        await input({ label: 'Integer within range', range: [0, 10] })
        await input({ label: 'Integer within range, with steps', range: [0, 10], step: 2 })
        await input({ label: 'Integer within range, with default', value: 5, range: [0, 10] })
        await input({ label: 'Integer within range, origin from zero', value: 3, range: [-5, 5] })
        await input({ label: 'Decimal within range', value: 0.6, range: [-1, 1], step: 0.2 })
        await input({ label: 'Integer range', value: [3, 7], range: [1, 10] })
        await input({ label: 'Integer range, origin from zero', value: [-1, 3], range: [-5, 5] })
        await input({ label: 'Integer field', value: 5, editable: true })
        await input({ label: 'Integer field with range', value: 5, range: [1, 10], editable: true })
        await input({ label: 'Integer field with range and step', value: 50, range: [0, 100], step: 10, editable: true })
        await input({ label: 'Decimal field with range and step', value: 0.5, range: [0.0, 1.0], step: 0.05, editable: true })
        await input({ label: 'Decimal field with range, step, and precision', value: 0.5, range: [0.0, 1.0], step: 0.05, precision: 2, editable: true })
        await input({ mode: 'rating', label: 'Rating' })
        await input({ mode: 'rating', label: 'Rating with value', value: 3 })
        await input({ mode: 'rating', label: 'Rating with zero allowed', min: 0 })
        await input({ mode: 'rating', label: 'Rating with max', value: 3, max: 10 })
        await input({ mode: 'rating', label: 'Rating with range', value: 3, range: [0, 7] })
        await input({ mode: 'time', label: 'Time', value: '3:04PM' })
        await input({ mode: 'time', label: 'Time, with seconds', value: '3:04:05PM' })
        await input({ mode: 'time', label: 'Time, hour only', value: '3PM' })
        await input({ mode: 'time', label: 'Time, 24-hr clock', value: '15:04' })
        await input({ mode: 'time', label: 'Time, 24-hr clock, with seconds', value: '15:04:05' })
        await input({ mode: 'time', label: 'Time, hour only, 24-hour clock', value: '15' })
        await input({ mode: 'day', label: 'Day picker', value: '2021-10-10' })
        await input({ mode: 'day', label: 'Day picker with range', value: '2021-10-10', range: ['2019-01-01', '2022-12-31'] })
        await input({ mode: 'week', label: 'Week picker', value: '2021-10-10' })
        await input({ mode: 'week', label: 'Week picker with range', value: '2021-10-10', range: ['2019-01-01', '2022-12-31'] })
        await input({ mode: 'month', label: 'Month picker', value: '2021-10-10' })
        await input({ mode: 'month', label: 'Month picker with range', value: '2021-10-10', range: ['2019-01-01', '2022-12-31'] })
        await input({
          multiple: true, label: 'Multiple choice list', choices: [
            { label: 'Apples', value: 'a' },
            { label: 'Bananas', value: 'b', selected: true },
            { label: 'Cherries', value: 'c' },
          ]
        })
        await input({ multiple: true, label: 'Multiple choice list from string', choices: 'Apples Bananas Cherries' })
        await input({ multiple: true, label: 'Multiple choice list from dictionary', choices: { Apples: 'a', Bananas: 'b', Cherries: 'c' } })
        await input({ multiple: true, label: 'Multiple choice list from string array', choices: ['Apples', 'Bananas', 'Cherries'] })
        await input({ multiple: true, label: 'Multiple choice list from tuples', choices: [['Apples', 'a'], ['Bananas', 'b'], ['Cherries', 'c']] })
        await input({ multiple: true, label: 'Multiple choice list, more than 10 choices', placeholder: 'Pick some fruits', choices: fruits })
        await input({ multiple: true, label: 'Multiple choice list, with error message', placeholder: 'Pick some fruits', choices: fruits, error: 'Error message' })
        await input({ multiple: true, label: 'Multiple choice list, editable', placeholder: 'Pick or enter some fruits', choices: fruits, editable: true })
        await input({ multiple: true, label: 'Multiple choice list, required', placeholder: 'Pick or enter some fruits', choices: fruits, required: true })
        await input({ mode: 'tag', label: 'Tags', choices: fruits })
        await input({
          label: 'Choice list, short', placeholder: 'Pick a fruit', choices: [
            { label: 'Apples', value: 'a', selected: true },
            { label: 'Bananas', value: 'b' },
            { label: 'Cherries', value: 'c' },
          ]
        })
        await input({
          label: 'Choice list, short, required', placeholder: 'Pick a fruit', required: true, choices: [
            { label: 'Apples', value: 'a', selected: true },
            { label: 'Bananas', value: 'b' },
            { label: 'Cherries', value: 'c' },
          ]
        })
        await input({
          label: 'Choice list, with icons', choices: [
            { label: 'Area', value: 'area', icon: 'AreaChart', selected: true },
            { label: 'Bar', value: 'bar', icon: 'BarChartHorizontal' },
            { label: 'Column', value: 'column', icon: 'BarChartVertical' },
            { label: 'Line', value: 'line', icon: 'LineChart' },
            { label: 'Scatter', value: 'scatter', icon: 'ScatterChart' },
          ]
        })
        await input({ label: 'Choice list, long', placeholder: 'Pick a fruit', choices: fruits })
        await input({ label: 'Choice list, long, editable', placeholder: 'Pick a fruit', choices: fruits, editable: true })
        await input({ label: 'Choice list, long, required', placeholder: 'Pick a fruit', choices: fruits, required: true })
        await input({ label: 'Choice list, with error message', placeholder: 'Pick a fruit', choices: fruits, error: 'Error message' })
        await input({
          label: 'Choice list, grouped', placeholder: 'Pick an item', choices: [
            {
              label: 'Fruits', value: 'f', choices: [
                { label: 'Apple', value: 'a' },
                { label: 'Banana', value: 'b' },
                { label: 'Cherry', value: 'c' },
              ]
            },
            {
              label: 'Vegetables', value: 'g', choices: [
                { label: 'Lettuce', value: 'l' },
                { label: 'Tomato', value: 't' },
              ]
            },
          ]
        })
        await input({ mode: 'color', label: 'Color picker, arbitrary color', value: '#a241e8' })
        await input({
          mode: 'color', label: 'Color picker, with choices', choices: [
            { label: 'orange', value: '#ca5010' },
            { label: 'cyan', value: '#038387' },
            { label: 'blueMagenta', value: '#8764b8' },
            { label: 'magenta', value: '#881798' },
            { label: 'white', value: '#ffffff' },
          ]
        })
        await input({
          actions: [
            { label: 'Apples', value: 'a', selected: true },
            { label: 'Bananas', value: 'b' },
            { label: 'Cherries', value: 'c' },
          ]
        })
        await input({
          actions: [
            { label: 'Yes', value: 'yes', selected: true },
            { label: 'No', value: 'no' },
          ],
          inline: true,
        })
        await input({
          actions: [
            { label: 'Sign me up!', value: 'yes', caption: 'Terms and conditions apply', selected: true },
            { label: 'Not now', value: 'no', caption: "I'll decide later." },
          ],
        })
        await input({
          actions: [
            { label: 'Sign me up!', value: 'yes', caption: 'Terms and conditions apply', selected: true },
            { label: 'Not now', value: 'no', caption: "I'll decide later." },
          ],
          inline: true,
        })
        await input({
          actions: [
            {
              label: 'Yes', value: 'yes', selected: true, choices: [
                { label: 'Remind me later', value: 'later', icon: 'ChatBot' },
                { label: "Don't ask me again", value: 'never', icon: 'MuteChat' },
              ]
            },
            { label: 'No', value: 'no' },
          ],
          inline: true,
        })
        await input({
          actions: [
            { label: 'Yes', value: 'yes', selected: true },
            {
              label: 'No', value: 'no', choices: [
                { label: 'Remind me later', value: 'later', icon: 'ChatBot' },
                { label: "Don't ask me again", value: 'never', icon: 'MuteChat' },
              ]
            },
          ],
          inline: true,
        })
        // More than 5 actions displays a menu.
        await input({
          label: 'Add a new chart',
          actions: [
            { label: 'Area Chart', value: 'area', icon: 'AreaChart' },
            { label: 'Bar Chart', value: 'bar', icon: 'BarChartHorizontal' },
            { label: 'Column Chart', value: 'column', icon: 'BarChartVertical' },
            { label: 'Line Chart', value: 'line', icon: 'LineChart' },
            { label: 'Scatterplot', value: 'scatter', icon: 'ScatterChart' },
            { label: 'Donut Chart', value: 'donut', icon: 'DonutChart' },
          ],
        })
        await input({
          inputs: [
            { label: 'Username', placeholder: 'someone@company.com' },
            { label: 'Password', placeholder: 'Password', password: true },
          ]
        })
        await input({
          inline: true,
          inputs: [
            { label: 'Username', placeholder: 'someone@company.com' },
            { label: 'Password', placeholder: 'Password', password: true },
          ]
        })
        await input({
          inline: true,
          inputs: [
            { label: 'Username', placeholder: 'someone@company.com' },
            { label: 'Password', placeholder: 'Password', password: true },
            { actions: [{ value: 'Login', selected: true }] },
          ]
        })
        await input({
          inputs: [
            {
              inline: true, inputs: [
                { label: 'First name' },
                { label: 'Last name' },
              ]
            },
            { label: 'Address line 1' },
            { label: 'Address line 2' },
            {
              inline: true, inputs: [
                { label: 'City' },
                { label: 'State' },
                { label: 'Zip' },
              ]
            },
          ]
        })
        await input({
          inputs: [
            {
              inline: true, inputs: [
                { label: 'First name' },
                { label: 'M.I', size: '10%' }, // 10% of available width
                { label: 'Last name' },
              ]
            },
            { label: 'Address line 1' },
            { label: 'Address line 2' },
            {
              inline: true, inputs: [
                { label: 'City', size: 5 },
                { label: 'State', size: '20%' },
                { label: 'Zip', size: 1 },
              ]
            },
            {
              actions: [
                { label: 'Sign me up!', value: 'yes', caption: 'Terms and conditions apply', selected: true },
                { label: 'Not now', value: 'no', caption: "I'll decide later." },
              ],
              inline: true,
            }
          ],
        })
      }
    return { connect }
  }

const
  elevated = `
    box-shadow: 0 14px 28px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.01);
  `,
  AppContainer = styled.div`
    width: 680px;
    margin: 0 auto;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  `,
  ChatContainer = styled.div`
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    background-color: #fff;
    padding: 1rem 2rem;
    box-sizing: border-box;
    ${elevated}
  `,
  ChatHeader = styled.div`
    display: flex;
    align-items: center;
    background-color: #fff;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    ${elevated}
  `,
  ChatHeaderContent = styled.div`
    flex-grow: 1;
    margin: 0 1rem;
  `,
  ChatHeaderTitle = styled.div`
    font-size: 1.5rem;
    font-weight: 700;
    color: #818181;
  `,
  ChatHeaderCaption = styled.div`
    color: #aaa;
  `,
  ChatHeaderCommands = styled.div`
  `,
  bubbleRadius = '0.75rem',
  bubble = (r: S) => 'border-radius: ' + r.replace(/\./g, bubbleRadius) + ';',
  ChatBubble = styled.div`
    max-width: 60%;
    padding: 0.5rem 0.75rem;
    margin-bottom: 2px;
  `,
  ChatBubbleGroup = styled.div`
    display: flex;
    flex-direction: column;
    margin: 0.75rem 0;

    font-size: 1rem;
    font-weight: 400;
  `,
  ChatBubbleGroupLeft = styled(ChatBubbleGroup)`
    align-items: flex-start;
    &>div {
      color: #002e5c;
      background: #e7eff6;
      border: 1px solid #dae6f1;
      ${bubble('0 . . 0')};
      &:first-child {
        ${bubble('. . . 0')};
      }
      &:last-child, &:only-child {
        ${bubble('0 . . .')};
      }
    }
  `,
  ChatBubbleGroupRight = styled(ChatBubbleGroup)`
    align-items: flex-end;
    &>div {
      color: #fff;
      background: #4a00e0;
      background: linear-gradient(to left, #8e2de2, #4a00e0);
      text-align: right;
      ${bubble('. 0 0 .')};
      &:first-child {
        ${bubble('. . 0 .')};
      }
      &:last-child, &:only-child {
        ${bubble('. 0 . .')};
      }
    }
  `,
  ChatLog = styled.div`
    display: flex;
    flex-grow: 1;
    flex-direction: column;
    justify-content: flex-end;
  `,
  InputContainer = styled.div`
    background: #fff;
    box-sizing: border-box;
    padding: 2rem 2rem 4rem 2rem;
    box-shadow: 0 -14px 28px rgba(0,0,0,0.1), 0 -10px 10px rgba(0,0,0,0.01);
  `,
  getDefaultValue = (value: any, min: any, max: any, step: any): N | undefined => {
    if (isN(value)) return value
    if (isN(min)) return Math.max(0, min)
    if (isN(max)) return Math.min(0, max)
    if (isN(step)) return 0
    return undefined
  },
  sanitizeInput = (input: RawInput): Input => {
    const { choices, actions, range, inputs } = input
    input.choices = toChoices(choices)
    input.actions = toChoices(actions)
    if (isPair(range)) {
      const [x, y] = range
      if ((isN(x) && isN(y)) || (isS(x) && isS(y))) {
        input.min = x
        input.max = y
      }
    }
    if (Array.isArray(inputs)) {
      input.inputs = inputs.map(sanitizeInput)
    }
    return input as Input
  }

const
  groupOutputs = (outputs: OutputMessage[]): OutputMessage[][] => { // TODO speed up
    if (outputs.length === 0) return []
    const groups: OutputMessage[][] = [[outputs[0]]]
    if (outputs.length === 1) return groups
    for (let i = 1; i < outputs.length; i++) {
      const
        o = outputs[i],
        group = groups[groups.length - 1],
        author = group.length ? group[group.length - 1].author : null
      if (o.author === author) group.push(o); else groups.push([o]) // TODO split if next day
    }
    return groups
  }

class OutputsView extends React.Component<{ outputs: OutputMessage[] }, { outputs: OutputMessage[] }> {
  render() {
    const
      { outputs } = this.props,
      // TODO insert day marker
      groups = groupOutputs(outputs).map(g => {
        const
          bubbles = g.map(o => <ChatBubble key={o.id}><XMarkdown text={o.text ?? ''} /></ChatBubble>),
          key = g[0].id
        return g[0].author
          ? <ChatBubbleGroupRight key={key}>{bubbles}</ChatBubbleGroupRight>
          : <ChatBubbleGroupLeft key={key}>{bubbles}</ChatBubbleGroupLeft>
      })

    return (
      <ChatLog>{groups}</ChatLog>
    )
  }
}


export class App extends React.Component<{}, { outputs: OutputMessage[], inputs: InputMessage[] }> {
  constructor(props: {}) {
    super(props)
    this.state = { outputs: [], inputs: [] }
  }
  componentDidMount() {
    const
      self = this,
      handle = (m: Message) => {
        switch (m.t) {
          case 'o':
            self.setState({ outputs: [...self.state.outputs, m] })
            break
          case 'i':
            self.setState({ inputs: [...self.state.inputs, m] })
            break
          case 's':
            self.setState({ outputs: m.outputs, inputs: m.input ? [m.input] : [] })
            break
        }
      },
      socket = newSocket(handle)

    socket.connect()
  }
  render() {
    const inputs = this.state.inputs.map(i => <InputView key={i.id} input={i} />)
    return (
      <AppContainer>
        <ChatHeader>
          <Persona
            imageInitials="D"
            imageAlt="Recipe"
            size={PersonaSize.size56}
            presence={PersonaPresence.online}
            hidePersonaDetails />
          <ChatHeaderContent>
            <ChatHeaderTitle>Create Driverless AI Model</ChatHeaderTitle>
            <ChatHeaderCaption>Started 29 min ago, updated just now.</ChatHeaderCaption>
          </ChatHeaderContent>
          <ChatHeaderCommands></ChatHeaderCommands>
        </ChatHeader>
        <ChatContainer>
          <OutputsView outputs={this.state.outputs} />
        </ChatContainer>
        {inputs}
      </AppContainer>
    )
  }
}
