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
/* Don't indent lists */
&>ul, &>ol {
  padding-left: 1rem;
}
`

export const Markdown = ({ text }: { text: S }) => {
  const html = micromark(text, opts)
  return <Container dangerouslySetInnerHTML={{ __html: html }} />
}