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

import { Dict, S } from "./core";

type V = string | number | boolean
type Model = Dict<V | Model>

enum FormatT { Number, DateTime, List, Plural, RelHour, RelMin, RelSec, RelYear, RelQuarter, RelWeek, RelMonth, RelDay }
type FormatOptions = any

const fsplit = (s: S): [S, S] => {
  const i = s.indexOf('-')
  return i < 0 ? [s, ''] : [s.substring(0, i), s.substring(i + 1)]
}

export const format = (locales: S[], s: S, model: Model): S => {
  if (!s) return s
  const result = s.replaceAll(/\{([^{}]*)\}/g, (_, expr) => {
    if (!expr) return expr

    expr = expr.trim()
    if (!expr) return expr

    const tokens = expr.split(/\s+/g)
    if (!tokens.length) return ''

    const [path, ...attrs] = tokens
    const value = evaluate(path, model)

    if (attrs.length === 0) return String(value)

    const [algo, opts] = makeFormatOptions(attrs)
    switch (algo) {
      case FormatT.Number:
        const nf = new Intl.NumberFormat(locales, opts) // TODO cache
        return nf.format(value)
      case FormatT.DateTime:
        const dtf = new Intl.DateTimeFormat(locales, opts) // TODO cache
        return dtf.format(value)
    }
  })
  return result
}

const evaluate = (path: S, model: Model): any => {
  const i = path.indexOf('.')
  if (i < 0) return String(model[path])
  const m = model[path.substring(0, i)]
  if (m) return evaluate(path.substring(i + 1), m as any)
  return undefined
}

const relFormats: Dict<FormatT> = {
  dy: FormatT.RelYear,
  dq: FormatT.RelQuarter,
  dm: FormatT.RelMonth,
  dw: FormatT.RelWeek,
  dd: FormatT.RelDay,
  th: FormatT.RelHour,
  tm: FormatT.RelMin,
  ts: FormatT.RelSec,
}

