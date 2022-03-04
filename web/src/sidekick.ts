import { Input } from './protocol'
import { connect, Socket, SocketEvent } from './socket'


export const newSidekick = () => {
  const inputs: Input[] = []

  let _socket: Socket | null = null
  const socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
    if (_socket) return _socket
    const baseURL = document.getElementsByTagName('body')[0].getAttribute('data-baseurl') ?? '/'
    return _socket = connect(`${baseURL}sidekick`, e => { if (_socket) handle(_socket, e) })
  }
  return {
    inputs,
    socket,
  }
}

export type Sidekick = ReturnType<typeof newSidekick>
