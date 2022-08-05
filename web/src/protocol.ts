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

import { B, Dict, I, N, Pair, S, Triple, U, V } from "./core"

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

export enum EditPosition { Inside = 1, At, Before, After }

export type Edit = {
  t: EditType
  p: EditPosition
  s?: S | S[] // selector
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

export type Settings = {
  title?: S,
  caption?: S,
  menu?: Option[]
  nav?: Option[]
  theme?: Theme
  plugins?: Plugin[]
  mode?: DisplayMode
  locale?: Dict<S>
}

// *** Warning ***
// If you add a new mode here, update heuristics.tsx to mark it as non-interactive (index=0) if applicable.
export type BoxMode = 'box'
  | 'blocked'
  | 'button'
  | 'check'
  | 'col'
  | 'color'
  | 'critical'
  | 'date'
  | 'day'
  | 'error'
  | 'file'
  | 'image'
  | 'info'
  | 'md'
  | 'menu'
  | 'month'
  | 'number'
  | 'password'
  | 'progress'
  | 'radio'
  | 'range'
  | 'rating'
  | 'row'
  | 'separator'
  | 'spinner'
  | 'success'
  | 'svg'
  | 'tab'
  | 'table'
  | 'tag'
  | 'text'
  | 'time'
  | 'toggle'
  | 'warning'
  | 'web'
  | 'week'

export type Box = {
  xid: S
  index: I // (front-end only) don't record if -1
  ignore?: B // don't record if true
  text?: S
  name?: S
  modes: Set<S>
  value?: V | Pair<V>
  options: Option[]
  headers?: Header[]
  items?: Box[]
  data?: any
  halt?: B
  title?: S
  caption?: S
  hint?: S
  help?: S
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
  path?: S // file upload path or web view path
  error?: S
  lines?: U
}

export type Option = {
  value: V
  text?: S
  name?: S
  icon?: S
  caption?: S
  selected?: B
  options?: Option[]
}

export type Header = {
  text: S
  modes: Set<S>
  style?: S
  icon?: S
}
