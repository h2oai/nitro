import { loadTheme } from '@fluentui/react'
import { S, on, signal } from './core'
import { Box, Option } from './protocol'
import { connect, Socket, SocketEvent } from './socket'
import { defaultScheme, loadScheme } from './theme'


export const newClient = (endpoint: S) => {
  let _socket: Socket | null = null
  const
    boxes: Box[] = [],
    titleB = signal('H2O Nitro'),
    captionB = signal('v0.1.0'),
    menuB = signal<Option[]>([]),
    navB = signal<Option[]>([]),
    schemeB = signal(defaultScheme),
    socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
      if (_socket) return _socket
      return _socket = connect(endpoint, e => {
        if (_socket) handle(_socket, e)
      })
    }

  on(titleB, title => document.title = title)
  on(schemeB, scheme => loadScheme(scheme))

  return {
    titleB,
    captionB,
    menuB,
    navB,
    schemeB,
    boxes,
    socket,
  }
}

export type Client = ReturnType<typeof newClient>
