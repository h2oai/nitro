import { S, N, B, U, V, Pair, I } from "./core"

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
  d: Input
  p?: I
} | {
  t: MsgType.Update
  d: Input
  p?: I
} | {
  t: MsgType.Remove
  d: Input
} | {
  t: MsgType.Input,
  d: Array<V | null>
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
}

export enum WidgetT {
  Stack = 1,
  Input,
  Option,
}

export type Stackable = {
  width?: S
  height?: S
  grow?: U
  shrink?: U
  basis?: S
}

export type Widget = Stackable & (Stack | Input)

export type InputMode = 'markdown' | 'button' | 'menu' | 'radio' | 'check' | 'text' | 'range' | 'number' | 'time' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating'

export type Stacking = {
  row?: B
  justify?: S
  align?: S
  wrap?: S
  gap?: S
}

export type Stack = Stacking & {
  t: WidgetT.Stack
  items: Widget[]
}

export type Input = Stacking & {
  t: WidgetT.Input
  xid: S
  index?: U
  text?: S
  name?: S
  mode?: InputMode
  icon?: S
  value?: V | Pair<V>
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
  options: Option[]
}

export type Option = {
  t: WidgetT.Option
  value: V
  text?: S
  icon?: S
  caption?: S
  selected?: B
  options?: Option[]
}
