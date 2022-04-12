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

import { ITag, TagPicker as FTagPicker } from '@fluentui/react';
import React from 'react';
import { S } from './core';
import { Labeled } from './label';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';


export const TagPicker = make(({ context, box }: BoxProps) => {
  const
    { index, text, options } = box,
    selectedOptions = selectedsOf(box),
    selectedKeys = selectedOptions.map(o => String(o.value)),
    tags: ITag[] = options.map(o => ({ key: o.value, name: String(o.text) })),
    selectedTags = tags.filter(tag => selectedKeys.includes(tag.key as S)),
    capture = (tags: ITag[]) => context.capture(index, tags.map(tag => String(tag.key))),
    listContainsTagList = (tag: ITag, tagList?: ITag[]) => (!tagList || !tagList.length || tagList.length === 0)
      ? false
      : tagList.some(compareTag => compareTag.key === tag.key),
    suggest = (filterText: string, tagList?: ITag[]): ITag[] =>
      filterText
        ? tags.filter(tag => tag.name.toLowerCase().includes(filterText.toLowerCase()) && !listContainsTagList(tag, tagList))
        : [],
    resolve = (item: ITag) => item.name,
    whenEmpty = () => tags,
    onChange = (tags?: ITag[]) => {
      if (tags) capture(tags)
    },
    render = () => {
      return (
        <Labeled label={text}>
          <FTagPicker
            pickerSuggestionsProps={{
              suggestionsHeaderText: 'Suggestions',
              noResultsFoundText: 'No matches found',
            }}
            onResolveSuggestions={suggest}
            getTextFromItem={resolve}
            onEmptyResolveSuggestions={whenEmpty}
            defaultSelectedItems={selectedTags}
            onChange={onChange}
          />
        </Labeled>
      )
    }

  capture(selectedTags)

  return { render }
})