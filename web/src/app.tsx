import React from 'react';
import { box, defer, S, U, xid } from './core';
import { XInputView } from './inputs';
import { ErrCode, Input, Msg, MsgOp, MsgType, Output } from './protocol';
import { Sidekick } from './sidekick';
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
  input: Input
} | {
  t: AppStateT.Outputs
  outputs: Output[]
}

const hello: Msg = {
  t: MsgType.Join,
  d: {
    language: window.navigator.language, // XXX formalize
  }
}

const XOutputView = ({ outputs }: { outputs: Output[] }) => {
  return <div>output</div>
}

export const App = make(({ sidekick }: { sidekick: Sidekick }) => {
  const
    stateB = box<AppState>({ t: AppStateT.Connecting }),
    onMessage = (socket: Socket, e: SocketEvent) => {
      switch (e.t) {
        case SocketEventT.Connect:
          if (socket) socket.send(MsgOp.Message, hello)
          break
        case SocketEventT.Message:
          {
            const msg = e.message
            switch (msg.t) {
              case MsgType.Error:
                const { c: code } = msg
                switch (code) {
                  case ErrCode.BadOp:
                    stateB({ t: AppStateT.Invalid, error: 'unknown operation' })
                    break
                  case ErrCode.PeerDead:
                    stateB({ t: AppStateT.Invalid, error: 'remote died' })
                    break
                  case ErrCode.PeerUnavailable:
                    stateB({ t: AppStateT.Invalid, error: 'remote unavailable, retrying in 10 seconds' })
                    defer(10, () => { if (socket) socket.send(MsgOp.Message, hello) })
                    break
                  case ErrCode.RateLimited:
                    stateB({ t: AppStateT.Invalid, error: 'rate limited' })
                    break
                  default:
                    stateB({ t: AppStateT.Invalid, error: `unhandled error code ${code}` })
                }
                break
              case MsgType.Read:
                {
                  const input = msg.d
                  input.xid = xid()
                  sidekick.outputs.length = 0
                  stateB({ t: AppStateT.Input, socket, input })
                }
                break
              case MsgType.Write:
                {
                  const output = msg.d
                  output.xid = xid()
                  const outputs = sidekick.outputs
                  outputs.length = 0
                  outputs.push(output)
                  stateB({ t: AppStateT.Outputs, outputs })
                }
                break
              case MsgType.Append:
                {
                  const output = msg.d
                  output.xid = xid()
                  const outputs = sidekick.outputs
                  outputs.push(output)
                  stateB({ t: AppStateT.Outputs, outputs })
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
      sidekick.socket(onMessage)
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
          return <XInputView send={state.socket.send} input={state.input} />
        case AppStateT.Outputs:
          return <XOutputView outputs={state.outputs} />
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

