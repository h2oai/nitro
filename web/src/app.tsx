import React from 'react';
import { box, defer, isN, S, U, xid } from './core';
import { AppContainer, Header, XWidgets } from './inputs';
import { Input, Msg, MsgType, Conf } from './protocol';
import { Client } from './client';
import { Socket, SocketEvent, SocketEventT } from './socket';
import { make } from './ui';
import styled from 'styled-components';

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
  inputs: Input[]
  conf: Conf
}

const hello: Msg = {
  t: MsgType.Join,
  d: {
    language: window.navigator.language, // XXX formalize
  }
}

// TODO make configurable
// Source: https://projects.verou.me/css3patterns/#tartan
const Texture = styled.div`
  height: 1.5rem;
  background-color: hsl(2, 57%, 40%);
  background-image: repeating-linear-gradient(transparent, transparent 50px, rgba(0,0,0,.4) 50px, rgba(0,0,0,.4) 53px, transparent 53px, transparent 63px, rgba(0,0,0,.4) 63px, rgba(0,0,0,.4) 66px, transparent 66px, transparent 116px, rgba(0,0,0,.5) 116px, rgba(0,0,0,.5) 166px, rgba(255,255,255,.2) 166px, rgba(255,255,255,.2) 169px, rgba(0,0,0,.5) 169px, rgba(0,0,0,.5) 179px, rgba(255,255,255,.2) 179px, rgba(255,255,255,.2) 182px, rgba(0,0,0,.5) 182px, rgba(0,0,0,.5) 232px, transparent 232px),
  repeating-linear-gradient(270deg, transparent, transparent 50px, rgba(0,0,0,.4) 50px, rgba(0,0,0,.4) 53px, transparent 53px, transparent 63px, rgba(0,0,0,.4) 63px, rgba(0,0,0,.4) 66px, transparent 66px, transparent 116px, rgba(0,0,0,.5) 116px, rgba(0,0,0,.5) 166px, rgba(255,255,255,.2) 166px, rgba(255,255,255,.2) 169px, rgba(0,0,0,.5) 169px, rgba(0,0,0,.5) 179px, rgba(255,255,255,.2) 179px, rgba(255,255,255,.2) 182px, rgba(0,0,0,.5) 182px, rgba(0,0,0,.5) 232px, transparent 232px),
  repeating-linear-gradient(125deg, transparent, transparent 2px, rgba(0,0,0,.2) 2px, rgba(0,0,0,.2) 3px, transparent 3px, transparent 5px, rgba(0,0,0,.2) 5px);
`
export const App = make(({ client }: { client: Client }) => {
  const
    stateB = box<AppState>({ t: AppStateT.Connecting }),
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
                  const { d: input, p: position } = msg
                  input.xid = xid()
                  const { conf, inputs } = client
                  if (isN(position) && position >= 0 && position < inputs.length) {
                    inputs[position] = input
                  } else {
                    inputs.length = 0
                    inputs.push(input)
                  }
                  stateB({ t: AppStateT.Connected, socket, conf, inputs })
                }
                break
              case MsgType.Conf:
                {
                  const { d: conf } = msg
                  client.conf = conf
                  const state = stateB()
                  if (state.t === AppStateT.Connected) {
                    const { conf, inputs } = client
                    stateB({ t: AppStateT.Connected, socket, conf, inputs })
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
            <div>
              <Texture />
              <AppContainer>
                <Header send={state.socket.send} conf={state.conf} />
                <XWidgets send={state.socket.send} widgets={state.inputs} />
              </AppContainer>
            </div>
          )
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

