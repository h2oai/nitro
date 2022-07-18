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

import React from 'react';
import { Dict, S, words } from './core';
import { colorPalette, sizeScale, stylize } from './style'

const compare = (spec: string, expected: React.CSSProperties) => {
  const actual: React.CSSProperties = {}
  stylize(actual, spec)
  expect(actual).toStrictEqual(expected)
}

function loopd<T>(d: Dict<T>, f: (k: S, v: T) => void) {
  for (const k in d) f(k, d[k])
}

function loop<T>(xs: T[], f: (x: T) => void) {
  for (const x of xs) f(x)
}

type CSS = React.CSSProperties
const cases: [string, CSS][] = []
const tc = (input: S, expected: CSS) => cases.push([input, expected])

tc('w-auto', { width: 'auto' })
loopd(sizeScale, (k, v) => tc('w-' + k, { width: v }))
tc('w-1/2', { width: '50%' })
tc('w-1/3', { width: '33.333333%' })
tc('w-2/3', { width: '66.666667%' })
tc('w-1/4', { width: '25%' })
tc('w-2/4', { width: '50%' })
tc('w-3/4', { width: '75%' })
tc('w-1/5', { width: '20%' })
tc('w-2/5', { width: '40%' })
tc('w-3/5', { width: '60%' })
tc('w-4/5', { width: '80%' })
tc('w-1/6', { width: '16.666667%' })
tc('w-2/6', { width: '33.333333%' })
tc('w-3/6', { width: '50%' })
tc('w-4/6', { width: '66.666667%' })
tc('w-5/6', { width: '83.333333%' })
tc('w-1/12', { width: '8.333333%' })
tc('w-2/12', { width: '16.666667%' })
tc('w-3/12', { width: '25%' })
tc('w-4/12', { width: '33.333333%' })
tc('w-5/12', { width: '41.666667%' })
tc('w-6/12', { width: '50%' })
tc('w-7/12', { width: '58.333333%' })
tc('w-8/12', { width: '66.666667%' })
tc('w-9/12', { width: '75%' })
tc('w-10/12', { width: '83.333333%' })
tc('w-11/12', { width: '91.666667%' })
tc('w-full', { width: '100%' })
tc('w-screen', { width: '100vw' })
tc('w-min', { width: 'min-content' })
tc('w-max', { width: 'max-content' })
tc('w-fit', { width: 'fit-content' })

tc('h-auto', { height: 'auto' })
loopd(sizeScale, (k, v) => tc('h-' + k, { height: v }))
tc('h-1/2', { height: '50%' })
tc('h-1/3', { height: '33.333333%' })
tc('h-2/3', { height: '66.666667%' })
tc('h-1/4', { height: '25%' })
tc('h-2/4', { height: '50%' })
tc('h-3/4', { height: '75%' })
tc('h-1/5', { height: '20%' })
tc('h-2/5', { height: '40%' })
tc('h-3/5', { height: '60%' })
tc('h-4/5', { height: '80%' })
tc('h-1/6', { height: '16.666667%' })
tc('h-2/6', { height: '33.333333%' })
tc('h-3/6', { height: '50%' })
tc('h-4/6', { height: '66.666667%' })
tc('h-5/6', { height: '83.333333%' })
tc('h-1/12', { height: '8.333333%' })
tc('h-2/12', { height: '16.666667%' })
tc('h-3/12', { height: '25%' })
tc('h-4/12', { height: '33.333333%' })
tc('h-5/12', { height: '41.666667%' })
tc('h-6/12', { height: '50%' })
tc('h-7/12', { height: '58.333333%' })
tc('h-8/12', { height: '66.666667%' })
tc('h-9/12', { height: '75%' })
tc('h-10/12', { height: '83.333333%' })
tc('h-11/12', { height: '91.666667%' })
tc('h-full', { height: '100%' })
tc('h-screen', { height: '100vw' })
tc('h-min', { height: 'min-content' })
tc('h-max', { height: 'max-content' })
tc('h-fit', { height: 'fit-content' })

