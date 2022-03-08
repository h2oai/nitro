import React from 'react';
import { box, defer, isN, S, U, xid } from './core';
import { XWidgets } from './inputs';
import { Input, Msg, MsgType } from './protocol';
import { Client } from './client';
import { Socket, SocketEvent, SocketEventT } from './socket';
import { make } from './ui';

enum AppStateT { Connecting, Disconnected, Invalid, Input, Outputs }

type AppState = {
  t: AppStateT.Connecting
} | {
  t: AppStateT.Disconnected
  retry: U
} | {
  t: AppStateT.Invalid
  error: S
} | {
  t: AppStateT.Input
  socket: Socket
  inputs: Input[]
}

const hello: Msg = {
  t: MsgType.Join,
  d: {
    language: window.navigator.language, // XXX formalize
  }
}

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
                  const { inputs } = client
                  if (isN(position) && position >= 0 && position < inputs.length) {
                    inputs[position] = input
                  } else {
                    inputs.length = 0
                    inputs.push(input)
                  }
                  stateB({ t: AppStateT.Input, socket, inputs })
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
        case AppStateT.Input:
          return <XWidgets send={state.socket.send} widgets={state.inputs} />
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

