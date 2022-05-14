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

import { DefaultButton, FontIcon, Icon, Label, MessageBar, MessageBarType, PrimaryButton, ProgressIndicator } from '@fluentui/react';
import { BrowserScreenShotIcon } from '@fluentui/react-icons-mdl2';
import { getSplitButtonVerticalDividerClassNames } from '@fluentui/react/lib/components/ContextualMenu/ContextualMenu.classNames';
import React from 'react';
import styled from 'styled-components';
import { B, F, on, S, signal, Signal, U, xid } from './core';
import { BoxProps, make } from './ui';

const Container = styled.div`
  margin: 0.5rem 0;
`
const FileList = styled.div`
  margin: 1rem 0;
`
const FileItemContainer = styled.div`
  display: flex;
`
const FileDetail = styled.div`
  flex-grow: 1;
`
const FileIcon = styled.div`
  margin-right: 0.8rem;
`
const fileIconSize = 24
const fileIconStyle = {
  fontSize: fileIconSize,
  width: fileIconSize,
  height: fileIconSize,
}

const FileDropZone = styled.div`
  border: 1px dashed var(--neutral-secondary);
  border-radius: 1.2rem;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`
const FileDropZoneLabel = styled.div`
  font-size: 1.6rem;
  margin-bottom: 1.2rem;
`
const FileInputLabel = styled.label`
  display: inline-block;
  cursor: pointer;
  background: var(--accent);
  color: var(--background);
  border-radius: 2px;
  box-sizing: border-box;
  height: 3.2rem;
  line-height: 3.2rem;
  padding: 0 1.6rem;
  font-size: 1.4rem;
  font-weight: 600;
  text-align: center;
`

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
        <FileItemContainer>
          <FileIcon><FontIcon iconName={iconName} style={fileIconStyle} /></FileIcon>
          <FileDetail>
            {
              error
                ? <MessageBar messageBarType={MessageBarType.error}>{`${label}: ${error}`}</MessageBar>
                : progress < 1
                  ? <ProgressIndicator label={label} percentComplete={progress} />
                  : <Label>{label}</Label>
            }
          </FileDetail>
        </FileItemContainer>
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
    { index, text, multiple, path } = box,
    inputID = xid(),
    itemsB = signal<Uploadable[]>([]),
    uploadKeys: S[] = [],
    upload = (files: File[]) => {
      const uploadables = files.map((file): Uploadable => {
        const
          progressB = signal(0),
          errorB = signal('')
        return { key: xid(), label: file.name, file, progressB, errorB }
      })
      itemsB([...itemsB(), ...uploadables])
      setTimeout(() => {
        uploadables.forEach(({ file, progressB, errorB }) => {
          doUpload(path ?? '/upload', file, progressB, r => {
            switch (r.t) {
              case UploadResultT.Success:
                progressB(1)
                uploadKeys.push(r.key)
                context.capture(index, uploadKeys)
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
      upload(files)
    },
    onDrag = (e: React.DragEvent<HTMLFormElement>) => {
      e.preventDefault()
      e.stopPropagation()
    },
    render = () => {
      const items = itemsB().map(({ key, label, progressB, errorB }) => (
        <FileItem key={key} label={label} progressB={progressB} errorB={errorB} />
      ))
      return (
        <Container>
          <form
            onDragStart={onDrag}
            onDragEnter={onDrag}
            onDragEnd={onDrag}
            onDragLeave={onDrag}
            onDragOver={onDrag}
            onDrop={onDrop}
          >
            <Label>{text}</Label>
            <FileList>{items}</FileList>
            <FileDropZone>
              <input id={inputID} type='file' onChange={onChange} multiple={multiple} style={{ opacity: 0 }} />
              <FileDropZoneLabel>Drag files here, or</FileDropZoneLabel>
              <FileInputLabel htmlFor={inputID}>Browse...</FileInputLabel>
            </FileDropZone>
          </form>
        </Container>
      )
    }

  return { render, itemsB }
})