loopd(sizeScale, (k, v) => tc('p-' + k, { padding: v }))
loopd(sizeScale, (k, v) => tc('px-' + k, { paddingLeft: v, paddingRight: v }))
loopd(sizeScale, (k, v) => tc('py-' + k, { paddingTop: v, paddingBottom: v }))
loopd(sizeScale, (k, v) => tc('pt-' + k, { paddingTop: v }))
loopd(sizeScale, (k, v) => tc('pr-' + k, { paddingRight: v }))
loopd(sizeScale, (k, v) => tc('pb-' + k, { paddingBottom: v }))
loopd(sizeScale, (k, v) => tc('pl-' + k, { paddingLeft: v }))

tc('m-auto', { margin: 'auto' })
tc('mx-auto', { marginLeft: 'auto', marginRight: 'auto' })
tc('my-auto', { marginTop: 'auto', marginBottom: 'auto' })
tc('mt-auto', { marginTop: 'auto' })
tc('mr-auto', { marginRight: 'auto' })
tc('mb-auto', { marginBottom: 'auto' })
tc('ml-auto', { marginLeft: 'auto' })

loopd(sizeScale, (k, v) => tc('m-' + k, { margin: v }))
loopd(sizeScale, (k, v) => tc('mx-' + k, { marginLeft: v, marginRight: v }))
loopd(sizeScale, (k, v) => tc('my-' + k, { marginTop: v, marginBottom: v }))
loopd(sizeScale, (k, v) => tc('mt-' + k, { marginTop: v }))
loopd(sizeScale, (k, v) => tc('mr-' + k, { marginRight: v }))
loopd(sizeScale, (k, v) => tc('mb-' + k, { marginBottom: v }))
loopd(sizeScale, (k, v) => tc('ml-' + k, { marginLeft: v }))

tc('bg-inherit', { backgroundColor: 'inherit' })
loopd(colorPalette, (k, v) => tc('bg-' + k, { backgroundColor: v }));

tc('border', { borderWidth: 1 })
tc('border-x', { borderLeftWidth: 1, borderRightWidth: 1 })
tc('border-y', { borderTopWidth: 1, borderBottomWidth: 1 })
tc('border-t', { borderTopWidth: 1 })
tc('border-r', { borderRightWidth: 1 })
tc('border-b', { borderBottomWidth: 1 })
tc('border-l', { borderLeftWidth: 1 })

loopd(colorPalette, (k, v) => {
  tc('border-' + k, { borderColor: v })
  tc('border-x-' + k, { borderLeftColor: v, borderRightColor: v })
  tc('border-y-' + k, { borderTopColor: v, borderBottomColor: v })
  tc('border-t-' + k, { borderTopColor: v })
  tc('border-r-' + k, { borderRightColor: v })
  tc('border-b-' + k, { borderBottomColor: v })
  tc('border-l-' + k, { borderLeftColor: v })
});

loop([0, 2, 4, 8], v => {
  tc('border-' + v, { borderWidth: v })
  tc('border-x-' + v, { borderLeftWidth: v, borderRightWidth: v })
  tc('border-y-' + v, { borderTopWidth: v, borderBottomWidth: v })
  tc('border-t-' + v, { borderTopWidth: v })
  tc('border-r-' + v, { borderRightWidth: v })
  tc('border-b-' + v, { borderBottomWidth: v })
  tc('border-l-' + v, { borderLeftWidth: v })
});

loop(['solid', 'dashed', 'dotted', 'double', 'hidden', 'none'], v => {
  tc('border-' + v, { borderStyle: v })
})

tc('text-left', { textAlign: 'left' })
tc('text-center', { textAlign: 'center' })
tc('text-right', { textAlign: 'right' })
tc('text-justify', { textAlign: 'justify' })
tc('text-start', { textAlign: 'start' })
tc('text-end', { textAlign: 'end' })

tc('text-inherit', { color: 'inherit' })
loopd(colorPalette, (k, v) => tc('text-' + k, { color: v }))


cases.forEach(([spec, expected]) => it(spec, () => { compare(spec, expected) }))
