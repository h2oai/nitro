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

import { Checkbox as FCheckbox } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B } from './core';
import { BoxProps, make } from './ui';

const Container = styled.div`
  margin: 0.5rem 0;
`
export const Checkbox = make(({ box }: BoxProps) => {
  const
    { context, value, text } = box,
    onChecked = (checked?: B) => {
      context.record(checked ? true : false)
    },
    render = () => {
      return (
        <Container>
          <FCheckbox
            label={text}
            defaultChecked={value ? true : false}
            onChange={(_, checked) => onChecked(checked)}
          />
        </Container>
      )
    }

  onChecked(value ? true : false)

  return { render }
})

