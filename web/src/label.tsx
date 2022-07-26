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

import { Label } from '@fluentui/react';
import React from 'react';
import { B } from './core';
import { css } from './css';
import { Box } from './protocol';

export const FormItem = ({ box, children }: { box: Box, children: React.ReactNode }) => (
  <div className={css('flex flex-col', box.style)}>
    {children}
  </div>
)

export const Labeled = ({ box, offset, children }: { box: Box, offset?: B, children: React.ReactNode }) => (
  <FormItem box={box}>
    {box.text
      ? <Label>{box.text}</Label>
      : offset
        ? <Label>&nbsp;</Label>
        : null}
    {children}
  </FormItem>
)
