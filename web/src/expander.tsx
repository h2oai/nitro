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
import { S, signal } from './core';
import { css } from './css';
import { make } from './ui';

const
  down: IIconProps = { iconName: 'ChevronDownMed' },
  right: IIconProps = { iconName: 'ChevronRightMed' },
  open: React.CSSProperties = { display: 'block' },
  close: React.CSSProperties = { display: 'none' },
  buttonStyles: IButtonStyles = {
    root: { padding: 0 },
    label: { fontWeight: 600 },
  }

// TODO  mode=`expander`, mode=`open expander`
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
              iconProps={expanded ? down : right}
              onClick={toggle}
              styles={buttonStyles}
            >{headerText}</ActionButton>
          </div>
          <div className={css('pb-3 pl-8')} style={expanded ? open : close}>{children}</div>
        </div>
      )
    }
  return { render, expandedB }
})