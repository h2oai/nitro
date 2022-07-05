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

/** Synonym for boolean. */
export type B = boolean
/** Synonym for unsigned int. */
export type U = number
/** Synonym for int. */
export type I = number
/** Synonym for float. */
export type F = number
/** Synonym for number. */
export type N = number
/** Synonym for string. */
export type S = string
/** Synonym for string or number. */
export type V = S | N
/** Synonym for date. */
export type D = Date
/** Synonym for number, string or date. */
// export type V = F | S | D
/** A primitive. */
// export type Prim = S | F | B | null
/** Dictionary or generic object. */
export interface Dict<T> { [key: string]: T }
/** Identifier (non-empty string). */
// export type Id = S
export type Pair<T> = [T, T]
export type Triple<T> = [T, T, T]


/** Action. */
export type Act = () => void
/** Action, 1 argument. */
export type Eff<T> = (t: T) => void
/** Action, 2 arguments. */
export type Eff2<A, B> = (a: A, b: B) => void
/** Action, 3 arguments. */
export type Eff3<A, B, C> = (a: A, b: B, c: C) => void
/** Action, 4 arguments. */
export type Eff4<A, B, C, D> = (a: A, b: B, c: C, d: D) => void
/** Function, 1 argument. */
export type Func<A, B> = (a: A) => B
/** Function, 2 arguments. */
export type Func2<A, B, C> = (a: A, b: B) => C
/** Function, 3 arguments. */
export type Func3<A, B, C, D> = (a: A, b: B, c: C) => D
/** Anything that needs disposing. */
export interface Disposable { dispose(): void }

interface Arrow<T> extends Disposable { f: Eff<T> }

/** A container that holds some value, and can be observed. */
export interface Signal<T> extends Disposable {
  (): T
  (value: T): T
}

interface SignalImpl<T> extends Signal<T> {
  __is_signal__: boolean // marker
  on(f: Eff<T>, o?: any): Arrow<T>
  touch(): void
}

type Equal<T> = (a: T, b: T) => boolean
function different<T>(_a: T, _b: T) { return false }
/** Create a signal with a pre-defined value comparator. */
export function signal<T>(value?: T, equal?: Equal<T>): Signal<T>;
/** Create a signal. */
export function signal<T>(...args: any[]): Signal<T> {
  let
    x: T = (args.length > 0 ? args[0] : undefined) as T
  const
    equal = args.length > 0 ? (args.length > 1 ? args[1] : null) : different,
    arrows: Arrow<T>[] = [],
    on = (f: Eff<T>): Arrow<T> => {
      const a: Arrow<T> = { f, dispose: () => remove(arrows, a) }
      arrows.push(a)
      return a
    },
    dispose = (): void => { arrows.length = 0 },
    broadcast = (t: T): void => { for (const a of arrows) a.f(t) },
    touch = (): void => broadcast(x),
    f = (...ys: T[]): T => {
      if (ys.length) { // f(x) invoked
        const y = ys[0]
        if (!(equal ? equal(x, y) : (x === y))) broadcast(x = y) // store and broadcast new value if changed
      } // else f() invoked
      return x
    }

  f.on = on
  f.touch = touch
  f.dispose = dispose
  f.__is_signal__ = true

  return f as Signal<T>
}
/** Is this a signal? */
export function isSignal<T>(x: any): x is Signal<T> { return x && x.__is_signal__ === true }
/** Get the value from a signal, if a signal, else return the argument as-is. */
export function unwrap<T>(x: T | Signal<T>): T { return isSignal<T>(x) ? x() : x }
/** Send a signal's value to f() and broadcast its value. */
export function rewrap<T>(b: Signal<T>, f: Eff<T>) { const x = b(); f(x); (b as SignalImpl<T>).touch() }
/** Subscribe to changes in a signal. */
export function on<A>(a: Signal<A>, f: Eff<A>): Disposable;
/** Subscribe to changes in 2 signals. */
export function on<A, B>(a: Signal<A>, b: Signal<B>, f: Eff2<A, B>): Disposable;
/** Subscribe to changes in 3 signals. */
export function on<A, B, C>(a: Signal<A>, b: Signal<B>, c: Signal<C>, f: Eff3<A, B, C>): Disposable;
/** Subscribe to changes in 4 signals. */
export function on<A, B, C, D>(a: Signal<A>, b: Signal<B>, c: Signal<C>, d: Signal<D>, f: Eff4<A, B, C, D>): Disposable;
/** Subscribe to changes in N signals. */
export function on(...args: any[]): Disposable { return react(false, args.slice(0, args.length - 1), args[args.length - 1]) }
/** Subscribe to changes in a signal, and broadcast immediately. */
export function to<A>(a: Signal<A>, f: Eff<A>): Disposable;
/** Subscribe to changes in 2 signals, and broadcast immediately. */
export function to<A, B>(a: Signal<A>, b: Signal<B>, f: Eff2<A, B>): Disposable;
/** Subscribe to changes in 3 signals, and broadcast immediately. */
export function to<A, B, C>(a: Signal<A>, b: Signal<B>, c: Signal<C>, f: Eff3<A, B, C>): Disposable;
/** Subscribe to changes in 4 signals, and broadcast immediately. */
export function to<A, B, C, D>(a: Signal<A>, b: Signal<B>, c: Signal<C>, d: Signal<D>, f: Eff4<A, B, C, D>): Disposable;
/** Subscribe to changes in N signals, and broadcast immediately. */
export function to(...args: any[]): Disposable { return react(true, args.slice(0, args.length - 1), args[args.length - 1]) }

