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

type TableRow = Dict<any> & { value: S }

export const Table = make(({ context, box }: BoxProps) => {
  const
    { index, multiple } = box,
    selecteds = selectedsOf(box),
    selectedValues = new Set<S>(selecteds.map(s => String(s.value))),
    capture = () => context.capture(index, Array.from(selectedValues)),
    selection = new Selection({
      onSelectionChanged: () => {
        const items = selection.getSelection() as TableRow[]
        selectedValues.clear()
        for (const item of items) {
          selectedValues.add(item.value)
        }
        capture()
      }
    }),
    onItemInvoked = (item: any) => {
      console.log('invoked', item)
    },
    onRenderItemColumn = (item: TableRow, _?: U, column?: IColumn) => {
      if (!column) return <span />

      const text = item[column.key]
      if (multiple) {
        return <span>{text}</span>
      }
      const onClick = () => {
        context.capture(index, item.value)
        context.submit()
      }
      return column.key === 'f0'
        ? <Link href="" onClick={onClick}>{text}</Link>
        : <span>{text}</span>
    },
    render = () => {
      const
        { headers, options } = box,
        columns = (headers ?? []).map((h, i): IColumn => {
          return {
            key: `f${i}`,
            name: h.text,
            minWidth: 100, // TODO pick from width tuple
            fieldName: `f${i}`,
            // isRowHeader: i===0, 
            // isSorted: false, // TODO
            // data: 'string', // TODO
            // iconName: '' // TODO
            // isIconOnly: true, // TODO
          }
        }),
        items = options.map((o): TableRow => {
          const
            { value, options } = o,
            row: TableRow = { value: String(value) }

          if (options) {
            options.forEach((o, i) => row[`f${i}`] = o.text)
          }

          return row
        })

      return (
        <DetailsList
          items={items}
          columns={columns}
          setKey="set"
          layoutMode={DetailsListLayoutMode.justified}
          selection={selection}
          selectionPreservedOnEmptyClick={true}
          ariaLabelForSelectionColumn="Toggle selection"
          ariaLabelForSelectAllCheckbox="Toggle selection for all items"
          checkButtonAriaLabel="select row"
          onRenderItemColumn={onRenderItemColumn}
          onItemInvoked={onItemInvoked}
          selectionMode={multiple ? SelectionMode.multiple : SelectionMode.single}
          checkboxVisibility={multiple ? undefined : CheckboxVisibility.hidden}
        />
      )
    }
  return { render }
})