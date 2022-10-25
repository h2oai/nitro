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

import { BoxProps } from './ui';
import { css } from './css';
import { useEffect, useRef } from 'react';
import { F, S } from './core';

const
  lerp = (f: F, a: F, b: F) => a * (1.0 - f) + (b * f),
  clamp1 = (f: F) => f < 0 ? 0 : f > 1 ? 1 : f,
  clamp1s = (fs: F[]) => fs.map(clamp1),
  makeLineY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 2) return ''
    const
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i], h, 0))
    return d.join(' ')
  },
  makeAreaY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 2) return ''
    const
      dx = w / (n - 1),
      d: Array<S | F> = []
    d.push('M', 0, h)
    for (let i = 0; i < n; i++) d.push('L', dx * i, lerp(ys[i], h, 0))
    d.push('L', w, h)
    d.push('Z')
    return d.join(' ')
  }
export const Graphic = ({ context, box }: BoxProps) => {
  const { modes, style, data } = box
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const div = ref.current
    if (div) {
      const
        rect = div.getBoundingClientRect(),
        w = Math.round(rect.width),
        h = Math.round(rect.height),
        { color } = window.getComputedStyle(div), // TODO stroke width
        svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')

      svg.setAttribute('viewBox', `0 0 ${w} ${h}`)
      svg.setAttribute('width', `${w}`)
      svg.setAttribute('height', `${h}`)

      if (modes.has('line-y')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeLineY(clamp1s(data as F[]), w, h));
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      } else if (modes.has('area-y')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeAreaY(clamp1s(data as F[]), w, h));
        path.setAttribute('fill', color);
        path.setAttribute('stroke', 'none');
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      }
      while (div.firstChild) div.removeChild(div.firstChild)
      div.appendChild(svg)
    }
  })
  return <div ref={ref} className={css(style)} />
}