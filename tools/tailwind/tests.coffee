fs = require 'fs'

cases = []
css = fs.readFileSync 'output.css', 'utf8'
css = css.substring css.indexOf '.pointer-events'

toRGB = (r, g, b) ->
  [r, g, b] = [r, g, b].map (x) -> parseInt x, 16
  "rgb(#{r} #{g} #{b})"

replaceHex = (s) ->
  s
    .replace /#([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})\b/gi, (_, r, g, b) -> toRGB r, g, b
    .replace /#([a-f\d])([a-f\d])([a-f\d])\b/gi, (_, r, g, b) -> toRGB r+r, g+g, b+b

classes = [...css.matchAll /^([^\n]+?)\s*\{(.+?)\}/gms]

tests = []
for c in classes
  [_, name, body] = c
  continue unless name.startsWith '.'
  continue if name.startsWith '.prose'

  name = name.split(' ', 1)[0] # ".foo > * ~ *" -> ".foo"
    .substring 1 # .foo -> foo
    .replace /\\\./g, '.' # foo\.bar -> foo.bar

  lines = body
    .trim()
    .split ';'
    .map (x) -> x.trim()
    .filter (x) -> if x then yes else no
    .filter (x) -> not x.startsWith '-ms-'
    .map (x) ->
      [l, r] = x.split /\s*:\s*/, 2
      l + ':' + replaceHex r
  rule = lines.join ';'

  tests.push "  expect(c('#{name}')).toEqual('#{rule}')"

  begin = '''
  //
  // DO NOT EDIT THIS FILE DIRECTLY!
  // Generated by tools/tailwind
  //

  import { stylize as c } from './css'

  it('style should match tailwind', () => {
  '''

  end = '''
  })
  '''

  ts = [begin, ...tests, end].join '\n'

fs.writeFileSync '../../web/src/css.test.ts', ts, 'utf8'

