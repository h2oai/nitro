import { CommandBar, ContextualMenu } from '@fluentui/react';
import { GlobalNavButtonActiveIcon, GlobalNavButtonIcon, RocketIcon } from '@fluentui/react-icons-mdl2';
import React from 'react';
import styled from 'styled-components';
import { signal, V } from './core';
import { toContextualMenuItem } from './options';
import { Conf, MsgType, Option } from './protocol';
import { Send } from './socket';
import { make } from './ui';

const HeaderContainer = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
`
const HeaderTitle = styled.div` 
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1rem;
  color: #555;
  margin-left: 0.5rem;
`
const HeaderSubtitle = styled.div`
  font-weight: 400;
  color: #999;
  margin-left: 0.5rem;
`
const MenuContainer = styled.div`
  cursor: pointer;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
`
const XMenu = make(({ send, options }: { send: Send, options: Option[] }) => {
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
const NavBar = styled.div`
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
`

const XCommandBar = make(({ send, options }: { send: Send, options: Option[] }) => {
  const
    switchTo = (v: V) => {
      send({ t: MsgType.Switch, d: v })
    },
    items = options.map(o => toContextualMenuItem(o, switchTo)),
    render = () => (
      <CommandBar items={items} />
    )
  return { render }
})

export const Header = make(({ send, conf }: { send: Send, conf: Conf }) => {
  const
    render = () => {
      return (
        <HeaderContainer>
          <XMenu send={send} options={conf.menu ?? []} />
          <HeaderTitle>{conf.title}</HeaderTitle>
          <HeaderSubtitle>{conf.caption}</HeaderSubtitle>
          <NavBar>
            <XCommandBar send={send} options={conf.nav ?? []} />
          </NavBar>
        </HeaderContainer>
      )
    }
  return { render }
})
