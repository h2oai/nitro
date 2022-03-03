import { S, N, B, U, V, Pair } from "./core"

export enum MsgOp {
  Control = 1,
  Message,
}

export enum MsgType {
  Error = 1,
  Join,
  Leave,
  Request,
  Response,
  Watch,
  Event,
  Text,
  Input,
  Abort,
  Resume,
  Read,
  Write,
  Append,
}

export enum ErrCode {
  PeerUnavailable = 1,
  PeerDead,
  RateLimited,
  BadOp,
}

export type Msg = {
  t: MsgType.Error
  c: ErrCode
} | {
  t: MsgType.Join
  d: any // XXX formalize
} | {
  t: MsgType.Read
  d: Input
} | {
  t: MsgType.Write
  d: Output
} | {
  t: MsgType.Append
  d: Output
} | {
  t: MsgType.Input,
  d: Array<V | null>
}

export enum WidgetT {
  Output = 1,
  Input,
  Option,
}

type IO = Input | Output

export type Output = {
  t: WidgetT.Output
  xid: S
  text: S
  size?: S | U
  inline?: B
  items?: IO[]
}

export type Input = {
  t: WidgetT.Input
  xid: S
  label?: S
  inline?: B
  size?: S | U
  items?: IO[]
  mode?: 'text' | 'int' | 'float' | 'time' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating'
  icon?: S
  value?: V | Pair<V>
  min?: V
  max?: V
  step?: N
  precision?: U
  range?: [V, V] | [V, V, V] | [V, V, V, V]
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
  options: Option[]
  actions: Option[]
}

export type Option = {
  t: WidgetT.Option
  value: N | S
  label?: S
  icon?: S
  caption?: S
  selected?: B
  options?: Option[]
}
