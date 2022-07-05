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

import { Checkbox } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B, S, V } from './core';
import { Labeled } from './label';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';

const Container = styled.div`
  margin: 1rem 0;
`
export const Checklist = make(({ context, box }: BoxProps) => {
  const
    { text, options, live } = box,
    selecteds = selectedsOf(box),
    selection = new Set<S>(selecteds.map(s => String(s.value))),
    capture = () => context.record(Array.from(selection)),
    onChecked = (value?: V, checked?: B) => {
      if (checked) {
        selection.add(String(value))
      } else {
        selection.delete(String(value))
      }
      capture()
      if (live) context.commit()
    },
    render = () => {
      const
        checkboxes = options.map(c => (
          <Container key={c.value}>
            <Checkbox
              label={c.text}
              defaultChecked={selection.has(String(c.value))}
              onChange={(_, checked) => onChecked(c.value, checked)}
            />
          </Container>
        ))

      return (
        <Labeled label={text}><div>{checkboxes}</div></Labeled>
      )
    }

  capture()

  return { render }
})
