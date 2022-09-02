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

import { Dict, isN, P, S, toDate } from "./core";
import { Bundle, Data } from "./protocol";

enum FormatT { Number, DateTime, List, Plural, RelHour, RelMin, RelSec, RelYear, RelQuarter, RelWeek, RelMonth, RelDay }
type FormatOptions = any

export type Formatter = {
  load(locale: S | S[]): Formatter
  translate(s: S, data?: Data): S
}

const loadBundle = (d: Dict<Bundle>, locale: S | S[]): Bundle | undefined => {
  if (Array.isArray(locale)) {
    for (const l of locale) {
      const b = d[l]
      if (b) return b
    }
    return undefined
  }
  return d[locale]
}

export const formatter = (d: Dict<Bundle>, locale: S | S[]): Formatter => {
  let bundle: Bundle | null | undefined = null

  const
    load = (locale: S) => formatter(d, locale),
    translate = (s: S, data?: Dict<P>) => {
      if (!s) return s

      // Lazy load: 
      // translate() could be invoked purely for formatting, 
      // in which case the lookup is wasteful 
      if (!bundle === null) bundle = loadBundle(d, locale)

      if (bundle && /^@\w+$/.test(s)) {
        const x = bundle.resources[s.substring(1)]
        if (x) s = x
      }

      if (data && /^=/.test(s)) {
        s = format(locale, s.substring(1), data)
      }

      return s
    }
  return { load, translate }
}

const fsplit = (s: S): [S, S] => {
  const i = s.indexOf('-')
  return i < 0 ? [s, ''] : [s.substring(0, i), s.substring(i + 1)]
}

export const format = (locale: S | S[], s: S, data: Data): S => {
  if (!s) return s
  const result = s.replaceAll(/\{([^{}]*)\}/g, (_, expr) => {
    if (!expr) return expr

    expr = expr.trim()
    if (!expr) return expr

    const tokens = expr.split(/\s+/g)
    if (!tokens.length) return ''

    const
      [path, ...attrs] = tokens,
      value = read(path, data)

    if (attrs.length === 0) {
      if (Array.isArray(value)) {
        attrs.push('list')
      } else if (isN(value)) {
        attrs.push('num')
      } else {
        return String(value)
      }
    }

    const [algo, opts] = makeFormatOptions(attrs)
    switch (algo) {
      case FormatT.Number:
        const nf = new Intl.NumberFormat(locale, opts) // TODO cache
        try {
          return nf.format(value) // value can be string for bignum
        } catch (e) {
          return `(${e})`
        }
      case FormatT.DateTime:
        const dtf = new Intl.DateTimeFormat(locale, opts) // TODO cache
        const date = toDate(value)
        if (!date) return '(ParseError: Invalid date)'
        try {
          return dtf.format(date)
        } catch (e) {
          return `(${e})`
        }
      case FormatT.List:
        const lf = new Intl.ListFormat(locale, opts) // TODO cache
        if (!Array.isArray(value)) return '(ParseError: Invalid list)'
        try {
          return lf.format(value)
        } catch (e) {
          return `(${e})`
        }
    }
  })
  return result
}

const read = (path: S, data?: any): any => {
  if (!data) return data
  const i = path.indexOf('.')
  if (Array.isArray(data)) {
    const k = parseInt(i < 0 ? path : path.substring(0, i))
    return isNaN(k)
      ? undefined
      : i < 0
        ? data[k]
        : read(path.substring(i + 1), data[k])
  }
  return i < 0 ? data[path] : read(path.substring(i + 1), data[path.substring(0, i)])
}

const relFormats: Dict<FormatT> = {
  year: FormatT.RelYear,
  quarter: FormatT.RelQuarter,
  month: FormatT.RelMonth,
  week: FormatT.RelWeek,
  day: FormatT.RelDay,
  hour: FormatT.RelHour,
  minute: FormatT.RelMin,
  second: FormatT.RelSec,
}

