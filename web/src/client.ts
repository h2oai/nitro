import { S } from './core'
import { Conf, Input } from './protocol'
import { connect, Socket, SocketEvent } from './socket'


export const newClient = (endpoint: S) => {
  const inputs: Input[] = []
  const conf: Conf = {
    title: 'H2O Nitro',
    caption: 'v0.1.0', // XXX show actual version
    menu: [],
  }

  let _socket: Socket | null = null
  const socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
    if (_socket) return _socket
    return _socket = connect(endpoint, e => { if (_socket) handle(_socket, e) })
  }
  return {
    conf,
    inputs,
    socket,
  }
}

export type Client = ReturnType<typeof newClient>
