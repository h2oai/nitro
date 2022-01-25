import { Calendar, Checkbox, ChoiceGroup, ColorPicker, ComboBox, CompoundButton, DateRangeType, DefaultButton, Dropdown, DropdownMenuItemType, IButtonStyles, IChoiceGroupOption, IColorCellProps, IDropdownOption, ISliderProps, ITextFieldProps, Label, MaskedTextField, Persona, PersonaPresence, PersonaSize, PrimaryButton, Rating, Slider, SpinButton, Stack, SwatchColorPicker, TextField } from '@fluentui/react';
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

type Choice = {
  value: V
  label?: S
  icon?: S
  caption?: S
  selected?: B
  choices?: Choice[]
}

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
  toChoices = (x: any): Choice[] | undefined => {
    if (!x) return undefined
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
    return undefined
  }

type InputBase = {
  label?: S
  mode?: 'text' | 'int' | 'float' | 'time' | 'day' | 'week' | 'month' | 'list' | 'color' | 'menu' | 'rating' | 'slider'
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
  required?: B
  password?: B
  editable?: B
  inline?: B
}

type Input = InputBase & {
  t: 'i'
  id: S
  choices?: Choice[]
  actions?: Choice[]
}

type RawChoice = V | Pair<V>
type RawChoices = S | RawChoice[] | Dict<V> | Choice[]

type RawInput = InputBase & {
  choices?: RawChoices
  actions?: RawChoices
}

type OutputBase = {
  author: S
  text?: S
}

type Output = OutputBase & {
  t: 'o'
  id: S
}

type Session = {
  t: 's'
  outputs: Output[]
  input?: Input
}

type InputProps = { input: Input }

const
  WithSend = ({ hasLabel, children }: { hasLabel?: B, children: React.ReactChild }) => (
    <Stack horizontal tokens={{ childrenGap: 5 }} >
      <Stack.Item grow>{children}</Stack.Item>
      <Stack.Item>
        {hasLabel ? <Label>&nbsp;</Label> : null}
        <PrimaryButton iconProps={{ iconName: 'Send' }} />
      </Stack.Item>
    </ Stack>
  )


class XTextField extends React.Component<InputProps, {}> {
  render() {
    const
      { label, placeholder, icon, value, mask, prefix, suffix, error, lines, required, password } = this.props.input,
      props: Partial<ITextFieldProps> = {
        label: label,
        defaultValue: isS(value) ? value : isN(value) ? String(value) : undefined,
        placeholder,
        errorMessage: error,
        required: required === true,
      },
      field = password === true
        ? <TextField {...props} type='password' canRevealPassword revealPasswordAriaLabel='Show password' />
        : mask
          ? <MaskedTextField {...props} mask={mask} />
          : lines && (lines >= 1)
            ? <TextField {...props} multiline resizable autoAdjustHeight rows={lines} />
            : <TextField {...props} iconProps={icon ? { iconName: icon } : undefined} prefix={prefix} suffix={suffix} />

    return <WithSend hasLabel={label ? true : false}>{field}</WithSend>

  }
}

class XSpinButton extends React.Component<InputProps, {}> {
  // TODO format string
  render() {
    const
      { label, value, min, max, step, precision } = this.props.input

    return (
      <WithSend>
        <SpinButton
          label={label}
          defaultValue={isS(value) ? value : isN(value) ? String(value) : undefined}
          min={unum(min)}
          max={unum(max)}
          step={step}
          precision={precision}
        />
      </WithSend>
    )
  }
}

class XSlider extends React.Component<InputProps, {}> {
  // TODO format string
  render() {
    const
      { label, value, min, max, step } = this.props.input,
      originFromZero = isN(min) && min < 0 && isN(max) && max > 0,
      props: Partial<ISliderProps> = { label: label, min: unum(min), max: unum(max), step, originFromZero },
      slider = Array.isArray(value) && value.length === 2 && isN(value[0]) && isN(value[1])
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
    return <WithSend>{slider}</WithSend>

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
      <WithSend>
        <WithLabel label={label}>
          <Rating
            defaultRating={unum(value)}
            allowZeroStars={isN(min) && min <= 0}
            max={unum(max)}
          />
        </WithLabel>
      </WithSend>
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
      <WithSend hasLabel={label ? true : false}>
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
      </WithSend>
    )
  }
}

