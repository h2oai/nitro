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
import { B, Dict, Disposable, isSignal, on, S } from './core';
import { Box, Input, InputValue, MsgType } from './protocol';
import { Send } from './socket';

export type CaptureContext = {
  scoped(index: any, xid: S): Context
  record(index: any, xid: S, value: InputValue): void
  submit(): void
}

export type Context = {
  record(value: InputValue): void
  submit(): void
}

export const noopContext: Context = {
  record: (_: InputValue) => { },
  submit: () => { }
}

export const newCaptureContext = (send: Send): CaptureContext => {
  const
    data: Array<Input> = [],
    record = (index: any, xid: S, value: InputValue) => {
      if (index >= 0) data[index] = [xid, value]
    },
    submit = () => send({ t: MsgType.Input, d: data.filter(e => e !== undefined) }),
    scoped = (index: any, xid: S): Context => ({
      record: (value: InputValue) => record(index, xid, value),
      submit,
    })

  return { record, submit, scoped }
}

export type BoxProps = { box: Box }

export type StyledBoxProps = BoxProps & { style: React.CSSProperties }
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
