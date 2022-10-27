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
type Pair = [F, F]
type Pairs = Pair[]

const
  lerp = (f: F, a: F, b: F) => a * (1.0 - f) + (b * f),
  clamp1 = (f: F) => isN(f) ? f < 0 ? 0 : f > 1 ? 1 : f : 0,
  clamp1s = (fs: F[]) => fs.map(clamp1),
  isPair = (x: any) => Array.isArray(x) && x.length === 2,
  arePairs = (xs: any[]): xs is Pairs => xs.every(isPair),
  newPath = () => document.createElementNS('http://www.w3.org/2000/svg', 'path'),
  newFill = (d: PathD) => {
    const p = newPath()
    p.setAttribute('stroke', 'none')
    p.setAttribute('stroke-linejoin', 'round')
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
    const
      n = ys.length,
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i], h, 0))
    return newStroke(d)
  },
  makeLineYFill = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d: Array<S | F> = []
    d.push('M', 0, h)
    for (let i = 0; i < n; i++) d.push('L', dx * i, lerp(ys[i], h, 0))
    d.push('L', w, h)
    d.push('Z')
    return newFill(d)
  },
  makeLineYi = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (const j of [0, 1]) {
      for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i][j], h, 0))
    }

    return newStroke(d)
  },
  makeLineYFilli = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i][0], h, 0))
    for (let i = n - 1; i >= 0; i--) d.push('L', dx * i, lerp(ys[i][1], h, 0))
    d.push('Z')
    return newFill(d)
  },
  makeStepY = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
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
    return newStroke(d)
  },
  makeStepYFill = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    d.push('M', 0, h)
    for (let i = 0; i < n; i++) {
      d.push('V', lerp(ys[i], h, 0))
      d.push('h', dx)
    }
    d.push('V', w, h)
    d.push('Z')
    return newFill(d)
  },
  makeStepYi = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    for (const j of [0, 1]) {
      for (let i = 0; i < n; i++) {
        const y = lerp(ys[i][j], h, 0)
        if (i) {
          d.push('V', y)
        } else {
          d.push('M', 0, y)
        }
        d.push('h', dx)
      }
    }
    return newStroke(d)
  },
  makeStepYFilli = (ys: Pairs, w: F, h: F) => {
    console.log('in filli')
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      if (i) {
        d.push('V', lerp(ys[i][0], h, 0))
      } else {
        d.push('M', 0, lerp(ys[i][0], h, 0))
      }
      d.push('h', dx)
    }
    for (let i = n - 1; i >= 0; i--) {
      d.push('V', lerp(ys[i][1], h, 0))
      d.push('h', -dx)
    }
    d.push('Z')
    return newFill(d)
  },
  makeIntervalY = (ys: F[], w: F, h: F) => {
    const p = makeStrokeY(ys, w, h)
    p.setAttribute('stroke-width', String(w / ys.length - 1)) // 1px gap
    return p
  },
  makeIntervalYi = (ys: Pairs, w: F, h: F) => {
    const p = makeStrokeYi(ys, w, h)
    p.setAttribute('stroke-width', String(w / ys.length - 1)) // 1px gap
    return p
  },
  makeStrokeY = (ys: F[], w: F, h: F) => {
    const
      d: Array<S | F> = [],
      dx = w / ys.length
    let x = dx / 2
    for (const y of ys) {
      d.push(
        'M', x, h,
        'V', lerp(y, h, 0)
      )
      x += dx
    }
    return newStroke(d)
  },
  makeStrokeYi = (ys: Pairs, w: F, h: F) => {
    const
      d: Array<S | F> = [],
      dx = w / ys.length
    let x = dx / 2
    for (const y of ys) {
      d.push(
        'M', x, lerp(y[0], h, 0),
        'V', lerp(y[1], h, 0)
      )
      x += dx
    }
    return newStroke(d)
  },
  makeTickY = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      d.push('M', dx * i, lerp(ys[i], h, 0))
      d.push('h', dx)
    }
    return newStroke(d)
  },
  makeGuideX = (xs: F[], w: F, h: F) => {
    const d: Array<S | F> = []
    for (const x of xs) {
      d.push('M', lerp(x, 0, w), 0)
      d.push('v', h)
    }
    return newStroke(d)
  },
  makeGuideY = (ys: F[], w: F, h: F) => {
    const d: Array<S | F> = []
    for (const y of ys) {
      d.push('M', 0, lerp(y, h, 0))
      d.push('h', w)
    }
    return newStroke(d)
  },
  makeBarX = (ds: F[], w: F, h: F) => {
    let [a, b] = ds
    if (!isN(a)) a = 0
    if (!isN(b)) b = 0
    const p = newStroke([
      'M', a * w, h / 2,
      'H', b * w,
    ])
    p.setAttribute('stroke-width', String(h))
    return p
  },
  makeBarXFill = (ds: F[], w: F, h: F) => {
    return newFill([
      'M', 0, 0,
      'h', w,
      'v', h,
      'h', -w,
      'Z'
    ])
  },
  makeBarY = (ds: F[], w: F, h: F) => {
    let [a, b] = ds
    if (!isN(a)) a = 0
    if (!isN(b)) b = 0
    const p = newStroke([
      'M', w / 2, (1 - a) * h,
      'V', (1 - b) * h,
    ])
    p.setAttribute('stroke-width', String(w))
    return p
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
  const
    { modes, style, data: rawData } = box,
    ref = useRef<HTMLDivElement>(null),
    unclamped: any = rawData || [],
    paired = arePairs(unclamped),
    data: any = paired ? unclamped.map(clamp1s) : clamp1s(unclamped)

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

      if (data.length) {
        if (modes.has('line-y')) {
          if (paired) {
            svg.appendChild(makeLineYFilli(data, w, h))
            svg.appendChild(makeLineYi(data, w, h))
          } else {
            svg.appendChild(makeLineYFill(data, w, h))
            svg.appendChild(makeLineY(data, w, h))
          }
        } else if (modes.has('step-y')) {
          if (paired) {
            svg.appendChild(makeStepYFilli(data, w, h))
            svg.appendChild(makeStepYi(data, w, h))
          } else {
            svg.appendChild(makeStepYFill(data, w, h))
            svg.appendChild(makeStepY(data, w, h))
          }
        } else if (modes.has('interval-y')) {
          if (paired) {
            svg.appendChild(makeIntervalYi(data, w, h))
          } else {
            svg.appendChild(makeIntervalY(data, w, h))
          }
        } else if (modes.has('stroke-y')) {
          if (paired) {
            svg.appendChild(makeStrokeYi(data, w, h))
          } else {
            svg.appendChild(makeStrokeY(data, w, h))
          }
        } else if (modes.has('tick-y')) {
          svg.appendChild(makeTickY(data, w, h))
        } else if (modes.has('guide-x')) {
          svg.appendChild(makeGuideX(data, w, h))
        } else if (modes.has('guide-y')) {
          svg.appendChild(makeGuideY(data, w, h))
        } else if (modes.has('bar-x')) {
          svg.appendChild(makeBarXFill(data, w, h))
          svg.appendChild(makeBarX(data, w, h))
        } else if (modes.has('bar-y')) {
          svg.appendChild(makeBarXFill(data, w, h))
          svg.appendChild(makeBarY(data, w, h))
        } else if (modes.has('circle')) {
          svg.appendChild(makeCircleFill(data, w, h))
          svg.appendChild(makeCircle(data, w, h))
        } else if (modes.has('arc')) {
          svg.appendChild(makeArcFill(data, w, h))
          svg.appendChild(makeArc(data, w, h))
        }
      }

      while (div.firstChild) div.removeChild(div.firstChild)
      div.appendChild(svg)
    }
  })
  return <div ref={ref} className={css(style)} />
}