class XColorPicker extends React.Component<InputProps, {}> {
  render() {
    const
      { label, value } = this.props.input
    return (
      <WithSend hasLabel={label ? true : false}>
        <WithLabel label={label}>
          <ColorPicker color={isS(value) ? value : '#ff0000'} />
        </WithLabel>
      </WithSend>
    )
  }
}

type ChoiceProps = InputProps & { choices: Choice[] }

const CheckboxContainer = styled.div`
  margin: 0.5rem 0;
`
class XCheckList extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { label }, choices } = this.props,
      checkboxes = choices.map(c => (
        <CheckboxContainer key={c.value}>
          <Checkbox label={c.label} checked={c.selected ? true : false} />
        </CheckboxContainer>
      ))

    return (
      <WithSend hasLabel={label ? true : false}>
        <WithLabel label={label}><div>{checkboxes}</div></WithLabel>
      </WithSend>
    )
  }
}

class XMultiSelectDropdown extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { label, placeholder, error, required }, choices } = this.props,
      options: IDropdownOption[] = choices.map(c => ({ key: c.value, text: String(c.label) })),
      selectedKeys = choices.filter(c => c.selected).map(c => String(c.value))

    return (

      <WithSend hasLabel={label ? true : false}>
        <Dropdown
          multiSelect
          label={label}
          placeholder={placeholder}
          options={options}
          defaultSelectedKeys={selectedKeys}
          errorMessage={error}
          required={required ? true : false}
        />
      </WithSend>
    )
  }
}

class XMultiSelectComboBox extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { label, placeholder }, choices } = this.props,
      options: IDropdownOption[] = choices.map(c => ({ key: c.value, text: String(c.label) })),
      selectedKeys = choices.filter(c => c.selected).map(c => String(c.value))

    return (

      <WithSend hasLabel={label ? true : false}>
        <ComboBox
          multiSelect
          label={label}
          placeholder={placeholder}
          options={options}
          selectedKey={selectedKeys}
        />
      </WithSend>
    )
  }
}

class XButtons extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { inline }, choices } = this.props,
      horizontal = inline ? true : false,
      textAlign = horizontal ? 'center' : 'left',
      styles: IButtonStyles = { root: { width: '100%', textAlign } },
      compoundStyles: IButtonStyles = { root: { width: '100%', maxWidth: 'auto' } },
      buttons = choices.map(c => {
        const
          text = c.label,
          button = c.selected
            ? c.caption
              ? <CompoundButton primary text={text} secondaryText={c.caption} styles={compoundStyles} />
              : <PrimaryButton text={text} styles={styles} />
            : c.caption
              ? <CompoundButton text={text} secondaryText={c.caption} styles={compoundStyles} />
              : <DefaultButton text={text} styles={styles} />
        return <Stack.Item key={c.value} grow={horizontal}>{button}</Stack.Item>
      })
    return <Stack horizontal={horizontal} tokens={{ childrenGap: 5 }}>{buttons}</Stack>
  }
}

const
  gensym = (prefix: S) => {
    let k = 0
    return () => `__sidekick__${prefix}${++k}`
  },
  toDropdownOption = (c: Choice): IDropdownOption => (
    { key: c.value, text: String(c.label) }
  ),
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

class XSwatchPicker extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { label }, choices } = this.props,
      cells: IColorCellProps[] = choices.map(c => ({ id: String(c.value), label: String(c.label), color: String(c.value) }))

    return (
      <WithLabel label={label}>
        <SwatchColorPicker columnCount={10} colorCells={cells} />
      </WithLabel>
    )
  }
}

