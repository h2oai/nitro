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


export type Input = {
  xid: S
  label?: S
  mode?: 'text' | 'int' | 'float' | 'time' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating'
  icon?: S
  value?: V | Pair<V>
  min?: V
  max?: V
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
  options: Option[]
  actions: Option[]
  inputs: Input[]
  range?: Pair<N | S>
}
export type Option = {
  value: N | S
  label?: S
  icon?: S
  caption?: S
  selected?: B
  options?: Option[]
}

export type Output = {
  xid: S
  content: S
}
