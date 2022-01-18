import { ISliderProps, ITextFieldProps, Label, MaskedTextField, Persona, PersonaPresence, PersonaSize, PrimaryButton, Rating, RatingSize, Slider, SpinButton, Stack, TextField } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import './App.css';

type S = string
type N = number
type U = N
type I = N
type F = N
type B = boolean
type V = S | I | F | B
type Dict<T> = { [key: string]: T }
type Pair<T> = [T, T]

type Choice = {
  label: S
  key?: S
  icon?: S
  color?: S
  selected?: S
}

type Choicelike = Choice | S
type Choices = Choicelike[] | Dict<S>

type InputBase = {
  label?: S
  mode?: 'text' | 'int' | 'float' | 'date' | 'time' | 'list' | 'color' | 'menu' | 'rating' | 'slider'
  icon?: S
  choices?: Choices
  actions?: Choices
  value?: V | Pair<V>
  min?: N
  max?: N
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
}

type Input = {
  t: 'i'
  id: S
} & InputBase

type Output = {
  t: 'o'
  id: S
  author: S
  text?: S
}

type Session = {
  t: 's'
  outputs: Output[]
  input?: Input
}

type InputProps = { input: Input }

const
  WithSend = ({ hasLabel: hasPrompt, children }: { hasLabel?: B, children: React.ReactChild }) => (
    <Stack horizontal tokens={{ childrenGap: 5 }} >
      <Stack.Item grow>{children}</Stack.Item>
      <Stack.Item>
        {hasPrompt ? <Label>&nbsp;</Label> : null}
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
        defaultValue: value ? String(value) : undefined,
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
          defaultValue={value ? String(value) : undefined}
          min={min}
          max={max}
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
      originFromZero = isNum(min) && min < 0 && isNum(max) && max > 0,
      props: Partial<ISliderProps> = { label: label, min, max, step, originFromZero },
      slider = Array.isArray(value) && value.length === 2 && isNum(value[0]) && isNum(value[1])
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

class XRating extends React.Component<InputProps, {}> {
  // TODO format string; aria-label
  render() {
    const
      { label, value, min, max } = this.props.input
    return (
      <WithSend>
        <Stack>
          <Stack.Item>
            <Label>{label}</Label>
          </Stack.Item>
          <Stack.Item>
            <Rating
              defaultRating={isNum(value) ? value : undefined}
              allowZeroStars={isNum(min) && min <= 0}
              max={max}
            />
          </Stack.Item>
        </Stack>
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
      input = (m: InputBase) => send({ t: 'i', id: xid(), ...m }),
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
  isNum = (n: any): n is number => typeof n === 'number',
  getDefaultValue = (value: any, min: any, max: any, step: any): N | undefined => {
    if (isNum(value)) return value
    if (isNum(min)) return Math.max(0, min)
    if (isNum(max)) return Math.min(0, max)
    if (isNum(step)) return 0
    return undefined
  },
  InputImpl = ({ input }: InputProps) => {
    const { mode, choices } = input
    if (choices) {
      if (choices.length) {
      }
    }
    if (mode === 'slider') return <XSlider input={input} />
    if (mode === 'rating') return <XRating input={input} />
    input.value = getDefaultValue(input.value, input.min, input.max, input.step)
    if (isNum(input.value)) return <XSpinButton input={input} />
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
