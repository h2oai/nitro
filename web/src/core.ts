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
export interface Box<T> extends Disposable {
  (): T
  (value: T): T
}

interface Boxed<T> extends Box<T> {
  __boxed__: boolean // marker
  on(f: Eff<T>, o?: any): Arrow<T>
  touch(): void
}

type Equal<T> = (a: T, b: T) => boolean
function different<T>(_a: T, _b: T) { return false }
/** Create a Box with a pre-defined value comparator. */
export function box<T>(value?: T, equal?: Equal<T>): Box<T>;
/** Create a Box. */
export function box<T>(...args: any[]): Box<T> {
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
  f.__boxed__ = true

  return f as Box<T>
}
/** Is this a Box? */
export function boxed<T>(x: any): x is Box<T> { return x && x.__boxed__ === true }
/** Get the value from a Box, if a Box, else return the argument as-is. */
export function unbox<T>(x: T | Box<T>): T { return boxed(x) ? x() : x }
/** Send a Box's value to f() and broadcast its value. */
export function rebox<T>(b: Box<T>, f: Eff<T>) { const x = b(); f(x); (b as Boxed<T>).touch() }
/** Subscribe to changes in a Box. */
export function on<A>(a: Box<A>, f: Eff<A>): Disposable;
/** Subscribe to changes in 2 Boxes. */
export function on<A, B>(a: Box<A>, b: Box<B>, f: Eff2<A, B>): Disposable;
/** Subscribe to changes in 3 Boxes. */
export function on<A, B, C>(a: Box<A>, b: Box<B>, c: Box<C>, f: Eff3<A, B, C>): Disposable;
/** Subscribe to changes in 4 Boxes. */
export function on<A, B, C, D>(a: Box<A>, b: Box<B>, c: Box<C>, d: Box<D>, f: Eff4<A, B, C, D>): Disposable;
/** Subscribe to changes in N Boxes. */
export function on(...args: any[]): Disposable { return react(false, args.slice(0, args.length - 1), args[args.length - 1]) }
/** Subscribe to changes in a box, and broadcast immediately. */
export function to<A>(a: Box<A>, f: Eff<A>): Disposable;
/** Subscribe to changes in 2 Boxes, and broadcast immediately. */
export function to<A, B>(a: Box<A>, b: Box<B>, f: Eff2<A, B>): Disposable;
/** Subscribe to changes in 3 Boxes, and broadcast immediately. */
export function to<A, B, C>(a: Box<A>, b: Box<B>, c: Box<C>, f: Eff3<A, B, C>): Disposable;
/** Subscribe to changes in 4 Boxes, and broadcast immediately. */
export function to<A, B, C, D>(a: Box<A>, b: Box<B>, c: Box<C>, d: Box<D>, f: Eff4<A, B, C, D>): Disposable;
/** Subscribe to changes in N Boxes, and broadcast immediately. */
export function to(...args: any[]): Disposable { return react(true, args.slice(0, args.length - 1), args[args.length - 1]) }

// eslint-disable-next-line @typescript-eslint/ban-types
function react(immediate: boolean, boxen: Box<any>[], f: Function): Disposable {
  const
    xs = boxen as Boxed<any>[],
    emit = () => f(...xs.map(x => x())),
    arrows = xs.map(x => x.on(emit)),
    dispose = () => arrows.forEach(a => a.dispose())

  if (immediate) emit()
  return { dispose }
}

/** Create a Box computed from another Box. */
export function by<A, B>(a: Box<A>, map: Func<A, B>): Box<B>
/** Create a Box computed from 2 other Boxes. */
export function by<A, B, C>(a: Box<A>, b: Box<B>, zip: Func2<A, B, C>): Box<B>
/** Create a Box computed from 3 other Boxes. */
export function by<A, B, C, D>(a: Box<A>, b: Box<B>, c: Box<C>, zip: Func3<A, B, C, D>): Box<B>
/** Create a Box computed from N other Boxes. */
export function by(...args: any[]): any {
  if (args.length < 2) throw new Error(`invalid number of args: want 2 or more, got ${args.length}`)
  const
    m = args.length - 1,
    xs = args.slice(0, m) as Boxed<any>[],
    // eslint-disable-next-line @typescript-eslint/ban-types
    f = args[m] as Function,
    yB = box(f(...xs.map(x => x())))

  xs.forEach(x => x.on(_ => yB(f(...xs.map(x => x())))))
  return yB
}
/** Watch a Box for changes and print changes to the console. */
export function watch<T>(x: Box<T>, label?: string): Disposable {
  // eslint-disable-next-line no-console
  return on(x, label ? ((x: T) => console.log(label, x)) : ((x: T) => console.log(x)))
}

function remove<T>(xs: T[], x: T): void { const i = xs.indexOf(x); if (i > -1) xs.splice(i, 1) }

export const gensym = (prefix: S) => {
  let k = 0
  return () => prefix + k++
}
export const xid = gensym('x')
export const isN = (x: any): x is number => typeof x === 'number'
export const isS = (x: any): x is string => typeof x === 'string'
export const isV = (x: any): x is S | N => isS(x) || isN(x)
export const isO = (x: any) => x && (typeof x === 'object')
export const isPair = (x: any): x is any[] => Array.isArray(x) && x.length === 2
export const defer = (seconds: U, f: TimerHandler) => window.setTimeout(f, seconds * 1000)