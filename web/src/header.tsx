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
import { Client } from './client';
import { signal, V } from './core';
import { toContextualMenuItem } from './options';
import { MsgType, Option } from './protocol';
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

export const Header = make(({ send, client }: { send: Send, client: Client }) => {
  const
    render = () => {
      const
        title = client.titleB(),
        caption = client.captionB(),
        menu = client.menuB() ?? [],
        nav = client.navB() ?? []

      return (
        <div className='header'>
          <Menu send={send} options={menu} />
          <div className='title'>{title}</div>
          <div className='caption'>{caption}</div>
          <NavBar send={send} options={nav} />
        </div>
      )
    }
  return { render }
})
