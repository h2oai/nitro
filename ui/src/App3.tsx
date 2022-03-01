import React, { useRef, useEffect, useState } from 'react';

import msgpack from '@ygoe/msgpack'

export type B = boolean
export type U = number
export type I = number
export type F = number
export type S = string
export type D = Date

type Output = {
  xid: S
  content: S
}

type Input = {
  xid: S
  caption: S
  value: S
}

enum MsgType {
  Error = 1,
  Join,
  Leave,
  Request,
  Response,
  Watch,
  Event,
  Text,
  Input,
  Abort,
  Resume,
  Read,
  Write,
  Append,
}

enum ErrCode {
  PeerUnavailable = 1,
  PeerDead,
  RateLimited,
  BadOp,
}

type Msg = {
  t: MsgType.Error
  c: ErrCode
} | {
  t: MsgType.Join
  d: any // XXX formalize
} | {
  t: MsgType.Read
  d: Input
} | {
  t: MsgType.Write
  d: Output
} | {
  t: MsgType.Append
  d: Output
}

export enum SocketEventT {
  Connect,
  Disconnect,
  Message,
  Error,
}

export type SocketEvent = {
  t: SocketEventT.Connect
} | {
  t: SocketEventT.Disconnect, retry: U
} | {
  t: SocketEventT.Error, error: any
} | {
  t: SocketEventT.Message, message: Msg
}
const connectEvent: SocketEvent = { t: SocketEventT.Connect }

type SocketEventHandler = (e: SocketEvent) => void

enum MsgOp { Control = 1, Message }

const defer = (seconds: U, f: TimerHandler) => window.setTimeout(f, seconds * 1000)

const toSocketAddress = (path: S): S => {
  const
    { protocol, host } = window.location,
    p = protocol === 'https:' ? 'wss' : 'ws'
  return p + "://" + host + path
}

const marshal = (op: MsgOp, data: any): Uint8Array => {
  const m = msgpack.serialize(data)
  const d = new Uint8Array(1 + m.length)
  d.set([op], 0) // 1-byte header
  d.set(m, 1) // append message
  return d
}
const unmarshal = (d: Uint8Array): Msg => msgpack.deserialize(d)
type Socket = {
  send(op: MsgOp, message: Msg): void
  disconnect(): void
}
export const
  connect = (address: S, handle: SocketEventHandler): Socket => {
    let
      _socket: WebSocket | null = null,
      _backoff = 1

    const
      disconnect = () => {
        if (_socket) _socket.close()
      },
      reconnect = (address: S) => {
        const retry = () => reconnect(address)
        const socket = new WebSocket(address)
        socket.binaryType = 'arraybuffer'
        socket.onopen = () => {
          _socket = socket
          handle(connectEvent)
          _backoff = 1
        }
        socket.onclose = (e) => {
          if (e.code === 1013) { // try again later
            return
          }
          _socket = null
          _backoff *= 2
          if (_backoff > 16) _backoff = 16
          handle({ t: SocketEventT.Disconnect, retry: _backoff })
          window.setTimeout(retry, _backoff * 1000)
        }
        socket.onmessage = (e) => {
          const data = e.data
          if (!data) return
          try {
            const message = unmarshal(data)
            handle({ t: SocketEventT.Message, message })
          } catch (error) {
            console.error(error)
            handle({ t: SocketEventT.Error, error })
          }
        }
        socket.onerror = (error) => {
          console.error(error)
          handle({ t: SocketEventT.Error, error })
        }
      },
      send = (op: MsgOp, data: any) => {
        defer(0, () => {
          if (_socket && data) _socket.send(marshal(op, data))
        })
      }

    reconnect(toSocketAddress(address))

    return { send, disconnect }
  }

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

// let socket: Socket | null = null
const hello: Msg = {
  t: MsgType.Join,
  d: {
    language: window.navigator.language,
  }
}

const idgen = (prefix: S, initial = 0) => {
  let _id = initial
  return () => prefix + _id++
}

export const newSidekick = () => {
  const outputs: Output[] = []

  let _socket: Socket | null = null
  const socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
    if (_socket) return _socket
    const route = window.location.pathname
    const baseURL = document.getElementsByTagName('body')[0].getAttribute('data-baseurl') ?? '/'
    return _socket = connect(`${baseURL}ws/f?r=${route}`, e => { if (_socket) handle(_socket, e) })
  }
  const xid = idgen('x')
  return {
    xid,
    outputs,
    socket,
  }
}

type Sidekick = ReturnType<typeof newSidekick>

const Input = ({ socket, input }: { socket: Socket, input: Input }) => {
  return <div>{JSON.stringify(input)}</div>
}

const Outputs = ({ outputs }: { outputs: Output[] }) => {
  return <div>output</div>
}

export const App = ({ sidekick }: { sidekick: Sidekick }) => {
  const [state, stateB] = useState<AppState>({ t: AppStateT.Connecting })
  const onMessage = (socket: Socket, e: SocketEvent) => {
    console.log('got event', e)
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
                input.xid = sidekick.xid()
                sidekick.outputs.length = 0
                stateB({ t: AppStateT.Input, socket, input })
              }
              break
            case MsgType.Write:
              {
                const output = msg.d
                output.xid = sidekick.xid()
                const outputs = sidekick.outputs
                outputs.length = 0
                outputs.push(output)
                stateB({ t: AppStateT.Outputs, outputs })
              }
              break
            case MsgType.Append:
              {
                const output = msg.d
                output.xid = sidekick.xid()
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
  }
  useEffect(() => { sidekick.socket(onMessage) }, [sidekick])
  switch (state.t) {
    case AppStateT.Connecting:
      return <div>connecting</div>
    case AppStateT.Disconnected:
      return <div>disconnected, retrying in {state.retry} seconds </div>
    case AppStateT.Invalid:
      return <div>error: {state.error}</div>
    case AppStateT.Input:
      return <Input socket={state.socket} input={state.input} />
    case AppStateT.Outputs:
      return <Outputs outputs={state.outputs} />
  }
  return <div>Hello!</div>
}
