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

import hljs from 'highlight.js';
import 'highlight.js/styles/base16/bright.css';
import { micromark, Options } from 'micromark';
import { gfm, gfmHtml } from 'micromark-extension-gfm';
import { B, Dict, S, U } from './core';

const opts: Options = {
  allowDangerousHtml: false,
  extensions: [gfm()],
  htmlExtensions: [gfmHtml()]
}

const getIndentation = (rx: RegExp, lines: S[]): U => {
  const indents: U[] = []
  for (const line of lines) {
    if (line.trim().length === 0) continue // don't count empty lines
    const m = line.match(rx)
    if (!m) return 0
    indents.push(m[0].length)
  }
  return Math.min(...indents)
}
const getSpaceIndentation = (lines: S[]): U => getIndentation(/^ +/, lines)
const getTabIndentation = (lines: S[]): U => getIndentation(/^\t+/, lines)
const dedent = (block: S): S => {
  let lines = block.split(/\r?\n/)
  const n = lines.length
  if (n > 0) {
    lines = lines.slice(
      lines[0].trim().length === 0 ? 1 : 0,
      lines[n - 1].trim().length === 0 ? n - 1 : n
    )
  }
  const indent = getSpaceIndentation(lines) || getTabIndentation(lines)
  return indent === 0
    ? block
    : lines.map(s => s.length > indent ? s.substring(indent) : s) // don't dedent empty lines
      .map(s => s.trimEnd()) // Workaround for a bug in micromark - trailing spaces trip up list rendering
      .join('\n')
}

// Micromark encodes these chars inside <pre><code> blocks, which trips up highlight.js.
const revertMicromarkEncodings = (s: S) => s.replace(/&(quot|amp|lt|gt);/g, (value) => micromarkReplacements[value])

// Source: https://github.com/micromark/micromark/blob/main/packages/micromark-util-encode/index.js
const micromarkReplacements: Dict<S> = {
  '&quot;': '"',
  '&amp;': '&',
  '&lt;': '<',
  '&gt;': '>',
}

export const
  highlight = (html: S) => html
    .replace(/<code class="language-(.+?)">(.+?)<\/code>/gms, (_, language, code) => {
      const src = hljs.highlight(revertMicromarkEncodings(code), { language }).value
      return `<code>${src}</code>`
    }),
  markdown = (text: S): [S, B] => {
    const tmp = document.createElement('div')

    tmp.innerHTML = highlight(micromark(dedent(text), opts))

    let hasLinks = false
    for (const link of tmp.querySelectorAll('a')) {
      const href = link.getAttribute('href')
      if (href) {
        if (href.indexOf('#') === 0) {
          if (href.indexOf('#user-content') === 0) continue // gfm-footnote default; ignore
          hasLinks = true
          if (href.indexOf('#!') === 0) continue  // ignore hashbangs
          link.setAttribute('href', '') // don't affect address bar when clicked
          link.setAttribute('data-jump', href.substring(1)) // marker attribute; will be hijacked later
        } else {
          // Open all non-local links in a new window
          link.target = '_blank'
        }
      }
    }
    return [tmp.innerHTML, hasLinks]
  }
