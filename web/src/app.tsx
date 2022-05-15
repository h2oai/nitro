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

import React from 'react';
import styled from 'styled-components';
import { Body, Popup } from './body';
import { Client } from './client';
import { isN, newIncr, S, signal, U, xid } from './core';
import { Header } from './header';
import { reIndex, sanitizeBox, sanitizeOptions } from './heuristics';
import { Msg, MsgType } from './protocol';
import { Socket, SocketEvent, SocketEventT } from './socket';
import { defaultScheme, Scheme } from './theme';
import { make } from './ui';

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
  socket: Socket
  client: Client
}

const hello: Msg = {
  t: MsgType.Join,
  d: {
    language: window.navigator.language, // XXX formalize
  }
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

export const App = make(({ client }: { client: Client }) => {
  const
    stateB = signal<AppState>({ t: AppStateT.Connecting }),
    onMessage = (socket: Socket, e: SocketEvent) => {
      switch (e.t) {
        case SocketEventT.Connect:
          if (socket) socket.send(hello)
          break
        case SocketEventT.Message:
          {
            const msg = e.message
            switch (msg.t) {
              case MsgType.Error:
                const { e: error } = msg
                stateB({ t: AppStateT.Invalid, error })
                break
              case MsgType.Update:
                {
                  const { d: box, p: position } = msg
                  box.xid = xid()
                  const { body, popup } = client
                  if (box.popup) {
                    popup.length = 0
                    popup.push(sanitizeBox(box))
                    reIndex(popup, newIncr())
                  } else {
                    if (isN(position) && position >= 0 && position < body.length) { // XXX not used
                      body[position] = box
                    } else {
                      popup.length = 0
                      body.length = 0
                      body.push(sanitizeBox(box))
                    }
                    reIndex(body, newIncr())
                  }
                  stateB({ t: AppStateT.Connected, socket, client })
                }
                break
              case MsgType.Set:
                {
                  const
                    { d: conf } = msg,
                    { title, caption, menu, nav, theme } = conf

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

                  const state = stateB()
                  if (state.t === AppStateT.Connected) {
                    stateB({ t: AppStateT.Connected, socket, client })
                  }
                }
                break
              default:
                stateB({ t: AppStateT.Invalid, error: 'unknown message type' })
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
      client.socket(onMessage)
    },
    render = () => {
      const state = stateB()
      switch (state.t) {
        case AppStateT.Connecting:
          return (
            <Overlay>
              <Warning>Connecting...</Warning>
            </Overlay>
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
          return (
            <div className='view'>
              <div className='art' />
              <div className='page'>
                <Header send={state.socket.send} client={client} />
                <Body send={state.socket.send} boxes={client.body} />
                {client.popup.length ? <Popup send={state.socket.send} boxes={client.popup} /> : <></>}
              </div>
            </div>
          )
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

