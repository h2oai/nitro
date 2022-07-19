fs = require 'fs'

camel_case = (s) => s.replace /-(\w)/g, (x) -> x[1].toUpperCase()

not_empty = (x) -> if x then yes else no

to_rule = (line) =>
  [l, r] = line.split /\s*:\s*/
  r = "'#{r}'" unless /^\d+$/.test r
  "#{camel_case l}: #{r}"

to_style = (css) =>
  lines = css
    # 16rem; /* 256px */ -> 256;
    .replace /\b[\d\.]+rem;\s+\/\*\s+(\d+)px\s+\*\//g, '$1;'
    # 16px -> 16
    .replace /\b(\d+)px\b/g, '$1'
    .split /;/g
    .map (x) -> x.trim()
    .filter not_empty
    .map to_rule

  "{ #{lines.join ', '} }"

capture = (cases, line, i) ->
  return unless line # empty
  return if 0 is line.indexOf '#' # comment
  throw "--tw-* vars not implemented #{i}: '#{line}'" if -1 < line.indexOf '--tw-'
  [input, output] = line.split /\t/
  throw "bad line #{i}: '#{line}'" unless output
  cases.push [input, to_style output]

main = () ->
  cases = []
  fs
    .readFileSync 'samples.txt', 'utf8'
    .split /\n/g
    .forEach (line, i) -> capture cases, line, i

  tests = cases.map (c) ->
    [input, output] = c
    "t('#{input}', #{output})"

  begin = '''
  import React from 'react'
  import { stylize } from './style'

  const t = (input: string, expected: React.CSSProperties) => {
    it(input, () => {
      const actual: React.CSSProperties = {}
      stylize(actual, input) 
      expect(actual).toStrictEqual(expected)
    })
  }

  '''

  ts = [begin, ...tests].join '\n'
  fs.writeFileSync '../../web/src/style.test.ts', ts, 'utf8'


main()
