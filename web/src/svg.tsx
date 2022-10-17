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

import { css } from './css';
import { BoxProps } from './ui';

export const SVGBox = ({ box }: BoxProps) => {
  const { name, text, style } = box
  if (text) {
    // TODO: clean up asset lookup implementation. 
    // TODO: look up assets on a different dict. 
    // The Fluent icons are pre-wrapped in a <span/> with preset classes that interfere with tailwind, hence unusable.
    // if (text.startsWith('@')) {
    //   const
    //     iconName = kebabToPascalCase(text.substring(1)),
    //     icon = icons[iconName]
    //   if (icon) return <div className={css(style)}>{icon}</div>
    // }
    return (
      <div className={css(style)} dangerouslySetInnerHTML={{ __html: text ?? '' }} data-name={name} />
    )
  }
  return <span className={css(style)} data-name={name} />
}




