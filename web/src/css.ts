import { Dict, S, U } from "./core"

type Match = (s: S) => S | undefined
type Apply = (s: S) => S | undefined
type Rule = [Match, Apply]

const shades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900']
const spectrum: Dict<U[][]> = {
  slate: [[248, 250, 252], [241, 245, 249], [226, 232, 240], [203, 213, 225], [148, 163, 184], [100, 116, 139], [71, 85, 105], [51, 65, 85], [30, 41, 59], [15, 23, 42]],
  gray: [[249, 250, 251], [243, 244, 246], [229, 231, 235], [209, 213, 219], [156, 163, 175], [107, 114, 128], [75, 85, 99], [55, 65, 81], [31, 41, 55], [17, 24, 39]],
  zinc: [[250, 250, 250], [244, 244, 245], [228, 228, 231], [212, 212, 216], [161, 161, 170], [113, 113, 122], [82, 82, 91], [63, 63, 70], [39, 39, 42], [24, 24, 27]],
  neutral: [[250, 250, 250], [245, 245, 245], [229, 229, 229], [212, 212, 212], [163, 163, 163], [115, 115, 115], [82, 82, 82], [64, 64, 64], [38, 38, 38], [23, 23, 23]],
  stone: [[250, 250, 249], [245, 245, 244], [231, 229, 228], [214, 211, 209], [168, 162, 158], [120, 113, 108], [87, 83, 78], [68, 64, 60], [41, 37, 36], [28, 25, 23]],
  red: [[254, 242, 242], [254, 226, 226], [254, 202, 202], [252, 165, 165], [248, 113, 113], [239, 68, 68], [220, 38, 38], [185, 28, 28], [153, 27, 27], [127, 29, 29]],
  orange: [[255, 247, 237], [255, 237, 213], [254, 215, 170], [253, 186, 116], [251, 146, 60], [249, 115, 22], [234, 88, 12], [194, 65, 12], [154, 52, 18], [124, 45, 18]],
  amber: [[255, 251, 235], [254, 243, 199], [253, 230, 138], [252, 211, 77], [251, 191, 36], [245, 158, 11], [217, 119, 6], [180, 83, 9], [146, 64, 14], [120, 53, 15]],
  yellow: [[254, 252, 232], [254, 249, 195], [254, 240, 138], [253, 224, 71], [250, 204, 21], [234, 179, 8], [202, 138, 4], [161, 98, 7], [133, 77, 14], [113, 63, 18]],
  lime: [[247, 254, 231], [236, 252, 203], [217, 249, 157], [190, 242, 100], [163, 230, 53], [132, 204, 22], [101, 163, 13], [77, 124, 15], [63, 98, 18], [54, 83, 20]],
  green: [[240, 253, 244], [220, 252, 231], [187, 247, 208], [134, 239, 172], [74, 222, 128], [34, 197, 94], [22, 163, 74], [21, 128, 61], [22, 101, 52], [20, 83, 45]],
  emerald: [[236, 253, 245], [209, 250, 229], [167, 243, 208], [110, 231, 183], [52, 211, 153], [16, 185, 129], [5, 150, 105], [4, 120, 87], [6, 95, 70], [6, 78, 59]],
  teal: [[240, 253, 250], [204, 251, 241], [153, 246, 228], [94, 234, 212], [45, 212, 191], [20, 184, 166], [13, 148, 136], [15, 118, 110], [17, 94, 89], [19, 78, 74]],
  cyan: [[236, 254, 255], [207, 250, 254], [165, 243, 252], [103, 232, 249], [34, 211, 238], [6, 182, 212], [8, 145, 178], [14, 116, 144], [21, 94, 117], [22, 78, 99]],
  sky: [[240, 249, 255], [224, 242, 254], [186, 230, 253], [125, 211, 252], [56, 189, 248], [14, 165, 233], [2, 132, 199], [3, 105, 161], [7, 89, 133], [12, 74, 110]],
  blue: [[239, 246, 255], [219, 234, 254], [191, 219, 254], [147, 197, 253], [96, 165, 250], [59, 130, 246], [37, 99, 235], [29, 78, 216], [30, 64, 175], [30, 58, 138]],
  indigo: [[238, 242, 255], [224, 231, 255], [199, 210, 254], [165, 180, 252], [129, 140, 248], [99, 102, 241], [79, 70, 229], [67, 56, 202], [55, 48, 163], [49, 46, 129]],
  violet: [[245, 243, 255], [237, 233, 254], [221, 214, 254], [196, 181, 253], [167, 139, 250], [139, 92, 246], [124, 58, 237], [109, 40, 217], [91, 33, 182], [76, 29, 149]],
  purple: [[250, 245, 255], [243, 232, 255], [233, 213, 255], [216, 180, 254], [192, 132, 252], [168, 85, 247], [147, 51, 234], [126, 34, 206], [107, 33, 168], [88, 28, 135]],
  fuchsia: [[253, 244, 255], [250, 232, 255], [245, 208, 254], [240, 171, 252], [232, 121, 249], [217, 70, 239], [192, 38, 211], [162, 28, 175], [134, 25, 143], [112, 26, 117]],
  pink: [[253, 242, 248], [252, 231, 243], [251, 207, 232], [249, 168, 212], [244, 114, 182], [236, 72, 153], [219, 39, 119], [190, 24, 93], [157, 23, 77], [131, 24, 67]],
  rose: [[255, 241, 242], [255, 228, 230], [254, 205, 211], [253, 164, 175], [251, 113, 133], [244, 63, 94], [225, 29, 72], [190, 18, 60], [159, 18, 57], [136, 19, 55]],
}

const createPalette = () => {
  const palette: Dict<S> = {}
  for (const name in spectrum) {
    const colors = spectrum[name]
    for (let i = 0; i < shades.length; i++) {
      const [r, g, b] = colors[i]
      palette[`${name}-${shades[i]}`] = `${r} ${g} ${b}`
    }
  }
  return palette
}

const palette = createPalette()

