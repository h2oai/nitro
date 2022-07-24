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

import { Dict, isS, newIncr, on, S, Signal, signal, U, V } from './core';
import { reIndex, sanitizeBox, sanitizeOptions } from './heuristics';
import { installPlugins } from './plugin';
import { Box, DisplayMode, Edit, EditPosition, EditType, Input, InputValue, Message, MessageType, Option, Server, ServerEvent, ServerEventT } from './protocol';
import { defaultScheme, loadScheme, Scheme } from './theme';

export enum ClientStateT { Connecting, Disconnected, Invalid, Connected }

export type ClientState = {
  t: ClientStateT.Connecting
} | {
  t: ClientStateT.Disconnected
  retry: U
} | {
  t: ClientStateT.Invalid
  error: S
} | {
  t: ClientStateT.Connected
  client: Client
}

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

export type ClientContext = {
  scoped(index: any, xid: S): Context
  commit(): void
  switch(method: S, params?: Dict<S>): void
  help(id: S): void
}

export type Context = {
  record(value: InputValue): void
  commit(): void
}

export const newClientContext = (server: Server, helpE: Signal<S>, onBusy: () => void): ClientContext => {
  const
    inputs: Input[] = [],
    popAll = (): Input[] => {
      const a = inputs.slice()
      inputs.length = 0
      return a
    },
    record = (index: any, xid: S, value: InputValue) => {
      if (index >= 0) inputs[index] = [xid, value]
    },
    commit = () => {
      onBusy()
      server.send({ t: MessageType.Input, inputs: popAll() })
    },
    change = (m: S, p?: Dict<S>) => {
      onBusy()
      inputs.length = 0 // clear any un-commit()-ed state.
      server.send({ t: MessageType.Switch, method: m, params: p })
    },
    scoped = (index: any, xid: S): Context => ({
      record: (value: InputValue) => record(index, xid, value),
      commit,
    })
  return { commit, scoped, switch: change, help: helpE }
}


type HashRPC = {
  method: S
  params?: Dict<S>
}

const getHashRPC = (): HashRPC | null => {
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
  const { s } = e
  const selector = isS(s) ? s.trim().split(/\s+/) : []
  return {
    t: e.t,
    p: e.p,
    s: selector,
  }
}

const getLocale = () => {
  const { language, languages } = window.navigator
  if (Array.isArray(languages)) for (const lang of languages) if (lang?.length) return lang
  if (language?.length) return language
  return ''
}

export const newClient = (server: Server) => {
  const
    body: Box[] = [],
    popup: Box[] = [],
    titleB = signal('H2O Nitro'),
    captionB = signal('v0.1.0'),
    menuB = signal<Option[]>([]),
    navB = signal<Option[]>([]),
    schemeB = signal(defaultScheme),
    modeB = signal<DisplayMode>('normal'),
    localeB = signal<Dict<S>>({}),
    helpE = signal<S>(),
    context = newClientContext(server, helpE, () => {
      client.busy = true
      stateB({ t: ClientStateT.Connected, client })
    }),
    stateB = signal<ClientState>({ t: ClientStateT.Connecting }),
    connect = () => {
      server.connect(handleEvent)
    },
    jump = (v: V, params?: Dict<S>) => {
      if (isS(v) && /^http[s]*:\/\//.test(v)) {
        const
          p = params ?? {},
          target = p['target'] ?? '_self',
          features: S[] = []
        for (const k in p) if (k !== 'target') features.push(`${k}=${p[k]}`)
        if (features.length) {
          console.log(v, target, features)
          window.open(v, target, features.join(','))
        } else {
          console.log(v, target)
          window.open(v, target)
        }
        return
      }
      window.location.hash = '!' + v
    },
    bounce = () => {
      const hashbang = getHashRPC()
      if (hashbang) {
        const { method, params } = hashbang
        context.switch(method, params)
      }
    },
    invalidate = () => {
      client.busy = false
      stateB({ t: ClientStateT.Connected, client })
    },
    handleEvent = (e: ServerEvent) => {
      switch (e.t) {
        case ServerEventT.Connect:
          if (server) {
            const
              join: Message = { t: MessageType.Join, client: { locale: getLocale() } },
              rpc = getHashRPC()
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
                const { text: error } = msg
                stateB({ t: ClientStateT.Invalid, error })
                break
              case MessageType.Output:
                {
                  const
                    { box: rawBox, edit: rawEdit } = msg,
                    box = sanitizeBox(localeB(), rawBox),
                    boxes = box.items ?? [],
                    root = body[0]?.items ?? []
                  if (box.popup) {
                    popup.length = 0
                    popup.push(box)
                    reIndex(popup, newIncr())
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
                    reIndex(body, newIncr())
                  }
                  invalidate()
                }
                break
              case MessageType.Switch:
                {
                  const { method, params } = msg
                  jump(method, params)
                }
                break
              case MessageType.Set:
                {
                  const
                    { settings } = msg,
                    { title, caption, menu, nav, theme, plugins, mode, locale } = settings

                  if (title) titleB(title)
                  if (caption) captionB(caption)
                  if (menu) menuB(sanitizeOptions(menu))
                  if (nav) navB(sanitizeOptions(nav))
                  if (theme) {
                    const
                      d = defaultScheme,
                      scheme: Scheme = {
                        primaryFont: d.primaryFont,
                        monospaceFont: d.monospaceFont,
                        backgroundColor: theme.background_color ?? d.backgroundColor,
                        foregroundColor: theme.foreground_color ?? d.foregroundColor,
                        primaryColor: theme.accent_color ?? d.primaryColor,
                        primaryColorName: theme.accent_color_name ?? d.primaryColorName,
                      }
                    schemeB(scheme)
                  }
                  if (mode) modeB(mode)
                  if (plugins) installPlugins(plugins)
                  if (locale) localeB(locale)

                  const state = stateB()
                  if (state.t === ClientStateT.Connected) {
                    invalidate()
                  }
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
  on(schemeB, scheme => window.setTimeout(() => loadScheme(scheme), 100))
  window.addEventListener('hashchange', () => { bounce() })

  const client = {
    titleB,
    captionB,
    menuB,
    navB,
    schemeB,
    modeB,
    localeB,
    helpE,
    body,
    popup,
    context,
    connect,
    jump,
    stateB,
    busy: true,
  }

  return client
}

export type Client = ReturnType<typeof newClient>
