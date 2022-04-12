import { Checkbox as FCheckbox } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B } from './core';
import { BoxProps, make } from './ui';

const Container = styled.div`
  margin: 0.5rem 0;
`
export const Checkbox = make(({ context, box }: BoxProps) => {
  const
    { index, value, text } = box,
    onChecked = (checked?: B) => {
      context.capture(index, checked ? true : false)
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

