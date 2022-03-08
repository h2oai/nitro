import { S } from './core'
import { Input } from './protocol'
import { connect, Socket, SocketEvent } from './socket'


export const newClient = (endpoint: S) => {
  const inputs: Input[] = []

  let _socket: Socket | null = null
  const socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
    if (_socket) return _socket
    return _socket = connect(endpoint, e => { if (_socket) handle(_socket, e) })
  }
  return {
    inputs,
    socket,
  }
}

export type Client = ReturnType<typeof newClient>
