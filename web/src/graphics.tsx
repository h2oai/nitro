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
import { F, isN, S } from './core';

type PathD = Array<S | F>

const
  lerp = (f: F, a: F, b: F) => a * (1.0 - f) + (b * f),
  clamp1 = (f: F) => f < 0 ? 0 : f > 1 ? 1 : f,
  clamp1s = (fs: F[]) => fs.map(clamp1),
  newPath = () => document.createElementNS('http://www.w3.org/2000/svg', 'path'),
  newFill = (d: PathD) => {
    const p = newPath()
    p.setAttribute('stroke', 'none')
    p.setAttribute('d', d.join(' '))
    return p
  },
  newStroke = (d: PathD) => {
    const p = newPath()
    p.setAttribute('fill', 'none')
    p.setAttribute('d', d.join(' '))
    return p
  },
  makeLineY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 2) return ''
    const
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i], h, 0))
    return d.join(' ')
  },
  makeLineYFill = (ys: F[], w: F, h: F) => {
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
  },
  makeStepY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 1) return ''
    const
      dx = w / n,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const y = lerp(ys[i], h, 0)
      if (i) {
        d.push('V', y)
      } else {
        d.push('M', 0, y)
      }
      d.push('h', dx)
    }
    return d.join(' ')
  },
  makeStepYFill = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 1) return ''
    const
      dx = w / n,
      d: Array<S | F> = []
    d.push('M', 0, h)
    for (let i = 0; i < n; i++) {
      d.push('V', lerp(ys[i], h, 0))
      d.push('h', dx)
    }
    d.push('V', w, h)
    d.push('Z')
    return d.join(' ')
  },
  makeBarY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 1) return ''
    const
      dx = (w / n) - 1, // 1px gap
      d: Array<S | F> = [],
      n1 = n - 1
    d.push('M', 0, h)
    for (let i = 0; i < n; i++) {
      const y = lerp(ys[i], h, 0)
      d.push('V', y)
      d.push('h', dx)
      if (i < n1) {
        d.push('V', h)
        d.push('h', 1) // gap
        d.push('V', y)
      }
    }
    d.push('V', w, h)
    d.push('Z')
    return d.join(' ')
  },
  makeStrokeY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 1) return ''
    const
      dx = w / n,
      dx2 = dx / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      d.push('M', dx2 + dx * i, h)
      d.push('V', lerp(ys[i], h, 0))
    }
    return d.join(' ')
  },
  makeTickY = (ys: F[], w: F, h: F) => {
    const n = ys.length
    if (n < 1) return ''
    const
      dx = w / n,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      d.push('M', dx * i, lerp(ys[i], h, 0))
      d.push('h', dx)
    }
    return d.join(' ')
  },
  makeGuideX = (xs: F[], w: F, h: F) => {
    const d: Array<S | F> = []
    for (const x of xs) {
      d.push('M', lerp(x, 0, w), 0)
      d.push('v', h)
    }
    return d.join(' ')
  },
  makeGuideY = (ys: F[], w: F, h: F) => {
    const d: Array<S | F> = []
    for (const y of ys) {
      d.push('M', 0, lerp(y, h, 0))
      d.push('h', w)
    }
    return d.join(' ')
  },
  makeCircle = (xs: F[], w: F, h: F) => {
    let [a1, a2, r1, r2] = xs
    if (!isN(a1)) a1 = 0
    if (!isN(a2)) a2 = 0
    if (!isN(r1)) r1 = 0
    if (!isN(r2)) r2 = 1
    const
      rmax = Math.min(w, h) / 2,
      t1 = Math.PI * (2 * Math.min(a1, a2) + 0.5),
      t2 = Math.PI * (2 * Math.max(a1, a2) + 0.5),
      tt = (t1 + t2) / 2
    r1 *= rmax
    r2 *= rmax
    const r = (r1 + r2) / 2
    const path = newStroke([
      'M', w / 2 - r * Math.cos(t1), h / 2 - r * Math.sin(t1),
      'A', r, r, 0, 0, 1, w / 2 - r * Math.cos(tt), h / 2 - r * Math.sin(tt),
      'A', r, r, 0, 0, 1, w / 2 - r * Math.cos(t2), h / 2 - r * Math.sin(t2)
    ])
    path.setAttribute('stroke-width', String(r2 - r1))
    return path
  },
  makeCircleFill = (xs: F[], w: F, h: F) => {
    let [a1, a2, r1, r2] = xs
    if (!isN(r1)) r1 = 0
    if (!isN(r2)) r2 = 1
    const rmax = Math.min(w, h) / 2
    r1 *= rmax
    r2 *= rmax
    const d1 = r1 * 2, d2 = r2 * 2
    return newFill([
      'M', w / 2, h / 2 - r2,
      'a', r2, r2, 0, 0, 1, 0, d2, // outer arc  1
      'a', r2, r2, 0, 0, 1, 0, -d2, // outer arc 2
      'v', r2 - r1, // slit
      'a', r1, r1, 0, 0, 0, 0, d1, // inner arc 1
      'a', r1, r1, 0, 0, 0, 0, -d1, // inner arc 2
      'Z'
    ])
  },
  makeArc = (xs: F[], w: F, h: F) => {
    let [a1, a2, r1, r2] = xs
    if (!isN(a1)) a1 = 0
    if (!isN(a2)) a2 = 0
    if (!isN(r1)) r1 = 0
    if (!isN(r2)) r2 = 1
    const
      rmax = Math.min(w / 2, h),
      t1 = Math.PI * Math.min(a1, a2),
      t2 = Math.PI * Math.max(a1, a2)
    r1 *= rmax
    r2 *= rmax
    const r = (r1 + r2) / 2
    const path = newStroke([
      'M', w / 2 - r * Math.cos(t1), h - r * Math.sin(t1),
      'A', r, r, 0, 0, 1, w / 2 - r * Math.cos(t2), h - r * Math.sin(t2)
    ])
    path.setAttribute('stroke-width', String(r2 - r1))
    return path
  },
  makeArcFill = (xs: F[], w: F, h: F) => {
    const rmax = Math.min(w / 2, h)
    let [a1, a2, r1, r2] = xs
    if (!isN(r1)) r1 = 0
    if (!isN(r2)) r2 = 1
    r1 *= rmax
    r2 *= rmax
    return newFill([
      'M', w / 2 - r2, h,
      'a', r2, r2, 0, 0, 1, r2 * 2, 0, // outer arc
      'h', r1 - r2, // slit
      'a', r1, r1, 0, 0, 0, -r1 * 2, 0, // inner arc
      'Z'
    ])
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
        svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')

      svg.setAttribute('viewBox', `0 0 ${w} ${h}`)
      svg.setAttribute('width', `${w}`)
      svg.setAttribute('height', `${h}`)

      if (modes.has('line-y')) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        line.setAttribute('d', makeLineY(clamp1s(data as F[]), w, h))
        line.setAttribute('fill', 'none') // inherit stroke
        line.setAttribute('stroke-linecap', 'round')
        line.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(line)
        const area = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        area.setAttribute('d', makeLineYFill(clamp1s(data as F[]), w, h))
        area.setAttribute('stroke', 'none') // inherit fill
        area.setAttribute('stroke-linecap', 'round')
        area.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(area)
      } else if (modes.has('step-y')) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        line.setAttribute('d', makeStepY(clamp1s(data as F[]), w, h))
        line.setAttribute('fill', 'none')
        line.setAttribute('stroke-linecap', 'round')
        line.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(line)
        const area = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        area.setAttribute('d', makeStepYFill(clamp1s(data as F[]), w, h))
        area.setAttribute('stroke', 'none') // inherit fill
        area.setAttribute('stroke-linecap', 'round')
        area.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(area)
      } else if (modes.has('bar-y')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeBarY(clamp1s(data as F[]), w, h))
        path.setAttribute('stroke', 'none')
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      } else if (modes.has('stroke-y')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeStrokeY(clamp1s(data as F[]), w, h))
        path.setAttribute('fill', 'none')
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      } else if (modes.has('tick-y')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeTickY(clamp1s(data as F[]), w, h))
        path.setAttribute('fill', 'none')
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      } else if (modes.has('guide-x')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeGuideX(clamp1s(data as F[]), w, h))
        path.setAttribute('fill', 'none')
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      } else if (modes.has('guide-y')) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', makeGuideY(clamp1s(data as F[]), w, h))
        path.setAttribute('fill', 'none')
        path.setAttribute('stroke-linecap', 'round')
        path.setAttribute('stroke-linejoin', 'round')
        svg.appendChild(path)
      } else if (modes.has('arc')) {
        svg.appendChild(makeArcFill(clamp1s(data as F[]), w, h))
        svg.appendChild(makeArc(clamp1s(data as F[]), w, h))
      } else if (modes.has('circle')) {
        svg.appendChild(makeCircleFill(clamp1s(data as F[]), w, h))
        svg.appendChild(makeCircle(clamp1s(data as F[]), w, h))
      }

      while (div.firstChild) div.removeChild(div.firstChild)
      div.appendChild(svg)
    }
  })
  return <div ref={ref} className={css(style)} />
}