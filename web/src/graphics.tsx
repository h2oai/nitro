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

import { useEffect, useRef } from 'react';
import { B, F, isN, S } from './core';
import { css } from './css';
import { BoxProps } from './ui';

type PathD = Array<S | F>
type Pair = [F, F]
type Pairs = Pair[]

const
  lerp = (f: F, a: F, b: F) => a * (1.0 - f) + (b * f),
  clamp1 = (f: any) => isN(f) ? f < 0 ? 0 : f > 1 ? 1 : f : 0,
  clamp1s = (fs: any[]) => fs.map(clamp1),
  isPair = (x: any) => Array.isArray(x) && x.length === 2,
  arePairs = (xs: any[]): xs is Pairs => xs.every(isPair),
  newEl = (t: S) => document.createElementNS('http://www.w3.org/2000/svg', t),
  newFill = (d: PathD) => {
    const p = newEl('path')
    p.setAttribute('stroke', 'none')
    p.setAttribute('stroke-linejoin', 'round')
    p.setAttribute('d', d.join(' '))
    return p
  },
  newStroke = (d: PathD) => {
    const p = newEl('path')
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
  joinCurveX = (ps: Pair[]) => {
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
  makeCurveYPoints = (ys: F[], w: F, h: F, rev: B) => {
    const
      n = ys.length,
      dx = w / (n - 1),
      d = new Array<Pair>(n)
    for (let i = 0; i < n; i++) {
      d[i] = [rev ? w - dx * i : dx * i, lerp(ys[i], h, 0)]
    }
    return joinCurveX(d)
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
  drawCurveY = (ps: F[][], d: Array<S | F>) => {
    for (let i = 0; i < ps.length; i++) {
      const p = ps[i]
      if (i) {
        d.push('C', ...p)
      } else {
        d.push('M', p[4], p[5])
      }
    }
  },
  makeCurveY = (ps: F[][]) => {
    const d: Array<S | F> = []
    drawCurveY(ps, d)
    return newStroke(d)
  },
  makeCurveYFill = (ps: F[][], w: F, h: F) => {
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
  makeCurveYi = (ps0: F[][], ps1: F[][]) => {
    const d: Array<S | F> = []
    drawCurveY(ps0, d)
    drawCurveY(ps1, d)
    return newStroke(d)
  },
  makeCurveYFilli = (ps0: F[][], ps1: F[][]) => {
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
    const
      n = ys.length,
      dx = w / n,
      d: Array<S | F> = []
    for (let i = 0; i < n; i++) {
      if (i) {
        d.push(
          'V', lerp(ys[i][0], h, 0),
          'h', dx
        )
      } else {
        d.push(
          'M', 0, lerp(ys[i][0], h, 0),
          'h', dx
        )
      }
    }
    for (let i = n - 1; i >= 0; i--) {
      d.push(
        'V', lerp(ys[i][1], h, 0),
        'h', -dx
      )
    }
    d.push('Z')
    return newFill(d)
  },
  makeBarY = (ys: F[], w: F, h: F) => {
    const p = makeStrokeY(ys, w, h)
    p.setAttribute('stroke-width', String(w / ys.length - 1)) // 1px gap
    return p
  },
  makeBarYi = (ys: Pairs, w: F, h: F) => {
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
  makeGaugeX = (ds: F[], w: F, h: F) => {
    let [a, b, s] = ds
    if (!isN(a)) a = 0
    if (!isN(b)) b = 0
    if (!isN(s)) s = 1
    const p = newStroke([
      'M', a * w, h / 2,
      'H', b * w,
    ])
    p.setAttribute('stroke-width', String(h * s))
    return p
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
  makeGaugeY = (ds: F[], w: F, h: F) => {
    let [a, b, s] = ds
    if (!isN(a)) a = 0
    if (!isN(b)) b = 0
    if (!isN(s)) s = 1
    const p = newStroke([
      'M', w / 2, (1 - a) * h,
      'V', (1 - b) * h,
    ])
    p.setAttribute('stroke-width', String(w * s))
    return p
  },
  makeGaugeC = (xs: F[], w: F, h: F) => {
    let [a1, a2, r1, r2, s] = xs
    if (!isN(a1)) a1 = 0
    if (!isN(a2)) a2 = 0
    if (!isN(r1)) r1 = 0
    if (!isN(r2)) r2 = 1
    if (!isN(s)) s = 1
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
    path.setAttribute('stroke-width', String((r2 - r1) * s))
    return path
  },
  makeGaugeCFill = (xs: F[], w: F, h: F) => {
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
  makeGaugeSC = (xs: F[], w: F, h: F) => {
    let [a1, a2, r1, r2, s] = xs
    if (!isN(a1)) a1 = 0
    if (!isN(a2)) a2 = 0
    if (!isN(r1)) r1 = 0
    if (!isN(r2)) r2 = 1
    if (!isN(s)) s = 1
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
    path.setAttribute('stroke-width', String((r2 - r1) * s))
    return path
  },
  makeGaugeSCFill = (xs: F[], w: F, h: F) => {
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
        </div>)
    }
  })
  return <div className={css('relative', style)}>{labels}</div>
}

export const Graphic2 = ({ box }: BoxProps) => {
  const
    { modes, style, data } = box,
    ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const div = ref.current
    if (div && Array.isArray(data) && data.length) {
      const
        bounds = div.getBoundingClientRect(),
        width = Math.round(bounds.width),
        height = Math.round(bounds.height),
        svg = newEl('svg')

      svg.setAttribute('viewBox', `0 0 ${width} ${height}`)
      svg.setAttribute('width', `${width}`)
      svg.setAttribute('height', `${height}`)

      if (modes.has('g-rect')) {
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
      } else if (modes.has('g-circle')) {
        for (const d of data) {
          if (Array.isArray(d)) {
            let [x, y, r] = d
            x = clamp1(x) * width
            y = (1 - clamp1(y)) * height
            r = clamp1(r) * Math.min(width, height)

            const el = newEl('circle')
            el.setAttribute('cx', String(x))
            el.setAttribute('cy', String(y))
            el.setAttribute('r', String(r))

            svg.appendChild(el)
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
              svg.appendChild(newFill([
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
      }

      while (div.firstChild) div.removeChild(div.firstChild)
      div.appendChild(svg)
    }
  })
  return <div ref={ref} className={css(style)} />
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
        svg = newEl('svg')

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
        } else if (modes.has('curve-y')) {
          if (paired) {
            const
              ps0 = makeCurveYPoints(data.map((x: Pair) => x[0]).slice(0).reverse(), w, h, true),
              ps1 = makeCurveYPoints(data.map((x: Pair) => x[1]), w, h, false)
            svg.appendChild(makeCurveYFilli(ps0, ps1))
            svg.appendChild(makeCurveYi(ps0, ps1))
          } else {
            const ps = makeCurveYPoints(data, w, h, false)
            svg.appendChild(makeCurveYFill(ps, w, h))
            svg.appendChild(makeCurveY(ps))
          }
        } else if (modes.has('step-y')) {
          if (paired) {
            svg.appendChild(makeStepYFilli(data, w, h))
            svg.appendChild(makeStepYi(data, w, h))
          } else {
            svg.appendChild(makeStepYFill(data, w, h))
            svg.appendChild(makeStepY(data, w, h))
          }
        } else if (modes.has('bar-y')) {
          if (paired) {
            svg.appendChild(makeBarYi(data, w, h))
          } else {
            svg.appendChild(makeBarY(data, w, h))
          }
        } else if (modes.has('stroke-y')) {
          if (paired) {
            svg.appendChild(makeStrokeYi(data, w, h))
          } else {
            svg.appendChild(makeStrokeY(data, w, h))
          }
        } else if (modes.has('tick-y')) {
          if (paired) {
            svg.appendChild(makeTickYi(data, w, h))
          } else {
            svg.appendChild(makeTickY(data, w, h))
          }
        } else if (modes.has('guide-x')) {
          svg.appendChild(makeGuideX(data, w, h))
        } else if (modes.has('guide-y')) {
          svg.appendChild(makeGuideY(data, w, h))
        } else if (modes.has('gauge-x')) {
          svg.appendChild(makeGaugeFill(data, w, h))
          svg.appendChild(makeGaugeX(data, w, h))
        } else if (modes.has('gauge-y')) {
          svg.appendChild(makeGaugeFill(data, w, h))
          svg.appendChild(makeGaugeY(data, w, h))
        } else if (modes.has('gauge-c')) {
          svg.appendChild(makeGaugeCFill(data, w, h))
          svg.appendChild(makeGaugeC(data, w, h))
        } else if (modes.has('gauge-sc')) {
          svg.appendChild(makeGaugeSCFill(data, w, h))
          svg.appendChild(makeGaugeSC(data, w, h))
        }
      }

      while (div.firstChild) div.removeChild(div.firstChild)
      div.appendChild(svg)
    }
  })
  return <div ref={ref} className={css(style)} />
}
