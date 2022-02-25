import React, { useRef, useEffect } from 'react';

import msgpack from '@ygoe/msgpack'

export type B = boolean
export type U = number
export type I = number
export type F = number
export type S = string
export type D = Date

type Output = {
  t: 0
  content: S
}
type Input = {
  t: 1
  caption: S
  value: S
}
type IO = Input | Output

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
  t: SocketEventT.Message, message: IO
}
const
  connectEvent: SocketEvent = { t: SocketEventT.Connect }

type SocketEventHandler = (e: SocketEvent) => void

type SendSocketData = (data: any) => void

const defer = (f: TimerHandler) => window.setTimeout(f, 0)

const
  toSocketAddress = (path: S): S => {
    const
      { protocol, host } = window.location,
      p = protocol === 'https:' ? 'wss' : 'ws'
    return p + "://" + host + path
  }
export const
  connect = (address: S, handle: SocketEventHandler): SendSocketData => {
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
          // const hash = window.location.hash
          // socket.send(`+ ${slug} ${hash.charAt(0) === '#' ? hash.substr(1) : hash}`) // protocol: t<sep>addr<sep>data
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
            const message = msgpack.deserialize(data) as IO
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
      }

    reconnect(toSocketAddress(address))

    return (data: any) => {
      defer(() => {
        if (_socket) _socket.send(msgpack.serialize(data ?? {}))
      })
    }
  }

export const App = () => {
  let send: SendSocketData | null = null
  useEffect(() => {
    if (!send) {
      const route = window.location.pathname
      const baseURL = document.getElementsByTagName('body')[0].getAttribute('data-baseurl') ?? '/'
      send = connect(`${baseURL}ws/ui?r=${route}`, (e) => {
        console.log('got event', e)
        switch (e.t) {
          case SocketEventT.Connect:
            if (send) send({ t: 'h', h: { language: window.navigator.language } })
            break
          case SocketEventT.Message:

            break
          case SocketEventT.Disconnect:
            break
          case SocketEventT.Error:
            console.error(e.error)
            break
        }
      })
    }
  })
  return <div>Hello!</div>
}
