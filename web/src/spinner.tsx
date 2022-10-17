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

import { Spinner as FSpinner } from '@fluentui/react';
import { css } from './css';
import { BoxProps } from './ui';

// TODO add size variants 
export const Spinner = ({ box }: BoxProps) => {
  const
    { name, text, modes, style } = box,
    labelPosition = modes.has('top')
      ? 'bottom'
      : modes.has('right')
        ? 'left'
        : modes.has('left')
          ? 'right'
          : modes.has('bottom')
            ? 'top'
            : undefined

  return (
    <div className={css(style)} data-name={name}>
      <FSpinner label={text ?? undefined} labelPosition={labelPosition} />
    </div>
  )
}



