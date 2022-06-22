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

import msgpack from '@ygoe/msgpack';
import { defer, S } from "./core";
import { Message, Server, ServerEvent, ServerEventHandler, ServerEventT } from "./protocol";


const
  noopHandler: ServerEventHandler = () => { },
  connectEvent: ServerEvent = { t: ServerEventT.Connect },
  toSocketAddress = (path: S): S => {
    const
      { protocol, host } = window.location,
      p = protocol === 'https:' ? 'wss' : 'ws'
    return p + "://" + host + path
  },
  marshal = (data: any): Uint8Array => msgpack.serialize(data),
  unmarshal = (d: Uint8Array): Message => msgpack.deserialize(d)

export const newSocketServer = (address: S): Server => {
  let
    _socket: WebSocket | null = null,
    _backoff = 1,
    _handle = noopHandler

  const
    connect = (handle: ServerEventHandler) => {
      _handle = handle
      reconnect(toSocketAddress(address))
    },
    disconnect = () => {
      if (_socket) _socket.close()
    },
    reconnect = (address: S) => {
      const retry = () => reconnect(address)
      const socket = new WebSocket(address)
      socket.binaryType = 'arraybuffer'
      socket.onopen = () => {
        _socket = socket
        _handle(connectEvent)
        _backoff = 1
      }
      socket.onclose = (e) => {
        if (e.code === 1013) { // try again later
          return
        }
        _socket = null
        _backoff *= 2
        if (_backoff > 16) _backoff = 16
        _handle({ t: ServerEventT.Disconnect, retry: _backoff })
        window.setTimeout(retry, _backoff * 1000)
      }
      socket.onmessage = (e) => {
        const data = e.data
        if (!data) return
        try {
          const message = unmarshal(data)
          // console.log('recv', message)
          _handle({ t: ServerEventT.Message, message })
        } catch (error) {
          console.error(error)
          _handle({ t: ServerEventT.Error, error })
        }
      }
      socket.onerror = (error) => {
        console.error(error)
        _handle({ t: ServerEventT.Error, error })
      }
    },
    send = (message: Message) => {
      // console.log('send', message)
      defer(0, () => {
        if (_socket && message) _socket.send(marshal(message))
      })
    }

  return { connect, send, disconnect }
}
