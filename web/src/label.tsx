import { Label, Stack } from '@fluentui/react';
import React from 'react';
import { S } from './core';


export const Labeled = ({ label, children }: { label?: S, children: JSX.Element }) => (
  label
    ? (
      <Stack>
        <Stack.Item>
          {label === ' ' ? <Label>&nbsp;</Label> : <Label>{label}</Label>}
        </Stack.Item>
        <Stack.Item>{children}</Stack.Item>
      </Stack>
    ) : (
      children
    )
)
