import { Toggle as FToggle } from '@fluentui/react';
import React from 'react';
import styled from 'styled-components';
import { B } from './core';
import { BoxProps, make } from './ui';

const Container = styled.div`
  margin: 0.5rem 0;
`
export const Toggle = make(({ context, box }: BoxProps) => {
    const
        { index, value, text } = box,
        onChecked = (checked?: B) => {
            context.capture(index, checked ? true : false)
            context.submit()
        },
        render = () => {
            return (
                <Container>
                    <FToggle
                        label={text}
                        defaultChecked={value ? true : false}
                        onChange={(_, checked) => onChecked(checked)}
                        inlineLabel
                    />
                </Container>
            )
        }

    context.capture(index, value ? true : false)

    return { render }
})


