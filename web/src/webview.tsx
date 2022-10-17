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

import { xid } from './core';
import { css } from './css';
import { BoxProps } from './ui';

export const WebView = ({ box }: BoxProps) => {
  const
    { name: rawName, link, style } = box,
    name = rawName ?? xid()
  return (
    <iframe
      className={css(style)}
      name={name}
      title={name}
      src={link}
      data-name={rawName}
    />
  )
}



