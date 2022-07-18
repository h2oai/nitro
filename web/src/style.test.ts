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

function forEach<T>(d: Dict<T>, f: (k: S, v: T) => void) {
  for (const k in d) f(k, d[k])
}

const cases: [string, React.CSSProperties][] = [
  ['w-auto', { width: 'auto' }],
  ['w-1/2', { width: '50%' }],
  ['w-1/3', { width: '33.333333%' }],
  ['w-2/3', { width: '66.666667%' }],
  ['w-1/4', { width: '25%' }],
  ['w-2/4', { width: '50%' }],
  ['w-3/4', { width: '75%' }],
  ['w-1/5', { width: '20%' }],
  ['w-2/5', { width: '40%' }],
  ['w-3/5', { width: '60%' }],
  ['w-4/5', { width: '80%' }],
  ['w-1/6', { width: '16.666667%' }],
  ['w-2/6', { width: '33.333333%' }],
  ['w-3/6', { width: '50%' }],
  ['w-4/6', { width: '66.666667%' }],
  ['w-5/6', { width: '83.333333%' }],
  ['w-1/12', { width: '8.333333%' }],
  ['w-2/12', { width: '16.666667%' }],
  ['w-3/12', { width: '25%' }],
  ['w-4/12', { width: '33.333333%' }],
  ['w-5/12', { width: '41.666667%' }],
  ['w-6/12', { width: '50%' }],
  ['w-7/12', { width: '58.333333%' }],
  ['w-8/12', { width: '66.666667%' }],
  ['w-9/12', { width: '75%' }],
  ['w-10/12', { width: '83.333333%' }],
  ['w-11/12', { width: '91.666667%' }],
  ['w-full', { width: '100%' }],
  ['w-screen', { width: '100vw' }],
  ['w-min', { width: 'min-content' }],
  ['w-max', { width: 'max-content' }],
  ['w-fit', { width: 'fit-content' }],

  ['h-auto', { height: 'auto' }],
  ['h-1/2', { height: '50%' }],
  ['h-1/3', { height: '33.333333%' }],
  ['h-2/3', { height: '66.666667%' }],
  ['h-1/4', { height: '25%' }],
  ['h-2/4', { height: '50%' }],
  ['h-3/4', { height: '75%' }],
  ['h-1/5', { height: '20%' }],
  ['h-2/5', { height: '40%' }],
  ['h-3/5', { height: '60%' }],
  ['h-4/5', { height: '80%' }],
  ['h-1/6', { height: '16.666667%' }],
  ['h-2/6', { height: '33.333333%' }],
  ['h-3/6', { height: '50%' }],
  ['h-4/6', { height: '66.666667%' }],
  ['h-5/6', { height: '83.333333%' }],
  ['h-1/12', { height: '8.333333%' }],
  ['h-2/12', { height: '16.666667%' }],
  ['h-3/12', { height: '25%' }],
  ['h-4/12', { height: '33.333333%' }],
  ['h-5/12', { height: '41.666667%' }],
  ['h-6/12', { height: '50%' }],
  ['h-7/12', { height: '58.333333%' }],
  ['h-8/12', { height: '66.666667%' }],
  ['h-9/12', { height: '75%' }],
  ['h-10/12', { height: '83.333333%' }],
  ['h-11/12', { height: '91.666667%' }],
  ['h-full', { height: '100%' }],
  ['h-screen', { height: '100vw' }],
  ['h-min', { height: 'min-content' }],
  ['h-max', { height: 'max-content' }],
  ['h-fit', { height: 'fit-content' }],

  ['text-left', { textAlign: 'left' }],
  ['text-center', { textAlign: 'center' }],
  ['text-right', { textAlign: 'right' }],
  ['text-justify', { textAlign: 'justify' }],
  ['text-start', { textAlign: 'start' }],
  ['text-end', { textAlign: 'end' }],

  ['m-auto', { margin: 'auto' }],
  ['mx-auto', { marginLeft: 'auto', marginRight: 'auto' }],
  ['my-auto', { marginTop: 'auto', marginBottom: 'auto' }],
  ['mt-auto', { marginTop: 'auto' }],
  ['mr-auto', { marginRight: 'auto' }],
  ['mb-auto', { marginBottom: 'auto' }],
  ['ml-auto', { marginLeft: 'auto' }],

  ['text-inherit', { color: 'inherit' }],
  ['bg-inherit', { backgroundColor: 'inherit' }],
]

forEach(sizeScale, (k, v) => cases.push(['w-' + k, { width: v }]))
forEach(sizeScale, (k, v) => cases.push(['h-' + k, { height: v }]))
forEach(sizeScale, (k, v) => cases.push(['p-' + k, { padding: v }]))
forEach(sizeScale, (k, v) => cases.push(['px-' + k, { paddingLeft: v, paddingRight: v }]))
forEach(sizeScale, (k, v) => cases.push(['py-' + k, { paddingTop: v, paddingBottom: v }]))
forEach(sizeScale, (k, v) => cases.push(['pt-' + k, { paddingTop: v }]))
forEach(sizeScale, (k, v) => cases.push(['pr-' + k, { paddingRight: v }]))
forEach(sizeScale, (k, v) => cases.push(['pb-' + k, { paddingBottom: v }]))
forEach(sizeScale, (k, v) => cases.push(['pl-' + k, { paddingLeft: v }]))
forEach(sizeScale, (k, v) => cases.push(['m-' + k, { margin: v }]))
forEach(sizeScale, (k, v) => cases.push(['mx-' + k, { marginLeft: v, marginRight: v }]))
forEach(sizeScale, (k, v) => cases.push(['my-' + k, { marginTop: v, marginBottom: v }]))
forEach(sizeScale, (k, v) => cases.push(['mt-' + k, { marginTop: v }]))
forEach(sizeScale, (k, v) => cases.push(['mr-' + k, { marginRight: v }]))
forEach(sizeScale, (k, v) => cases.push(['mb-' + k, { marginBottom: v }]))
forEach(sizeScale, (k, v) => cases.push(['ml-' + k, { marginLeft: v }]))
forEach(colorPalette, (k, v) => cases.push(['text-' + k, { color: v }]))
forEach(colorPalette, (k, v) => cases.push(['bg-' + k, { backgroundColor: v }]))

cases.forEach(([spec, expected]) => it(spec, () => { compare(spec, expected) }))
