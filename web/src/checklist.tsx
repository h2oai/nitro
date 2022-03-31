import { Checkbox } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B, S, V } from './core';
import { Labeled } from './label';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';

const Container = styled.div`
  margin: 0.5rem 0;
`
export const Checklist = make(({ context, box }: BoxProps) => {
  const
    { index, text, options } = box,
    selecteds = selectedsOf(box),
    selection = new Set<S>(selecteds.map(s => String(s.value))),
    capture = () => context.capture(index, Array.from(selection)),
    onChecked = (value?: V, checked?: B) => {
      if (checked) {
        selection.add(String(value))
      } else {
        selection.delete(String(value))
      }
      capture()
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
