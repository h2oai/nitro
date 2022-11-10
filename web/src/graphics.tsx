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

import { useLayoutEffect, useRef } from 'react';
import { B, debounce, F, isN, S } from './core';
import { css } from './css';
import { Box } from './protocol';
import { BoxProps } from './ui';

type PathD = Array<S | F>
type Pair = [F, F]
type Pairs = Pair[]

const
  lerp = (f: F, a: F, b: F) => a * (1.0 - f) + (b * f),
  isPair = (x: any) => Array.isArray(x) && x.length === 2,
  arePairs = (xs: any[]): xs is Pairs => xs.every(isPair),
  clamp1 = (f: any) => isN(f) ? f < 0 ? 0 : f > 1 ? 1 : f : 0,
  clamp1s = (fs: any[]) => fs.map(clamp1),
  clampPairs = (fs: Pairs) => fs.map(clamp1s) as Pairs,
  newEl = (t: S) => document.createElementNS('http://www.w3.org/2000/svg', t),
  newPath = (d: PathD) => {
    const p = newEl('path')
    p.setAttribute('d', d.join(' '))
    return p
  },
  newFill = (d: PathD) => {
    const p = newPath(d)
    p.setAttribute('stroke', 'none')
    p.setAttribute('stroke-linejoin', 'round')
    return p
  },
  newStroke = (d: PathD) => {
    const p = newPath(d)
    p.setAttribute('fill', 'none')
    return p
  },
  makeLineX = (xs: F[], w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', lerp(xs[i], 0, w), dy * i)
    return newStroke(d)
  },
  makeLineY = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i], h, 0))
    return newStroke(d)
  },
  makeAreaX = (xs: F[], w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      d: Array<S | F> = []
    d.push('M', 0, 0)
    for (let i = 0; i < n; i++) d.push('L', lerp(xs[i], 0, w), dy * i)
    d.push('L', 0, h)
    d.push('Z')
    return newFill(d)
  },
  makeAreaY = (ys: F[], w: F, h: F) => {
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
  makeLineXi = (xs: Pairs, w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      d: Array<S | F> = []
    for (const j of [0, 1]) {
      for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', lerp(xs[i][j], 0, w), dy * i)
    }
    return newStroke(d)
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
  makeAreaXi = (xs: Pairs, w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', lerp(xs[i][0], 0, w), dy * i)
    for (let i = n - 1; i >= 0; i--) d.push('L', lerp(xs[i][1], 0, w), dy * i)
    d.push('Z')
    return newFill(d)
  },
  makeAreaYi = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) d.push(i ? 'L' : 'M', dx * i, lerp(ys[i][0], h, 0))
    for (let i = n - 1; i >= 0; i--) d.push('L', dx * i, lerp(ys[i][1], h, 0))
    d.push('Z')
    return newFill(d)
  },
  joinCurveX = (ps: Pair[]) => {
    const d: F[][] = []
    for (let i = 0; i < ps.length; i++) {
      const [x, y] = ps[i]
      if (i) {
        const [x0, y0] = ps[i - 1]
        // B-spline, with control points 1/3 away from nodes.
        const dy = (y - y0) / 3
        d.push([x0, y0 + dy, x, y - dy, x, y])
      } else {
        d.push([0, 0, 0, 0, x, y])
      }
    }
    return d
  },
  joinCurveY = (ps: Pair[]) => {
    const d: F[][] = []
    for (let i = 0; i < ps.length; i++) {
      const [x, y] = ps[i]
      if (i) {
        const [x0, y0] = ps[i - 1]
        // B-spline, with control points 1/3 away from nodes.
        const dx = (x - x0) / 3
        d.push([x0 + dx, y0, x - dx, y, x, y])
      } else {
        d.push([0, 0, 0, 0, x, y])
      }
    }
    return d
  },
  makeCurveX = (xs: F[], w: F, h: F, rev: B) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      d = new Array<Pair>(n)
    for (let i = 0; i < n; i++) {
      d[i] = [lerp(xs[i], 0, w), rev ? h - dy * i : dy * i]
    }
    return joinCurveX(d)
  },
  makeCurveY = (ys: F[], w: F, h: F, rev: B) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d = new Array<Pair>(n)
    for (let i = 0; i < n; i++) {
      d[i] = [rev ? w - dx * i : dx * i, lerp(ys[i], h, 0)]
    }
    return joinCurveY(d)
  },
  drawCurve = (ps: F[][], d: Array<S | F>) => {
    for (let i = 0; i < ps.length; i++) {
      const p = ps[i]
      if (i) {
        d.push('C', ...p)
      } else {
        d.push('M', p[4], p[5])
      }
    }
  },
  makeCurve = (ps: F[][]) => {
    const d: Array<S | F> = []
    drawCurve(ps, d)
    return newStroke(d)
  },
  makeCurveArea = (ps: F[][], w: F, h: F) => {
    const d: Array<S | F> = []
    d.push('M', 0, h)
    for (let i = 0; i < ps.length; i++) {
      const p = ps[i]
      if (i) {
        d.push('C', ...p)
      } else {
        d.push('L', p[4], p[5])
      }
    }
    d.push('L', w, h)
    d.push('Z')
    return newFill(d)
  },
  makeCurvei = (ps0: F[][], ps1: F[][]) => {
    const d: Array<S | F> = []
    drawCurve(ps0, d)
    drawCurve(ps1, d)
    return newStroke(d)
  },
  makeCurveAreai = (ps0: F[][], ps1: F[][]) => {
    const d: Array<S | F> = []
    for (let i = 0; i < ps1.length; i++) {
      const p = ps1[i]
      if (i) {
        d.push('C', ...p)
      } else {
        d.push('M', p[4], p[5])
      }
    }
    for (let i = 0; i < ps0.length; i++) {
      const p = ps0[i]
      if (i) {
        d.push('C', ...p)
      } else {
        d.push('L', p[4], p[5])
      }
    }
    d.push('Z')
    return newFill(d)
  },
  makeStepX = (xs: F[], w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      dy2 = dy / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const x = lerp(xs[i], 0, w)
      if (i) {
        d.push(
          'v', dy2,
          'H', x,
          'v', dy2,
        )
      } else {
        d.push('M', x, 0)
      }
    }
    return newStroke(d)
  },
  makeStepAreaX = (xs: F[], w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      dy2 = dy / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const x = lerp(xs[i], 0, w)
      if (i) {
        d.push(
          'v', dy2,
          'H', x,
          'v', dy2,
        )
      } else {
        d.push('M', x, 0)
      }
    }
    d.push(
      'H', 0,
      'V', 0,
      'Z'
    )
    return newFill(d)
  },
  makeStepY = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      dx2 = dx / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const y = lerp(ys[i], h, 0)
      if (i) {
        d.push(
          'h', dx2,
          'V', y,
          'h', dx2,
        )
      } else {
        d.push('M', 0, y)
      }
    }
    return newStroke(d)
  },
  makeStepAreaY = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      dx2 = dx / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const y = lerp(ys[i], h, 0)
      if (i) {
        d.push(
          'h', dx2,
          'V', y,
          'h', dx2,
        )
      } else {
        d.push('M', 0, y)
      }
    }
    d.push(
      'V', h,
      'H', 0,
      'Z'
    )
    return newFill(d)
  },
  makeStepXi = (xs: Pairs, w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      dy2 = dy / 2,
      d: Array<S | F> = []
    for (const j of [0, 1]) {
      for (let i = 0; i < n; i++) {
        const x = lerp(xs[i][j], 0, w)
        if (i) {
          d.push(
            'v', dy2,
            'H', x,
            'v', dy2,
          )
        } else {
          d.push('M', x, 0)
        }
      }
    }
    return newStroke(d)
  },
  makeStepAreaXi = (xs: Pairs, w: F, h: F) => {
    const
      n = xs.length,
      dy = h / (n - 1),
      dy2 = dy / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const x = lerp(xs[i][0], 0, w)
      if (i) {
        d.push(
          'v', dy2,
          'H', x,
          'v', dy2,
        )
      } else {
        d.push('M', x, 0)
      }
    }
    const nn = n - 1
    for (let i = nn; i >= 0; i--) {
      const x = lerp(xs[i][1], 0, w)
      if (i === nn) {
        d.push('H', x)
      } else {
        d.push(
          'v', -dy2,
          'H', x,
          'v', -dy2
        )
      }
    }
    d.push('Z')
    return newFill(d)
  },
  makeStepYi = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      dx2 = dx / 2,
      d: Array<S | F> = []
    for (const j of [0, 1]) {
      for (let i = 0; i < n; i++) {
        const y = lerp(ys[i][j], h, 0)
        if (i) {
          d.push(
            'h', dx2,
            'V', y,
            'h', dx2,
          )
        } else {
          d.push('M', 0, y)
        }
      }
    }
    return newStroke(d)
  },
  makeStepAreaYi = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      dx2 = dx / 2,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      const y = lerp(ys[i][0], h, 0)
      if (i) {
        d.push(
          'h', dx2,
          'V', y,
          'h', dx2,
        )
      } else {
        d.push('M', 0, y)
      }
    }
    const nn = n - 1
    for (let i = nn; i >= 0; i--) {
      const y = lerp(ys[i][1], h, 0)
      if (i === nn) {
        d.push('V', y)
      } else {
        d.push(
          'h', -dx2,
          'V', y,
          'h', -dx2
        )
      }
    }
    d.push('Z')
    return newFill(d)
  },
  makeBarX = (xs: F[], w: F, h: F) => {
    const p = makeStrokeX(xs, w, h)
    p.setAttribute('stroke-width', String(h / xs.length - 1)) // 1px gap
    return p
  },
  makeBarY = (ys: F[], w: F, h: F) => {
    const p = makeStrokeY(ys, w, h)
    p.setAttribute('stroke-width', String(w / ys.length - 1)) // 1px gap
    return p
  },
  makeBarXi = (xs: Pairs, w: F, h: F) => {
    const p = makeStrokeXi(xs, w, h)
    p.setAttribute('stroke-width', String(h / xs.length - 1)) // 1px gap
    return p
  },
  makeBarYi = (ys: Pairs, w: F, h: F) => {
    const p = makeStrokeYi(ys, w, h)
    p.setAttribute('stroke-width', String(w / ys.length - 1)) // 1px gap
    return p
  },
  makeStrokeX = (xs: F[], w: F, h: F) => {
    const
      d: Array<S | F> = [],
      dy = h / xs.length
    let y = dy / 2
    for (const x of xs) {
      d.push(
        'M', 0, y,
        'H', lerp(x, 0, w)
      )
      y += dy
    }
    return newStroke(d)
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
  makeStrokeXi = (xs: Pairs, w: F, h: F) => {
    const
      d: Array<S | F> = [],
      dy = h / xs.length
    let y = dy / 2
    for (const x of xs) {
      d.push(
        'M', lerp(x[0], 0, w), y,
        'H', lerp(x[1], 0, w)
      )
      y += dy
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
  makeTickX = (xs: F[], w: F, h: F) => {
    const
      n = xs.length,
      dy = h / n,
      d: Array<S | F> = []
    let y = 0
    for (const x of xs) {
      d.push(
        'M', lerp(x, 0, w), y,
        'v', dy
      )
      y += dy
    }
    return newStroke(d)
  },
  makeTickY = (ys: F[], w: F, h: F) => {
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    let x = 0
    for (const y of ys) {
      d.push(
        'M', x, lerp(y, h, 0),
        'h', dx
      )
      x += dx
    }
    return newStroke(d)
  },
  makeTickXi = (xs: Pairs, w: F, h: F) => {
    const
      n = xs.length,
      dy = h / n,
      d: Array<S | F> = []
    let y = 0
    for (const x of xs) {
      d.push(
        'M', lerp(x[0], 0, w), y,
        'v', dy,
        'M', lerp(x[1], 0, w), y,
        'v', dy
      )
      y += dy
    }
    return newStroke(d)
  },
  makeTickYi = (ys: Pairs, w: F, h: F) => {
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    let x = 0
    for (const y of ys) {
      d.push(
        'M', x, lerp(y[0], h, 0),
        'h', dx,
        'M', x, lerp(y[1], h, 0),
        'h', dx
      )
      x += dx
    }
    return newStroke(d)
  },
  makeGuideX = (xs: F[], w: F, h: F) => {
    const d: Array<S | F> = []
    for (const x of xs) {
      d.push(
        'M', lerp(x, 0, w), 0,
        'v', h
      )
    }
    return newStroke(d)
  },
  makeGuideY = (ys: F[], w: F, h: F) => {
    const d: Array<S | F> = []
    for (const y of ys) {
      d.push(
        'M', 0, lerp(y, h, 0),
        'h', w
      )
    }
    return newStroke(d)
  },
  makeGaugeFill = (ds: F[], w: F, h: F) => {
    return newFill([
      'M', 0, 0,
      'h', w,
      'v', h,
      'h', -w,
      'Z'
    ])
  },
  makeGaugeX = (ds: F[], w: F, h: F) => {
    let [len, s] = ds
    if (!isN(len)) len = 0
    if (!isN(s)) s = 1
    const p = newStroke([
      'M', 0, h / 2,
      'h', len * w,
    ])
    p.setAttribute('stroke-width', String(h * s))
    return p
  },
  makeGaugeY = (ds: F[], w: F, h: F) => {
    let [len, s] = ds
    if (!isN(len)) len = 0
    if (!isN(s)) s = 1
    const p = newStroke([
      'M', w / 2, h,
      'v', -len * h
    ])
    p.setAttribute('stroke-width', String(w * s))
    return p
  },
  makePolyline = (d: any, width: F, height: F) => {
    const points: S[] = []
    for (let i = 0; i < d.length; i += 2) {
      const
        x = clamp1(d[i]) * width,
        y = (1 - clamp1(d[i + 1])) * height
      points.push(`${x},${y}`)
    }
    return points.join(' ')
  },
  makeArcFill = (x: F, y: F, len: F, size: F, dia: F, rot: F, width: F, height: F) => {
    const
      r2 = dia * Math.min(width, height) / 2,
      r1 = (1 - size) * r2,
      t1 = Math.PI * 2 * (rot + .75),
      t2 = Math.PI * 2 * (rot + len + .75),
      tt = (t1 + t2) / 2

    if (len < 1) { // arc
      const path: PathD = []
      path.push(
        'M', x + r2 * Math.cos(t1), y + r2 * Math.sin(t1),
        'A', r2, r2, 0, 0, 1, x + r2 * Math.cos(tt), y + r2 * Math.sin(tt),
        'A', r2, r2, 0, 0, 1, x + r2 * Math.cos(t2), y + r2 * Math.sin(t2),
      )
      if (r1 < r2) {
        // reverse arc
        path.push(
          'L', x + r1 * Math.cos(t2), y + r1 * Math.sin(t2),
          'A', r1, r1, 0, 0, 0, x + r1 * Math.cos(tt), y + r1 * Math.sin(tt),
          'A', r1, r1, 0, 0, 0, x + r1 * Math.cos(t1), y + r1 * Math.sin(t1),
          'Z'
        )
      } else {
        // connect to center
        path.push(
          'L', x, y,
          'Z'
        )
      }
      return newPath(path)
    }

    if (r1 < r2) { // donut
      return newPath([
        'M', x + r2 * Math.cos(t1), y + r2 * Math.sin(t1),
        'A', r2, r2, 0, 0, 1, x + r2 * Math.cos(tt), y + r2 * Math.sin(tt),
        'A', r2, r2, 0, 0, 1, x + r2 * Math.cos(t2), y + r2 * Math.sin(t2),
        'Z',
        'M', x + r1 * Math.cos(t1), y + r1 * Math.sin(t1),
        'A', r1, r1, 0, 1, 0, x + r1 * Math.cos(tt), y + r1 * Math.sin(tt),
        'A', r1, r1, 0, 1, 0, x + r1 * Math.cos(t2), y + r1 * Math.sin(t2),
        'Z'
      ])
    }

    const circle = newEl('circle')
    circle.setAttribute('cx', String(x))
    circle.setAttribute('cy', String(y))
    circle.setAttribute('r', String(r2))
    return circle
  },
  makeArc = (x: F, y: F, len: F, trackSize: F, size: F, dia: F, rot: F, width: F, height: F) => {
    const
      r2 = dia * Math.min(width, height) / 2,
      r1 = (1 - trackSize) * r2,
      r = (r1 + r2) / 2,
      t1 = Math.PI * 2 * (rot + .75),
      t2 = Math.PI * 2 * (rot + len + .75),
      tt = (t1 + t2) / 2

    const arc = newStroke([
      'M', x + r * Math.cos(t1), y + r * Math.sin(t1),
      'A', r, r, 0, 0, 1, x + r * Math.cos(tt), y + r * Math.sin(tt),
      'A', r, r, 0, 0, 1, x + r * Math.cos(t2), y + r * Math.sin(t2),
    ])
    arc.setAttribute('stroke-width', String((r2 - r1) * size))
    return arc
  }

export const GraphicLabel = ({ context, box }: BoxProps) => {
  const
    { style, data: rawData } = box,
    data = Array.isArray(rawData) ? rawData : []

  const labels = data.map((item, i) => {
    if (Array.isArray(item)) {
      const
        [x, y, text, j, a] = item,
        left = clamp1(x as any) * 100 + '%',
        top = (1 - clamp1(y as any)) * 100 + '%',
        justify = j === 0 ? 'start' : j === 1 ? 'end' : 'center',
        align = a === 0 ? 'end' : a === 1 ? 'start' : 'center'
      return (
        <div
          key={i}
          className={css(`absolute w-0 h-0 flex justify-${justify} items-${align}`)}
          style={{ left, top }}
        >
          <div>{text}</div>
        </div>
      )
    }
    return <></>
  })
  return <div className={css('relative', style)}>{labels}</div>
}

const redraw = (box: Box, div: HTMLDivElement | null) => {
  const { modes, data } = box

  if (!(div && Array.isArray(data) && data.length)) return
  const
    bounds = div.getBoundingClientRect(),
    width = Math.round(bounds.width),
    height = Math.round(bounds.height),
    svg = newEl('svg')

  svg.setAttribute('viewBox', `0 0 ${width} ${height}`)
  svg.setAttribute('width', `${width}`)
  svg.setAttribute('height', `${height}`)

  if (modes.has('g-point')) {
    const path: PathD = []
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x, y, w, shape, rot] = d
        x = clamp1(x) * width
        y = (1 - clamp1(y)) * height
        if (!isN(w)) w = 10
        rot = clamp1(rot)

        switch (shape) {
          case 's':
            {
              const r = w / 2
              path.push(
                'M', x - r, y - r,
                'h', w,
                'v', w,
                'h', -w,
                'Z'
              )
            }
            break
          case 'd':
            {
              const r = w / 2
              path.push(
                'M', x, y - r,
                'l', r, r,
                'l', -r, r,
                'l', -r, -r,
                'Z'
              )
            }
            break
          case 'tu':
            {
              const s = w * 2 / Math.sqrt(3)
              path.push(
                'M', x, y - w * 2 / 3,
                'l', s / 2, w,
                'h', -s,
                'Z'
              )
            }
            break
          case 'tr':
            {
              const s = w * 2 / Math.sqrt(3)
              path.push(
                'M', x + w * 2 / 3, y,
                'l', -w, s / 2,
                'v', -s,
                'Z'
              )
            }
            break
          case 'td':
            {
              const s = w * 2 / Math.sqrt(3)
              path.push(
                'M', x, y + w * 2 / 3,
                'l', s / 2, -w,
                'h', -s,
                'Z'
              )
            }
            break
          case 'tl':
            {
              const s = w * 2 / Math.sqrt(3)
              path.push(
                'M', x - w * 2 / 3, y,
                'l', w, s / 2,
                'v', -s,
                'Z'
              )
            }
            break
          case 'h':
            {
              const r = w / 2
              path.push(
                'M', x - r, y,
                'h', w,
              )
            }
            break
          case 'v':
            {
              const r = w / 2
              path.push(
                'M', x, y - r,
                'v', w,
              )
            }
            break
          case 'p':
            {
              const r = w / 2
              path.push(
                'M', x, y - r,
                'v', w,
                'M', x - r, y,
                'h', w,
              )
            }
            break
          case 'x':
            {
              const r = w / 2
              path.push(
                'M', x - r, y - r,
                'l', w, w,
                'M', x - r, y + r,
                'l', w, -w,
              )
            }
            break
          case 'au':
            {
              const r = w / 2
              path.push(
                'M', x - r, y + r,
                'l', r, -r,
                'l', r, r,
              )
            }
            break
          case 'ar':
            {
              const r = w / 2
              path.push(
                'M', x - r, y - r,
                'l', r, r,
                'l', -r, r,
              )
            }
            break
          case 'ad':
            {
              const r = w / 2
              path.push(
                'M', x + r, y - r,
                'l', -r, r,
                'l', -r, -r,
              )
            }
            break
          case 'al':
            {
              const r = w / 2
              path.push(
                'M', x + r, y - r,
                'l', -r, r,
                'l', r, r,
              )
            }
            break
          default:
            {
              const r = w / 2
              path.push(
                'M', x - r, y,
                'a', r, r, 0, 0, 1, w, 0,
                'a', r, r, 0, 0, 1, -w, 0,
                'Z'
              )
            }
        }
      }
    }
    svg.appendChild(newPath(path))
  } else if (modes.has('g-line-x')) {
    if (arePairs(data)) {
      const d = clampPairs(data)
      svg.appendChild(makeAreaXi(d, width, height))
      svg.appendChild(makeLineXi(d, width, height))
    } else {
      const d = clamp1s(data)
      svg.appendChild(makeAreaX(d, width, height))
      svg.appendChild(makeLineX(d, width, height))
    }
  } else if (modes.has('g-line-y')) {
    if (arePairs(data)) {
      const d = clampPairs(data)
      svg.appendChild(makeAreaYi(d, width, height))
      svg.appendChild(makeLineYi(d, width, height))
    } else {
      const d = clamp1s(data)
      svg.appendChild(makeAreaY(d, width, height))
      svg.appendChild(makeLineY(d, width, height))
    }
  } else if (modes.has('g-curve-x')) {
    if (arePairs(data)) {
      const d = clampPairs(data)
      const
        ps0 = makeCurveX(d.map((x: Pair) => x[0]).slice(0).reverse(), width, height, true),
        ps1 = makeCurveX(d.map((x: Pair) => x[1]), width, height, false)
      svg.appendChild(makeCurveAreai(ps0, ps1))
      svg.appendChild(makeCurvei(ps0, ps1))
    } else {
      const ps = makeCurveX(clamp1s(data), width, height, false)
      svg.appendChild(makeCurveArea(ps, width, height))
      svg.appendChild(makeCurve(ps))
    }
  } else if (modes.has('g-curve-y')) {
    if (arePairs(data)) {
      const d = clampPairs(data)
      const
        ps0 = makeCurveY(d.map((x: Pair) => x[0]).slice(0).reverse(), width, height, true),
        ps1 = makeCurveY(d.map((x: Pair) => x[1]), width, height, false)
      svg.appendChild(makeCurveAreai(ps0, ps1))
      svg.appendChild(makeCurvei(ps0, ps1))
    } else {
      const ps = makeCurveY(clamp1s(data), width, height, false)
      svg.appendChild(makeCurveArea(ps, width, height))
      svg.appendChild(makeCurve(ps))
    }
  } else if (modes.has('g-step-x')) {
    if (arePairs(data)) {
      const d = clampPairs(data)
      svg.appendChild(makeStepAreaXi(d, width, height))
      svg.appendChild(makeStepXi(d, width, height))
    } else {
      const d = clamp1s(data)
      svg.appendChild(makeStepAreaX(d, width, height))
      svg.appendChild(makeStepX(d, width, height))
    }
  } else if (modes.has('g-step-y')) {
    if (arePairs(data)) {
      const d = clampPairs(data)
      svg.appendChild(makeStepAreaYi(d, width, height))
      svg.appendChild(makeStepYi(d, width, height))
    } else {
      const d = clamp1s(data)
      svg.appendChild(makeStepAreaY(d, width, height))
      svg.appendChild(makeStepY(d, width, height))
    }
  } else if (modes.has('g-bar-x')) {
    if (arePairs(data)) {
      svg.appendChild(makeBarXi(clampPairs(data), width, height))
    } else {
      svg.appendChild(makeBarX(clamp1s(data), width, height))
    }
  } else if (modes.has('g-bar-y')) {
    if (arePairs(data)) {
      svg.appendChild(makeBarYi(clampPairs(data), width, height))
    } else {
      svg.appendChild(makeBarY(clamp1s(data), width, height))
    }
  } else if (modes.has('g-stroke-x')) {
    if (arePairs(data)) {
      svg.appendChild(makeStrokeXi(clampPairs(data), width, height))
    } else {
      svg.appendChild(makeStrokeX(clamp1s(data), width, height))
    }
  } else if (modes.has('g-stroke-y')) {
    if (arePairs(data)) {
      svg.appendChild(makeStrokeYi(clampPairs(data), width, height))
    } else {
      svg.appendChild(makeStrokeY(clamp1s(data), width, height))
    }
  } else if (modes.has('g-tick-x')) {
    if (arePairs(data)) {
      svg.appendChild(makeTickXi(clampPairs(data), width, height))
    } else {
      svg.appendChild(makeTickX(clamp1s(data), width, height))
    }
  } else if (modes.has('g-tick-y')) {
    if (arePairs(data)) {
      svg.appendChild(makeTickYi(clampPairs(data), width, height))
    } else {
      svg.appendChild(makeTickY(clamp1s(data), width, height))
    }
  } else if (modes.has('g-guide-x')) {
    svg.appendChild(makeGuideX(clamp1s(data), width, height))
  } else if (modes.has('g-guide-y')) {
    svg.appendChild(makeGuideY(clamp1s(data), width, height))
  } else if (modes.has('g-gauge-x')) {
    const d = clamp1s(data)
    svg.appendChild(makeGaugeFill(d, width, height))
    svg.appendChild(makeGaugeX(d, width, height))
  } else if (modes.has('g-gauge-y')) {
    const d = clamp1s(data)
    svg.appendChild(makeGaugeFill(d, width, height))
    svg.appendChild(makeGaugeY(d, width, height))
  } else if (modes.has('g-rect')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x, y, w, h, r] = d
        x = clamp1(x) * width
        y = (1 - clamp1(y)) * height
        w = clamp1(w) * width
        h = clamp1(h) * height

        const el = newEl('rect')
        el.setAttribute('x', String(x - w / 2))
        el.setAttribute('y', String(y - h / 2))
        el.setAttribute('width', String(w))
        el.setAttribute('height', String(h))
        if (isN(r)) {
          el.setAttribute('rx', String(r))
          el.setAttribute('ry', String(r))
        }

        svg.appendChild(el)
      }
    }
  } else if (modes.has('g-gauge-c')) {
    let [len, size, trackLen, trackSize, rot, dia] = clamp1s(data)

    if (!isN(len)) len = 1
    if (!isN(size)) size = 1
    if (!isN(trackLen)) trackLen = 1
    if (!isN(trackSize)) trackSize = 1
    if (!isN(rot)) rot = 0
    if (!isN(dia)) dia = 1

    const
      x = width / 2,
      y = height / 2,
      track = makeArcFill(x, y, trackLen, trackSize, dia, rot, width, height),
      bar = makeArc(x, y, len * trackLen, trackSize, size, dia, rot, width, height)

    track.setAttribute('stroke', 'none')
    bar.setAttribute('fill', 'none')

    svg.appendChild(track)
    svg.appendChild(bar)
  } else if (modes.has('g-arc')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x, y, dia, len, size, rot] = clamp1s(d)

        if (!isN(dia)) dia = 1
        if (!isN(rot)) rot = 0
        if (!isN(len)) len = 1

        x *= width
        y = (1 - y) * height

        svg.appendChild(makeArcFill(x, y, len, size, dia, rot, width, height))
      }
    }
  } else if (modes.has('g-polyline')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        const el = newEl('polyline')
        el.setAttribute('points', makePolyline(d, width, height))
        svg.appendChild(el)
      }
    }
  } else if (modes.has('g-polygon')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        const el = newEl('polygon')
        el.setAttribute('points', makePolyline(d, width, height))
        svg.appendChild(el)
      }
    }
  } else if (modes.has('g-link-x')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x1, y1, x2, y2, t1, t2] = clamp1s(d)
        x1 *= width
        y1 = (1 - y1) * height
        x2 *= width
        y2 = (1 - y2) * height
        if (isN(t1)) {
          if (!isN(t2)) t2 = t1
          t1 *= height / 2
          t2 *= height / 2
          const el = newEl('polygon')
          el.setAttribute('points', `${x1},${y1 - t1} ${x2},${y2 - t2} ${x2},${y2 + t2} ${x1},${y1 + t1}`)
          svg.appendChild(el)
        } else {
          const el = newEl('polyline')
          el.setAttribute('points', `${x1},${y1} ${x2},${y2}`)
          svg.appendChild(el)
        }
      }
    }
  } else if (modes.has('g-link-y')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x1, y1, x2, y2, t1, t2] = clamp1s(d)
        x1 *= width
        y1 = (1 - y1) * height
        x2 *= width
        y2 = (1 - y2) * height
        if (isN(t1)) {
          if (!isN(t2)) t2 = t1
          t1 *= width / 2
          t2 *= width / 2
          const el = newEl('polygon')
          el.setAttribute('points', `${x1 - t1},${y1} ${x2 - t2},${y2} ${x2 + t2},${y2} ${x1 + t2},${y1}`)
          svg.appendChild(el)
        } else {
          const el = newEl('polyline')
          el.setAttribute('points', `${x1},${y1} ${x2},${y2}`)
          svg.appendChild(el)
        }
      }
    }
  } else if (modes.has('g-spline-x')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x1, y1, x2, y2, t1, t2] = clamp1s(d)
        x1 *= width
        y1 = (1 - y1) * height
        x2 *= width
        y2 = (1 - y2) * height
        const xm = (x1 + x2) / 2
        if (isN(t1)) {
          if (!isN(t2)) t2 = t1
          t1 *= height / 2
          t2 *= height / 2
          svg.appendChild(newPath([
            'M', x1, y1 - t1,
            'C', xm, y1 - t1, xm, y2 - t2, x2, y2 - t2,
            'v', t2 * 2,
            'C', xm, y2 + t2, xm, y1 + t1, x1, y1 + t1,
            'Z'
          ]))
        } else {
          svg.appendChild(newStroke([
            'M', x1, y1,
            'C', xm, y1, xm, y2, x2, y2,
          ]))
        }
      }
    }
  } else if (modes.has('g-spline-y')) {
    for (const d of data) {
      if (Array.isArray(d)) {
        let [x1, y1, x2, y2, t1, t2] = clamp1s(d)
        x1 *= width
        y1 = (1 - y1) * height
        x2 *= width
        y2 = (1 - y2) * height
        const ym = (y1 + y2) / 2
        if (isN(t1)) {
          if (!isN(t2)) t2 = t1
          t1 *= width / 2
          t2 *= width / 2
          svg.appendChild(newPath([
            'M', x1 - t1, y1,
            'C', x1 - t1, ym, x2 - t2, ym, x2 - t2, y2,
            'h', t2 * 2,
            'C', x2 + t2, ym, x1 + t1, ym, x1 + t1, y1,
            'Z'
          ]))
        } else {
          svg.appendChild(newStroke([
            'M', x1, y1,
            'C', x1, ym, x2, ym, x2, y2,
          ]))
        }
      }
    }
  }
  while (div.firstChild) div.removeChild(div.firstChild)
  div.appendChild(svg)
}

export const Graphic = ({ box }: BoxProps) => {
  const ref = useRef<HTMLDivElement>(null)
  useLayoutEffect(() => {
    // Schedule redraws 1 second after the window has stopped resizing:
    const invalidate = debounce(1000, () => redraw(box, ref.current))
    window.addEventListener('resize', invalidate)

    // Draw immediately once:
    redraw(box, ref.current)

    // Dispose
    return () => window.removeEventListener('resize', invalidate)
  }, [box]);

  return <div ref={ref} className={css(box.style)} />
}
