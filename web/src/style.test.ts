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
import { borderRadii, colorPalette, ratioPercents, sizeScale, stylize } from './style'

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
loopd(ratioPercents, (k, v) => tc('w-' + k, { width: v }))
tc('w-full', { width: '100%' })
tc('w-screen', { width: '100vw' })
tc('w-min', { width: 'min-content' })
tc('w-max', { width: 'max-content' })
tc('w-fit', { width: 'fit-content' })

tc('h-auto', { height: 'auto' })
loopd(sizeScale, (k, v) => tc('h-' + k, { height: v }))
loopd(ratioPercents, (k, v) => tc('h-' + k, { height: v }))
tc('h-full', { height: '100%' })
tc('h-screen', { height: '100vh' })
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

const dash = (k: S) => k ? '-' + k : k

loopd(borderRadii, (k, v) => {
  tc('rounded' + dash(k), { borderRadius: v })
  tc('rounded-t' + dash(k), { borderTopLeftRadius: v, borderTopRightRadius: v })
  tc('rounded-r' + dash(k), { borderTopRightRadius: v, borderBottomRightRadius: v })
  tc('rounded-b' + dash(k), { borderBottomLeftRadius: v, borderBottomRightRadius: v })
  tc('rounded-l' + dash(k), { borderTopLeftRadius: v, borderBottomLeftRadius: v })
  tc('rounded-tr' + dash(k), { borderTopRightRadius: v })
  tc('rounded-tl' + dash(k), { borderTopLeftRadius: v })
  tc('rounded-br' + dash(k), { borderBottomRightRadius: v })
  tc('rounded-bl' + dash(k), { borderBottomLeftRadius: v })
})

cases.forEach(([spec, expected]) => it(spec, () => { compare(spec, expected) }))
