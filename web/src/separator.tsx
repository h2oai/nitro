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

import { Separator as FSeparator } from '@fluentui/react';
import { css } from './css';
import { BoxProps } from './ui';

export const Separator = ({ box }: BoxProps) => {
  const
    { name, text, modes, style } = box,
    vertical = modes.has('top') || modes.has('middle') || modes.has('bottom'),
    align = (modes.has('left') || modes.has('top'))
      ? 'start'
      : (modes.has('right') || modes.has('bottom'))
        ? 'end'
        : undefined

  return (
    <div className={css(style)} data-name={name}>
      <FSeparator vertical={vertical} alignContent={align} >{text}</FSeparator>
    </div>
  )
}


