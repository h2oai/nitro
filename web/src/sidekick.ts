import { Output } from './protocol'
import { connect, Socket, SocketEvent } from './socket'


export const newSidekick = () => {
  const outputs: Output[] = []

  let _socket: Socket | null = null
  const socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
    if (_socket) return _socket
    const route = window.location.pathname
    const baseURL = document.getElementsByTagName('body')[0].getAttribute('data-baseurl') ?? '/'
    return _socket = connect(`${baseURL}ws/f?r=${route}`, e => { if (_socket) handle(_socket, e) })
  }
  return {
    outputs,
    socket,
  }
}

export type Sidekick = ReturnType<typeof newSidekick>
