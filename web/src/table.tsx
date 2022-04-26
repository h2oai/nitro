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

import { CheckboxVisibility, DetailsList, DetailsListLayoutMode, IColumn, Link, Selection, SelectionMode } from '@fluentui/react';
import React from 'react';
import { Dict, S, U, V } from './core';
import { selectedsOf } from './options';
import { BoxProps, make } from './ui';

type TableRow = { key: S }

export const Table = make(({ context, box }: BoxProps) => {
  const
    { index, headers, options, multiple } = box,
    selecteds = selectedsOf(box),
    selectedValues = new Set<S>(selecteds.map(s => String(s.value))),
    capture = () => context.capture(index, Array.from(selectedValues)),
    columns = (headers ?? []).map((h, i): IColumn => {
      return {
        key: `f${i}`,
        name: h.text,
        minWidth: 100, // TODO pick from width tuple
        fieldName: `f${i}`,
        // isRowHeader: i===0, 
        isSorted: true,
        // data: 'string', // TODO
        // iconName: '' // TODO
        // isIconOnly: true, // TODO
      }
    }),
    items = options.map((o): TableRow => {
      const
        { value, options } = o,
        row: TableRow = { key: String(value) }

      if (options) {
        options.forEach((o, i) => (row as Dict<any>)[`f${i}`] = o.text)
      }

      return row
    }),
    selection = (() => {
      const selection = new Selection({
        onSelectionChanged: () => {
          const items = selection.getSelection() as TableRow[]
          selectedValues.clear()
          for (const item of items) {
            selectedValues.add(item.key)
          }
          capture()
        }
      })
      selection.setItems(items)

      // Init selection
      for (const key of Array.from(selectedValues)) selection.setKeySelected(key, true, false)

      return selection
    })(),
    onItemInvoked = (item: any) => {
      console.log('invoked', item)
    },
    onRenderItemColumn = (row: TableRow, _?: U, column?: IColumn) => {
      if (!column) return <span />

      const text = (row as Dict<any>)[column.key]
      if (multiple) {
        return <span>{text}</span>
      }
      const onClick = () => {
        context.capture(index, row.key)
        context.submit()
      }
      return column.key === 'f0'
        ? <Link href="" onClick={onClick}>{text}</Link>
        : <span>{text}</span>
    },
    render = () => {
      return (
        <DetailsList
          items={items}
          columns={columns}
          setKey="set"
          layoutMode={DetailsListLayoutMode.justified}
          selection={selection}
          selectionPreservedOnEmptyClick={true}
          ariaLabelForSelectionColumn="Toggle selection"
          ariaLabelForSelectAllCheckbox="Select All"
          checkButtonAriaLabel="Select"
          onRenderItemColumn={onRenderItemColumn}
          onItemInvoked={onItemInvoked}
          selectionMode={multiple ? SelectionMode.multiple : SelectionMode.single}
          checkboxVisibility={multiple ? undefined : CheckboxVisibility.hidden}
        />
      )
    }

  return { render }
})