import React from 'react';
import { Body } from './body';
import { Client } from './client';
import { isN, newIncr, S, signal, U, xid } from './core';
import { Header } from './header';
import { reIndex, sanitizeBox, sanitizeOptions } from './heuristics';
import { Box, Conf, Msg, MsgType } from './protocol';
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
                  const { boxes } = client
                  if (isN(position) && position >= 0 && position < boxes.length) {
                    boxes[position] = box
                  } else {
                    boxes.length = 0
                    boxes.push(sanitizeBox(box))
                  }
                  reIndex(boxes, newIncr())
                  stateB({ t: AppStateT.Connected, socket, client })
                }
                break
              case MsgType.Conf:
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
          stateB({ t: AppStateT.Invalid, error: e.error })
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
          return <div>connecting</div>
        case AppStateT.Disconnected:
          return <div>disconnected, retrying in {state.retry} seconds </div>
        case AppStateT.Invalid:
          return <div>error: {state.error}</div>
        case AppStateT.Connected:
          return (
            <div className='view'>
              <div className='art' />
              <div className='page'>
                <Header send={state.socket.send} client={client} />
                <Body send={state.socket.send} boxes={client.boxes} />
              </div>
            </div>
          )
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

