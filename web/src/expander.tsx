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

import { ActionButton, IButtonStyles, IIconProps } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { S, signal } from './core';
import { make } from './ui';

const
  iconOpen: IIconProps = { iconName: 'ChevronDownMed' },
  iconClose: IIconProps = { iconName: 'ChevronRightMed' },
  bodyOpenStyle: React.CSSProperties = { display: 'block' },
  bodyCloseStyle: React.CSSProperties = { display: 'none' },
  buttonStyles: IButtonStyles = { root: { padding: 0 } }

const
  Body = styled.div`
    padding: 0 0 10px 30px;
  `

export const Expander = make(({ headerText, children }: { headerText: S, children: JSX.Element }) => {
  const
    expandedB = signal(false),
    toggle = () => expandedB(!expandedB()),
    render = () => {
      const expanded = expandedB()
      return (
        <div>
          <div>
            <ActionButton
              iconProps={expanded ? iconOpen : iconClose}
              onClick={toggle}
              styles={buttonStyles}
            >{headerText}</ActionButton>
          </div>
          <Body style={expanded ? bodyOpenStyle : bodyCloseStyle}>{children}</Body>
        </div>
      )
    }
  return { render, expandedB }
})