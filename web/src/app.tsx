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

import styled from 'styled-components';
import { Body, Popup } from './body';
import { Client, ClientStateT } from './client';
import { signal, U } from './core';
import { Header } from './header';
import { HelpPanel } from './help';
import loadingAnimation from './loading.gif';
import { make } from './ui';

const Overlay = styled.div`
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`
const Danger = styled.div`
  text-align: center;
  padding: 2rem;
  font-size: 2rem;
  color: #842029;
  background-color: #f8d7da;
  border: 1px solid #f5c2c7;
`
const Warning = styled.div`
  text-align: center;
  padding: 2rem;
  font-size: 2rem;
  color: #664d03;
  background-color: #fff3cd;
  border: 1px solid #ffecb5;
`
const Blocker = styled(Overlay)`
  z-index: 1000;
  background-color: #000;
  opacity: 0;
  transition: opacity 0.3s
`

const Busy = make(({ timeout }: { timeout: U }) => {
  const
    visibleB = signal(false),
    render = () => (
      <Blocker style={{ opacity: visibleB() ? 0.5 : 0 }}>
        <img alt='Busy' src={loadingAnimation} />
      </Blocker>
    )

  setTimeout(() => { visibleB(true) }, timeout)

  return { render, visibleB }
})

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
            <Busy timeout={100} />
          )
        case ClientStateT.Disconnected:
          return (
            <Overlay>
              <Warning>Disconnected, retrying in {state.retry} seconds...</Warning>
            </Overlay>
          )
        case ClientStateT.Invalid:
          return (
            <Overlay>
              <Danger>Error: {state.error}</Danger>
            </Overlay>
          )
        case ClientStateT.Connected:
          const
            { popup, busy, modeB } = client,
            isChromeless = modeB() === 'chromeless'

          return (
            <>
              {busy && <Busy timeout={500} />}
              <HelpPanel helpE={client.helpE} />
              <div className='view'>
                {!isChromeless && <div className='art' />}
                <div className='page'>
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

