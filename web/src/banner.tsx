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

import { MessageBar, MessageBarType } from '@fluentui/react';
import { Dict, S } from './core';
import { BoxProps } from './ui';

const types: Dict<MessageBarType> = {
  info: MessageBarType.info,
  success: MessageBarType.success,
  warning: MessageBarType.warning,
  critical: MessageBarType.severeWarning,
  blocked: MessageBarType.blocked,
  error: MessageBarType.error,
}

export const Banner = ({ box }: BoxProps) => {
  const
    { mode, text } = box,
    type = types[mode as S] ?? undefined

  // TODO include link
  return (
    <MessageBar
      messageBarType={type}
      styles={{
        innerText: {
          fontFamily: 'var(--font-secondary)',
          fontSize: 14,
        }
      }}
    >{text}</MessageBar>
  )
}