// eslint-disable-next-line @typescript-eslint/ban-types
function react(immediate: boolean, signals: Signal<any>[], f: Function): Disposable {
  const
    xs = signals as SignalImpl<any>[],
    emit = () => f(...xs.map(x => x())),
    arrows = xs.map(x => x.on(emit)),
    dispose = () => arrows.forEach(a => a.dispose())

  if (immediate) emit()
  return { dispose }
}

/** Create a signal computed from another signal. */
export function by<A, B>(a: Signal<A>, map: Func<A, B>): Signal<B>
/** Create a signal computed from 2 other signals. */
export function by<A, B, C>(a: Signal<A>, b: Signal<B>, zip: Func2<A, B, C>): Signal<B>
/** Create a signal computed from 3 other signals. */
export function by<A, B, C, D>(a: Signal<A>, b: Signal<B>, c: Signal<C>, zip: Func3<A, B, C, D>): Signal<B>
/** Create a signal computed from N other signals. */
export function by(...args: any[]): any {
  if (args.length < 2) throw new Error(`invalid number of args: want 2 or more, got ${args.length}`)
  const
    m = args.length - 1,
    xs = args.slice(0, m) as SignalImpl<any>[],
    // eslint-disable-next-line @typescript-eslint/ban-types
    f = args[m] as Function,
    yB = signal(f(...xs.map(x => x())))

  xs.forEach(x => x.on(_ => yB(f(...xs.map(x => x())))))
  return yB
}
/** Watch a signal for changes and print changes to the console. */
export function watch<T>(x: Signal<T>, label?: string): Disposable {
  // eslint-disable-next-line no-console
  return on(x, label ? ((x: T) => console.log(label, x)) : ((x: T) => console.log(x)))
}

function remove<T>(xs: T[], x: T): void { const i = xs.indexOf(x); if (i > -1) xs.splice(i, 1) }

export const gensym = (prefix: S) => {
  let k = 0
  return () => prefix + k++
}
export const xid = gensym('x')
export const noop = () => { }
export const isB = (x: any): x is boolean => typeof x === 'boolean'
export const isN = (x: any): x is number => typeof x === 'number'
export const isS = (x: any): x is string => typeof x === 'string'
export const isV = (x: any): x is S | N => isS(x) || isN(x)
export const isO = (x: any) => x && (typeof x === 'object')
export const isPair = (x: any): x is any[] => Array.isArray(x) && x.length === 2
export const toN = (x: any): N | undefined => isN(x) ? x : undefined
export const toS = (x: any): S | undefined => isS(x) ? x : undefined
export const toDate = (x: any): Date | undefined => isS(x) ? new Date(x) : undefined
export const anyN = (...xs: any[]) => xs.some(isN)
export const anyS = (...xs: any[]) => xs.some(isS)
export const anyD = (...xs: any[]) => xs.some(x => x !== undefined)
export const defer = (seconds: U, f: TimerHandler) => window.setTimeout(f, seconds * 1000)
export const debounce = (ms: U, f: () => void) => {
  let t: U
  return () => {
    window.clearTimeout(t)
    t = window.setTimeout(() => f(), ms)
  }
}
export const words = (x: S) => x.trim().split(/\s+/g)
export const snakeToCamelCase = (s: S): S => s.replace(/(_\w)/g, m => m[1].toUpperCase())
export const valueFromRange = (value: any, min: any, max: any, step: any): N | undefined => {
  if (isN(value)) return value
  if (isN(min)) return Math.max(0, min)
  if (isN(max)) return Math.min(0, max)
  if (isN(step)) return 0
  return undefined
}
export const leftPad = (c: S, n: U) => {
  let pad = ''
  for (let i = 0; i < n; i++) pad += c
  return (s: S) => {
    if (s.length >= n) return s
    s = pad + s
    return s.substring(s.length - n)
  }
}
export const dateToString = (d: Date) => d.toISOString().substring(0, 10)
export const newIncr = (start = 0) => {
  let i = start
  return () => i++
}
export type Incr = ReturnType<typeof newIncr>
export function areSetsEqual<T>(xs: Set<T>, ys: Set<T>) {
  if (xs.size !== ys.size) return false
  for (const x of xs) if (!ys.has(x)) return false
  return true
}