export const makeFormatOptions = (tokens: S[]): [FormatT, FormatOptions] => {
  let algo: FormatT = FormatT.Number
  const o: FormatOptions = {}

  for (const token of tokens) {
    const [k, v] = fsplit(token)
    switch (k) {
      case 'r':
        {
          const [unit, size] = fsplit(v)
          const a = relFormats[unit]
          if (!a) continue
          algo = a
          switch (size) {
            case 'l': o.style = 'long'; break
            case 's': o.style = 'short'; break
            case 'xs': o.style = 'narrow'; break
          }
        }
        break
      case 'n':
        algo = FormatT.Number
        switch (v) {
          case '': o.style = 'decimal'; break
          case 's': o.notation = 'compact'; o.compactDisplay = 'long'; break
          case 'xs': o.notation = 'compact'; break
        }
        break
      case 'c':
        algo = FormatT.Number
        switch (v) {
          case 'l': o.currencyDisplay = 'name'; break
          case 'm': o.currencyDisplay = 'code'; break
          case 's': o.currencyDisplay = 'symbol'; break
          case 'xs': o.currencyDisplay = 'narrowSymbol'; break
          default:
            o.style = 'currency';
            o.currency = v
        }
        break
      case 'a':
        algo = FormatT.Number
        o.currencySign = 'accounting'
        break
      case 's':
        algo = FormatT.Number
        o.notation = 'scientific'
        break
      case 'e':
        algo = FormatT.Number
        o.notation = 'engineering'
        break
      case 'g':
        algo = FormatT.Number
        switch (v) {
          case 'n0': o.signDisplay = 'auto'; break
          case 'pn0': o.signDisplay = 'always'; break
          case 'pn': o.signDisplay = 'exceptZero'; break
          case 'n': o.signDisplay = 'negative' as any; break // experimental as of Aug 2022
          case 'off': o.signDisplay = 'never'; break
        }
        break
      case 'p':
        algo = FormatT.Number
        o.style = 'percent'
        break
      case 'u':
        algo = FormatT.Number
        switch (v) {
          case 'l': o.unitDisplay = 'long'; break
          case 's': o.unitDisplay = 'short'; break
          case 'xs': o.unitDisplay = 'narrow'; break
          default:
            o.style = 'unit'
            o.unit = v
        }
        break
      case 'id':
        algo = FormatT.Number
        {
          const min = parseInt(v)
          if (!isNaN(min)) o.minimumIntegerDigits = min
        }
        break
      case 'fd':
        algo = FormatT.Number
        {
          const
            [a, b] = fsplit(v),
            min = parseInt(a),
            max = parseInt(b)
          if (!isNaN(min)) o.minimumFractionDigits = min
          if (!isNaN(max)) o.maximumFractionDigits = max
        }
        break
      case 'sd':
        algo = FormatT.Number
        {
          const
            [a, b] = fsplit(v),
            min = parseInt(a),
            max = parseInt(b)
          if (!isNaN(min)) o.minimumSignificantDigits = min
          if (!isNaN(max)) o.maximumSignificantDigits = max
        }
        break
      case 'd':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.dateStyle = 'full'; break
          case 'l': o.dateStyle = 'long'; break
          case 'm': o.dateStyle = 'medium'; break
          case 's': o.dateStyle = 'short'; break
        }
        break
      case 't':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.timeStyle = 'full'; break
          case 'l': o.timeStyle = 'long'; break
          case 'm': o.timeStyle = 'medium'; break
          case 's': o.timeStyle = 'short'; break
        }
        break
      case 'dt':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.dateStyle = 'full'; o.timeStyle = 'full'; break
          case 'l': o.dateStyle = 'long'; o.timeStyle = 'long'; break
          case 'm': o.dateStyle = 'medium'; o.timeStyle = 'medium'; break
          case 's': o.dateStyle = 'short'; o.timeStyle = 'short'; break
        }
        break
      case 'ca':
        algo = FormatT.DateTime
        o.calendar = v
        break
      case 'dp':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.dayPeriod = 'long'; break
          case 's': o.dayPeriod = 'short'; break
          case 'xs': o.dayPeriod = 'narrow'; break
        }
        break
      case 'nu':
        o.numberingSystem = v
        break
      case 'lm':
        switch (v) {
          case 'fit': o.localeMatcher = 'best fit'; break
          case 'lookup': o.localeMatcher = 'lookup'; break
        }
        break
      case 'hc':
        algo = FormatT.DateTime
        switch (v) {
          case '12': o.hourCycle = 'h12'; break
          case '24': o.hourCycle = 'h24'; break
          case '11': o.hourCycle = 'h11'; break
          case '23': o.hourCycle = 'h23'; break
        }
        break
      case 'fm':
        switch (v) {
          case 'fit': o.formatMatcher = 'best fit'; break
          case 'basic': o.formatMatcher = 'basic'; break
        }
        break
      case 'wd':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.weekday = 'long'; break
          case 's': o.weekday = 'short'; break
          case 'xs': o.weekday = 'narrow'; break
        }
        break
      case 'er':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.era = 'long'; break
          case 's': o.era = 'short'; break
          case 'xs': o.era = 'narrow'; break
        }
        break
      case 'dy':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.year = 'numeric'; break
          case '2': o.year = '2-digit'; break
        }
        break
      case 'dm':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.month = 'numeric'; break
          case '2': o.month = '2-digit'; break
          case 'l': o.month = 'long'; break
          case 's': o.month = 'short'; break
          case 'xs': o.month = 'narrow'; break
        }
        break
      case 'dd':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.day = 'numeric'; break
          case '2': o.day = '2-digit'; break
        }
        break
      case 'th':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.hour = 'numeric'; break
          case '2': o.hour = '2-digit'; break
        }
        break
      case 'tm':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.minute = 'numeric'; break
          case '2': o.minute = '2-digit'; break
        }
        break
      case 'ts':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.second = 'numeric'; break
          case '2': o.second = '2-digit'; break
        }
        break
      case 'fs':
        algo = FormatT.DateTime
        switch (v) {
          case '0': o.fractionalSecondDigits = 0; break
          case '1': o.fractionalSecondDigits = 1; break
          case '2': o.fractionalSecondDigits = 2; break
          case '3': o.fractionalSecondDigits = 3; break
        }
        break
      case 'tz':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.timeZoneName = 'long'; break
          case 's': o.timeZoneName = 'short'; break
          case 'o-s': o.timeZoneName = 'shortOffset'; break
          case 'o-l': o.timeZoneName = 'longOffset'; break
          case 'g-s': o.timeZoneName = 'shortGeneric'; break
          case 'g-l': o.timeZoneName = 'longGeneric'; break
        }
        break
    }
  }
  return [algo, o]
}