class XDropdown extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { label, placeholder, error, required }, choices } = this.props,
      hasGroups = choices.some(c => c.choices?.length ? true : false),
      options: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(choices) : choices.map(toDropdownOption),
      selectedItem = choices.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <WithSend hasLabel={label ? true : false}>
        <Dropdown
          label={label}
          placeholder={placeholder}
          options={options}
          selectedKey={selectedKey}
          errorMessage={error}
          required={required ? true : false}
        />
      </WithSend>
    )
  }
}
class XChoiceGroup extends React.Component<ChoiceProps, {}> {
  render() {
    const
      { input: { label, placeholder, required }, choices } = this.props,
      options: IChoiceGroupOption[] = choices.map(c => ({ key: String(c.value), text: String(c.label) })),
      selectedItem = choices.find(c => c.selected),
      selectedKey = selectedItem ? selectedItem.value : undefined

    return (
      <WithSend hasLabel={label ? true : false}>
        <ChoiceGroup
          label={label}
          placeholder={placeholder}
          options={options}
          defaultSelectedKey={selectedKey}
          required={required ? true : false}
        />
      </WithSend>
    )
  }
}
class InputView extends React.Component<InputProps, {}> {
  render() {
    return <InputContainer><InputImpl input={this.props.input}></InputImpl></InputContainer>
  }
}


