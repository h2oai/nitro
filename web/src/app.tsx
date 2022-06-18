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

import styled from 'styled-components';
import { Body, Popup } from './body';
import { Client } from './client';
import { Dict, isS, newIncr, S, signal, U } from './core';
import { Header } from './header';
import { reIndex, sanitizeBox, sanitizeOptions } from './heuristics';
import { installPlugins } from './plugin';
import { Box, Edit, EditPosition, EditType, Msg, MsgType } from './protocol';
import { Socket, SocketEvent, SocketEventT } from './socket';
import { defaultScheme, Scheme } from './theme';
import { make, newClientContext } from './ui';

enum AppStateT { Connecting, Disconnected, Invalid, Connected }

type AppState = {
  t: AppStateT.Connecting
} | {
  t: AppStateT.Disconnected
  retry: U
} | {
  t: AppStateT.Invalid
  error: S
} | {
  t: AppStateT.Connected
  client: Client
}

const Overlay = styled.div`
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`
const Danger = styled.div`
  text-align: center;
  padding: 2rem;
  font-size: 2rem;
  color: #842029;
  background-color: #f8d7da;
  border: 1px solid #f5c2c7;
`
const Warning = styled.div`
  text-align: center;
  padding: 2rem;
  font-size: 2rem;
  color: #664d03;
  background-color: #fff3cd;
  border: 1px solid #ffecb5;
`
const Blocker = styled(Overlay)`
  z-index: 1000;
  background-color: #000;
  opacity: 0;
  transition: opacity 0.3s
`

const Busy = make(({ timeout }: { timeout: U }) => {
  const
    visibleB = signal(false),
    render = () => (
      <Blocker style={{ opacity: visibleB() ? 0.5 : 0 }}>
        <img alt='Busy' src="busy32.gif" />
      </Blocker>
    )

  setTimeout(() => { visibleB(true) }, timeout)

  return { render, visibleB }
})

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

export const App = make(({ client }: { client: Client }) => {
  const
    stateB = signal<AppState>({ t: AppStateT.Connecting }),
    invalidate = (xid: S, socket: Socket) => {
      client.busy = false
      client.context = newClientContext(xid, socket.send, () => {
        client.busy = true
        stateB({ t: AppStateT.Connected, client })
      })
      stateB({ t: AppStateT.Connected, client })
    },
    onMessage = (socket: Socket, e: SocketEvent) => {
      switch (e.t) {
        case SocketEventT.Connect:
          if (socket) {
            const
              join: Msg = { t: MsgType.Join },
              rpc = getHashRPC()
            if (rpc) {
              const { method, params } = rpc
              if (method) join.method = method
              if (params) join.params = params
            }
            socket.send(join)
          }
          break
        case SocketEventT.Message:
          {
            const msg = e.message
            switch (msg.t) {
              case MsgType.Error:
                const { text: error } = msg
                stateB({ t: AppStateT.Invalid, error })
                break
              case MsgType.Output:
                {
                  const { xid, box: rawBox, edit: rawEdit } = msg
                  const box = sanitizeBox(rawBox)
                  const boxes = box.items ?? []
                  const { body, popup } = client
                  const root = body[0]?.items ?? []
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
                  invalidate(xid, socket)
                }
                break
              case MsgType.Set:
                {
                  const
                    { xid, settings } = msg,
                    { title, caption, menu, nav, theme, plugins, mode } = settings

                  if (title) client.titleB(title)
                  if (caption) client.captionB(caption)
                  if (menu) client.menuB(sanitizeOptions(menu))
                  if (nav) client.navB(sanitizeOptions(nav))
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
                    client.schemeB(scheme)
                  }
                  if (mode) client.modeB(mode)
                  if (plugins) installPlugins(plugins)

                  const state = stateB()
                  if (state.t === AppStateT.Connected) {
                    invalidate(xid, socket)
                  }
                }
                break
              default:
                stateB({ t: AppStateT.Invalid, error: `unknown message type: ${e.t}` })
                break
            }
          }
          break
        case SocketEventT.Disconnect:
          stateB({ t: AppStateT.Disconnected, retry: e.retry })
          break
        case SocketEventT.Error:
          stateB({ t: AppStateT.Invalid, error: String(e.error) })
          break
      }
    },
    init = () => {
      window.addEventListener('hashchange', () => {
        const hashbang = getHashRPC()
        if (hashbang) {
          const { method, params } = hashbang
          client.context.switch(method, params)
        }
      })
      client.socket(onMessage)
    },
    render = () => {
      const state = stateB()
      switch (state.t) {
        case AppStateT.Connecting:
          return (
            <Busy timeout={100} />
          )
        case AppStateT.Disconnected:
          return (
            <Overlay>
              <Warning>Disconnected, retrying in {state.retry} seconds...</Warning>
            </Overlay>
          )
        case AppStateT.Invalid:
          return (
            <Overlay>
              <Danger>Error: {state.error}</Danger>
            </Overlay>
          )
        case AppStateT.Connected:
          const
            { popup, busy, modeB } = client,
            isChromeless = modeB() === 'chromeless'

          return (
            <>
              {busy && <Busy timeout={500} />}
              <div className='view'>
                {!isChromeless && <div className='art' />}
                <div className='page'>
                  {!isChromeless && <Header client={client} />}
                  <Body client={client} />
                  {popup.length ? <Popup client={client} /> : <></>}
                </div>
              </div>
            </>
          )
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

