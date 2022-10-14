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

import hotkeys from "hotkeys-js";
import { B, Dict, isS, on, S, Signal, signal, U, V } from './core';
import { formatter } from "./format";
import { freeze, sanitizeBox, sanitizeHelp, sanitizeOptions } from './heuristics';
import { installPlugins } from './plugin';
import { Box, Translation, DisplayMode, Edit, EditType, Input, InputValue, Message, MessageType, Option, Server, ServerEvent, ServerEventT, Theme } from './protocol';
import { applyTheme } from './theme';
import { Context } from "./ui";

export enum ClientStateT { Connecting, Disconnected, Invalid, Connected }

export type ClientState = {
  t: ClientStateT.Connecting
} | {
  t: ClientStateT.Disconnected
  retry: U
} | {
  t: ClientStateT.Invalid
  error: S
  trace?: S
} | {
  t: ClientStateT.Connected
}

enum EditPosition { Inside, Before, At, After }

type SanitizedEdit = {
  t: EditType
  p: EditPosition
  s: S[]
}

const defaultEdit: SanitizedEdit = {
  t: EditType.Update,
  p: EditPosition.Inside,
  s: [],
}

// depth-first, like querySelector()
const queryContainer = (boxes: Box[], s: S[], i: U, imax: U): Box[] | null => {
  if (s.length === 0) return boxes
  const name = s[i]
  for (const box of boxes) {
    if (box.name === name) {
      const { items } = box
      if (items) {
        if (i === imax) return items
        const res = queryContainer(items, s, i + 1, imax)
        if (res) return res
      }
    }
    const { items } = box
    if (items) {
      const res = queryContainer(items, s, i, imax)
      if (res) return res
    }
  }
  return null
}
// depth-first, like querySelector()
const queryBox = (boxes: Box[], name: S): [Box[], U] | null => {
  for (let i = 0, n = boxes.length; i < n; i++) {
    const box = boxes[i]
    if (box.name === name) return [boxes, i]
    const { items } = box
    if (items) {
      const res = queryBox(items, name)
      if (res) return res
    }
  }
  return null
}

type Switch = {
  method: S
  params?: Dict<S>
}

type ContextState = {
  inputs: Input[]
  switchE: Signal<Switch>
  commitE: Signal<Input[]>
  helpE: Signal<S>
  hotkey(chord: S, callback: () => void): () => void
}

const newContext = (state: ContextState, index: any, xid: S): Context => {
  const
    { inputs, switchE, commitE, helpE, hotkey } = state,
    capture = (index: any, xid: S, value: InputValue) => {
      if (index >= 0) inputs[index] = [xid, value]
    },
    record = (value: InputValue) => capture(index, xid, value),
    commit = () => {
      const a = inputs.slice()
      inputs.length = 0
      commitE(a)
    },
    change = (method: S, params?: Dict<S>) => {
      inputs.length = 0 // clear any un-commit()-ed state.
      switchE({ method, params })
    },
    scoped = (index: any, xid: S): Context => newContext(state, index, xid)
  return { scoped, record, commit, switch: change, help: helpE, hotkey }
}

const parseSwitch = (): Switch | null => {
  const h = window.location.hash
  if (h && h.length > 2 && h.startsWith('#!')) {
    const
      [method, q] = h.substring(2).split('?'),
      params: Dict<S> = {}
    let n = 0
    if (q) {
      for (const kv of q.split('&')) {
        const [k, v] = kv.split('=')
        if (k && v) {
          params[k] = decodeURIComponent(v)
          n++
        }
      }
    }
    return n > 0 ? { method, params } : { method }
  }
  return null
}

const sanitizeEdit = (e?: Edit): SanitizedEdit => {
  if (!e) return defaultEdit
  const
    { s } = e,
    xs = (s ? s : '*')
      .split(/\s*\b\s*/)
      .filter(x => x.length ? true : false),
    n = xs.length,
    p = xs[n - 1] === '*'
      ? EditPosition.Inside
      : xs[n - 1] === ':'
        ? EditPosition.After
        : xs[n - 2] === ':'
          ? EditPosition.Before
          : EditPosition.At
  return {
    t: e.t,
    p,
    s: xs.filter(x => x !== '*' && x !== ':'),
  }
}

