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

import React from 'react';
import { B, Dict, Disposable, isSignal, on, V } from './core';
import { Box, MsgType } from './protocol';
import { Send } from './socket';

export const newCaptureContext = (send: Send, data: Array<V | V[]>) => {
  const capture = <T extends V | V[]>(index: any, value: T) => {
    if (index >= 0) data[index] = value
  }
  const submit = () => send({ t: MsgType.Input, d: data })
  return { capture, submit }
}

export type Context = ReturnType<typeof newCaptureContext>

export type BoxProps = { context: Context, box: Box }

interface Renderable {
  render(): JSX.Element
  init?(): void
  update?(): void
  dispose?(): void
}

const reserved: Dict<B> = {
  render: true,
  dispose: true,
  init: true,
  update: true,
}

export function make<TProps, TState extends Renderable>(ctor: (props: TProps) => TState) {
  return class extends React.Component<TProps> {
    private readonly model: TState
    private readonly arrows: Disposable[]
    constructor(props: TProps) {
      super(props)

      const
        // eslint-disable-next-line @typescript-eslint/no-this-alias
        self = this,
        model = ctor(props),
        arrows: Disposable[] = [],
        initialState: Dict<any> = {}

      Object.keys(model).forEach(k => {
        if (reserved[k]) return
        const v = (model as any)[k]
        if (isSignal(v)) {
          initialState[k] = v()
          arrows.push(on(v, v => {
            const newState: Dict<any> = {}
            newState[k] = v
            self.setState(newState)
          }))
        }
      })

      this.model = model
      this.arrows = arrows
      this.state = initialState
    }
    componentDidMount() {
      if (this.model.init) this.model.init()
    }
    componentDidUpdate() {
      if (this.model.update) this.model.update()
    }
    componentWillUnmount() {
      if (this.model.dispose) this.model.dispose()
      for (const a of this.arrows) a.dispose()
    }
    render() {
      return this.model.render()
    }
  }
}
