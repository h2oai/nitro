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
  method?: S // method
  params?: Dict<S> // params
  d?: any // XXX formalize
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

export type Theme = {
  foreground_color?: S
  background_color?: S
  accent_color?: S
  accent_color_name?: S
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
}

export type BannerMode = 'info' | 'success' | 'warning' | 'critical' | 'blocked' | 'error'

// *** Warning ***
// If you add a new mode here, update heuristics.tsx to mark it as non-interactive (index=0) if applicable.
export type BoxMode = 'none' | 'row' | 'tabs' | 'md' | 'button' | 'menu' | 'radio' | 'check' | 'toggle'
  | 'text' | 'range' | 'number' | 'time' | 'date' | 'day' | 'week' | 'month' | 'tag' | 'color'
  | 'rating' | 'table' | 'file' | 'progress' | 'spinner' | 'separator' | 'image' | 'web' | BannerMode

export type Box = {
  xid: S
  index: I // front-end only -1 => don't capture
  ignore?: B // true => don't capture
  text?: S
  name?: S
  mode?: BoxMode
  value?: V | Pair<V>
  options: Option[]
  headers?: Header[]
  items?: Box[]
  data?: any
  halt?: B
  title?: S
  caption?: S
  popup?: B
  layout?: 'row' | 'column'
  tile?: S
  cross_tile?: S
  wrap?: S
  gap?: S
  align?: S // CSS text-align
  width?: S | [S] | Pair<S> | Triple<S> // CSS width / [min] / [min, max] / [min, max, initial]
  height?: S | [S] | Pair<S> | Triple<S> // CSS height / [min] / [min, max] / [min, max, initial]
  margin?: S // CSS margin
  padding?: S // CSS padding
  border?: S // CSS border 1px solid ~
  color?: S  // CSS color
  background?: S // CSS background
  image?: S // img tag or CSS background-image
  fit?: S // CSS object-fit or background-size
  grow?: U // CSS flex-grow
  shrink?: U // CSS flex-shrink
  basis?: S // CSS flex-basis
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
  multiple?: B
  required?: B
  password?: B
  editable?: B
  live?: B
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
  mode?: 'md' | 'link'
  icon?: S
  width?: S | [S] | Pair<S> | Triple<S> // CSS width / [min] / [min, max] / [min, max, initial]
  resizable?: B
  multiline?: B
}