const
  strs = (xs: U[]) => xs.map(x => '' + x),
  eq = (k: S) => (x: S) => { if (x === k) return x },
  empty = eq(''),
  none = eq('none'),
  auto = eq('auto'),
  full = eq('full'),
  map = (dict: Dict<any>) => (x: S) => { if (x in dict) return dict[x] },
  any = (...xs: S[]) => {
    const set = new Set(xs)
    return (x: S) => { if (set.has(x)) return x }
  },
  either = (...matchers: Match[]) => (x: S) => {
    for (const m of matchers) {
      const v = m(x)
      if (v !== undefined) return v
    }
  },
  mapF = (xs: S[], f: (x: S) => S) => {
    const d: Dict<S> = {}
    for (const x of xs) d[x] = f(x)
    return map(d)
  },
  _seq = (m: U, n: U) => {
    const
      k = n - m + 1,
      ns = new Array<U>(k)
    for (let i = 0; i < k; i++, m++) ns[i] = m
    return ns
  },
  num = (...ns: U[]) => {
    const d: Dict<S> = {}
    for (const n of ns) {
      const s = '' + n
      d[s] = s
    }
    return map(d)
  },
  range = (m: U, n: U) => num(..._seq(m, n)),
  numF = (ns: U[], f: (x: any) => any) => mapF(strs(ns), f)


const sizePresets = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96]
const makeSizeScale = () => {
  const d: Dict<S> = { '0': '0px', 'px': '1px' }
  sizePresets.forEach(f => { d['' + f] = `${f * 0.25}rem` })
  return d
}
const size = map(makeSizeScale())
const ratio = map({
  full: '100%',
  '1/2': '50%',
  '1/3': '33.333333%',
  '2/3': '66.666667%',
  '1/4': '25%',
  '2/4': '50%',
  '3/4': '75%',
  '1/5': '20%',
  '2/5': '40%',
  '3/5': '60%',
  '4/5': '80%',
  '1/6': '16.666667%',
  '2/6': '33.333333%',
  '3/6': '50%',
  '4/6': '66.666667%',
  '5/6': '83.333333%',
  '1/12': '8.333333%',
  '2/12': '16.666667%',
  '3/12': '25%',
  '4/12': '33.333333%',
  '5/12': '41.666667%',
  '6/12': '50%',
  '7/12': '58.333333%',
  '8/12': '66.666667%',
  '9/12': '75%',
  '10/12': '83.333333%',
  '11/12': '91.666667%',
})
const ratioSubset = map({
  '1/2': '50%',
  '1/3': '33.333333%',
  '2/3': '66.666667%',
  '1/4': '25%',
  '2/4': '50%',
  '3/4': '75%',
  full: '100%',
})

const replacements = new Map<S, S>()
const evaluations = new Map<S, Rule[]>()
const repl = (find: S, replace: S) => replacements.set(find, replace)
const rule = (find: S, ...rule: Rule[]) => {
  let rules = evaluations.get(find)
  if (!rules) evaluations.set(find, (rules = []))
  rules.push(...rule)
}

// --- begin rules ---

repl('container', 'width:100%')
rule('pointer-events', [any('none', 'auto'), v => `pointer-events:${v}`])
repl('visible', 'visibility:visible')
repl('invisible', 'visibility:hidden')
repl('static', 'position:static')
repl('fixed', 'position:fixed')
repl('absolute', 'position:absolute')
repl('relative', 'position:relative')
repl('sticky', 'position:-webkit-sticky;position:sticky')

const inset = either(size, auto, ratioSubset)
rule('inset', [inset, v => `top:${v};right:${v};bottom:${v};left:${v}`])
rule('inset-x', [inset, v => `left:${v};right:${v}`])
rule('inset-y', [inset, v => `top:${v};bottom:${v}`])
rule('top', [inset, v => `top:${v}`])
rule('right', [inset, v => `right:${v}`])
rule('bottom', [inset, v => `bottom:${v}`])
rule('left', [inset, v => `left:${v}`])
repl('isolate', 'isolation:isolate')
repl('isolation-auto', 'isolation:auto')
rule('z', [either(num(0, 10, 20, 30, 40, 50), auto), v => `z-index:${v}`])
rule('order', [either(range(1, 12), map({ 'first': '-9999', 'last': '9999', 'none': '0' })), v => `order:${v}`])

repl('col-auto', 'grid-column:auto')
rule('col-span',
  [range(1, 12), v => `grid-column:span ${v} / span ${v}`],
  [full, () => 'grid-column:1 / -1'],
)

const colstart = either(range(1, 13), auto)
rule('col-start', [colstart, v => `grid-column-start:${v}`])
rule('col-end', [colstart, v => `grid-column-end:${v}`])

repl('row-auto', 'grid-row:auto')
rule('row-span',
  [range(1, 12), v => `grid-row:span ${v} / span ${v}`],
  [full, () => 'grid-row:1 / -1'],
)

const rowstart = either(range(1, 7), auto)
rule('row-start', [rowstart, v => `grid-row-start:${v}`])
rule('row-end', [rowstart, v => `grid-row-end:${v}`])

rule('float', [any('right', 'left', 'none'), v => `float:${v}`])
rule('clear', [any('left', 'right', 'both', 'none'), v => `clear:${v}`])

const margin = either(size, auto)
rule('m', [margin, v => `margin:${v}`])
rule('mx', [margin, v => `margin-left:${v};margin-right:${v}`])
rule('my', [margin, v => `margin-top:${v};margin-bottom:${v}`])
rule('mt', [margin, v => `margin-top:${v}`])
rule('mr', [margin, v => `margin-right:${v}`])
rule('mb', [margin, v => `margin-bottom:${v}`])
rule('ml', [margin, v => `margin-left:${v}`])

rule('box', [any('border', 'content'), v => `box-sizing:${v}-box`])

repl('block', 'display:block')
repl('inline-block', 'display:inline-block')
repl('inline', 'display:inline')
repl('flex', 'display:flex')
repl('inline-flex', 'display:inline-flex')
repl('table', 'display:table')
repl('inline-table', 'display:inline-table')
rule('table', [any('caption', 'cell', 'column', 'column-group', 'footer-group', 'header-group', 'row-group', 'row'), v => `display:table-${v}`])
repl('flow-root', 'display:flow-root')
repl('grid', 'display:grid')
repl('inline-grid', 'display:inline-grid')
repl('contents', 'display:contents')
repl('list-item', 'display:list-item')
repl('hidden', 'display:none')