const getLocale = () => {
  const { language, languages } = window.navigator
  if (Array.isArray(languages)) for (const lang of languages) if (lang?.length) return lang
  if (language?.length) return language
  return ''
}

const clientLocale = getLocale()

export const jump = (v: V, params?: Dict<S>) => {
  if (!isS(v)) v = String(v)

  const
    p = params ?? {},
    target = p['target']
  if (target) delete p['target']


  // hash without target
  if (!target && v.indexOf('#') === 0) {
    window.location.hash = v.substring(1)
    return
  }

  // not hash, or hash with target
  const features: S[] = []
  for (const k in p) features.push(`${k}=${p[k]}`)

  window.open(v, target ?? '_blank', features.length ? features.join(',') : undefined)
}

const emptyTranslation: Translation = { locale: clientLocale, strings: {} }
const toTranslationLookup = (bs: Translation[]) => {
  const d: Dict<Translation> = {}
  for (const b of bs) d[b.locale] = b
  return d
}


export const newClient = (server: Server) => {
  const
    body: Box[] = [],
    popup: Box[] = [],
    titleB = signal('H2O Nitro'),
    captionB = signal('v0.1.0'),
    menuB = signal<Option[]>([]),
    navB = signal<Option[]>([]),
    themeB = signal<Theme>({}),
    modeB = signal<DisplayMode>('normal'),
    formatterB = signal(formatter(toTranslationLookup([emptyTranslation]), emptyTranslation.locale)),
    busyB = signal<B>(true, () => false),
    inputs: Input[] = [],
    switchE = signal<Switch>(),
    commitE = signal<Input[]>(),
    helpB = signal<Dict<S>>({}),
    helpE = signal<S>(),
    hotkey = (chord: S, handle: () => void) => {
      hotkeys.unbind(chord)
      hotkeys(chord, e => {
        e.preventDefault()
        handle()
        return false
      })
      return () => hotkeys.unbind(chord)
    },
    context = newContext({ inputs, commitE, switchE, helpE, hotkey }, -1, ''),
    stateB = signal<ClientState>({ t: ClientStateT.Connecting }),
    connect = () => {
      server.connect(handleEvent)
    },
    bounce = () => {
      const rpc = parseSwitch()
      if (rpc) {
        const { method, params } = rpc
        context.switch(method, params)
      }
    },
    handleEvent = (e: ServerEvent) => {
      switch (e.t) {
        case ServerEventT.Connect:
          if (server) {
            const
              join: Message = { t: MessageType.Join, client: { locale: clientLocale } },
              rpc = parseSwitch()
            if (rpc) {
              const { method, params } = rpc
              if (method) join.method = method
              if (params) join.params = params
            }
            server.send(join)
          }
          break
        case ServerEventT.Message:
          {
            const msg = e.message
            switch (msg.t) {
              case MessageType.Error:
                const { text: error, trace } = msg
                stateB({ t: ClientStateT.Invalid, error, trace })
                server.disconnect()
                break
              case MessageType.Output:
                {
                  const
                    { box: rawBox, edit: rawEdit } = msg,
                    box = sanitizeBox(formatterB(), rawBox),
                    boxes = box.items ?? [],
                    root = body[0]?.items ?? []
                  if (box.popup) {
                    popup.length = 0
                    popup.push(box)
                    freeze(popup)
                  } else {
                    popup.length = 0 // clear any existing popup

                    const edit = sanitizeEdit(rawEdit)

                    if (edit.p === EditPosition.Inside) {
                      const parent = queryContainer(root, edit.s, 0, edit.s.length - 1)
                      if (parent) {
                        switch (edit.t) {
                          case EditType.Update:
                            if (parent === root) {
                              // Default case: clobber body
                              body.length = 0
                              body.push(box)
                            } else {
                              parent.length = 0
                              parent.push(box)
                            }
                            break
                          case EditType.Insert:
                            parent.push(...boxes)
                            break
                          case EditType.Remove:
                            parent.length = 0
                            break
                        }
                      }
                    } else {
                      const container = edit.s.length > 1 ? queryContainer(root, edit.s, 0, edit.s.length - 2) : root
                      if (container) {
                        const target = queryBox(container, edit.s[edit.s.length - 1])
                        if (target) {
                          const [parent, i] = target
                          switch (edit.t) {
                            case EditType.Update:
                              switch (edit.p) {
                                case EditPosition.Before:
                                  if (i - boxes.length < 0) {
                                    parent.splice(0, i, ...boxes)
                                  } else {
                                    parent.splice(i - boxes.length, boxes.length, ...boxes)
                                  }
                                  break
                                case EditPosition.At:
                                  parent.splice(i, boxes.length, ...boxes)
                                  break
                                case EditPosition.After:
                                  parent.splice(i + 1, boxes.length, ...boxes)
                                  break
                              }
                              break
                            case EditType.Insert:
                              switch (edit.p) {
                                // "before" and "at" mean the same, otherwise gets unintuitive
                                case EditPosition.Before:
                                case EditPosition.At:
                                  parent.splice(i, 0, ...boxes)
                                  break
                                case EditPosition.After:
                                  parent.splice(i + 1, 0, ...boxes)
                                  break
                              }
                              break
                            case EditType.Remove:
                              switch (edit.p) {
                                case EditPosition.Before:
                                  parent.splice(0, i)
                                  break
                                case EditPosition.At:
                                  parent.splice(i, 1)
                                  break
                                case EditPosition.After:
                                  parent.splice(i + 1, parent.length - i)
                                  break
                              }
                              break
                          }
                        }
                      }
                    }
                    freeze(body)
                  }
                  busyB(false)
                }
                break
              case MessageType.Switch:
                {
                  const { method, params } = msg
                  jump(method, params)
                  busyB(false)
                }
                break
              case MessageType.Set:
                {
                  const
                    { settings } = msg,
                    { title, caption, menu, nav, theme, plugins, help, mode, resources } = settings

                  if (title) titleB(title)
                  if (caption) captionB(caption)
                  if (menu) menuB(sanitizeOptions(menu))
                  if (nav) navB(sanitizeOptions(nav))
                  if (theme) themeB(theme)
                  if (mode) modeB(mode)
                  if (plugins) installPlugins(plugins)
                  if (help) helpB(sanitizeHelp(formatterB(), help))
                  if (resources) formatterB(formatter(toTranslationLookup(resources.translations), resources.locale))
                  const state = stateB()
                  if (state.t === ClientStateT.Connected) busyB(false)
                }
                break
              default:
                stateB({ t: ClientStateT.Invalid, error: `unknown message type: ${e.t}` })
                break
            }
          }
          break
        case ServerEventT.Disconnect:
          stateB({ t: ClientStateT.Disconnected, retry: e.retry })
          break
        case ServerEventT.Error:
          stateB({ t: ClientStateT.Invalid, error: String(e.error) })
          break
      }
    }

  on(titleB, title => document.title = title)
  on(themeB, theme => window.setTimeout(() => applyTheme(theme), 100))
  on(switchE, ({ method, params }) => {
    server.send({ t: MessageType.Switch, method, params })
    busyB(true)
  })
  on(commitE, inputs => {
    server.send({ t: MessageType.Input, inputs })
    busyB(true)
  })
  on(busyB, () => { stateB({ t: ClientStateT.Connected }) })

  window.addEventListener('hashchange', () => { bounce() })

  return {
    titleB,
    captionB,
    menuB,
    navB,
    themeB,
    modeB,
    helpB,
    helpE,
    busyB,
    body,
    popup,
    context,
    hotkey,
    connect,
    jump,
    stateB,
  }
}

export type Client = ReturnType<typeof newClient>
