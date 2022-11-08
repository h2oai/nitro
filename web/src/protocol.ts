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

import { B, Dict, I, N, P, Pair, S, U, V } from "./core"

export type Server = {
  connect(handler: ServerEventHandler): void
  send(message: Message): void
  disconnect(): void
}

export enum ServerEventT {
  Connect,
  Disconnect,
  Message,
  Error,
}

export type ServerEvent = {
  t: ServerEventT.Connect
} | {
  t: ServerEventT.Disconnect, retry: U
} | {
  t: ServerEventT.Error, error: any
} | {
  t: ServerEventT.Message, message: Message
}

export type ServerEventHandler = (e: ServerEvent) => void

export enum MessageType {
  Error = 1,
  Join, // client -> server, initiate connection
  Switch, // client -> server, context switch
  Input, // client -> server, commit input
  Output, // server -> client, display output
  Set, // server -> client, set attributes
}

export type InputValue = B | S | N | S[] | N[] | null
export type Input = [S, InputValue]

export type Message = {
  t: MessageType.Error
  code: U // code
  text: S // description
  trace?: S // stack trace
} | {
  t: MessageType.Join
  client: Client
  method?: S // method
  params?: Dict<S> // params
} | {
  t: MessageType.Switch,
  method: S // method
  params?: Dict<S> // params
} | {
  t: MessageType.Input,
  inputs: Array<Input> // inputs
} | {
  t: MessageType.Output
  box: Box // root view
  edit?: Edit // edit command
} | {
  t: MessageType.Set,
  settings: Settings
}

export enum EditType { Insert = 1, Update, Remove }

export type Edit = {
  t: EditType
  s?: S // selector
}

export type Client = {
  locale: S
}

export type Theme = {
  mode?: S // light [gray] | dark [gray] | dark gray | dark slate | ...
  accent?: S // red | orange | amber | ...
}

export type Plugin = {
  name: S
  scripts: Script[]
}

export type Script = {
  source: S
  type?: S
  asynchronous?: B
  cross_origin?: S
  referrer_policy?: S
  integrity?: S
}

export type DisplayMode = 'normal' | 'chromeless'

export type Translation = { locale: S, strings: Dict<S> }

export type Resources = { locale: S, translations: Translation[] }

export type Settings = {
  title?: S,
  caption?: S,
  menu?: Option[]
  nav?: Option[]
  theme?: Theme
  plugins?: Plugin[]
  help?: Dict<S>
  resources?: Resources
  mode?: DisplayMode
}

type BoxType = { input: B, labeled: B }

const
  unlabeledInput: BoxType = { input: true, labeled: false },
  labeledInput: BoxType = { input: true, labeled: true },
  unlabeledOutput: BoxType = { input: false, labeled: false }

export const boxTypes = {
  box: unlabeledOutput,
  blocked: unlabeledOutput,
  button: labeledInput,
  check: unlabeledInput,
  col: unlabeledOutput,
  color: unlabeledInput,
  input: unlabeledInput,
  critical: unlabeledOutput,
  date: labeledInput,
  day: unlabeledInput,
  error: unlabeledOutput,
  file: unlabeledInput,
  group: unlabeledOutput,
  info: unlabeledOutput,
  md: unlabeledOutput, // not an input unless it contains hyperlinks
  menu: labeledInput,
  month: unlabeledInput,
  number: labeledInput,
  password: unlabeledInput,
  progress: unlabeledOutput,
  radio: unlabeledInput,
  range: unlabeledInput,
  rating: labeledInput,
  row: unlabeledOutput,
  separator: unlabeledOutput,
  spinner: unlabeledOutput,
  success: unlabeledOutput,
  svg: unlabeledOutput,
  table: unlabeledInput,
  tag: labeledInput,
  tap: unlabeledOutput, // input child
  text: labeledInput,
  time: unlabeledInput,
  toggle: unlabeledInput,
  warning: unlabeledOutput,
  web: unlabeledOutput,
  week: unlabeledInput,
  // Graphics ("g") modes:
  'g-label': unlabeledOutput,
  'g-point': unlabeledOutput,
  'g-rect': unlabeledOutput,
  'g-arc': unlabeledOutput,
  'g-polygon': unlabeledOutput,
  'g-polyline': unlabeledOutput,
  'g-link-x': unlabeledOutput,
  'g-link-y': unlabeledOutput,
  'g-spline-x': unlabeledOutput,
  'g-spline-y': unlabeledOutput,
  'g-gauge-c': unlabeledOutput,
  'g-gauge-sc': unlabeledOutput,
  'g-line-x': unlabeledOutput,
  'g-line-y': unlabeledOutput,
  'g-curve-x': unlabeledOutput,
  'g-curve-y': unlabeledOutput,
  'g-step-x': unlabeledOutput,
  'g-step-y': unlabeledOutput,
  'g-bar-x': unlabeledOutput,
  'g-bar-y': unlabeledOutput,
  'g-stroke-x': unlabeledOutput,
  'g-stroke-y': unlabeledOutput,
  'g-tick-x': unlabeledOutput,
  'g-tick-y': unlabeledOutput,
  'g-guide-x': unlabeledOutput,
  'g-guide-y': unlabeledOutput,
  'g-gauge-x': unlabeledOutput,
  'g-gauge-y': unlabeledOutput,
}

export type BoxMode = keyof typeof boxTypes

export const allBoxModes = Object.keys(boxTypes) as BoxMode[]
const boxEntries = Object.entries(boxTypes)
export const inputBoxModes = boxEntries.filter(([_, v]) => v.input).map(([k, _]) => k as BoxMode)
export const labeledBoxModes = boxEntries.filter(([_, v]) => v.labeled).map(([k, _]) => k as BoxMode)

export type BoxModifier = 'live'
  | 'editable' | 'multi' | 'required' | 'selectable'
  | 'vertical'
  | 'top' | 'middle' | 'bottom' | 'left' | 'center' | 'right'
  | 'open' | 'closed'

export type BoxT = BoxMode | BoxModifier

export type Data = Dict<P | Data> | Array<P | Data>

export type Box = {
  xid: S
  pid?: S // (front-end only) xid of parent, if applicable
  index: I // (front-end only) don't record if -1
  ignore?: B // don't record if true
  text?: S
  name?: S
  modes: Set<BoxT>
  value?: V | Pair<V>
  options?: Option[]
  headers?: Header[]
  items?: Box[]
  data?: Data
  halt?: B
  title?: S
  caption?: S
  hint?: S
  help?: S
  locale?: S | S[]
  hotkey?: S
  popup?: B
  disabled?: B
  style?: S
  image?: S // img tag or CSS background-image
  icon?: S
  min?: V
  max?: V
  step?: N
  precision?: U
  range?: [V, V] | [N, N, N] | [N, N, N, U]
  mask?: S
  prefix?: S
  suffix?: S
  // format?: S // TODO: displayed-value format string for spinbutton, slider
  placeholder?: S
  link?: S
  error?: S
  lines?: U
}

export type Option = {
  value: V
  text?: S
  name?: S
  icon?: S
  caption?: S
  hotkey?: S
  selected?: B
  disabled?: B
  data?: Data
  options?: Option[]
}

export type Header = {
  text: S
  modes: Set<S>
  style?: S
  icon?: S
}
