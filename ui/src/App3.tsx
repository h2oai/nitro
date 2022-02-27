import React, { useRef, useEffect, useState } from 'react';

import msgpack from '@ygoe/msgpack'

export type B = boolean
export type U = number
export type I = number
export type F = number
export type S = string
export type D = Date

type Output = {
  content: S
}
type Input = {
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

enum AppStateT { Connecting, Disconnected, Valid, Invalid }

type AppState = {
  t: AppStateT.Connecting
} | {
  t: AppStateT.Disconnected
  retry: U
} | {
  t: AppStateT.Invalid
  error: S
} | {
  t: AppStateT.Valid
}

let socket: Socket | null = null
const hello: Msg = {
  t: MsgType.Join,
  d: {
    language: window.navigator.language,
  }
}
export const App = () => {
  const [state, stateB] = useState<AppState>({ t: AppStateT.Connecting })
  const onMessage = (e: SocketEvent) => {
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
              break
            case MsgType.Write:
              break
            case MsgType.Append:
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
  useEffect(() => {
    if (!socket) {
      const route = window.location.pathname
      const baseURL = document.getElementsByTagName('body')[0].getAttribute('data-baseurl') ?? '/'
      socket = connect(`${baseURL}ws/f?r=${route}`, onMessage)
    }
  })
  switch (state.t) {
    case AppStateT.Connecting:
      return <div>connecting</div>
    case AppStateT.Disconnected:
      return <div>disconnected, retrying in {state.retry} seconds </div>
    case AppStateT.Invalid:
      return <div>{state.error}</div>
  }
  return <div>Hello!</div>
}
