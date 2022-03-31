import { Rating } from '@fluentui/react';
import React from 'react';
import { isN, unum } from './core';
import { Labeled } from './label';
import { BoxProps, make } from './ui';


export const XRating = make(({ context, box }: BoxProps) => {
  const
    { index, text, placeholder, min, max, value } = box,
    allowZeroStars = isN(min) && min <= 0,
    defaultRating = unum(value) ?? (allowZeroStars ? 0 : 1),
    onChange = (event: React.FormEvent<HTMLElement>, rating?: number) => {
      if (rating === undefined) return
      context.capture(index, rating)
    },
    render = () => {
      return (
        <Labeled label={text}>
          <Rating
            defaultRating={defaultRating}
            allowZeroStars={allowZeroStars}
            max={unum(max)}
            onChange={onChange}
            placeholder={placeholder}
          />
        </Labeled>
      )
    }

  context.capture(index, defaultRating)

  return { render }
})
