import msgpack from '@ygoe/msgpack';
import { S, U, defer } from "./core"
import { Msg } from "./protocol"

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

export type Send = (message: Msg) => void

export type Socket = {
  send: Send
  disconnect(): void
}

const connectEvent: SocketEvent = { t: SocketEventT.Connect }

type SocketEventHandler = (e: SocketEvent) => void

const toSocketAddress = (path: S): S => {
  const
    { protocol, host } = window.location,
    p = protocol === 'https:' ? 'wss' : 'ws'
  return p + "://" + host + path
}

const marshal = (data: any): Uint8Array => msgpack.serialize(data)

const unmarshal = (d: Uint8Array): Msg => msgpack.deserialize(d)

export const connect = (address: S, handle: SocketEventHandler): Socket => {
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
          console.log('recv', message) // XXX remove
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
    send = (message: any) => {
      console.log('send', message) // XXX remove
      defer(0, () => {
        if (_socket && message) _socket.send(marshal(message))
      })
    }

  reconnect(toSocketAddress(address))

  return { send, disconnect }
}
