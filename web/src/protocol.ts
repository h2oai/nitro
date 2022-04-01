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
  Leave,
  Abort,
  Resume,
  Request,
  Response,
  Watch,
  Event,
  Input,
  Insert,
  Update,
  Remove,
  Conf,
  Switch,
}

export type Msg = {
  t: MsgType.Error
  e: S
} | {
  t: MsgType.Join
  d: any // XXX formalize
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
} | {
  t: MsgType.Input, // XXX rename
  d: Array<V | V[] | null>
} | {
  t: MsgType.Conf,
  d: Conf
} | {
  t: MsgType.Switch,
  d: V
}

export type Conf = {
  title?: S,
  caption?: S,
  menu?: Option[]
  nav?: Option[]
}

export type BoxMode = 'md' | 'button' | 'menu' | 'radio' | 'check' | 'text' | 'range' | 'number' | 'time' | 'date' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating'

export type Box = {
  xid: S
  index: I // -1 = don't capture
  text?: S
  name?: S
  mode?: BoxMode
  value?: V | Pair<V>
  options: Option[]
  items?: Box[]
  row?: B
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
  icon?: S
  caption?: S
  selected?: B
  options?: Option[]
}