rule('aspect', [map({ auto: 'auto', square: '1 / 1', video: '16 / 9' }), v => `aspect-ratio:${v}`])

const sizing = either(size, ratio, auto)
rule('h',
  [sizing, v => `height:${v}`],
  [eq('screen'), v => 'height:100vh'],
  [any('min', 'max', 'fit'), v => `height:-webkit-${v}-content;height:-moz-${v}-content;height:${v}-content`],
)
rule('max-h',
  [size, v => `max-height:${v}`],
  [map({ full: '100%', screen: '100vh' }), v => `max-height:${v}`],
  [any('min', 'max', 'fit'), v => `max-height:-webkit-${v}-content;max-height:-moz-${v}-content;max-height:${v}-content`],
)
rule('min-h',
  [map({ '0': '0px', full: '100%', screen: '100vh' }), v => `min-height:${v}`],
  [any('min', 'max', 'fit'), v => `min-height:-webkit-${v}-content;min-height:-moz-${v}-content;min-height:${v}-content`],
)
rule('w',
  [sizing, v => `width:${v}`],
  [eq('screen'), v => 'width:100vw'],
  [any('min', 'max', 'fit'), v => `width:-webkit-${v}-content;width:-moz-${v}-content;width:${v}-content`],
)
rule('min-w',
  [map({ '0': '0px', full: '100%' }), v => `min-width:${v}`],
  [any('min', 'max', 'fit'), v => `min-width:-webkit-${v}-content;min-width:-moz-${v}-content;min-width:${v}-content`],
)
rule('max-w',
  [map({
    '0': '0rem',
    'none': 'none',
    'xs': '20rem',
    'sm': '24rem',
    'md': '28rem',
    'lg': '32rem',
    'xl': '36rem',
    '2xl': '42rem',
    '3xl': '48rem',
    '4xl': '56rem',
    '5xl': '64rem',
    '6xl': '72rem',
    '7xl': '80rem',
    'full': '100%',
    'prose': '65ch',
    'screen-sm': '640px',
    'screen-md': '768px',
    'screen-lg': '1024px',
    'screen-xl': '1280px',
    'screen-2xl': '1536px',
  }), v => `max-width:${v}`],
  [any('min', 'max', 'fit'), v => `max-width:-webkit-${v}-content;max-width:-moz-${v}-content;max-width:${v}-content`],
)

rule('flex', [map({
  '1': '1 1 0%',
  'auto': '1 1 auto',
  'initial': '0 1 auto',
  'none': 'none',
}), v => `flex:${v}`])

repl('shrink', 'flex-shrink:1')
repl('shrink-0', 'flex-shrink:0')
repl('grow', 'flex-grow:1')
repl('grow-0', 'flex-grow:0')

rule('basis', [sizing, v => `flex-basis:${v}`])

rule('table', [any('auto', 'fixed'), v => `table-layout:${v}`])

rule('border', [any('collapse', 'separate'), v => `border-collapse:${v}`])
rule('border-spacing', [size, v => `--tw-border-spacing-x:${v};--tw-border-spacing-y:${v};border-spacing:var(--tw-border-spacing-x) var(--tw-border-spacing-y)`])
rule('border-spacing-x', [size, v => `--tw-border-spacing-x:${v};border-spacing:var(--tw-border-spacing-x) var(--tw-border-spacing-y)`])
rule('border-spacing-y', [size, v => `--tw-border-spacing-y:${v};border-spacing:var(--tw-border-spacing-x) var(--tw-border-spacing-y)`])

rule('origin', [map({
  'center': 'center',
  'top': 'top',
  'top-right': 'top right',
  'right': 'right',
  'bottom-right': 'bottom right',
  'bottom': 'bottom',
  'bottom-left': 'bottom left',
  'left': 'left',
  'top-left': 'top left',
}), v => `transform-origin:${v}`])

const translate = either(size, ratioSubset)

rule('translate-x', [translate, v => `--tw-translate-x:${v};transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])
rule('translate-y', [translate, v => `--tw-translate-y:${v};transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])

