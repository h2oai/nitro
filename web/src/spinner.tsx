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

import { Spinner as FSpinner, SpinnerLabelPosition } from '@fluentui/react';
import { BoxProps } from './ui';

export const Spinner = ({ box }: BoxProps) => {
  const
    { text, align } = box,
    labelPosition: SpinnerLabelPosition | undefined = align === 'left'
      ? 'left'
      : align === 'right'
        ? 'right'
        : align === 'top'
          ? 'top'
          : align === 'bottom'
            ? 'bottom'
            : undefined

  return (
    <FSpinner label={text ?? undefined} labelPosition={labelPosition} />
  )
}



