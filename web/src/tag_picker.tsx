import { ITag, TagPicker } from '@fluentui/react';
import React from 'react';
import { S } from './core';
import { Labeled } from './label';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';


export const XTagPicker = make(({ context, box }: BoxProps) => {
  const
    { index, text, options } = box,
    selectedOptions = selectedsOf(box),
    selectedKeys = selectedOptions.map(o => String(o.value)),
    tags: ITag[] = options.map(o => ({ key: o.value, name: String(o.text) })),
    selectedTags = tags.filter(tag => selectedKeys.includes(tag.key as S)),
    capture = (tags: ITag[]) => context.capture(index, tags.map(tag => tag.key)),
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
          <TagPicker
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