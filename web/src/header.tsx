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

import { CommandBar, ContextualMenu } from '@fluentui/react';
import { GlobalNavButtonActiveIcon, GlobalNavButtonIcon, RocketIcon } from '@fluentui/react-icons-mdl2';
import React from 'react';
import styled from 'styled-components';
import { signal, V } from './core';
import { toContextualMenuItem } from './options';
import { Conf, MsgType, Option } from './protocol';
import { Send } from './socket';
import { make } from './ui';

const MenuContainer = styled.div`
  cursor: pointer;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
`

const Menu = make(({ send, options }: { send: Send, options: Option[] }) => {
  const
    hasMenu = options.length > 0,
    switchTo = (v: V) => {
      send({ t: MsgType.Switch, d: v })
    },
    items = options.map(o => toContextualMenuItem(o, switchTo)),
    containerRef = React.createRef<HTMLDivElement>(),
    showMenuB = signal(false),
    showMenu = () => showMenuB(true),
    hideMenu = () => showMenuB(false),
    render = () => {
      const isMenuVisible = showMenuB()
      return (
        <MenuContainer ref={containerRef} onClick={showMenu}>
          {
            hasMenu
              ? isMenuVisible
                ? <GlobalNavButtonActiveIcon />
                : <GlobalNavButtonIcon />
              : <RocketIcon />
          }
          <ContextualMenu
            items={items}
            hidden={!isMenuVisible}
            target={containerRef}
            onItemClick={hideMenu}
            onDismiss={hideMenu}
          />
        </MenuContainer>
      )
    }
  return { render, showMenuB }
})

const NavBarContainer = styled.div`
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
`

const NavBar = make(({ send, options }: { send: Send, options: Option[] }) => {
  const
    switchTo = (v: V) => {
      send({ t: MsgType.Switch, d: v })
    },
    items = options.map(o => toContextualMenuItem(o, switchTo)),
    render = () => (
      <NavBarContainer>
        <CommandBar items={items} />
      </NavBarContainer>
    )
  return { render }
})

const Container = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
`
const Title = styled.div` 
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1rem;
  color: #555;
  margin-left: 0.5rem;
`
const Subtitle = styled.div`
  font-weight: 400;
  color: #999;
  margin-left: 0.5rem;
`

export const Header = make(({ send, conf }: { send: Send, conf: Conf }) => {
  const
    render = () => {
      return (
        <Container>
          <Menu send={send} options={conf.menu ?? []} />
          <Title>{conf.title}</Title>
          <Subtitle>{conf.caption}</Subtitle>
          <NavBar send={send} options={conf.nav ?? []} />
        </Container>
      )
    }
  return { render }
})
