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

import { FontIcon, Label, MessageBar, MessageBarType, ProgressIndicator } from '@fluentui/react';
import React from 'react';
import { F, S, signal, Signal, xid } from './core';
import { css } from './css';
import { BoxProps, make } from './ui';

const fileIconSize = 24
const fileIconStyle = {
  fontSize: fileIconSize,
  width: fileIconSize,
  height: fileIconSize,
}


enum UploadResultT { Success, Failure }
type UploadResult = { t: UploadResultT.Success, key: S } | { t: UploadResultT.Failure, error: S }

const doUpload = async (path: S, file: File, progressB: Signal<F>, done: (r: UploadResult) => void) => {
  const formData = new FormData()
  formData.append('file', file)
  try {
    const { responseText } = await new Promise<XMLHttpRequest>((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open("POST", path ?? '/upload')
      xhr.upload.onprogress = e => progressB(e.loaded / e.total)
      xhr.send(formData)
      xhr.onreadystatechange = () => {
        if (xhr.readyState !== XMLHttpRequest.DONE) return
        xhr.status >= 200 && xhr.status < 300 ? resolve(xhr) : reject(xhr)
      }
    })
    const response = JSON.parse(responseText)
    done({ t: UploadResultT.Success, key: response.files[0] })
  } catch ({ responseText }) {
    done({ t: UploadResultT.Failure, error: responseText as S ?? 'File upload failed.' })
  }
}

const FileItem = make(({ label, progressB, errorB }: { label: S, progressB: Signal<F>, errorB: Signal<S> }) => {
  const
    render = () => {
      const
        progress = progressB(),
        error = errorB(),
        iconName = error ? 'FileOff' : progress < 1 ? 'OpenFile' : 'DocumentApproval'
      return (
        <div className={css('flex')}>
          <div className={css('mr-2')}><FontIcon iconName={iconName} style={fileIconStyle} /></div>
          <div className={css('grow')}>
            {
              error
                ? <MessageBar messageBarType={MessageBarType.error}>{`${label}: ${error}`}</MessageBar>
                : progress < 1
                  ? <ProgressIndicator label={label} percentComplete={progress} />
                  : <Label>{label}</Label>
            }
          </div>
        </div>
      )
    }
  return { render, progressB, errorB }
})

type Uploadable = {
  key: S
  label: S
  file: File
  progressB: Signal<F>
  errorB: Signal<S>
}

export const FileUpload = make(({ context, box }: BoxProps) => {
  const
    { text, path, style } = box,
    multiple = box.multiple ? true : false,
    label = multiple ? 'Drag files here, or' : 'Drag a file here, or',
    inputID = xid(),
    itemsB = signal<Uploadable[]>([]),
    warningB = signal(''),
    uploadKeys: S[] = [],
    upload = (files: File[]) => {
      const uploadables = files.map((file): Uploadable => {
        const
          progressB = signal(0),
          errorB = signal('')
        return { key: xid(), label: file.name, file, progressB, errorB }
      })

      itemsB([...itemsB(), ...uploadables])
      warningB('')

      setTimeout(() => {
        uploadables.forEach(({ file, progressB, errorB }) => {
          doUpload(path ?? '/upload', file, progressB, r => {
            switch (r.t) {
              case UploadResultT.Success:
                progressB(1)
                if (multiple) {
                  uploadKeys.push(r.key)
                  context.record(uploadKeys)
                } else {
                  context.record(r.key)
                }
                break
              case UploadResultT.Failure:
                errorB(r.error)
                break
            }
          })
        })
      }, 0)
    },
    onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
      const rawFiles = e.target.files
      if (!rawFiles?.length) return
      const files = Array.from(rawFiles)
      upload(files)
    },
    onDrop = async (e: React.DragEvent<HTMLFormElement>) => {
      onDrag(e)
      const rawFiles = e.dataTransfer.files
      if (!rawFiles.length) return
      const files = Array.from(rawFiles)
      if (!multiple && files.length !== 1) {
        warningB(`You dropped ${files.length} files here, but only one file is allowed.`)
        return
      }
      upload(files)
    },
    onDrag = (e: React.DragEvent<HTMLFormElement>) => {
      e.preventDefault()
      e.stopPropagation()
    },
    render = () => {
      const
        warning = warningB(),
        items = itemsB().map(({ key, label, progressB, errorB }) => (
          <FileItem key={key} label={label} progressB={progressB} errorB={errorB} />
        ))

      return (
        <form
          onDragStart={onDrag}
          onDragEnter={onDrag}
          onDragEnd={onDrag}
          onDragLeave={onDrag}
          onDragOver={onDrag}
          onDrop={onDrop}
        >
          <div className={css('flex flex-col gap-1', style)}>
            <Label>{text}</Label>
            {warning ? <MessageBar messageBarType={MessageBarType.severeWarning}>{warning}</MessageBar> : <></>}
            <div className={css('flex flex-col gap-1')}>{items}</div>
            <div className={css('flex flex-col gap-2 justify-center items-center h-48 border border-dashed rounded-xl')}>
              <input id={inputID} type='file' onChange={onChange} multiple={multiple} style={{ opacity: 0 }} />
              <div>{label}</div>
              <label
                className={css('flex justify-center items-center cursor-pointer text-sm font-bold text-center rounded-sm h-8 px-4 bg-red-500')}
                htmlFor={inputID}
              ><span>Browse...</span></label>
            </div>
          </div>
        </form>
      )
    }

  context.record(multiple ? [] : null)

  return { render, itemsB, warningB }
})