export const makeFormatOptions = (tokens: S[]): [FormatT, FormatOptions] => {
  let algo: FormatT = FormatT.Number
  const o: FormatOptions = {}

  for (const token of tokens) {
    const [k, v] = fsplit(token)
    switch (k) {
      case 'rel':
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
      case 'num':
        algo = FormatT.Number
        switch (v) {
          case 's': o.notation = 'compact'; o.compactDisplay = 'long'; break
          case 'xs': o.notation = 'compact'; break
        }
        break
      case 'cur':
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
      case 'acc':
        algo = FormatT.Number
        o.currencySign = 'accounting'
        break
      case 'sci':
        algo = FormatT.Number
        o.notation = 'scientific'
        break
      case 'eng':
        algo = FormatT.Number
        o.notation = 'engineering'
        break
      case 'sign':
        algo = FormatT.Number
        switch (v) {
          case 'auto': o.signDisplay = 'auto'; break
          case 'always': o.signDisplay = 'always'; break
          case 'except-zero': o.signDisplay = 'exceptZero'; break
          case 'negative': o.signDisplay = 'negative' as any; break // experimental as of Aug 2022
          case 'none': o.signDisplay = 'never'; break
        }
        break
      case 'pct':
        algo = FormatT.Number
        o.style = 'percent'
        break
      case 'unit':
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
      case 'd':
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
      case 'date':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.dateStyle = 'short'; break
          case 'xl': o.dateStyle = 'full'; break
          case 'l': o.dateStyle = 'long'; break
          case 'm': o.dateStyle = 'medium'; break
          case 's': o.dateStyle = 'short'; break
        }
        break
      case 'time':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.timeStyle = 'short'; break
          case 'xl': o.timeStyle = 'full'; break
          case 'l': o.timeStyle = 'long'; break
          case 'm': o.timeStyle = 'medium'; break
          case 's': o.timeStyle = 'short'; break
        }
        break
      case 'calendar':
        algo = FormatT.DateTime
        o.calendar = v
        break
      case 'period':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.dayPeriod = 'long'; break
          case 's': o.dayPeriod = 'short'; break
          case 'xs': o.dayPeriod = 'narrow'; break
        }
        break
      case 'numbering':
        o.numberingSystem = v
        break
      case 'locale':
        switch (v) {
          case 'fit': o.localeMatcher = 'best fit'; break
          case 'lookup': o.localeMatcher = 'lookup'; break
        }
        break
      case 'cycle':
        algo = FormatT.DateTime
        switch (v) {
          case '12': o.hourCycle = 'h12'; break
          case '24': o.hourCycle = 'h24'; break
          case '11': o.hourCycle = 'h11'; break
          case '23': o.hourCycle = 'h23'; break
        }
        break
      case 'format':
        switch (v) {
          case 'fit': o.formatMatcher = 'best fit'; break
          case 'basic': o.formatMatcher = 'basic'; break
        }
        break
      case 'weekday':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.weekday = 'long'; break
          case 's': o.weekday = 'short'; break
          case 'xs': o.weekday = 'narrow'; break
        }
        break
      case 'era':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.era = 'long'; break
          case 's': o.era = 'short'; break
          case 'xs': o.era = 'narrow'; break
        }
        break
      case 'year':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.year = 'numeric'; break
          case '2': o.year = '2-digit'; break
        }
        break
      case 'month':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.month = 'numeric'; break
          case '2': o.month = '2-digit'; break
          case 'l': o.month = 'long'; break
          case 's': o.month = 'short'; break
          case 'xs': o.month = 'narrow'; break
        }
        break
      case 'day':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.day = 'numeric'; break
          case '2': o.day = '2-digit'; break
        }
        break
      case 'hour':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.hour = 'numeric'; break
          case '2': o.hour = '2-digit'; break
        }
        break
      case 'minute':
        algo = FormatT.DateTime
        switch (v) {
          case '': o.minute = 'numeric'; break
          case '2': o.minute = '2-digit'; break
        }
        break
      case 'second':
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
      case 'zone':
        algo = FormatT.DateTime
        switch (v) {
          case 'l': o.timeZoneName = 'long'; break
          case 's': o.timeZoneName = 'short'; break
          case 'offset-s': o.timeZoneName = 'shortOffset'; break
          case 'offset-l': o.timeZoneName = 'longOffset'; break
          case 'generic-s': o.timeZoneName = 'shortGeneric'; break
          case 'generic-l': o.timeZoneName = 'longGeneric'; break
        }
        break
      case 'list':
        algo = FormatT.List
        o.type = 'unit'
        switch (v) {
          case 'l': o.style = 'long'; break
          case 's': o.style = 'short'; break
          case 'xs': o.style = 'narrow'; break
        }
        break
      case 'and':
        algo = FormatT.List
        o.type = 'conjunction'
        switch (v) {
          case 'l': o.style = 'long'; break
          case 's': o.style = 'short'; break
          case 'xs': o.style = 'narrow'; break
        }
        break
      case 'or':
        algo = FormatT.List
        o.type = 'disjunction'
        switch (v) {
          case 'l': o.style = 'long'; break
          case 's': o.style = 'short'; break
          case 'xs': o.style = 'narrow'; break
        }
        break
    }
  }
  return [algo, o]
}