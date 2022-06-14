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
import 'highlight.js/styles/github.css';
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
    .replaceAll(/<code class="language-(.+?)">(.+?)<\/code>/gms, (_, language, code) => {
      const src = hljs.highlight(revertMicromarkEncodings(code), { language }).value
      return `<code>${src}</code>`
    }),
  isFootnoteLink = (s: S) => s.startsWith('user-content'), // gfm-footnote default
  markdown = (text: S): [S, B] => {
    let hasLinks = false
    const md = micromark(dedent(text), opts)
    const hl = highlight(md)
      // Change <a href="#foo"> to <a data-jump="foo" href>
      // Exclude hashbangs #!, which act as context switches.
      // Exclude footnote references.
      // We need the links to be rendered as such, but not affect the address bar.
      .replaceAll(/href="#([^!].+?)"/g, (all, ref) => {
        if (isFootnoteLink(ref)) return all
        hasLinks = true
        return `data-jump="${ref}" href`
      })
    return [hl, hasLinks]
  }
