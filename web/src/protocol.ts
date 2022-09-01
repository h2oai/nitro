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

export type Bundle = { locale: S, resources: Dict<S> }

export type Settings = {
  title?: S,
  caption?: S,
  menu?: Option[]
  nav?: Option[]
  theme?: Theme
  plugins?: Plugin[]
  bundles?: Bundle[]
  mode?: DisplayMode
}

export const boxTypes = {
  box: { input: false, labeled: false },
  blocked: { input: false, labeled: false },
  button: { input: true, labeled: true },
  check: { input: true, labeled: false },
  col: { input: false, labeled: false },
  color: { input: true, labeled: false },
  input: { input: true, labeled: false },
  critical: { input: false, labeled: false },
  date: { input: true, labeled: true },
  day: { input: true, labeled: false },
  error: { input: false, labeled: false },
  file: { input: true, labeled: false },
  group: { input: false, labeled: false },
  info: { input: false, labeled: false },
  md: { input: false, labeled: false }, // not an input unless it contains hyperlinks
  menu: { input: true, labeled: true },
  month: { input: true, labeled: false },
  number: { input: true, labeled: true },
  password: { input: true, labeled: false },
  progress: { input: false, labeled: false },
  radio: { input: true, labeled: false },
  range: { input: true, labeled: false },
  rating: { input: true, labeled: true },
  row: { input: false, labeled: false },
  separator: { input: false, labeled: false },
  spinner: { input: false, labeled: false },
  success: { input: false, labeled: false },
  svg: { input: false, labeled: false },
  table: { input: true, labeled: false },
  tag: { input: true, labeled: true },
  tap: { input: false, labeled: false }, // input child
  text: { input: true, labeled: true },
  time: { input: true, labeled: false },
  toggle: { input: true, labeled: false },
  warning: { input: false, labeled: false },
  web: { input: false, labeled: false },
  week: { input: true, labeled: false },
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
  locale?: S | S[]
  hint?: S
  help?: S
  hotkey?: S
  popup?: B
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
  data?: Data
  options?: Option[]
}

export type Header = {
  text: S
  modes: Set<S>
  style?: S
  icon?: S
}
