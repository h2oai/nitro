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

import { CheckboxVisibility, DetailsList, DetailsListLayoutMode, IColumn, IGroup, Link, Selection, SelectionMode } from '@fluentui/react';
import React from 'react';
import { areSetsEqual, B, Dict, isN, S, signal, U } from './core';
import { markdown } from './markdown';
import { selectedOf, selectedsOf } from './options';
import { Header, Option } from './protocol';
import { BoxProps, make } from './ui';

type TableRow = { key: S }
type TableGroup = { key: S, text: S, rows: TableRow[], groups: TableGroup[] }


export const Table = make(({ context, box }: BoxProps) => {
  const
    { headers, options, multiple, live } = box,
    isMultiple = multiple === true,
    isSingle = multiple === false,
    isList = isMultiple || isSingle,
    selectedOne = selectedOf(box),
    selecteds = isSingle && selectedOne ? [selectedOne] : selectedsOf(box),
    selectedValues = new Set<S>(selecteds.map(s => String(s.value))),
    capture = () => {
      if (isList) {
        const vs = Array.from(selectedValues)
        context.record(isMultiple ? vs : vs.length ? vs[0] : null)
      } else {
        context.record(null)
      }
    },
    linkColumnIndex = headers ? headers.findIndex(h => h.mode === 'link') : -1,
    linkColumnKey = `f${linkColumnIndex}`,
    sortRows = (rows: TableRow[], key: S, descending?: B): TableRow[] => {
      return rows.slice(0).sort((a: any, b: any) => ((descending ? a[key] < b[key] : a[key] > b[key]) ? 1 : -1));
    },
    onColumnClick = (ev: React.MouseEvent<HTMLElement>, clickedColumn: IColumn) => {
      const
        [currentColumns, currentItems] = contentB(),
        columns = currentColumns.slice(0),
        column = columns.filter(c => c.key === clickedColumn.key)[0]

      columns.forEach(c => {
        if (c === column) {
          c.isSortedDescending = !c.isSortedDescending
          c.isSorted = true
        } else {
          c.isSorted = false
          c.isSortedDescending = true
        }
      })

      const rows = sortRows(currentItems, column.fieldName!, column.isSortedDescending)

      contentB([columns, rows])
    },
    columns = (headers ?? []).map((h, i): IColumn => {
      const
        { text, icon, width, resizable, multiline } = h,
        iconName = icon ?? undefined,
        isIconOnly = icon ? true : false

      let
        minWidth: U = 0,
        maxWidth: U | undefined = undefined

      if (width !== undefined) {
        if (Array.isArray(width)) {
          switch (width.length) {
            case 1:
              {
                const [min] = width
                if (isN(min)) minWidth = min
                break
              }
            case 2:
              {
                const [min, max] = width
                if (isN(min)) minWidth = min
                if (isN(max)) maxWidth = max
                break
              }
          }
        } else {
          minWidth = width as any
        }
      }

      return {
        key: `f${i}`,
        name: text,
        ariaLabel: text,
        minWidth,
        maxWidth,
        fieldName: `f${i}`,
        isSorted: false,
        isSortedDescending: true,
        iconName,
        isIconOnly,
        onColumnClick,
        data: h,
        isResizable: resizable ?? true,
        isMultiline: multiline,
      }
    }),
    isRow = ({ options }: Option) => {
      if (!options) return false
      for (const option of options) if (option.options?.length) return false
      return true
    },
    createRow = (o: Option): TableRow => {
      const
        { value, options } = o,
        row: TableRow = { key: String(value) }

      if (options) options.forEach((o, i) => (row as Dict<any>)[`f${i}`] = o.text)

      return row
    },
    createGroup = (o: Option): TableGroup => {
      const
        rows: TableRow[] = [],
        groups: TableGroup[] = [],
        { options } = o
      if (options) {
        for (const o of options) {
          if (isRow(o)) {
            rows.push(createRow(o))
          } else {
            groups.push(createGroup(o))
          }
        }
      }
      return { key: String(o.value), text: o.text ?? 'Group', rows, groups }
    },
    countRows = (groups: IGroup[]) => {
      let count = 0
      for (const group of groups) {
        count += group.children?.length ? countRows(group.children) : group.count
      }
      return count
    },
    initRows = (): [TableRow[], IGroup[]] => {
      const
        { rows, groups } = createGroup({ value: '', options }),
        items: TableRow[] = [],
        igroups: IGroup[] = [],
        flatten = (group: TableGroup, level: U): IGroup => {
          const
            startIndex = items.length,
            children = group.groups.map(g => flatten(g, level + 1)),
            count = children.length ? countRows(children) : group.rows.length,
            igroup = { key: group.key, name: group.text, startIndex, count, level, children }
          for (const row of group.rows) items.push(row)
          return igroup
        }

      for (const group of groups) igroups.push(flatten(group, 0))
      for (const row of rows) items.push(row)

      return [items, igroups]
    },
    [rows, groups] = initRows(),
    initSelection = () => {
      const selection = new Selection({
        onSelectionChanged: () => {
          const
            items = selection.getSelection() as TableRow[],
            newSelectedValues = new Set<S>(items.map(item => item.key))

          // Prevent inf loop: don't commit unless selection has changed.
          if (!areSetsEqual(selectedValues, newSelectedValues)) {
            selectedValues.clear()
            for (const v of newSelectedValues) selectedValues.add(v)
            capture()
            if (live) context.commit()
          }
        }
      })
      selection.setItems(rows)

      // Init selection
      for (const key of Array.from(selectedValues)) selection.setKeySelected(key, true, false)

      return selection
    },
    selection = initSelection(),
    renderCell = (text: S, h?: Header) => {
      if (h) {
        switch (h.mode) {
          case 'md':
            {
              const __html = markdown(text)[0]
              return <span className='table-md' dangerouslySetInnerHTML={{ __html }} />
            }
        }
      }
      return <span>{text}</span>
    },
    onRenderItemColumn = (row: TableRow, _?: U, column?: IColumn) => {
      if (!column) return <span />

      const text = (row as Dict<any>)[column.key]
      if (isList) return renderCell(text, column.data as Header)

      // mode = 'table'
      const onClick = () => {
        context.record(row.key)
        context.commit()
      }
      return column.key === linkColumnKey
        ? <Link href="" onClick={onClick}>{text}</Link>
        : renderCell(text, column.data as Header)
    },
    contentB = signal<[IColumn[], TableRow[]]>([columns, rows]),
    render = () => {
      const [columns, rows] = contentB()
      return (
        <DetailsList
          items={rows}
          groups={groups.length ? groups : undefined}
          columns={columns}
          setKey="set"
          layoutMode={DetailsListLayoutMode.justified}
          selection={selection}
          selectionPreservedOnEmptyClick={true}
          ariaLabelForSelectionColumn="Toggle selection"
          ariaLabelForSelectAllCheckbox="Select All"
          checkButtonAriaLabel="Select"
          onRenderItemColumn={onRenderItemColumn}
          selectionMode={isMultiple ? SelectionMode.multiple : isSingle ? SelectionMode.single : SelectionMode.none}
          checkboxVisibility={isList ? undefined : CheckboxVisibility.hidden}
        />
      )
    }

  capture()

  return { render, contentB }
})