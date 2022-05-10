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

import { B, I, N, Pair, S, Triple, U, V } from "./core"

export enum MsgType {
  Error = 1,
  Join,
  Switch,
  Input,
  Set,
  Insert,
  Update,
  Remove,
}

export type Input = B | S | N | S[] | N[]

export type Msg = {
  t: MsgType.Error
  e: S
} | {
  t: MsgType.Join
  d: any // XXX formalize
} | {
  t: MsgType.Switch,
  d: V
} | {
  t: MsgType.Input, // XXX rename
  d: Array<Input | null>
} | {
  t: MsgType.Set,
  d: Setting
} | {
  t: MsgType.Insert
  d: Box
  p?: I
} | {
  t: MsgType.Update
  d: Box
  p?: I
} | {
  t: MsgType.Remove
  d: Box
}

export type Theme = {
  foreground_color?: S
  background_color?: S
  accent_color?: S
  accent_color_name?: S
}

export type Setting = {
  title?: S,
  caption?: S,
  menu?: Option[]
  nav?: Option[]
  theme?: Theme
}

export type BoxMode = 'none' | 'md' | 'image' | 'button' | 'menu' | 'radio' | 'check' | 'toggle' | 'text' | 'range' | 'number' | 'time' | 'date' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating' | 'table' | 'separator'

export type Box = {
  xid: S
  index: I // -1 = don't capture
  text?: S
  name?: S
  mode?: BoxMode
  value?: V | Pair<V>
  options: Option[]
  headers?: Header[]
  items?: Box[]
  row?: B
  title?: S
  popup?: B
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
  error?: S
  lines?: U
  multiple?: B
  required?: B
  password?: B
  editable?: B
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