import React from 'react';
import styled from 'styled-components';
import { micromark, Options } from 'micromark';
import { gfm, gfmHtml } from 'micromark-extension-gfm'
import { S } from './core';

const opts: Options = {
  allowDangerousHtml: false,
  extensions: [gfm()],
  htmlExtensions: [gfmHtml()]
}

const Container = styled.div`
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
  margin-bottom: 0.5rem;
}
h2 {
  font-weight: 300;
  font-size: 2rem;
  line-height: 3rem;
}
h3 {
  font-size: 1.44rem;
  line-height: 2rem;
  font-weight: 400;
  margin-bottom: 0.25rem;
  color: #333;
}
h4 {
  font-size: 1.2rem;
  line-height: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
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
  margin-bottom: 1rem;
  color: #242424;
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
`

export const Markdown = ({ text }: { text: S }) => {
  const html = micromark(text, opts)
  return <Container dangerouslySetInnerHTML={{ __html: html }} />
}