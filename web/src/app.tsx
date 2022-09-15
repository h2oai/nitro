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

import { FontIcon } from '@fluentui/react';
import React from 'react';
import { Body, Popup } from './body';
import { Client, ClientStateT } from './client';
import { S, signal, U } from './core';
import { css } from './css';
import { Header } from './header';
import { HelpPanel } from './help';
import loadingAnimation from './loading.gif';
import { make } from './ui';

const Busy = make(({ timeout }: { timeout: U }) => {
  const
    visibleB = signal(false),
    render = () => (
      <div
        className={css('absolute inset-0 flex flex-col justify-center items-center bg-black opacity-0 transition-opacity')}
        style={{ zIndex: 1000, opacity: visibleB() ? 0.5 : 0 }}
      >
        <img alt='Busy' src={loadingAnimation} />
      </div>
    )

  setTimeout(() => { visibleB(true) }, timeout)

  return { render, visibleB }
})

const Signage = ({ title, icon, children }: { title: S, icon: S, children: React.ReactNode }) => (
  <div className={css('absolute inset-0 flex justify-center items-center')}>
    <div className={css('flex gap-4')}>
      <FontIcon className={css('text-5xl text-red-500 animate-pulse')} iconName={icon} />
      <div className={css('')}>
        <div className={css('text-4xl font-black tracking-tight')}>{title}</div>
        <div className='prose'>{children}</div>
      </div>
    </div>
  </div>
)

export const App = make(({ client }: { client: Client }) => {
  const
    { stateB } = client,
    init = () => {
      client.connect()
    },
    render = () => {
      const state = stateB()
      switch (state.t) {
        case ClientStateT.Connecting:
          return (
            <Busy timeout={500000} />
          )
        case ClientStateT.Disconnected:
          return (
            <Signage title='Disconnected' icon='PlugDisconnected'>Retrying in {state.retry} seconds...</Signage>
          )
        case ClientStateT.Invalid:
          {
            const
              { error, trace } = state,
              body = trace ? (
                <>
                  <p>{error}</p>
                  <pre>
                    <code>{trace}</code>
                  </pre>
                </>
              ) : (
                <p>{error}</p>
              )
            return (<Signage title='Error' icon='Error'>{body}</Signage>)
          }
        case ClientStateT.Connected:
          const
            { popup, busyB, modeB } = client,
            isChromeless = modeB() === 'chromeless'
          return (
            <>
              {busyB() && <Busy timeout={500} />}
              <HelpPanel helpE={client.helpE} helpB={client.helpB} />
              <div className='view'>
                {!isChromeless && <div className='stripe' />}
                <div className={css('max-w-3xl mx-auto')}>
                  {!isChromeless && <Header client={client} />}
                  <Body client={client} />
                  {popup.length ? <Popup client={client} /> : <></>}
                </div>
              </div>
            </>
          )
      }
      return <div>Hello!</div>
    }
  return { init, render, stateB }
})