export type Message = Input | Output | Session

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
        await input({ label: 'Integer field', value: 5 })
        await input({ label: 'Integer field with min', min: 5 })
        await input({ label: 'Integer field with max', max: 5 })
        await input({ label: 'Integer field with step', step: 5 })
        await input({ label: 'Integer field with range', value: 5, min: 1, max: 10 })
        await input({ label: 'Integer field with range and step', value: 50, min: 0, max: 100, step: 10 })
        await input({ label: 'Decimal field with range and step', value: 0.5, min: 0.0, max: 1.0, step: 0.05 })
        await input({ label: 'Decimal field with range, step, and precision', value: 0.5, min: 0.0, max: 1.0, step: 0.05, precision: 2 })
        await input({ mode: 'slider', label: 'Slider', value: 5 })
        await input({ mode: 'slider', label: 'Slider with min', min: 5 })
        await input({ mode: 'slider', label: 'Slider with max', max: 5 })
        await input({ mode: 'slider', label: 'Slider with step', step: 5 })
        await input({ mode: 'slider', label: 'Slider with range', value: 5, min: 1, max: 10 })
        await input({ mode: 'slider', label: 'Slider with origin from zero', value: 5, min: -10, max: 10 })
        await input({ mode: 'slider', label: 'Ranged Slider', value: [3, 7] })
        await input({ mode: 'slider', label: 'Ranged Slider with range', value: [3, 7], min: 1, max: 10 })
        await input({ mode: 'slider', label: 'Ranged Slider with origin from zero', value: [3, 7], min: -10, max: 10 })
        await input({ mode: 'rating', label: 'Rating' })
        await input({ mode: 'rating', label: 'Rating with value', value: 3 })
        await input({ mode: 'rating', label: 'Rating with zero allowed', min: 0 })
        await input({ mode: 'rating', label: 'Rating with max', value: 3, max: 10 })
        await input({ mode: 'day', label: 'Day picker', value: '2021-10-10' })
        await input({ mode: 'day', label: 'Day picker with range', value: '2021-10-10', min: '2019-01-01', max: '2022-12-31' })
        await input({ mode: 'week', label: 'Week picker', value: '2021-10-10' })
        await input({ mode: 'week', label: 'Week picker with range', value: '2021-10-10', min: '2019-01-01', max: '2022-12-31' })
        await input({ mode: 'month', label: 'Month picker', value: '2021-10-10' })
        await input({ mode: 'month', label: 'Month picker with range', value: '2021-10-10', min: '2019-01-01', max: '2022-12-31' })
        await input({
          mode: 'list', label: 'Multiple choice list', choices: [
            { label: 'Apples', value: 'a' },
            { label: 'Bananas', value: 'b', selected: true },
            { label: 'Cherries', value: 'c' },
          ]
        })
        await input({ mode: 'list', label: 'Multiple choice list from string', choices: 'Apples Bananas Cherries' })
        await input({ mode: 'list', label: 'Multiple choice list from dictionary', choices: { Apples: 'a', Bananas: 'b', Cherries: 'c' } })
        await input({ mode: 'list', label: 'Multiple choice list from string array', choices: ['Apples', 'Bananas', 'Cherries'] })
        await input({ mode: 'list', label: 'Multiple choice list from tuples', choices: [['Apples', 'a'], ['Bananas', 'b'], ['Cherries', 'c']] })
        await input({ mode: 'list', label: 'Multiple choice list, more than 10 choices', placeholder: 'Pick some fruits', choices: fruits })
        await input({ mode: 'list', label: 'Multiple choice list, with error message', placeholder: 'Pick some fruits', choices: fruits, error: 'Error message' })
        await input({ mode: 'list', label: 'Multiple choice list, editable', placeholder: 'Pick or enter some fruits', choices: fruits, editable: true })
        await input({ mode: 'list', label: 'Multiple choice list, required', placeholder: 'Pick or enter some fruits', choices: fruits, required: true })
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
            { label: 'Yes', value: 'yes', caption: 'Sign me up!', selected: true },
            { label: 'No', value: 'no', caption: "Not now, I'll decide later." },
          ],
        })
        await input({
          actions: [
            { label: 'Yes', value: 'yes', caption: 'Sign me up!', selected: true },
            { label: 'No', value: 'no', caption: "Not now, I'll decide later." },
          ],
          inline: true,
        })
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
        await input({ label: 'Choice list, long', placeholder: 'Pick a fruit', choices: fruits })
        await input({ label: 'Choice list, long, required', placeholder: 'Pick a fruit', required: true, choices: fruits })
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
    padding: 2rem 2rem 3rem 2rem;
    box-shadow: 0 -14px 28px rgba(0,0,0,0.1), 0 -10px 10px rgba(0,0,0,0.01);
  `,
  getDefaultValue = (value: any, min: any, max: any, step: any): N | undefined => {
    if (isN(value)) return value
    if (isN(min)) return Math.max(0, min)
    if (isN(max)) return Math.min(0, max)
    if (isN(step)) return 0
    return undefined
  },
  sanitizeInput = (input: RawInput): InputBase => {
    input.choices = toChoices(input.choices)
    input.actions = toChoices(input.actions)
    return input
  },
  InputImpl = ({ input }: InputProps) => {
    const { choices, actions } = input

    if (choices?.length) {
      switch (input.mode) {
        case 'list': // multiple choice
          if (input.editable) {
            return <XMultiSelectComboBox input={input} choices={choices} />
          }
          const hasLongLabels = choices.some(({ label }) => label && (label.length > 75))
          if (!hasLongLabels && choices.length > 10) {
            return <XMultiSelectDropdown input={input} choices={choices} />
          }
          return <XCheckList input={input} choices={choices} />
        case 'color':
          return <XSwatchPicker input={input} choices={choices} />
        default:
          const hasGroups = choices.some(c => c.choices?.length ? true : false)
          if (hasGroups || (choices.length > 7)) {
            return <XDropdown input={input} choices={choices} />
          }
          return <XChoiceGroup input={input} choices={choices} />
      }
    }

    if (actions?.length) {
      return <XButtons input={input} choices={actions} />
    }

    switch (input.mode) {
      case 'slider':
        return <XSlider input={input} />
      case 'rating':
        return <XRating input={input} />
      case 'day':
      case 'month':
      case 'week':
        return <XCalendar input={input} />
      case 'color':
        return <XColorPicker input={input} />
    }

    input.value = getDefaultValue(input.value, input.min, input.max, input.step)
    if (isN(input.value)) {
      return <XSpinButton input={input} />
    }
    // TODO mode=int/float + spin/slider?
    return <XTextField input={input} />
  }

const
  groupOutputs = (outputs: Output[]): Output[][] => { // TODO speed up
    if (outputs.length === 0) return []
    const groups: Output[][] = [[outputs[0]]]
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

class OutputsView extends React.Component<{ outputs: Output[] }, { outputs: Output[] }> {
  render() {
    const
      { outputs } = this.props,
      // TODO insert day marker
      groups = groupOutputs(outputs).map(g => {
        const
          bubbles = g.map(o => <ChatBubble key={o.id}>{o.text}</ChatBubble>),
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


export class App extends React.Component<{}, { outputs: Output[], inputs: Input[] }> {
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