rule('rotate', [num(0, 1, 2, 3, 6, 12, 45, 90, 180), v => `--tw-rotate:${v}deg;transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])

const skew = num(0, 1, 2, 3, 6, 12, 45, 90, 180)
rule('skew-x', [skew, v => `--tw-skew-x:${v}deg;transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])
rule('skew-y', [skew, v => `--tw-skew-y:${v}deg;transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])

const scale = map({
  '0': '0',
  '50': '.5',
  '75': '.75',
  '90': '.9',
  '95': '.95',
  '100': '1',
  '105': '1.05',
  '110': '1.1',
  '125': '1.25',
  '150': '1.5',
})
rule('scale', [scale, v => `--tw-scale-x:${v};--tw-scale-y:${v};transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])
rule('scale-x', [scale, v => `--tw-scale-x:${v};transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])
rule('scale-y', [scale, v => `--tw-scale-y:${v};transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))`])

rule('animate', [map({
  none: 'none',
  spin: 'spin 1s linear infinite',
  ping: 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
  pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  bounce: 'bounce 1s infinite',
}), v => `-webkit-animation:${v};animation:${v}`])

rule('cursor',
  [any(
    'auto',
    'default',
    'pointer',
    'wait',
    'text',
    'move',
    'help',
    'not-allowed',
    'none',
    'context-menu',
    'progress',
    'cell',
    'crosshair',
    'vertical-text',
    'alias',
    'copy',
    'no-drop',
    'all-scroll',
    'col-resize',
    'row-resize',
    'n-resize',
    'e-resize',
    's-resize',
    'w-resize',
    'ne-resize',
    'nw-resize',
    'se-resize',
    'sw-resize',
    'ew-resize',
    'ns-resize',
    'nesw-resize',
    'nwse-resize',
    'zoom-in',
    'zoom-out',
  ), v => `cursor:${v}`],
  [any('grab', 'grabbing'), v => `cursor:-webkit-${v};cursor:${v}`],
)

rule('touch',
  [any('auto', 'none', 'manipulation'), v => `touch-action:${v}`],
  [any(
    'pan-x',
    'pan-left',
    'pan-right',
  ), v => `--tw-pan-x:${v};touch-action:var(--tw-pan-x) var(--tw-pan-y) var(--tw-pinch-zoom)`],
  [any(
    'pan-y',
    'pan-up',
    'pan-down',
  ), v => `--tw-pan-y:${v};touch-action:var(--tw-pan-x) var(--tw-pan-y) var(--tw-pinch-zoom)`],
  [any(
    'pinch-zoom',
  ), v => `--tw-pinch-zoom:${v};touch-action:var(--tw-pan-x) var(--tw-pan-y) var(--tw-pinch-zoom)`],
)

rule('select',
  [any('none', 'text', 'auto'), v => `-webkit-user-select:${v};-moz-user-select:${v};user-select:${v}`],
  [eq('all'), () => '-webkit-user-select:all;-moz-user-select:all;user-select:all'],
)

rule('resize', [map({
  none: 'none',
  y: 'vertical',
  x: 'horizontal',
  '': 'both',
}), v => `resize:${v}`])

rule('snap',
  [any('mandatory', 'proximity'), v => `--tw-scroll-snap-strictness:${v}`],
  [none, () => 'scroll-snap-type:none'],
  [any('x', 'y', 'both'), v => `scroll-snap-type:${v} var(--tw-scroll-snap-strictness)`],
  [map({
    'start': 'start',
    'end': 'end',
    'center': 'center',
    'align-none': 'none',
  }), v => `scroll-snap-align:${v}`],
  [any('normal', 'always'), v => `scroll-snap-stop:${v}`],
)

rule('scroll-m', [size, v => `scroll-margin:${v}`])
rule('scroll-mx', [size, v => `scroll-margin-left:${v};scroll-margin-right:${v}`])
rule('scroll-my', [size, v => `scroll-margin-top:${v};scroll-margin-bottom:${v}`])
rule('scroll-mt', [size, v => `scroll-margin-top:${v}`])
rule('scroll-mr', [size, v => `scroll-margin-right:${v}`])
rule('scroll-mb', [size, v => `scroll-margin-bottom:${v}`])
rule('scroll-ml', [size, v => `scroll-margin-left:${v}`])
rule('scroll-p', [size, v => `scroll-padding:${v}`])
rule('scroll-px', [size, v => `scroll-padding-left:${v};scroll-padding-right:${v}`])
rule('scroll-py', [size, v => `scroll-padding-top:${v};scroll-padding-bottom:${v}`])
rule('scroll-pt', [size, v => `scroll-padding-top:${v}`])
rule('scroll-pr', [size, v => `scroll-padding-right:${v}`])
rule('scroll-pb', [size, v => `scroll-padding-bottom:${v}`])
rule('scroll-pl', [size, v => `scroll-padding-left:${v}`])

rule('list',
  [any('inside', 'outside'), v => `list-style-position:${v}`],
  [any('none', 'disc', 'decimal'), v => `list-style-type:${v}`],
)

repl('appearance-none', '-webkit-appearance:none;-moz-appearance:none;appearance:none')

rule('columns',
  [
    either(
      range(1, 12),
      auto,
      map({
        '3xs': '16rem',
        '2xs': '18rem',
        'xs': '20rem',
        'sm': '24rem',
        'md': '28rem',
        'lg': '32rem',
        'xl': '36rem',
        '2xl': '42rem',
        '3xl': '48rem',
        '4xl': '56rem',
        '5xl': '64rem',
        '6xl': '72rem',
        '7xl': '80rem',
      })
    ), v => `-moz-columns:${v};columns:${v}`
  ])

const columnBreak = any('auto', 'avoid', 'all', 'page', 'left', 'right', 'column')
rule('break-before',
  [columnBreak, v => `-moz-column-break-before:${v};break-before:${v}`],
  [eq('avoid-page'), () => '-moz-column-break-before:avoid;break-before:avoid-page'],
)
rule('break-inside',
  [any('auto', 'avoid'), v => `-moz-column-break-inside:${v};break-inside:${v}`],
  [eq('avoid-column'), () => '-moz-column-break-inside:avoid;break-inside:avoid-column'],
  [eq('avoid-page'), () => 'break-inside:avoid-page'],
)
rule('break-after',
  [columnBreak, v => `-moz-column-break-after:${v};break-after:${v}`],
  [eq('avoid-page'), () => '-moz-column-break-after:avoid;break-after:avoid-page'],
)

rule('auto-cols',
  [map({ auto: 'auto', fr: 'minmax(0, 1fr)' }), v => `grid-auto-columns:${v}`],
  [any('min', 'max'), v => `grid-auto-columns:-webkit-${v}-content;grid-auto-columns:${v}-content`],
)

rule('grid-flow',
  [map({
    'row': 'row',
    'col': 'column',
    'dense': 'dense',
    'row-dense': 'row dense',
    'col-dense': 'column dense',
  }), v => `grid-auto-flow:${v}`],
)

rule('auto-rows',
  [map({ auto: 'auto', fr: 'minmax(0, 1fr)' }), v => `grid-auto-rows:${v}`],
  [any('min', 'max'), v => `grid-auto-rows:-webkit-${v}-content;grid-auto-rows:${v}-content`],
)

rule('grid-cols',
  [range(1, 12), v => `grid-template-columns:repeat(${v}, minmax(0, 1fr))`],
  [none, () => 'grid-template-columns:none'],
)

rule('grid-rows',
  [range(1, 6), v => `grid-template-rows:repeat(${v}, minmax(0, 1fr))`],
  [none, () => 'grid-template-rows:none'],
)

rule('flex',
  [map({
    'row': 'row',
    'row-reverse': 'row-reverse',
    'col': 'column',
    'col-reverse': 'column-reverse',
  }), v => `flex-direction:${v}`],
  [any('wrap', 'wrap-reverse', 'nowrap'), v => `flex-wrap:${v}`],
)

const flexPlace = map({
  center: 'center',
  start: 'start',
  end: 'end',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
  stretch: 'stretch',
})
const flexJustify = any('start', 'end', 'center', 'stretch')
const flexAlign = map({
  start: 'flex-start',
  end: 'flex-end',
  center: 'center',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
})
const alignItems = map({
  start: 'flex-start',
  end: 'flex-end',
  center: 'center',
  baseline: 'baseline',
  stretch: 'stretch',
})

rule('place-content', [flexPlace, v => `place-content:${v}`])
rule('place-items', [flexJustify, v => `place-items:${v}`])
rule('content', [flexAlign, v => `align-content:${v}`])
rule('items', [alignItems, v => `align-items:${v}`])
rule('justify', [flexAlign, v => `justify-content:${v}`])
rule('justify-items', [flexJustify, v => `justify-items:${v}`])
rule('gap', [size, v => `gap:${v}`])
rule('gap-x', [size, v => `-moz-column-gap:${v};column-gap:${v}`])
rule('gap-y', [size, v => `row-gap:${v}`])
rule('place-self', [either(auto, flexJustify), v => `place-self:${v}`])
rule('self', [either(auto, alignItems), v => `align-self:${v}`])
rule('justify-self', [either(auto, flexJustify), v => `justify-self:${v}`])

const overflow = any('auto', 'hidden', 'clip', 'visible', 'scroll')
rule('overflow', [overflow, v => `overflow:${v}`])
rule('overflow-x', [overflow, v => `overflow-x:${v}`])
rule('overflow-y', [overflow, v => `overflow-y:${v}`])

const overscroll = any('auto', 'contain', 'none')
rule('overscroll', [overscroll, v => `overscroll-behavior:${v}`])
rule('overscroll-x', [overscroll, v => `overscroll-behavior-x:${v}`])
rule('overscroll-y', [overscroll, v => `overscroll-behavior-y:${v}`])

rule('scroll', [any('auto', 'smooth'), v => `scroll-behavior:${v}`])
repl('truncate', 'overflow:hidden;text-overflow:ellipsis;white-space:nowrap')

rule('text', [any('ellipsis', 'clip'), v => `text-overflow:${v}`])

rule('whitespace', [any('normal', 'nowrap', 'pre', 'pre-line', 'pre-wrap'), v => `white-space:${v}`])

rule('break',
  [eq('normal'), v => 'overflow-wrap:normal;word-break:normal'],
  [eq('words'), v => 'overflow-wrap:break-word'],
  [eq('all'), v => 'word-break:break-all'],
)

const rounded = map({
  'none': '0px',
  'sm': '0.125rem',
  '': '0.25rem',
  'md': '0.375rem',
  'lg': '0.5rem',
  'xl': '0.75rem',
  '2xl': '1rem',
  '3xl': '1.5rem',
  'full': '9999px',
})
rule('rounded', [rounded, v => `border-radius:${v}`])
rule('rounded-t', [rounded, v => `border-top-left-radius:${v};border-top-right-radius:${v}`])
rule('rounded-r', [rounded, v => `border-top-right-radius:${v};border-bottom-right-radius:${v}`])
rule('rounded-b', [rounded, v => `border-bottom-right-radius:${v};border-bottom-left-radius:${v}`])
rule('rounded-l', [rounded, v => `border-top-left-radius:${v};border-bottom-left-radius:${v}`])
rule('rounded-tl', [rounded, v => `border-top-left-radius:${v}`])
rule('rounded-tr', [rounded, v => `border-top-right-radius:${v}`])
rule('rounded-br', [rounded, v => `border-bottom-right-radius:${v}`])
rule('rounded-bl', [rounded, v => `border-bottom-left-radius:${v}`])

const borderWidth = map({
  '0': '0px',
  '': '1px',
  '2': '2px',
  '4': '4px',
  '8': '8px',
})
rule('border', [borderWidth, v => `border-width:${v}`])
rule('border-x', [borderWidth, v => `border-left-width:${v};border-right-width:${v}`])
rule('border-y', [borderWidth, v => `border-top-width:${v};border-bottom-width:${v}`])
rule('border-t', [borderWidth, v => `border-top-width:${v}`])
rule('border-r', [borderWidth, v => `border-right-width:${v}`])
rule('border-b', [borderWidth, v => `border-bottom-width:${v}`])
rule('border-l', [borderWidth, v => `border-left-width:${v}`])

rule('border', [any('solid', 'dashed', 'dotted', 'double', 'hidden', 'none'), v => `border-style:${v}`])

const namedColor = map({
  inherit: 'inherit',
  current: 'currentColor',
  transparent: 'transparent',
})
const color = either(map(palette), map({ white: '255 255 255', black: '0 0 0' }))

const borderRule = (n: S, t: S) =>
  rule(`border${n}`,
    [namedColor, v => `border${t}-color:${v}`],
    [color, v => `--tw-border-opacity:1;border${t}-color:rgb(${v} / var(--tw-border-opacity))`],
  )

borderRule('', '')

rule('border-x',
  [namedColor, v => `border-left-color:${v};border-right-color:${v}`],
  [color, v => `--tw-border-opacity:1;border-left-color:rgb(${v} / var(--tw-border-opacity));border-right-color:rgb(${v} / var(--tw-border-opacity))`],
)
rule('border-y',
  [namedColor, v => `border-top-color:${v};border-bottom-color:${v}`],
  [color, v => `--tw-border-opacity:1;border-top-color:rgb(${v} / var(--tw-border-opacity));border-bottom-color:rgb(${v} / var(--tw-border-opacity))`],
)

borderRule('-t', '-top')
borderRule('-r', '-right')
borderRule('-b', '-bottom')
borderRule('-l', '-left')

rule('bg',
  [namedColor, v => `background-color:${v}`],
  [color, v => `--tw-bg-opacity:1;background-color:rgb(${v} / var(--tw-bg-opacity))`],
  [none, () => 'background-image:none'],
)

rule('bg-gradient-to',
  [map({
    t: 'top',
    tr: 'top right',
    r: 'right',
    br: 'bottom right',
    b: 'bottom',
    bl: 'bottom left',
    l: 'left',
    tl: 'top left',
  }), v => `background-image:linear-gradient(to ${v}, var(--tw-gradient-stops))`])

const transparent = eq('transparent')
const inheritOrCurrent = map({ inherit: 'inherit', current: 'currentColor' })
rule('from',
  [inheritOrCurrent, v => `--tw-gradient-from:${v};--tw-gradient-to:rgb(255 255 255 / 0);--tw-gradient-stops:var(--tw-gradient-from), var(--tw-gradient-to)`],
  [transparent, () => '--tw-gradient-from:transparent;--tw-gradient-to:rgb(0 0 0 / 0);--tw-gradient-stops:var(--tw-gradient-from), var(--tw-gradient-to)'],
  [color, v => `--tw-gradient-from:rgb(${v});--tw-gradient-to:rgb(${v} / 0);--tw-gradient-stops:var(--tw-gradient-from), var(--tw-gradient-to)`],
)
rule('via',
  [inheritOrCurrent, v => `--tw-gradient-to:rgb(255 255 255 / 0);--tw-gradient-stops:var(--tw-gradient-from), ${v}, var(--tw-gradient-to)`],
  [transparent, () => '--tw-gradient-to:rgb(0 0 0 / 0);--tw-gradient-stops:var(--tw-gradient-from), transparent, var(--tw-gradient-to)'],
  [color, v => `--tw-gradient-to:rgb(${v} / 0);--tw-gradient-stops:var(--tw-gradient-from), rgb(${v}), var(--tw-gradient-to)`],
)
rule('to',
  [namedColor, v => `--tw-gradient-to:${v}`],
  [color, v => `--tw-gradient-to:rgb(${v})`],
)

rule('box-decoration', [any('slice', 'clone'), v => `-webkit-box-decoration-break:${v};box-decoration-break:${v}`])

rule('bg',
  [any('auto', 'cover', 'contain'), v => `background-size:${v}`],
  [any('fixed', 'local', 'scroll'), v => `background-attachment:${v}`],
)

rule('bg-clip',
  [map({
    'border': 'border-box',
    'padding': 'padding-box',
    'content': 'content-box',
  }), v => `background-clip:${v}`],
  [eq('text'), () => '-webkit-background-clip:text;background-clip:text'])

const position = map({
  'bottom': 'bottom',
  'center': 'center',
  'left': 'left',
  'left-bottom': 'left bottom',
  'left-top': 'left top',
  'right': 'right',
  'right-bottom': 'right bottom',
  'right-top': 'right top',
  'top': 'top',
})
rule('bg',
  [position, v => `background-position:${v}`],
  [eq('no-repeat'), () => 'background-repeat:no-repeat'],
)

rule('bg-repeat', [map({
  '': 'repeat',
  'x': 'repeat-x',
  'y': 'repeat-y',
  'round': 'round',
  'space': 'space',
}), v => `background-repeat:${v}`])

rule('bg-origin', [map({
  'border': 'border-box',
  'padding': 'padding-box',
  'content': 'content-box',
}), v => `background-origin:${v}`])

rule('object',
  [any('contain', 'cover', 'fill', 'none', 'scale-down'), v => `-o-object-fit:${v};object-fit:${v}`],
  [position, v => `-o-object-position:${v};object-position:${v}`],
)

rule('p', [size, v => `padding:${v}`])
rule('px', [size, v => `padding-left:${v};padding-right:${v}`])
rule('py', [size, v => `padding-top:${v};padding-bottom:${v}`])
rule('pt', [size, v => `padding-top:${v}`])
rule('pr', [size, v => `padding-right:${v}`])
rule('pb', [size, v => `padding-bottom:${v}`])
rule('pl', [size, v => `padding-left:${v}`])

rule('text', [any('left', 'center', 'right', 'justify', 'start', 'end'), v => `text-align:${v}`])

rule('indent', [size, v => `text-indent:${v}`])

rule('align', [any(
  'baseline', 'top', 'middle', 'bottom', 'text-top', 'text-bottom', 'sub', 'super',
), v => `vertical-align:${v}`])

rule('font', [map({
  sans: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
  serif: 'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
  mono: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
}), v => `font-family:${v}`])

rule('text', [map({
  'xs': ['0.75rem', '1rem'],
  'sm': ['0.875rem', '1.25rem'],
  'base': ['1rem', '1.5rem'],
  'lg': ['1.125rem', '1.75rem'],
  'xl': ['1.25rem', '1.75rem'],
  '2xl': ['1.5rem', '2rem'],
  '3xl': ['1.875rem', '2.25rem'],
  '4xl': ['2.25rem', '2.5rem'],
  '5xl': ['3rem', '1'],
  '6xl': ['3.75rem', '1'],
  '7xl': ['4.5rem', '1'],
  '8xl': ['6rem', '1'],
  '9xl': ['8rem', '1'],
}), ([f, l]) => `font-size:${f};line-height:${l}`])

rule('font', [map({
  'thin': 100,
  'extralight': 200,
  'light': 300,
  'normal': 400,
  'medium': 500,
  'semibold': 600,
  'bold': 700,
  'extrabold': 800,
  'black': 900,
}), v => `font-weight:${v}`])

repl('uppercase', 'text-transform:uppercase')
repl('lowercase', 'text-transform:lowercase')
repl('capitalize', 'text-transform:capitalize')
repl('normal-case', 'text-transform:none')
repl('italic', 'font-style:italic')
repl('not-italic', 'font-style:normal')
repl('normal-nums', 'font-variant-numeric:normal')

const fontVariant = (t: S) => `${t};font-variant-numeric:var(--tw-ordinal) var(--tw-slashed-zero) var(--tw-numeric-figure) var(--tw-numeric-spacing) var(--tw-numeric-fraction)`
repl('ordinal', fontVariant('--tw-ordinal:ordinal'))
repl('slashed-zero', fontVariant('--tw-slashed-zero:slashed-zero'))
repl('lining-nums', fontVariant('--tw-numeric-figure:lining-nums'))
repl('oldstyle-nums', fontVariant('--tw-numeric-figure:oldstyle-nums'))
repl('proportional-nums', fontVariant('--tw-numeric-spacing:proportional-nums'))
repl('tabular-nums', fontVariant('--tw-numeric-spacing:tabular-nums'))
repl('diagonal-fractions', fontVariant('--tw-numeric-fraction:diagonal-fractions'))
repl('stacked-fractions', fontVariant('--tw-numeric-fraction:stacked-fractions'))

rule('leading', [map({
  '3': '.75rem',
  '4': '1rem',
  '5': '1.25rem',
  '6': '1.5rem',
  '7': '1.75rem',
  '8': '2rem',
  '9': '2.25rem',
  '10': '2.5rem',
  'none': '1',
  'tight': '1.25',
  'snug': '1.375',
  'normal': '1.5',
  'relaxed': '1.625',
  'loose': '2',
}), v => `line-height:${v}`])

rule('tracking', [map({
  'tighter': '-0.05em',
  'tight': '-0.025em',
  'normal': '0em',
  'wide': '0.025em',
  'wider': '0.05em',
  'widest': '0.1em',
}), v => `letter-spacing:${v}`])

rule('text',
  [namedColor, v => `color:${v}`],
  [color, v => `--tw-text-opacity:1;color:rgb(${v} / var(--tw-text-opacity))`],
)
repl('underline', '-webkit-text-decoration-line:underline;text-decoration-line:underline')
repl('overline', '-webkit-text-decoration-line:overline;text-decoration-line:overline')
repl('line-through', '-webkit-text-decoration-line:line-through;text-decoration-line:line-through')
repl('no-underline', '-webkit-text-decoration-line:none;text-decoration-line:none')

rule('decoration',
  [namedColor, v => `-webkit-text-decoration-color:${v};text-decoration-color:${v}`],
  [color, v => `-webkit-text-decoration-color:rgb(${v});text-decoration-color:rgb(${v})`],
  [any('solid', 'double', 'dotted', 'dashed', 'wavy'), v => `-webkit-text-decoration-style:${v};text-decoration-style:${v}`],
  [map({
    auto: 'auto',
    'from-font': 'from-font',
    '0': '0px',
    '1': '1px',
    '2': '2px',
    '4': '4px',
    '8': '8px',
  }), v => `text-decoration-thickness:${v}`],
)

rule('underline-offset',
  [map({
    auto: 'auto',
    '0': '0px',
    '1': '1px',
    '2': '2px',
    '4': '4px',
    '8': '8px',
  }), v => `text-underline-offset:${v}`],
)

repl('antialiased', '-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale')
repl('subpixel-antialiased', '-webkit-font-smoothing:auto;-moz-osx-font-smoothing:auto')

rule('caret',
  [namedColor, v => `caret-color:${v}`],
  [color, v => `caret-color:rgb(${v})`],
)

rule('accent',
  [either(namedColor, auto), v => `accent-color:${v}`],
  [color, v => `accent-color:rgb(${v})`],
)

const opacity = numF([0, 5, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 95, 100], n => n / 100)
rule('opacity', [opacity, v => `opacity:${v}`])

const blendMode = any(
  'normal',
  'multiply',
  'screen',
  'overlay',
  'darken',
  'lighten',
  'color-dodge',
  'color-burn',
  'hard-light',
  'soft-light',
  'difference',
  'exclusion',
  'hue',
  'saturation',
  'color',
  'luminosity',
  'plus-lighter',
)
rule('bg-blend', [blendMode, v => `background-blend-mode:${v}`])
rule('mix-blend', [blendMode, v => `mix-blend-mode:${v}`])

rule('shadow',
  [map({
    'sm': '--tw-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05);--tw-shadow-colored:0 1px 2px 0 var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    '': '--tw-shadow:0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);--tw-shadow-colored:0 1px 3px 0 var(--tw-shadow-color), 0 1px 2px -1px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    'md': '--tw-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);--tw-shadow-colored:0 4px 6px -1px var(--tw-shadow-color), 0 2px 4px -2px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    'lg': '--tw-shadow:0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);--tw-shadow-colored:0 10px 15px -3px var(--tw-shadow-color), 0 4px 6px -4px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    'xl': '--tw-shadow:0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);--tw-shadow-colored:0 20px 25px -5px var(--tw-shadow-color), 0 8px 10px -6px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    '2xl': '--tw-shadow:0 25px 50px -12px rgb(0 0 0 / 0.25);--tw-shadow-colored:0 25px 50px -12px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    'inner': '--tw-shadow:inset 0 2px 4px 0 rgb(0 0 0 / 0.05);--tw-shadow-colored:inset 0 2px 4px 0 var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
    'none': '--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)',
  }), v => v],
  [namedColor, v => `--tw-shadow-color:${v};--tw-shadow:var(--tw-shadow-colored)`],
  [color, v => `--tw-shadow-color:rgb(${v});--tw-shadow:var(--tw-shadow-colored)`],
)

const eq01248 = num(0, 1, 2, 4, 8)
rule('outline',
  [none, () => 'outline:2px solid transparent;outline-offset:2px'],
  [empty, v => 'outline-style:solid'],
  [any('dashed', 'dotted', 'double', 'hidden'), v => `outline-style:${v}`],
  [eq01248, v => `outline-width:${v}px`],
)
rule('outline-offset', [eq01248, v => `outline-offset:${v}px`])
rule('outline',
  [namedColor, v => `outline-color:${v}`],
  [color, v => `outline-color:rgb(${v})`],
)

rule('ring', [map({
  '0': '0',
  '1': '1',
  '2': '2',
  '': '3',
  '4': '4',
  '8': '8',
}), v => `--tw-ring-offset-shadow:var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);--tw-ring-shadow:var(--tw-ring-inset) 0 0 0 calc(${v}px + var(--tw-ring-offset-width)) var(--tw-ring-color);box-shadow:var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000)`])
repl('ring-inset', '--tw-ring-inset:inset')
rule('ring',
  [namedColor, v => `--tw-ring-color:${v}`],
  [color, v => `--tw-ring-opacity:1;--tw-ring-color:rgb(${v} / var(--tw-ring-opacity))`],
)
rule('ring-offset',
  [eq01248, v => `--tw-ring-offset-width:${v}px`],
  [namedColor, v => `--tw-ring-offset-color:${v}`],
  [color, v => `--tw-ring-offset-color:rgb(${v})`],
)

const blur = map({
  'none': '0',
  'sm': '4px',
  '': '8px',
  'md': '12px',
  'lg': '16px',
  'xl': '24px',
  '2xl': '40px',
  '3xl': '64px',
})
const brightness = map({
  '0': '0',
  '50': '.5',
  '75': '.75',
  '90': '.9',
  '95': '.95',
  '100': '1',
  '105': '1.05',
  '110': '1.1',
  '125': '1.25',
  '150': '1.5',
  '200': '2',
})
const contrast = map({
  '0': '0',
  '50': '.5',
  '75': '.75',
  '100': '1',
  '125': '1.25',
  '150': '1.5',
  '200': '2',
})
const dropShadow = map({
  'sm': 'drop-shadow(0 1px 1px rgb(0 0 0 / 0.05))',
  '': 'drop-shadow(0 1px 2px rgb(0 0 0 / 0.1)) drop-shadow(0 1px 1px rgb(0 0 0 / 0.06))',
  'md': 'drop-shadow(0 4px 3px rgb(0 0 0 / 0.07)) drop-shadow(0 2px 2px rgb(0 0 0 / 0.06))',
  'lg': 'drop-shadow(0 10px 8px rgb(0 0 0 / 0.04)) drop-shadow(0 4px 3px rgb(0 0 0 / 0.1))',
  'xl': 'drop-shadow(0 20px 13px rgb(0 0 0 / 0.03)) drop-shadow(0 8px 5px rgb(0 0 0 / 0.08))',
  '2xl': 'drop-shadow(0 25px 25px rgb(0 0 0 / 0.15))',
  'none': 'drop-shadow(0 0 #0000)',
})
const grayscale = map({ '0': '0', '': '100%' })
const hueRotate = numF([0, 15, 30, 60, 90, 180], x => x + 'deg')
const saturate = map({
  '0': '0',
  '50': '.5',
  '100': '1',
  '150': '1.5',
  '200': '2',
})

const doFilter = ';filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)'
const filter = (f: S): Apply => v => `--tw-${f}:${f}(${v})` + doFilter
const rawFilter = (f: S): Apply => v => `--tw-${f}:${v}` + doFilter

rule('blur', [blur, filter('blur')])
rule('brightness', [brightness, filter('brightness')])
rule('contrast', [contrast, filter('contrast')])
rule('drop-shadow', [dropShadow, rawFilter('drop-shadow')])
rule('grayscale', [grayscale, filter('grayscale')])
rule('hue-rotate', [hueRotate, filter('hue-rotate')])
rule('invert', [grayscale, filter('invert')])
rule('saturate', [saturate, filter('saturate')])
rule('sepia', [grayscale, filter('sepia')])

const backdrop = (f: S): Apply => v => `--tw-backdrop-${f}:${f}(${v});-webkit-backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia);backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia)`

rule('backdrop-blur', [blur, backdrop('blur')])
rule('backdrop-brightness', [brightness, backdrop('brightness')])
rule('backdrop-contrast', [contrast, backdrop('contrast')])
rule('backdrop-grayscale', [grayscale, backdrop('grayscale')])
rule('backdrop-hue-rotate', [hueRotate, backdrop('hue-rotate')])
rule('backdrop-invert', [grayscale, backdrop('invert')])
rule('backdrop-opacity', [opacity, backdrop('opacity')])
rule('backdrop-saturate', [saturate, backdrop('saturate')])
rule('backdrop-sepia', [grayscale, backdrop('sepia')])

repl('transition-none', 'transition-property:none')
rule('transition',
  [
    either(
      any('all', 'opacity', 'transform'),
      map({
        '': 'color, background-color, border-color, fill, stroke, opacity, box-shadow, transform, filter, -webkit-text-decoration-color, -webkit-backdrop-filter;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter, -webkit-text-decoration-color, -webkit-backdrop-filter',
        'colors': 'color, background-color, border-color, fill, stroke, -webkit-text-decoration-color;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke, -webkit-text-decoration-color',
        'shadow': 'box-shadow',
      })
    ), v => `transition-property:${v};transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms`
  ])

const duration = num(75, 100, 150, 200, 300, 500, 700, 1000)
rule('delay', [duration, v => `transition-delay:${v}ms`])
rule('duration', [duration, v => `transition-duration:${v}ms`])

rule('ease', [map({
  'linear': 'linear',
  'in': 'cubic-bezier(0.4, 0, 1, 1)',
  'out': 'cubic-bezier(0, 0, 0.2, 1)',
  'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
}), v => `transition-timing-function:${v}`])

rule('will-change', [map({
  auto: 'auto',
  scroll: 'scroll-position',
  contents: 'contents',
  transform: 'transform',
}), v => `will-change:${v}`])

repl('content-none', '--tw-content:none;content:var(--tw-content)')

// --- end rules ---

const tryExpand = (rules: Rule[], suffix: S): S | undefined => {
  for (const [match, apply] of rules) {
    const s = match(suffix)
    if (s !== undefined) return apply(s)
  }
}

const expand = (prefix: S): S | undefined => {
  let replacement = replacements.get(prefix)
  if (replacement) return replacement

  let rules = evaluations.get(prefix)
  if (rules) {
    const css = tryExpand(rules, '')
    if (css) return css
  }

  let pos = prefix.indexOf('-')
  while (pos >= 0 && pos < prefix.length) {
    rules = evaluations.get(prefix.substring(0, pos))
    if (rules) {
      const css = tryExpand(rules, prefix.substring(pos + 1))
      if (css) return css
    }
    pos = prefix.indexOf('-', pos + 1)
  }
}

export const stylize = (style: S): S | undefined => {
  const names = style.split(/\s+/g)
  for (const name of names) {
    const css = expand(name)
    if (css) return css
    console.warn(`Unknown style: "${name}"`)
  }
}
