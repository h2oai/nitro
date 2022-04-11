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
import styled from 'styled-components';
import { B, S, U } from './core';

const opts: Options = {
  allowDangerousHtml: false,
  extensions: [gfm()],
  htmlExtensions: [gfmHtml()]
}

export const Markdown = styled.div`
/* Don't add margins before/after first/last paragraph */
&>p:first-child {
  margin-top: 0;
}
&>p:last-child {
  margin-bottom: 0;
}
&>p:only-child {
  margin: 0;
}

/* resets */

h1, h2, h3, h4, h5, h6, p, blockquote, pre {
  box-sizing: border-box;
  margin: 0;
  font-size: 1rem;
  line-height: 1.5rem;
  font-weight: 400;
}
img {
  max-width: 100%;
  display: block;
}

/* customizations */

h1 {
  font-weight: 200;
  font-size: 3rem;
  line-height: 3.3rem;
}
h2 {
  font-weight: 300;
  font-size: 2rem;
  line-height: 2.5rem;
  margin-top: 0.5rem;
}
h3 {
  font-size: 1.44rem;
  line-height: 2rem;
  font-weight: 400;
  margin-top: 0.5rem;
  color: #333;
}
h4 {
  font-size: 1.2rem;
  line-height: 1.75rem;
  font-weight: 600;
  margin-top: 0.5rem;
  color: #333;
}
h5 {
  font-size: 1rem;
  line-height: 1.75rem;
  font-weight: 700;
  text-transform: uppercase;
  font-feature-settings: 'smcp';
  color: #333;
}
h6 {
  font-size: 0.92rem;
  line-height: 1.25rem;
  margin-bottom: 1rem;
}
p, ul, ol {
  font-size: 1.2rem;
  line-height: 1.75rem;
  margin: 0.5rem 0;
}
strong {
  font-weight: 600;
}
ul {
  list-style: none;
  padding-left: 2rem;
  text-indent: -1rem;
}
ul>li:before {
  content: "—";
  text-indent: -1rem;
  margin-right: .5rem;
}
ol ol, ul ol {
  list-style-type: lower-roman;
}
ul ul ol, ul ol ol, ol ul ol, ol ol ol {
  list-style-type: lower-alpha;
}
/* Workaround: Markdown renderer adds superfluous p inside ol's li.*/
ol li p { 
  margin: 0;
}
blockquote {
  padding: 0 1em;
  border-left: 0.25em solid #ddd;
}
blockquote p {
  color: #555; 
}
.footnotes {
  h2 {
    font-size: 1rem;
    line-height: 1.75rem;
    font-weight: 700;
    text-transform: uppercase;
    font-feature-settings: 'smcp';
  }
  ol li, ol li p {
    font-size: 1rem;
  }
}
p code, li code, blockquote code {
  padding: 0.2em 0.4em;
  font-size: 85%;
  margin: 0;
  background-color: #eee;
}
pre {
  padding: 1rem;
  overflow: auto;
  margin-bottom: 1rem;
  background-color: #eee;
}

table {
  margin: 1rem 0;
  table-layout: fixed;
  border-collapse: collapse;
  border-bottom: 2px solid #eee;
  thead {
    background-color: #333;
  }
  th {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #fff;
  }
  td {
    padding: 0.25rem 0.75rem;
  }
  tr:nth-child(even) {
    background-color: #eee;
  }
}

/* Source: https://github.com/micromark/micromark-extension-gfm-footnote */

/* Style the footnotes section. */
.footnotes {
  font-size: smaller;
  color: #8b949e;
  border-top: 1px solid #30363d;
}

/* Hide the section label for visual users. */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  word-wrap: normal;
  border: 0;
}

/* Place [ and ] around footnote calls. */
[data-footnote-ref]::before {
  content: '[';
}

[data-footnote-ref]::after {
  content: ']';
}
`

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
    // don't dedent empty lines
    : lines.map(s => s.length > indent ? s.substring(indent) : s).join('\n')
}
export const
  highlight = (html: S) => html
    .replaceAll(/<code class="language-(.+?)">(.+?)<\/code>/gms, (_, language, code) => {
      return hljs.highlight(code, { language }).value
    }),
  isFootnoteLink = (s: S) => s.startsWith('user-content'), // gfm-footnote default
  markdown = (text: S): [S, B] => {
    let hasLinks = false
    const md = highlight(micromark(dedent(text), opts))
      // Change <a href="#foo"> to <a data-jump="foo" href>
      // Exclude footnote references.
      // We need the links to be rendered as such, but not affect the address bar.
      .replaceAll(/href="#(.+?)"/g, (all, ref) => {
        if (isFootnoteLink(ref)) return all
        hasLinks = true
        return `data-jump="${ref}" href`
      })
    return [md, hasLinks]
  }
