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

import { on, S, signal } from './core'
import { Box, Option } from './protocol'
import { connect, Socket, SocketEvent } from './socket'
import { defaultScheme, loadScheme } from './theme'
import { noopClientContext } from './ui'


export const newClient = (endpoint: S) => {
  let _socket: Socket | null = null
  const
    body: Box[] = [],
    popup: Box[] = [],
    titleB = signal('H2O Nitro'),
    captionB = signal('v0.1.0'),
    menuB = signal<Option[]>([]),
    navB = signal<Option[]>([]),
    schemeB = signal(defaultScheme),
    context = noopClientContext,
    socket = (handle: (s: Socket, e: SocketEvent) => void): Socket => {
      if (_socket) return _socket
      return _socket = connect(endpoint, e => {
        if (_socket) handle(_socket, e)
      })
    }

  on(titleB, title => document.title = title)
  on(schemeB, scheme => window.setTimeout(() => loadScheme(scheme), 100))

  return {
    titleB,
    captionB,
    menuB,
    navB,
    schemeB,
    body,
    popup,
    socket,
    context,
  }
}

export type Client = ReturnType<typeof newClient>
